# Google ADK Streaming Agent

## Description
This project demonstrates the use of the Google Agent Development Kit (ADK) to create a streaming AI agent with various capabilities, including filesystem operations, web search, code execution, content scraping, and fetching web content. The agent leverages multiple Model Context Protocol (MCP) servers and Google Search to perform these operations through natural language commands. The agent is designed to be run with `adk web` for a web-based interface.

## Features
- Web-based interface via `adk web`.
- Integration with Google ADK's `LlmAgent`.
- Utilizes local MCP servers for filesystem operations, code execution, content scraping, and fetching web content.
- Integrates with Google Search.
- Uses the `gemini-2.5-flash-preview-04-17` model for streaming responses.
- Supports `python-dotenv` for environment variable management.
- When none of the built-in tools fit a request, the agent can generate a short
  Python script and execute it through the MCP code executor, asking for
  confirmation if additional steps are required.

## Installation

### Prerequisites
- Python 3.8+
- `npm` or `npx` (for the MCP servers)
- Google ADK (`pip install google-generativeai-toolkit`)

### Steps
1. **Install Python dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the `app/` directory and add your Google API key:
   ```
   GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY_HERE
   GOOGLE_GENAI_USE_VERTEXAI=FALSE # Set to TRUE if using Vertex AI
   ```

3. **MCP Server Setup:**
   This project relies on several local MCP servers. Ensure you have the necessary servers installed and running or configured to be started by the agent. The agent is configured to start the following servers using `npx` or node:
   - `@modelcontextprotocol/server-filesystem`
   - `mcp_code_executor` (requires building from source)
   - `contentscraper-mcp-server` (requires building from source)
   - `fetch-server` (requires building from source)

## Usage
To run the ADK web agent, navigate to the `app/` directory in your terminal and execute:

```powershell
adk web
```

The agent will start, and you can access the web interface at the address provided in the terminal output (usually http://localhost:8000). Interact with the agent through the web interface by typing your commands.

## Project Structure
- `app/`: Contains the ADK agent module.
  - `my_streaming_agent/`: The agent module directory.
    - `agent.py`: The main script that initializes and runs the ADK agent.
    - `mcp_agent_utils.py`: Utility functions for the MCP agent.
    - `agent_files/`: Directory containing files used by the agent.
    - `.env`: Environment variables (e.g., API keys).
- `README.md`: Project README file.
- `requirements.txt`: Lists Python dependencies.
