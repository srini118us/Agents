from graphviz import Digraph

def create_agent_flow_diagram():
    dot = Digraph(comment='Stateful Agent System Workflow', format='png')
    dot.attr(rankdir='TB',  # Top-to-Bottom flow
            nodesep='0.8',    # Space between nodes
            ranksep='1.2',    # Space between ranks
            fontsize='12',
            fontname='Helvetica')

    # === Node Definitions with specific styles ===
    # Start Node
    dot.node('start', '_start_', shape='oval', fillcolor='#E6E6FA', style='filled')

    # Supervisor Node
    dot.node('supervisor', 'Supervisor', shape='box', fillcolor='#CCCCFF', style='filled')

    # Call Nodes (Grey, Box)
    dot.node('llm_call', 'Llm Call', shape='box', fillcolor='#D3D3D3', style='filled')
    dot.node('rag_call', 'Rag Call', shape='box', fillcolor='#D3D3D3', style='filled')
    dot.node('web_call', 'Web Call', shape='box', fillcolor='#D3D3D3', style='filled')

    # Agent Nodes (Light Purple/Blue, Box)
    dot.node('llm', 'LLM', shape='box', fillcolor='#CCCCFF', style='filled')
    dot.node('rag', 'RAG', shape='box', fillcolor='#CCCCFF', style='filled')
    dot.node('web', 'WEB', shape='box', fillcolor='#CCCCFF', style='filled')

    # Validation Node
    dot.node('validation', 'Validation', shape='box', fillcolor='#CCCCFF', style='filled')

    # Revoked State
    dot.node('revoked', 'revoked', shape='box', fillcolor='#D3D3D3', style='filled')

    # === Edge Definitions ===
    dot.edge('start', 'supervisor') # Solid line

    # Supervisor dispatch calls (dotted lines)
    dot.edge('supervisor', 'llm_call', style='dotted')
    dot.edge('supervisor', 'rag_call', style='dotted')
    dot.edge('supervisor', 'web_call', style='dotted')

    # Call results to agents (dotted lines)
    dot.edge('llm_call', 'llm', style='dotted')
    dot.edge('rag_call', 'rag', style='dotted')
    dot.edge('web_call', 'web', style='dotted')

    # Agent outputs to Validation (solid lines)
    dot.edge('llm', 'validation')
    dot.edge('rag', 'validation')
    dot.edge('web', 'validation')

    # Conditional/Revoked paths (dotted lines)
    dot.edge('supervisor', 'revoked', label='revoked', style='dotted')
    dot.edge('web_call', 'revoked', label='revoked', style='dotted')

    # Render the graph to a PNG file
    output_directory = 'MultiAgentGraph/knowledge_graph_builder/'
    dot.render('agent_flow_diagram', view=False, directory=output_directory)
    print(f"Agent flow diagram 'agent_flow_diagram.png' generated successfully in {output_directory}")

if __name__ == '__main__':
    create_agent_flow_diagram() 