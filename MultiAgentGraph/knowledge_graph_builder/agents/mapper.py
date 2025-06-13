import re

def map_to_graph(summary_text):
    """
    Converts '>' delimited roadmap text into a graph structure of nodes and edges.
    """
    lines = [line.strip() for line in summary_text.split('\n') if line.strip()]
    
    nodes = set()
    edges = []
    current_phase_label = None
    last_node_in_current_phase = {}
    phase_start_nodes = {}

    for line in lines:
        parts = [part.strip() for part in line.split('>') if part.strip()]
        
        if not parts:
            continue

        # Add all parts as nodes
        for part in parts:
            nodes.add(part)

        # Determine current phase and its start node
        phase_match = re.match(r'^(Phase \d+): (.+)', parts[0])
        if phase_match:
            current_phase_label = phase_match.group(1)
            phase_start_nodes[current_phase_label] = parts[0]
        
        # Create edges based on the hierarchy within the line
        for i in range(len(parts) - 1):
            source = parts[i]
            target = parts[i+1]
            if (source, target) not in edges:
                edges.append((source, target))
        
        # Track the last node in the current phase for potential inter-phase connections
        if current_phase_label and parts[-1] != current_phase_label:
            last_node_in_current_phase[current_phase_label] = parts[-1]

    # After processing all lines, add connections between phases
    # This assumes phases are ordered numerically and implicitly connected
    sorted_phase_labels = sorted(last_node_in_current_phase.keys(), 
                                 key=lambda x: int(re.search(r'\d+', x).group()))

    for i in range(len(sorted_phase_labels) - 1):
        current_phase = sorted_phase_labels[i]
        next_phase = sorted_phase_labels[i+1]
        
        # Connect the last node of current phase to the start node of the next phase
        last_node = last_node_in_current_phase.get(current_phase)
        next_phase_start_node = phase_start_nodes.get(next_phase)

        if last_node and next_phase_start_node and (last_node, next_phase_start_node) not in edges:
            edges.append((last_node, next_phase_start_node))

    # Handle Total Estimated Time node and connect it from the last node of the final phase
    total_time_node = None
    final_time_estimate_node = None
    for node in nodes:
        if "total estimated time" in node.lower():
            total_time_node = node
        if "estimated time" in node.lower() and "total" not in node.lower():
            final_time_estimate_node = node # Simple heuristic, might need refinement
    
    if total_time_node and final_time_estimate_node and (final_time_estimate_node, total_time_node) not in edges:
        edges.append((final_time_estimate_node, total_time_node))

    return {
        "nodes": list(nodes),
        "edges": edges
    }