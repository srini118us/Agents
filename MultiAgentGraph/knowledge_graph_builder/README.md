# Career Roadmap Knowledge Graph Generator

This project is a Streamlit application that generates a career roadmap as a knowledge graph, visualizing the learning path for a specific domain.

## Project Structure

The core logic of this multi-agent system resides in the `MultiAgentGraph/knowledge_graph_builder/` directory, which contains the following main subdirectories:

*   `agents/`: Core AI agents (e.g., researcher, synthesizer, mapper).
*   `helpers/`: Consolidated utilities and external tool wrappers.
*   `workflows/`: Agent orchestration and flow definitions.
*   `data/`: (Optional) For input/output data.

## File Structure

This project is structured to facilitate a modular and scalable multi-agent system. Below is an overview of the key directories and files:

*   **`agents/`**: Contains the implementations of various specialized AI agents, each responsible for a specific task within the knowledge graph generation pipeline. 
    *   `researcher.py`: Implements the **Knowledge Extraction Agent**, responsible for gathering raw information.
    *   `synthesizer.py`: Implements the **Knowledge Synthesis Agent**, which processes and refines extracted information.
    *   `mapper.py`: Implements the **Knowledge Graph Builder Agent**, responsible for constructing the graph structure.

*   **`helpers/`**: This consolidated directory contains reusable modules that provide external functionalities (formerly `tools/`) and general utility functions (formerly `utils/`) for the agents and application logic.
    *   `serpapi_tool.py`, `wikipedia_tool.py`, `research_api_tool.py`: These files contain wrappers or direct implementations for interacting with external services and APIs (e.g., web search) that the agents might use for data collection or validation.
    *   `graphviz_exporter.py`: This module is crucial for visualizing the knowledge graph, handling the conversion of graph data into a format suitable for Graphviz and generating image outputs.
    *   `generate_agent_flow_diagram.py`: A script to generate a visual diagram of the multi-agent system's internal flow.
    *   `config.py` (if present): Often used for managing application configurations and settings.

*   **`workflows/`**: Defines the orchestration logic and state management for the multi-agent system, particularly if using frameworks like LangChain/LangGraph.
    *   `langgraph_router.py`: This file is central to defining the multi-agent workflow. It orchestrates the flow between different agents and tools, often handling conditional routing and state transitions based on the process requirements.

*   **`data/`**: (if present) Typically used for storing any data-related files, such as raw inputs, processed outputs, or static assets.

*   **`app.py`**: The main Streamlit application file. It serves as the user interface, handles user inputs, and initiates the multi-agent workflow by interacting with the orchestration logic.

*   **`setup.py`**: A standard Python file used for packaging and distributing the project. It defines metadata about the project (like its name, version, dependencies) and specifies how the project can be installed.

## Repository

You can find the source code for this project on GitHub:
[https://github.com/srini118us/Agents]

## How to Run

1.  **Navigate to the project directory**:
    ```bash
    cd MultiAgentGraph/knowledge_graph_builder/
    ```
2.  **Ensure dependencies are installed**:
    If you haven't already, install the required Python packages (e.g., `streamlit`, `graphviz`, etc.). You can typically find these in `requirements.txt` within this directory.
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment Variables (Optional)**:
    If your agents require API keys (e.g., for LLMs or external search services), create a `.env` file in this directory (`MultiAgentGraph/knowledge_graph_builder/`).
    ```
    # Example .env content
    # OPENAI_API_KEY="your_openai_api_key"
    # SERP_API_KEY="your_serpapi_key"
    ```
    This file is ignored by Git (via the `.gitignore` at the workspace root) to prevent sensitive data from being committed.
4.  **Run the Streamlit application**:
    ```bash
    streamlit run app.py
    ```
    This will open the application in your web browser.

## Output

The application generates a visual knowledge graph. Additionally, a static PNG image of the graph is saved as `career_roadmap.png` in this directory (`MultiAgentGraph/knowledge_graph_builder/`).

## Agent Flow

The knowledge graph generation process involves multiple specialized agents working in a coordinated pipeline to transform a user's request into a structured visual roadmap.

```mermaid
graph TD
    A[User Input/Query] --> B[Orchestration Agent]
    B --> C[Knowledge Extraction Agent]
    C --> D[Knowledge Synthesis Agent]
    D --> E[Knowledge Graph Builder Agent]
    E --> F[Graph Export/Visualization Agent]
    F --> G[Streamlit Application]
    G --> H[Display Knowledge Graph]
    style E fill:#f9f,stroke:#333,stroke-width:2px
```

Here is a more detailed visual representation of the agent workflow:

![Agent Flow Diagram](agent_flow_diagram.png)

*   **User Input/Query**: The process begins with the user providing a specific query or topic for which they want a career roadmap through the Streamlit interface.

*   **Orchestration Agent** (`app.py`): This agent serves as the central control unit. It receives the user's initial query and intelligently delegates tasks to other specialized agents in a predefined sequence. It manages the overall workflow, ensuring each step is executed and its output is seamlessly passed to the next relevant agent in the pipeline.

*   **Knowledge Extraction Agent** (`researcher.py`): Upon receiving a task from the Orchestration Agent, this agent is responsible for gathering raw, unstructured information from various sources. It might interact with external tools or APIs (e.g., web search, encyclopedias) to collect data relevant to the user's query and the different phases of a career roadmap. Its primary output is raw extracted text or factual data.

*   **Knowledge Synthesis Agent** (`synthesizer.py`): This agent takes the raw information extracted by the Knowledge Extraction Agent. Its crucial role is to process, filter, summarize, and refine this information, transforming it into more coherent, concise, and structured data points. This synthesized information is optimized for subsequent graph construction.

*   **Knowledge Graph Builder Agent** (`mapper.py`): Receiving the refined and synthesized data, this agent is responsible for constructing the core knowledge graph structure. It identifies key concepts, career phases, required skills, and the relationships between them, defining these as nodes and edges. Essentially, it translates the processed information into a formal graph data format.

*   **Graph Export/Visualization Agent** (`graphviz_exporter.py`): This agent receives the structured knowledge graph data (nodes and edges) from the Knowledge Graph Builder Agent. It then leverages the Graphviz library to convert this data into a visual representation (DOT language string). This agent is responsible for generating two main outputs:
    *   **Interactive Streamlit Graph**: The generated DOT output is directly used by the Streamlit application to display an interactive and dynamic version of the career roadmap within the web interface.
    *   **Static PNG File**: A static image file named `career_roadmap.png` is automatically saved in this directory (`MultiAgentGraph/knowledge_graph_builder/`), providing a permanent and easily shareable visual output of the graph.

*   **Streamlit Application** (`app.py`): Beyond its role in orchestration, `app.py` serves as the primary user interface for the entire system. It handles user input, integrates all the agent interactions behind the scenes, and displays the final interactive knowledge graph, providing a seamless user experience.

*   **Display Knowledge Graph**: This represents the ultimate visual output of the system: the fully rendered career roadmap, available both as an interactive component within the Streamlit application and as a static `career_roadmap.png` image file. 