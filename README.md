# Google ADK Filesystem Agent

## Description
This project demonstrates the use of the Google Agent Development Kit (ADK) to create an AI agent capable of interacting with the local filesystem. The agent leverages a Model Context Protocol (MCP) filesystem server to perform operations like listing files and reading content, all through natural language commands.

## Features
- Interactive command-line interface for the agent.
- Integration with Google ADK's `LlmAgent`.
- Utilizes a local MCP filesystem server for file operations.
- Supports `python-dotenv` for environment variable management.

## Installation

### Prerequisites
- Python 3.8+
- `npm` or `npx` (for the MCP filesystem server)

### Steps
1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project root and add your Google API key:
   ```
   GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY_HERE
   GOOGLE_GENAI_USE_VERTEXAI=FALSE # Set to TRUE if using Vertex AI
   ```

## Usage
To run the interactive agent, execute the `mcp_agent.py` script:

```bash
python mcp_agent.py
```

The agent will start, and you can type commands like "list files in the current directory" or "read the file `README.md`". Type `exit` to quit the agent.

## Project Structure
- `mcp_agent.py`: The main script that initializes and runs the ADK agent.
- `google_adk_documentation.md`: Comprehensive documentation and code snippets for the Google ADK.
- `requirements.txt`: Lists Python dependencies.
- `.env`: Environment variables (e.g., API keys).
