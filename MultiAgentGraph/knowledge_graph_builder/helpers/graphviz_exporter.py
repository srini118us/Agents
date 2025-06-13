import re
from graphviz import Digraph

def export_to_graphviz(graph_data):
    """
    Generates a Graphviz Digraph from a structured graph_data dictionary.
    Phase headers are aligned horizontally (same rank), and layout flows top-to-bottom.
    """
    dot = Digraph(comment='Career Roadmap', format='png')
    # Set global graph attributes for better layout
    dot.attr(rankdir='TB',  # Overall graph flows Top-to-Bottom
            splines='ortho', # Use orthogonal splines for straight edges
            nodesep='1.0',    # Increase space between nodes
            ranksep='1.5',    # Increase space between ranks for better vertical separation
            fontsize='12',
            fontname='Helvetica',
            compound='true') # Enable compound graphs for edges between clusters

    # Default node style
    dot.attr('node',
            shape='box',
            style='rounded,filled',
            fillcolor='lightyellow',
            fontname='Helvetica',
            margin='0.3,0.15', # Adjust node padding
            fixedsize='false') # Allow auto-sizing based on content

    # Map labels to unique Graphviz IDs
    label_to_id = {}
    next_id = 0
    for node_label in graph_data["nodes"]:
        if node_label not in label_to_id:
            label_to_id[node_label] = f"n{next_id}"
            next_id += 1

    # Identify the Total Estimated Time node early
    total_time_node_label = None
    for node_label in graph_data["nodes"]:
        if "total estimated time" in node_label.lower():
            total_time_node_label = node_label
            break

    # Create all nodes in the main dot graph with initial styling, EXCEPT for the total_time_node_label
    for node_label in graph_data["nodes"]:
        node_id = label_to_id[node_label]
        if node_label == total_time_node_label: # Skip total_time_node_label for now
            continue
        elif node_label.strip().lower().startswith("phase"):
            dot.node(node_id, node_label,
                    fillcolor='lightblue',
                    style='rounded,filled,bold',
                    width='1.8',  # Make phase headers more prominent
                    height='0.7',
                    group='phase_headers_group') # Assign a group for strong horizontal alignment
        elif "estimated time" in node_label.lower(): # This will catch other estimated time nodes
            dot.node(node_id, node_label,
                    fillcolor='lightgoldenrod1',
                    shape='box',
                    style='rounded,filled')
        else:
            dot.node(node_id, node_label)


    # --- Phase Header Alignment and Ordering at the Top (Strictly Enforced) ---
    phase_header_labels = [label for label in graph_data["nodes"] if label.strip().lower().startswith("phase")]
    phase_header_labels.sort(key=lambda x: int(re.search(r'Phase (\d+)', x).group(1)) if re.search(r'Phase (\d+)', x) else float('inf'))
    sorted_phase_header_ids = [label_to_id[label] for label in phase_header_labels]

    if sorted_phase_header_ids:
        # Use a simple subgraph for phase headers, not a cluster, to avoid nesting conflicts
        # This subgraph forces them onto the same rank (horizontally).
        with dot.subgraph(name='phase_header_rank_group') as ph_group:
            ph_group.attr(rank='same', rankdir='LR') # Force to same rank, left-to-right
            for i, node_id in enumerate(sorted_phase_header_ids):
                ph_group.node(node_id, rank='min') # Explicitly set rank for each node in top header
                if i > 0:
                    # Invisible edges to ensure strict left-to-right ordering of headers
                    ph_group.edge(sorted_phase_header_ids[i-1], node_id, style="invis")


    # --- Grouping Nodes into Content Clusters for Vertical Flow ---
    # This mapping holds nodes that belong to a phase *excluding* the phase header itself and total_time_node_label.
    phase_content_mapping = {} 
    current_phase_label = None

    # Parse summary_text to accurately map content nodes to their phases
    summary_text = graph_data.get('summary', '')
    lines = [line.strip() for line in summary_text.split('\n') if line.strip()]

    for line in lines:
        parts = [p.strip() for p in line.split('>') if p.strip()]
        if not parts: # Skip empty lines
            continue

        candidate_phase_header = parts[0]
        if candidate_phase_header.lower().startswith("phase"):
            current_phase_label = candidate_phase_header
            if current_phase_label not in phase_content_mapping:
                phase_content_mapping[current_phase_label] = []

        if current_phase_label and current_phase_label in phase_content_mapping:
            for part in parts:
                # Add content nodes to the current phase's mapping (excluding the header itself and total_time_node_label)
                if part != current_phase_label and part != total_time_node_label and part not in phase_content_mapping[current_phase_label]:
                    phase_content_mapping[current_phase_label].append(part)


    # Create *content-only* clusters for each phase and link them from headers
    # Iterate through sorted phase labels to maintain ordering for cluster placement
    for phase_label in phase_header_labels: 
        content_nodes_labels = phase_content_mapping.get(phase_label, [])
        
        # Only create a content cluster if there are actual content nodes to place inside it.
        # The phase header itself is handled by the top-level non-cluster subgraph.
        if content_nodes_labels:
            cluster_id = f"cluster_content_for_{label_to_id[phase_label]}" # Unique ID for content cluster
            with dot.subgraph(name=cluster_id) as cluster:
                cluster.attr(label=f"{phase_label} Content", # Label for the content cluster
                            style='filled,rounded',
                            color='gray', # Border color for content cluster
                            fillcolor='#F0F0F0', # Lighter fill for content cluster
                            rankdir='TB') # Ensure vertical flow within the content cluster

                # Add content nodes to this cluster and create invisible vertical chain
                for i, node_label in enumerate(content_nodes_labels):
                    if node_label in label_to_id:
                        node_id = label_to_id[node_label]
                        cluster.node(node_id)
                        if i > 0:
                            # Create invisible vertical edge to force stacking within the cluster
                            cluster.edge(label_to_id[content_nodes_labels[i-1]], node_id, style="invis", minlen="1.0")

                # Crucial: Add an invisible edge from the phase header to the first node of its content cluster.
                # This establishes the vertical flow from the header to its content within the cluster context.
                if label_to_id[phase_label] and content_nodes_labels and label_to_id.get(content_nodes_labels[0]):
                    dot.edge(label_to_id[phase_label], label_to_id[content_nodes_labels[0]], 
                            style="invis",
                            lhead=cluster_id) # Directs the edge to the content cluster boundary


    # --- Create Actual Data Edges ---
    for source_label, target_label in graph_data["edges"]:
        source_id = label_to_id.get(source_label)
        target_id = label_to_id.get(target_label)

        if source_id and target_id:
            # Skip edges directly involving the total_time_node_label here,
            # as its primary connection is handled separately at the end for rank enforcement.
            if source_label == total_time_node_label or target_label == total_time_node_label:
                continue

            source_subgraph_id = None 
            target_subgraph_id = None

            # Check if source_label is a phase header or in a content cluster
            if source_label in phase_header_labels: 
                source_subgraph_id = 'phase_header_rank_group' 
            else:
                for phase_label, content_nodes in phase_content_mapping.items():
                    if source_label in content_nodes: 
                        source_subgraph_id = f"cluster_content_for_{label_to_id[phase_label]}"
                        break

            # Check if target_label is a phase header or in a content cluster
            if target_label in phase_header_labels: 
                target_subgraph_id = 'phase_header_rank_group' 
            else:
                for phase_label, content_nodes in phase_content_mapping.items():
                    if target_label in content_nodes: 
                        target_subgraph_id = f"cluster_content_for_{label_to_id[phase_label]}"
                        break
                
            # Apply constraint=false to inter-subgraph/cluster edges to prevent them from distorting layout.
            # Use ltail/lhead for cleaner routing. Make specific inter-phase logical edges invisible.
            if source_subgraph_id and target_subgraph_id and source_subgraph_id != target_subgraph_id: 
                # If target is a phase header, and source is an estimated time node, make the edge invisible.
                if target_label in phase_header_labels and "estimated time" in source_label.lower():
                    dot.edge(source_id, target_id,
                             arrowsize='0.8',
                             penwidth='1.0',
                             ltail=source_subgraph_id if source_subgraph_id.startswith('cluster_') else None,
                             lhead=target_subgraph_id if target_subgraph_id.startswith('cluster_') else None,
                             constraint='false',
                             style='invis') # Make invisible to prevent layout distortion
                else:
                    dot.edge(source_id, target_id,
                             arrowsize='0.8',
                             penwidth='1.0',
                             ltail=source_subgraph_id if source_subgraph_id.startswith('cluster_') else None, 
                             lhead=target_subgraph_id if target_subgraph_id.startswith('cluster_') else None, 
                             constraint='false') 
            else: # Intra-cluster or regular edge
                dot.edge(source_id, target_id,
                        arrowsize='0.8',
                        penwidth='1.0')

    # --- Define Total Estimated Time Node (Late Definition for Rank Enforcement) --- #
    if total_time_node_label:
        total_time_node_id = label_to_id[total_time_node_label]
        
        # Create a dedicated subgraph for the total time node to strictly enforce its rank
        with dot.subgraph(name='cluster_total_time_bottom') as total_time_cluster:
            total_time_cluster.attr(rank='max', style='invis', label='_') # Force this subgraph to the very bottom
            total_time_cluster.node(total_time_node_id, total_time_node_label,
                                    fillcolor='orange',
                                    style='rounded,filled,bold',
                                    shape='box') # Node styling is within the subgraph

        # --- Handle Total Estimated Time Node Connections (Ensured Invisible) --- #
        last_estimated_time_id = None
        
        # Find the source of the edge to the total_time_node from the original graph_data
        for source_label, target_label in graph_data["edges"]:
            if target_label == total_time_node_label and "estimated time" in source_label.lower():
                last_estimated_time_id = label_to_id.get(source_label)
                break
        
        if last_estimated_time_id: 
            source_cluster_of_last_estimated_time = None
            for phase_label, content_nodes in phase_content_mapping.items():
                if last_estimated_time_id in [label_to_id.get(n) for n in content_nodes]:
                    source_cluster_of_last_estimated_time = f"cluster_content_for_{label_to_id[phase_label]}"
                    break

            # Explicitly make this edge invisible to ensure rank=max is honored without visual interference
            if source_cluster_of_last_estimated_time:
                dot.edge(last_estimated_time_id, total_time_node_id,
                         arrowsize='0.8',
                         penwidth='1.0',
                         ltail=source_cluster_of_last_estimated_time,
                         lhead='cluster_total_time_bottom', # Explicitly direct to the new total time subgraph
                         constraint='false',
                         style='invis') # Make invisible to prevent layout distortion
            else:
                dot.edge(last_estimated_time_id, total_time_node_id,
                         arrowsize='0.8', penwidth='1.0',
                         lhead='cluster_total_time_bottom', # Explicitly direct to the new total time subgraph
                         constraint='false', style='invis')

    return dot

    # After dot graph is completely built
    dot.render('career_roadmap', view=False, directory='MultiAgentGraph/knowledge_graph_builder/')