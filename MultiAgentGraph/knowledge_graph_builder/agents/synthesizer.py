#pip install openai
#from knowledge_graph_builder.workflows.langgraph_router import generate_roadmap

from helpers.research_api_tool import call_openai


def synthesize_snippet(topic, snippet):
    prompt = f"""
    You are an expert career coach and educator.

    Based on the topic: "{topic}", break down the roadmap into clear phases.

    Output Format(Strict, Multi-line for hierarchy):
    Each line represents a direct hierarchical connection. Follow this exact format:
    Phase Title
    Phase Title > Prerequisites (subtopic)
    Prerequisites (subtopic) > Core Topic/Module
    Core Topic/Module > Tool/Platform/Framework
    Tool/Platform/Framework > Estimated Time (X months)

    Ensure ALL time estimates are linked to their corresponding tool/module.
    Ensure there is a single 'Total Estimated Time' node at the end, linked from the final phase's estimated time.

    Example:
    Phase 1: Fundamentals
    Phase 1: Fundamentals > Mathematics, Statistics, Programming Basics
    Mathematics, Statistics, Programming Basics > High School Mathematics, Introductory Logic Courses
    High School Mathematics, Introductory Logic Courses > Estimated Time (3 months)
    Phase 2: Advanced Programming
    Phase 2: Advanced Programming > Data Structures and Algorithms
    Data Structures and Algorithms > Algorithms, Part I & II by Princeton University on Coursera, Intro to Data Structures and Algorithms by Udacity
    Algorithms, Part I & II by Princeton University on Coursera, Intro to Data Structures and Algorithms by Udacity > Estimated Time (4 months)
    Total Estimated Time (X years) Note: ...

    Context:
    {snippet}

    Format it as a clear hierarchy for building a knowledge graph.
    Encourage commitment and clarity with timelines.
    """
    return call_openai(prompt)
