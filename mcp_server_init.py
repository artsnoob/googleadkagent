"""
MCP Server initialization module for MCP Agent system.
Contains all MCP server setup and error handling logic.
"""

import os
from contextlib import AsyncExitStack
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from mcp_agent_utils import print_status_message, COLOR_YELLOW, COLOR_RESET
from error_recovery_system import ErrorRecoverySystem, create_failure_context


async def initialize_mcp_server(server_name: str, init_func, error_recovery: ErrorRecoverySystem, exit_stack: AsyncExitStack):
    """Helper function with enhanced error recovery for MCP server initialization"""
    try:
        server_instance = init_func()
        exit_stack.push_async_callback(lambda: server_instance.close())
        print_status_message(f"{server_name} initialized successfully", "success", show_time=False)
        return server_instance
    except Exception as e:
        context = create_failure_context(e, tool_name=server_name, user_intent="initialize_mcp_server")
        fallback_result = await error_recovery.handle_failure(context)
        print_status_message(f"{server_name} failed to initialize: {fallback_result.user_message}", "warning", show_time=False)
        return None


async def initialize_all_mcp_servers(error_recovery: ErrorRecoverySystem, exit_stack: AsyncExitStack):
    """Initialize all MCP servers and return them as a dictionary."""
    
    # Initialize filesystem server
    mcp_toolset_instance_filesystem = await initialize_mcp_server(
        "filesystem_server",
        lambda: MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=["-y", "@modelcontextprotocol/server-filesystem",
                      "/Users/milanboonstra/code/googleadkagent/agent_files"],
            )
        ),
        error_recovery,
        exit_stack
    )

    # Initialize code executor server
    code_storage_dir = "/Users/milanboonstra/code/googleadkagent/agent_files"
    mcp_toolset_instance_code_executor = await initialize_mcp_server(
        "code_executor_server",
        lambda: MCPToolset(
            connection_params=StdioServerParameters(
                command='env',
                args=[
                    f"CODE_STORAGE_DIR={code_storage_dir}",
                    "ENV_TYPE=venv",
                    f"VENV_PATH={os.path.join(os.getcwd(), '.mcp_venv')}",
                    "node",
                    "/Users/milanboonstra/code/openaisdkmcp_server_copy/mcp_code_executor/build/index.js"
                ],
                env={}
            )
        ),
        error_recovery,
        exit_stack
    )

    # Initialize content scraper server
    mcp_toolset_instance_content_scraper = await initialize_mcp_server(
        "content_scraper_server",
        lambda: MCPToolset(
            connection_params=StdioServerParameters(
                command='node',
                args=["/Users/milanboonstra/Documents/Cline/MCP/contentscraper-mcp-server/build/index.js"],
            )
        ),
        error_recovery,
        exit_stack
    )

    # Initialize fetch server
    mcp_toolset_instance_fetch = await initialize_mcp_server(
        "fetch_server",
        lambda: MCPToolset(
            connection_params=StdioServerParameters(
                command='node',
                args=["/Users/milanboonstra/Documents/Cline/MCP/fetch-server/build/index.js"],
            )
        ),
        error_recovery,
        exit_stack
    )

    # Check for Perplexity API key and warn if missing
    perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
    if not perplexity_api_key:
        print(f"{COLOR_YELLOW}Warning: PERPLEXITY_API_KEY is not set in .env. Perplexity MCP server might fail.{COLOR_RESET}")

    # Initialize Perplexity server
    mcp_toolset_instance_perplexity = await initialize_mcp_server(
        "perplexity_server",
        lambda: MCPToolset(
            connection_params=StdioServerParameters(
                command='env',
                args=[
                    f"PERPLEXITY_API_KEY={perplexity_api_key}",
                    "node",
                    "/Users/milanboonstra/Documents/Cline/MCP/perplexity-mcp/build/index.js"
                ],
                env={}
            )
        ),
        error_recovery,
        exit_stack
    )

    # Check for Telegram bot tokens and warn if missing
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    default_chat_id = os.getenv("DEFAULT_CHAT_ID")
    if not telegram_bot_token or not default_chat_id:
        print(f"{COLOR_YELLOW}Warning: TELEGRAM_BOT_TOKEN or DEFAULT_CHAT_ID is not set in .env. Telegram MCP server might fail.{COLOR_RESET}")

    # Initialize Telegram server
    mcp_toolset_instance_telegram = await initialize_mcp_server(
        "telegram_server",
        lambda: MCPToolset(
            connection_params=StdioServerParameters(
                command='env',
                args=[
                    f"TELEGRAM_BOT_TOKEN={telegram_bot_token}",
                    f"DEFAULT_CHAT_ID={default_chat_id}",
                    "node",
                    "/Users/milanboonstra/Documents/Cline/MCP/telegram-server/build/index.js"
                ],
                env={}
            )
        ),
        error_recovery,
        exit_stack
    )

    return {
        'filesystem': mcp_toolset_instance_filesystem,
        'code_executor': mcp_toolset_instance_code_executor,
        'content_scraper': mcp_toolset_instance_content_scraper,
        'fetch': mcp_toolset_instance_fetch,
        'perplexity': mcp_toolset_instance_perplexity,
        'telegram': mcp_toolset_instance_telegram
    }