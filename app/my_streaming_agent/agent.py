import asyncio
from contextlib import AsyncExitStack
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
# InMemorySessionService, Session, and Runner are not strictly needed for adk web agent definition
# from google.adk.sessions import InMemorySessionService, Session
# from google.adk.runners import Runner
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types # Still needed for types.Content, types.Part
from google.adk.tools import google_search, agent_tool

# Import from our new utils file (optional for adk web, but kept for consistency if utils are used by agent logic)
from .mcp_agent_utils import (
    COLOR_GREEN,
    COLOR_YELLOW,
    COLOR_CYAN,
    COLOR_MAGENTA,
    COLOR_RESET,
    pretty_print_json_string
)
# The apply_genai_content_text_patch() is called within mcp_agent_utils.py upon import.

# Load environment variables from .env file
# This should be present in the 'app/' directory from where 'adk web' is run.
load_dotenv()

# --- Global MCP Toolset Instances ---
# These are defined globally so they can be used by the root_agent
# when this script is imported by 'adk web'.

# Instantiate MCPToolset for the filesystem server
mcp_toolset_instance_filesystem = MCPToolset(
    connection_params=StdioServerParameters(
        command='npx', # Command to run the server
        args=["-y",    # Arguments for the command
              "@modelcontextprotocol/server-filesystem",
              # IMPORTANT: This path specifies the folder the filesystem MCP server will operate on.
              # We are using the agent_files directory.
              # This path should be absolute or resolvable from where adk web runs.
              os.path.abspath(os.path.join(os.path.dirname(__file__), "agent_files"))],
    )
)

# Instantiate MCPToolset for the code executor server
# Note: os.getcwd() will be the CWD of the process running this script.
# If 'adk web' is run from an 'app/' directory, these paths will be relative to 'app/'.
# For robustness, make paths absolute or relative to this script's location.
script_dir = os.path.dirname(__file__)
code_storage_dir_path = os.path.join(script_dir, ".mcp_code_storage") # Relative to script
venv_path_val = os.path.join(script_dir, '.mcp_venv') # Relative to script

mcp_toolset_instance_code_executor = MCPToolset(
    connection_params=StdioServerParameters(
        command='env', # Use 'env' to set environment variables
        args=[
            f"CODE_STORAGE_DIR={code_storage_dir_path}",
            "ENV_TYPE=venv",
            f"VENV_PATH={venv_path_val}",
            "node",
            # This path should be absolute or resolvable.
            "/Users/milanboonstra/code/openaisdkmcp_server_copy/mcp_code_executor/build/index.js"
        ],
        env={}
    )
)

# Instantiate MCPToolset for the content scraper server
mcp_toolset_instance_content_scraper = MCPToolset(
    connection_params=StdioServerParameters(
        command='node',
        args=[
            # This path should be absolute or resolvable.
            "/Users/milanboonstra/Documents/Cline/MCP/contentscraper-mcp-server/build/index.js"
        ],
    )
)

# Instantiate MCPToolset for the fetch server
mcp_toolset_instance_fetch = MCPToolset(
    connection_params=StdioServerParameters(
        command='node',
        args=[
            # This path should be absolute or resolvable.
            "/Users/milanboonstra/Documents/Cline/MCP/fetch-server/build/index.js"
        ],
    )
)

# --- Global Agent Definitions ---
# Using a streaming-compatible model as per ADK Streaming Quickstart
# Ensure this model ID is correct and supports streaming / Live API.
# Example from docs: "gemini-2.0-flash-live-001" or "gemini-2.0-flash-exp"
# The user's original script used 'gemini-2.5-flash-preview-04-17'.
# We need to confirm if this model supports the Live API for streaming.
# For now, using a known streaming model from the docs.
STREAMING_MODEL_ID = 'gemini-2.0-flash-exp' # Or 'gemini-2.0-flash-exp'

# Filesystem agent with MCP toolset
filesystem_agent = LlmAgent(
    model=STREAMING_MODEL_ID,
    name='filesystem_agent',
    instruction='You are a specialist in filesystem operations. Help users interact with the local filesystem using available tools. When asked to save a file, use the "agent_files" directory.',
    tools=[mcp_toolset_instance_filesystem],
)

# Search agent with Google Search
search_agent = LlmAgent(
    model=STREAMING_MODEL_ID,
    name='search_agent',
    instruction='You are a specialist in web search. Help users find current information from the web.',
    tools=[google_search],
)

# MCP Code Executor agent
mcp_code_executor_agent = LlmAgent(
    model=STREAMING_MODEL_ID,
    name='mcp_code_executor_agent',
    instruction='You are a specialist in code execution using the MCP code executor server. Help users run code via this server.',
    tools=[mcp_toolset_instance_code_executor],
)

# Content Scraper agent
content_scraper_agent = LlmAgent(
    model=STREAMING_MODEL_ID,
    name='content_scraper_agent',
    instruction='You are a specialist in scraping content from web sources like Reddit, RSS feeds, and Twitter using the MCP content scraper server. Help users gather information from these sources.',
    tools=[mcp_toolset_instance_content_scraper],
)

# Fetch agent
fetch_agent = LlmAgent(
    model=STREAMING_MODEL_ID,
    name='fetch_agent',
    instruction='You are a specialist in fetching and processing web page content using the MCP fetch server. Help users retrieve content from URLs, optionally converting to Markdown or searching within the content.',
    tools=[mcp_toolset_instance_fetch],
)

# Root agent that can delegate
# This root_agent will be discovered by 'adk web' if this file is named 'agent.py'
# and placed in the correct directory structure (e.g., app/your_agent_module_name/agent.py).
# If this file is 'streaming_agent.py', 'adk web' would be run against a module containing this.
root_agent = LlmAgent(
    model=STREAMING_MODEL_ID, # Ensure root_agent also uses a streaming-compatible model
    name='assistant_streaming', # Giving a slightly different name to distinguish if needed
    instruction='''You are a helpful assistant.
- For filesystem operations (e.g., read, write, list files, save content to files in the 'agent_files' directory), delegate to filesystem_agent.
- For web searches (e.g., finding current information, general queries), delegate to search_agent.
- For executing code snippets, delegate to mcp_code_executor_agent.
- For fetching content from a specific URL (e.g., "fetch example.com", "get content of page X as markdown"), delegate to fetch_agent. This agent can use tools like `fetch` (to get content, optionally as markdown) and `fetch_and_search` (to get content and search within it using regex).
- For scraping content from web sources:
    - Delegate to content_scraper_agent. This agent can use tools like `scrape_rss`, `scrape_reddit`, and `scrape_twitter`.
    - Keywords: "scrape", "get posts from Reddit", "fetch tweets", "latest news from RSS", "get articles from [URL]", "AI news".
    - Default sources for general "AI news" requests:
        - Twitter Accounts: ["OpenAI", "GoogleDeepMind", "GoogleAI", "MIT_CSAIL", "AndrewYNg", "huggingface", "a16z", "alliekmiller", "mattshumer_", "OfficialLoganK", "drfeifei", "jeremyphoward", "demishassabis", "ylecun", "karpathy", "RickLamers"] (Use with `scrape_twitter` tool, `posts_per_account` can be defaulted to 3-5 if not specified by user).
        - Reddit Subreddits: ["LocalLLaMA", "singularity", "artificial"] (Use with `scrape_reddit` tool, `posts_per_subreddit` can be defaulted to 10 if not specified by user).
        - RSS Feeds: [{"name": "TechCrunch", "url": "https://techcrunch.com/feed/"}, {"name": "Wired", "url": "https://www.wired.com/feed/rss"}, {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"}, {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index"}, {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml"}] (Use with `scrape_rss` tool, `articles_per_feed` can be defaulted to 5-10 if not specified by user, and `saveAsMarkdown` can be set to true if user requests Markdown output).
    - If the user asks to scrape from RSS, Reddit, or Twitter and provides specific URLs, subreddits, or accounts, use those instead of the defaults.
    - If the user makes a general request (e.g., "latest AI news") without specifying sources, use the default sources listed above.
    - The `scrape_rss` tool has a `saveAsMarkdown` parameter. If the user requests Markdown output from RSS, set this to true.
    - For Reddit and Twitter, the `scrape_reddit` and `scrape_twitter` tools return JSON data. If the user asks to save this data as Markdown, the `content_scraper_agent` will provide the JSON. You (the assistant) must then process this JSON into a suitable Markdown format (e.g., for each item: "### [Title](Link)\n\nContent snippet...") and then use the `filesystem_agent` to save it to a file (e.g., "ai_news_summary.md") in the 'agent_files' directory.
- For comprehensive website scraping (e.g., "scrape example.com and all its subpages and save to output.md"):
    - Acknowledge the request. Explain that you will generate a Python script to perform the crawl and then ask the `mcp_code_executor_agent` to run this script.
    - The Python script you generate should:
        - Be a single block of code.
        - Explicitly install required Python packages (e.g., `requests`, `beautifulsoup4`, `markdownify`) using `subprocess.run([sys.executable, '-m', 'pip', 'install', 'package_name'])` at the beginning of the script. Ensure to import `sys` and `subprocess`.
        - Accept the starting URL and the desired output filename (e.g., `adk_docs.md`) as parameters or have them clearly defined at the top of the script.
        - Recursively crawl all accessible subpages originating from the starting URL, staying within the same domain.
        - For each crawled page, convert its HTML content to Markdown.
        - Aggregate all Markdown content from all crawled pages into a single string.
        - Save the aggregated Markdown content to an **absolute path**: `os.path.join(os.path.dirname(__file__), "agent_files", "YOUR_OUTPUT_FILENAME.md")`. Replace `YOUR_OUTPUT_FILENAME.md` with the filename requested by the user or a sensible default.
        - Include error handling for network requests and parsing.
        - Print a success message upon completion, including the path to the saved file.
    - After generating the script, delegate its execution (as a string of code) to the `mcp_code_executor_agent`.
    - Once the `mcp_code_executor_agent` reports completion (or error), inform the user of the result.
    - If successful, you can use the `filesystem_agent` to confirm the existence of the output file in the `agent_files/` directory (relative to this script).
Ensure you understand the user's request and delegate to the most appropriate specialized agent or generate code as needed. If a task requires multiple steps across different agents (e.g., scrape then save), coordinate these steps sequentially. When saving, confirm the filename with the user or use a descriptive default like "ai_news_YYYY-MM-DD.md".''' ,
    tools=[
        agent_tool.AgentTool(agent=filesystem_agent),
        agent_tool.AgentTool(agent=search_agent),
        agent_tool.AgentTool(agent=mcp_code_executor_agent),
        agent_tool.AgentTool(agent=content_scraper_agent),
        agent_tool.AgentTool(agent=fetch_agent)
    ],
)

# The console interaction loop (async_main, Runner, input loop) is omitted
# as 'adk web' handles the agent execution and interaction.
# If this script is run directly, it will define the agents but not start an interactive session.

# To make MCP toolsets close gracefully when the 'adk web' process exits,
# you might need to investigate ADK's lifecycle hooks for agents or tools,
# or rely on the OS to terminate the subprocesses started by StdioServerParameters.
# The AsyncExitStack was tied to the async_main execution context.
# For now, explicit close calls are omitted for simplicity in the 'adk web' context.

if __name__ == '__main__':
    # This block can be used for testing the agent definitions if needed,
    # but it won't run the interactive console loop from mcp_agent.py.
    print(f"Script {__file__} loaded. 'root_agent' named '{root_agent.name}' is defined.")
    print("This script is intended to be used with 'adk web'.")
    print("Example: adk web --agent_module_name your_app_folder.your_agent_module")
    print("Where 'your_agent_module' contains this 'streaming_agent.py' (or 'agent.py').")
