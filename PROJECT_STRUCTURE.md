# Google ADK Agent Project Structure

## Overview
A modular multi-agent system built with Google ADK that provides file operations, web search, code execution, content scraping, and AI research capabilities through specialized agents.

## Core Architecture

### Main Entry Point
- **`mcp_agent.py`** (169 lines) - Main orchestrator
  - Argument parsing for model selection
  - Token management initialization
  - Error recovery system setup
  - Conversation loop and user interaction
  - Agent coordination

### Modular Components

#### Agent Configuration
- **`agent_config.py`** - Agent creation and configuration
  - `create_filesystem_agent()` - File operations specialist
  - `create_search_agent()` - Web search and research
  - `create_code_executor_agent()` - Python code execution
  - `create_content_scraper_agent()` - Social media/RSS scraping
  - `create_fetch_agent()` - URL content retrieval
  - `create_perplexity_agent()` - Deep research and analysis
  - `create_root_agent()` - Coordinator that delegates to all agents
  - `create_all_agents()` - Factory function for all agents

#### MCP Server Management
- **`mcp_server_init.py`** - MCP server initialization
  - `initialize_mcp_server()` - Generic server setup with error recovery
  - `initialize_all_mcp_servers()` - Sets up all MCP servers:
    - Filesystem server (npx @modelcontextprotocol/server-filesystem)
    - Code executor server (custom Node.js MCP server)
    - Content scraper server (custom Node.js MCP server)
    - Fetch server (custom Node.js MCP server)
    - Perplexity server (custom Node.js MCP server)

#### Event Processing
- **`event_processor.py`** - Response handling and display
  - `process_events()` - Processes agent responses with error recovery
  - Handles text responses, function calls, and grounding metadata
  - Displays web search queries, sources, and URL context
  - Color-coded output formatting

### Supporting Modules

#### Utilities and Display
- **`mcp_agent_utils.py`** - UI utilities and formatting
  - Color constants and symbols
  - Pretty printing functions
  - Status messages and section headers
  - Tool response formatting
  - Conversation statistics tracking
  - GenAI content text patching

#### System Management
- **`token_manager.py`** - Context window management
  - Token counting and tracking
  - Conversation history truncation
  - Large message splitting
  - Model-specific token limits

- **`error_recovery_system.py`** - Error handling and recovery
  - Failure context creation
  - Recovery strategy suggestions
  - Graceful degradation patterns
  - Tool failure handling

### Configuration and Documentation
- **`config.md`** - Default sources for content scraping
- **`requirements.txt`** - Python dependencies
- **`agent_development_status.md`** - Development progress tracking
- **`adk_docs.md`** - ADK-specific documentation
- **`README.md`** - Project overview and setup instructions

### Data Directory
- **`agent_files/`** - Working directory for agent file operations
  - All file creation, reading, and processing happens here
  - Shared between filesystem MCP and code executor
  - User-accessible file storage

### Environment
- **`venv/`** - Python virtual environment
- **`.env`** - Environment variables (API keys, configuration)

## Agent Capabilities

### Filesystem Agent
- File and directory operations
- Content search and organization
- Format conversions
- Data processing

### Search Agent
- Google Search integration
- Information synthesis
- Source verification
- Current events research

### Code Executor Agent
- Python script execution
- Package management
- Data analysis
- Automation tasks

### Content Scraper Agent
- Reddit post collection
- RSS feed processing
- Twitter content gathering
- AI news aggregation

### Fetch Agent
- URL content retrieval
- HTML to Markdown conversion
- Content search and filtering
- Web scraping

### Perplexity Agent
- Deep research synthesis
- API documentation analysis
- Code security checking
- Expert-level insights

### Root Agent
- Multi-agent coordination
- Task delegation
- Error recovery orchestration
- Solution pathway planning

## Key Features

### Multi-Model Support
- Gemini models (default)
- OpenRouter integration
- Model-specific token management

### Error Recovery
- Automatic fallback strategies
- Alternative tool suggestions
- Graceful degradation
- User-friendly error messages

### Token Management
- Context window optimization
- Conversation history truncation
- Large input handling
- Model-aware limits

### Modular Design
- Single responsibility components
- Easy maintenance and updates
- Independent module testing
- Clean separation of concerns

## External Dependencies

### MCP Servers (Node.js)
- Filesystem operations
- Code execution environment
- Content scraping services
- Web fetching capabilities
- Perplexity AI integration

### APIs
- Google Gemini
- OpenRouter (optional)
- Perplexity AI
- Various content sources

## Usage Patterns

### Typical Workflows
1. **Data Analysis**: Search → Code Execution → Filesystem
2. **Content Creation**: Research → Analysis → File Saving
3. **Web Workflows**: Fetch → Process → Save → Report
4. **AI News**: Content Scraper → Analysis → Summary

### Command Line Options
```bash
python mcp_agent.py --llm_provider gemini --model_name gemini-2.5-flash-preview-05-20
python mcp_agent.py --llm_provider openrouter --model_name openrouter/anthropic/claude-3-haiku
```

This modular architecture ensures maintainability, scalability, and clear separation of concerns while providing a powerful multi-agent AI assistant system.