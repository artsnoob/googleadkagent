# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Agent

Start the interactive command-line agent:
```bash
python main.py
```

With specific model configuration:
```bash
python main.py --llm_provider gemini --model_name gemini-2.5-flash-preview-05-20
python main.py --llm_provider openrouter --model_name openrouter/anthropic/claude-3-haiku
```

Note: OpenRouter requires `OPENROUTER_API_KEY` in `.env`. Perplexity features require `PERPLEXITY_API_KEY`.

## Environment Setup

Required environment variables in `.env`:
- `GOOGLE_API_KEY` - Google Gemini API access
- `OPENROUTER_API_KEY` - (Optional) For OpenRouter models
- `PERPLEXITY_API_KEY` - (Optional) For Perplexity research features
- `TELEGRAM_BOT_TOKEN` - (Optional) For Telegram messaging features
- `DEFAULT_CHAT_ID` - (Optional) Default Telegram chat/channel ID

Install dependencies:
```bash
pip install -r config/requirements.txt
```

## Architecture Overview

This is a **modular multi-agent system** built on Google ADK with the following design:

### Agent Hierarchy
- **Root Agent** (`src/core/mcp_agent.py`) - Orchestrates and delegates to specialized agents
- **Specialized Agents** (`src/agents/agent_config.py`) - Each handles specific domains:
  - Filesystem operations
  - Web search and research  
  - Python code execution
  - Content scraping (Reddit/RSS/Twitter)
  - URL fetching and processing
  - Deep research via Perplexity

### Core Components
- **`main.py`** - Entry point script
- **`src/core/mcp_agent.py`** - Main conversation loop, model configuration
- **`src/agents/agent_config.py`** - Agent creation and instruction definitions
- **`src/mcp/mcp_server_init.py`** - MCP server lifecycle management with error recovery
- **`src/processors/event_processor.py`** - Response handling, grounding metadata display
- **`src/core/token_manager.py`** - Context window management and conversation truncation
- **`src/core/error_recovery_system.py`** - Automatic fallback strategies for tool failures

### MCP Server Dependencies
The system relies on external Node.js MCP servers that must be available:
- `@modelcontextprotocol/server-filesystem` (via npx)
- Custom code executor server at `/Users/milanboonstra/code/openaisdkmcp_server_copy/mcp_code_executor/build/index.js`
- Content scraper at `/Users/milanboonstra/Documents/Cline/MCP/contentscraper-mcp-server/build/index.js`  
- Fetch server at `/Users/milanboonstra/Documents/Cline/MCP/fetch-server/build/index.js`
- Perplexity server at `/Users/milanboonstra/Documents/Cline/MCP/perplexity-mcp/build/index.js`
- Telegram server at `/Users/milanboonstra/Documents/Cline/MCP/telegram-server/build/index.js`

### Agent Communication Pattern
1. User input goes to Root Agent
2. Root Agent delegates to appropriate specialized agent(s) 
3. Specialized agents use their MCP tools or built-in capabilities
4. Responses flow back through Root Agent to user
5. Error recovery system handles tool failures with automatic fallbacks

### File Operations
All agent file operations target the `data/agent_files/` directory, which serves as the shared workspace between the filesystem MCP server and code executor.

### Multi-Model Support
- Default: Gemini models with configurable context windows (120k-1M tokens)
- Optional: OpenRouter integration via LiteLLM
- Token management automatically handles model-specific limits

## Key Development Patterns

When extending the system:
- Add new agents in `src/agents/agent_config.py` following the existing pattern
- MCP servers are initialized in `src/mcp/mcp_server_init.py` with automatic error recovery
- All agents include comprehensive fallback instructions for when their tools fail
- Use the error recovery system for graceful degradation
- Agent instructions emphasize proactive behavior and cross-agent coordination

The modular design allows independent development and testing of each component while maintaining clean separation of concerns.