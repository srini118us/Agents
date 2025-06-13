from typing import Dict, Union, List, Tuple
from agents.researcher import research_topic
from agents.synthesizer import synthesize_snippet
from agents.mapper import map_to_graph

def generate_roadmap(topic: str) -> Dict[str, Union[Dict[str, List], str]]:
    """
    Generates a knowledge roadmap for the given topic by:
    1. Fetching relevant information (search + wiki)
    2. Synthesizing the content into a summary
    3. Mapping that summary into a graph structure

    Args:
        topic (str): The topic to generate a roadmap for. Must be a non-empty string
                    with length between 3 and 100 characters.

    Returns:
        Dict[str, Union[Dict[str, List], str]]: Either:
            - A dictionary containing the graph structure with 'nodes' and 'edges' keys
            - A dictionary with an 'error' key containing the error message

    Raises:
        ValueError: If the topic is invalid (empty, too short, or too long)
    """
    # Input validation
    if not isinstance(topic, str):
        return {"error": "Topic must be a string"}
    if not topic.strip():
        return {"error": "Topic cannot be empty"}
    if len(topic) < 3 or len(topic) > 100:
        return {"error": "Topic length must be between 3 and 100 characters"}

    try:
        # Research phase
        snippet = research_topic(topic)
        if not snippet or snippet.startswith("An error occurred"):
            return {"error": f"Research failed: {snippet}"}

        # Synthesis phase
        summary = synthesize_snippet(topic, snippet)
        if not summary:
            return {"error": "Synthesis failed - no summary generated"}

        # Mapping phase
        graph = map_to_graph(summary)
        if not graph or not isinstance(graph, dict) or 'nodes' not in graph or 'edges' not in graph:
            return {"error": "Mapping failed - invalid graph structure generated"}

        return {"nodes": graph["nodes"], "edges": graph["edges"], "summary": summary}

    except Exception as e:
        return {"error": f"Exception in generate_roadmap: {str(e)}"}