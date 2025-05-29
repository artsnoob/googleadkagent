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
- **Conversation Export**: Save entire conversation history (including tool calls) to markdown files for troubleshooting.

## Installation

### Prerequisites
- Python 3.8+
- `npm` or `npx` (for the MCP servers)
- Google ADK (`pip install google-generativeai-toolkit`)

### Steps
1. **Install Python dependencies:**
   ```powershell
   pip install -r config/requirements.txt
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

### Running the Agent
Start the interactive command-line agent:
```bash
python main.py
```

With specific model configuration:
```bash
python main.py --llm_provider gemini --model_name gemini-2.5-flash-preview-05-20
python main.py --llm_provider openrouter --model_name openrouter/anthropic/claude-3-haiku
```

### Interactive Commands
- Type your requests normally to interact with the agent
- `exit` - Quit the agent
- `save` - Export the current conversation to a markdown file in `data/conversation_exports/`

### Conversation Export
The agent automatically tracks all interactions including:
- User messages
- Agent responses  
- Tool calls with arguments and results
- Status messages and errors
- Metadata like web search queries and grounding sources

Exported conversations are saved as markdown files with timestamps, making them ideal for:
- Troubleshooting and debugging
- Sharing agent interactions
- Reviewing agent behavior
- Documentation

## Project Structure
- `main.py`: Entry point for the application
- `src/`: Main source code directory
  - `core/`: Core system components (mcp_agent.py, token_manager.py, error_recovery_system.py)
  - `agents/`: Agent configuration (agent_config.py)
  - `mcp/`: MCP server management (mcp_server_init.py)
  - `processors/`: Event and data processing (event_processor.py, conversation_logger.py)
  - `utils/`: Utilities and formatters (mcp_agent_utils.py, telegram_formatter.py)
- `data/`: Data and working files
  - `agent_files/`: Agent working directory
  - `conversation_exports/`: Exported conversation logs
- `docs/`: Documentation files
- `config/`: Configuration files (CLAUDE.md, requirements.txt)
    - `agent_files/`: Directory containing files used by the agent.
    - `.env`: Environment variables (e.g., API keys).
- `README.md`: Project README file.
- `requirements.txt`: Lists Python dependencies.
