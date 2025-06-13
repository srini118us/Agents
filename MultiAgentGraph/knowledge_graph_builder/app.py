import streamlit as st
from workflows.langgraph_router import generate_roadmap
from helpers.graphviz_exporter import export_to_graphviz

st.set_page_config(page_title="Career Roadmap Generator", layout="wide")

st.title("🚀 Career Path Roadmap Generator")
topic = st.text_input("🎯 Enter a career topic (e.g., Data Scientist, DevOps Engineer)")

# Add a checkbox to toggle debug output
show_debug_output = st.checkbox("Show Raw Synthesis Output (for Debugging)", value=False)

if topic:
    graph_data = generate_roadmap(topic)

    #st.subheader("🧠 Raw Output (for Debugging)")
    #st.json(graph_data)

    if 'error' in graph_data:
        st.error(graph_data['error'])
    else:
        if show_debug_output:
            st.subheader("Raw Synthesis Output (for Debugging)")
            st.code(graph_data.get('summary', "Summary not available."))
            # Display raw DOT string for debugging graph layout
            st.subheader("Raw Graphviz DOT Output (for Debugging)")
            dot = export_to_graphviz(graph_data)
            st.code(dot.source) # Display the raw .dot source

        if 'nodes' in graph_data and 'edges' in graph_data:
            st.subheader("📊 Career Roadmap Graph")
            # We re-render here to avoid issues if the above debug display consumes the dot object
            dot = export_to_graphviz(graph_data)
            st.graphviz_chart(dot)
        else:
            st.warning("⚠️ Graph format incorrect. Expected 'nodes' and 'edges'.")