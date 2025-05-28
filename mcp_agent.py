import asyncio
from contextlib import AsyncExitStack
import os # Import os
import argparse # Import argparse for command-line arguments
from dotenv import load_dotenv # Import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm # Import LiteLlm
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types # Still needed for types.Content, types.Part, types.Tool, types.GoogleSearch, types.UrlContext
from google.adk.tools import google_search # Import google_search tool
# Import from our new utils file
from mcp_agent_utils import (
    COLOR_GREEN,
    COLOR_YELLOW,
    COLOR_CYAN,
    COLOR_MAGENTA,
    COLOR_RESET,
    COLOR_BLUE,
    COLOR_RED,
    COLOR_DIM,
    SYMBOL_SUCCESS,
    SYMBOL_ERROR,
    SYMBOL_WARNING,
    SYMBOL_INFO,
    SYMBOL_THINKING,
    SYMBOL_TOOL,
    SYMBOL_SEARCH,
    pretty_print_json_string,
    print_section_header,
    print_status_message,
    format_tool_response,
    print_session_stats,
    ConversationStats,
)
# Import token manager
from token_manager import TokenManager
# Import error recovery system
from error_recovery_system import ErrorRecoverySystem, create_failure_context, handle_tool_failure, COLOR_ERROR, COLOR_WARNING, COLOR_SUCCESS, COLOR_INFO

# Define blue color for URL context metadata
COLOR_BLUE = "\033[94m"

# The apply_genai_content_text_patch() is called within mcp_agent_utils.py upon import.



# Load environment variables from .env file
load_dotenv()

# --- Argument Parsing for Model Selection ---
parser = argparse.ArgumentParser(description="Run ADK Agent with selectable LLM provider and model.")
parser.add_argument(
    "--llm_provider",
    type=str,
    default="gemini",
    choices=["gemini", "openrouter"],
    help="The LLM provider to use ('gemini' or 'openrouter'). Default is 'gemini'."
)
parser.add_argument(
    "--model_name",
    type=str,
    default="gemini-2.5-flash-preview-05-20",
    help="The model name to use. For Gemini, e.g., 'gemini-2.5-flash-preview-05-20'. For OpenRouter, e.g., 'openrouter/anthropic/claude-3-haiku'. Ensure OPENROUTER_API_KEY is set in .env if using OpenRouter."
)
args = parser.parse_args()

# --- Main Execution Logic ---
async def async_main():
  # Determine model configuration based on command-line arguments
  model_config_to_use = None
  if args.llm_provider == "openrouter":
    if not os.getenv("OPENROUTER_API_KEY"):
      print(f"{COLOR_YELLOW}Warning: --llm_provider is 'openrouter' but OPENROUTER_API_KEY is not set in .env. LiteLLM might fail.{COLOR_RESET}")
    model_config_to_use = LiteLlm(model=args.model_name)
    print_status_message(f"Using OpenRouter model: {args.model_name}", "info")
  else: # Default to Gemini
    model_config_to_use = args.model_name
    print_status_message(f"Using Gemini model: {args.model_name}", "info")

  # Initialize token manager with appropriate context window
  # Gemini 1.5 models have large context windows, adjust as needed
  max_tokens = 1000000 if "1.5" in args.model_name else 120000
  token_manager = TokenManager(model_name=args.model_name, max_context_tokens=max_tokens)
  print_status_message(f"Token manager initialized with {max_tokens:,} max context tokens", "success")
  
  # Initialize error recovery system
  error_recovery = ErrorRecoverySystem()
  print_status_message("Error recovery system initialized", "success")

  session_service = InMemorySessionService()
  # Artifact service might not be needed for this example
  # artifacts_service = InMemoryArtifactService() # Uncomment if you need artifact service

  session = await session_service.create_session(
      state={}, app_name='mcp_filesystem_app', user_id='user_fs'
  )

  # Create an AsyncExitStack to manage the lifecycle of MCPToolset
  async with AsyncExitStack() as exit_stack:
    # Enhanced error handling for MCP server initialization
    async def initialize_mcp_server(server_name: str, init_func):
      """Helper function with enhanced error recovery for MCP server initialization"""
      try:
        server_instance = init_func()
        exit_stack.push_async_callback(lambda: server_instance.close())
        print_status_message(f"{server_name} initialized successfully", "success")
        return server_instance
      except Exception as e:
        context = create_failure_context(e, tool_name=server_name, user_intent="initialize_mcp_server")
        fallback_result = await error_recovery.handle_failure(context)
        print_status_message(f"{server_name} failed to initialize: {fallback_result.user_message}", "warning")
        return None
    
    # Instantiate MCPToolset for the filesystem server with error recovery
    mcp_toolset_instance_filesystem = await initialize_mcp_server(
        "filesystem_server",
        lambda: MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=["-y", "@modelcontextprotocol/server-filesystem",
                      "/Users/milanboonstra/code/googleadkagent/agent_files"],
            )
        )
    )

    # Instantiate MCPToolset for the code executor server with error recovery
    code_storage_dir = os.path.join(os.getcwd(), ".mcp_code_storage")
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
        )
    )

    # Instantiate MCPToolset for the content scraper server with error recovery
    mcp_toolset_instance_content_scraper = await initialize_mcp_server(
        "content_scraper_server",
        lambda: MCPToolset(
            connection_params=StdioServerParameters(
                command='node',
                args=["/Users/milanboonstra/Documents/Cline/MCP/contentscraper-mcp-server/build/index.js"],
            )
        )
    )

    # Instantiate MCPToolset for the fetch server with error recovery
    mcp_toolset_instance_fetch = await initialize_mcp_server(
        "fetch_server",
        lambda: MCPToolset(
            connection_params=StdioServerParameters(
                command='node',
                args=["/Users/milanboonstra/Documents/Cline/MCP/fetch-server/build/index.js"],
            )
        )
    )

    # Instantiate MCPToolset for the Perplexity server
    perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
    if not perplexity_api_key:
        print(f"{COLOR_YELLOW}Warning: PERPLEXITY_API_KEY is not set in .env. Perplexity MCP server might fail.{COLOR_RESET}")
    
    # Instantiate MCPToolset for the Perplexity server with error recovery
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
        )
    )

    # Create separate agents due to ADK limitations:
    # Built-in tools (like google_search) cannot be combined with other tools in the same agent
    
    # Filesystem agent with MCP toolset
    filesystem_tools = [mcp_toolset_instance_filesystem] if mcp_toolset_instance_filesystem else []
    filesystem_agent = LlmAgent(
        model=model_config_to_use,
        name='filesystem_agent',
        instruction='''You are a filesystem specialist focused on efficient file and directory operations.

CAPABILITIES:
- Read, write, create, delete files and directories
- Search for files and content patterns
- File organization and cleanup
- Format conversions and data processing

PRINCIPLES:
- Always use the agent_files directory for user files
- Provide helpful error messages and suggest alternatives
- Proactively organize and structure data logically
- Collaborate with other agents when tasks span domains
- Suggest file naming conventions and organization improvements
- If filesystem tools are unavailable, coordinate with code executor to handle file operations using Python os/shutil libraries
- When operations fail, try alternative approaches (different paths, permissions, etc.)
- Suggest manual alternatives when automated solutions fail

Be efficient and proactive in managing the user's files and data.''',
        tools=filesystem_tools,
    )
    
    # Search agent with Google Search and URL Context for grounding
    # Configure Gemini API tools via GenerationConfig
    search_agent_generation_config = types.GenerationConfig()

    search_agent = LlmAgent(
        model=model_config_to_use,
        name='search_agent',
        instruction='''You are a web search and research specialist focused on finding and analyzing current information.

CAPABILITIES:
- Perform comprehensive Google searches
- Analyze and synthesize information from multiple sources
- Find current trends, news, and developments
- Verify information credibility and accuracy

PRINCIPLES:
- Always include source URLs in your responses
- Cross-reference information from multiple sources when possible
- Focus on the most current and relevant information
- Provide context and explain why sources are credible
- Suggest follow-up searches or related topics when helpful
- If search tools fail, coordinate with fetch_agent or perplexity_agent for alternative research
- When rate limited, suggest waiting periods and alternative information sources
- Provide manual search suggestions when automated tools are unavailable

Be thorough in your research and clear in presenting findings with proper attribution.''',
        tools=[google_search], # Add google_search tool
        generate_content_config=search_agent_generation_config,
    )

    # MCP Code Executor agent
    code_executor_tools = [mcp_toolset_instance_code_executor] if mcp_toolset_instance_code_executor else []
    mcp_code_executor_agent = LlmAgent(
        model=model_config_to_use,
        name='mcp_code_executor_agent',
        instruction='''You are a code execution specialist focused on running Python scripts and solving problems programmatically.

CAPABILITIES:
- Execute any Python code safely in an isolated environment
- Install packages automatically as needed
- Handle data processing, analysis, and automation tasks
- Debug and fix code errors
- Create custom solutions for unique problems

PRINCIPLES:
- Write clean, well-commented code that explains what it does
- Handle errors gracefully with informative messages
- Install required packages at the start of scripts
- Provide clear output and results
- Suggest code improvements and optimizations when relevant
- IMPORTANT: Keep output concise and limit print statements to essential information only
- For large datasets or long outputs, summarize results instead of printing everything
- If code execution tools are unavailable, provide complete code with installation instructions for manual execution
- When package installation fails, suggest alternative libraries or manual installation steps
- For execution errors, automatically debug and provide corrected versions
- Suggest local development environment setup when remote execution isn't available

Be creative in solving problems through code and always aim for robust, efficient solutions.''',
        tools=code_executor_tools,
    )

    # Content Scraper agent
    content_scraper_tools = [mcp_toolset_instance_content_scraper] if mcp_toolset_instance_content_scraper else []
    content_scraper_agent = LlmAgent(
        model=model_config_to_use,
        name='content_scraper_agent',
        instruction='''You are a content scraping specialist focused on gathering information from social media and news sources.

CAPABILITIES:
- Scrape Reddit posts and discussions from specified subreddits
- Collect RSS feed articles from news and blog sources
- Gather Twitter posts from specific accounts
- Process and format scraped content for analysis

PRINCIPLES:
- Default to quality AI/tech sources for general requests
- Format output clearly and include source attribution
- Suggest relevant subreddits, feeds, or accounts based on user interests
- Provide summaries and key insights from scraped content
- Recommend follow-up scraping based on findings
- If content scraping tools are unavailable, coordinate with fetch_agent or code executor to create custom scraping solutions
- When rate limited on social platforms, suggest alternative sources and manual approaches
- Provide direct URLs and manual instructions when automated scraping fails
- Suggest RSS alternatives when social media scraping is blocked

For AI news: use LocalLLaMA, singularity subreddits; top AI Twitter accounts; tech news RSS feeds.
Be proactive in suggesting the best sources for the user's information needs.''',
        tools=content_scraper_tools,
    )

    # Fetch agent
    fetch_tools = [mcp_toolset_instance_fetch] if mcp_toolset_instance_fetch else []
    fetch_agent = LlmAgent(
        model=model_config_to_use,
        name='fetch_agent',
        instruction='''You are a web content fetching specialist focused on retrieving and processing web pages.

CAPABILITIES:
- Fetch content from any URL with proper error handling
- Convert HTML to clean, readable Markdown format
- Search within fetched content using regex patterns
- Handle various content types and encodings

PRINCIPLES:
- Always provide clean, readable output formats
- Handle errors gracefully and suggest alternatives
- Offer content in the most useful format for the user's needs
- Suggest related pages or follow-up fetches when relevant
- Extract key information and provide summaries when helpful
- If fetch tools are unavailable, coordinate with code executor to use requests/urllib for web fetching
- When URLs are blocked or fail, suggest alternative sources or manual browser instructions
- For parsing errors, provide multiple format options (JSON, text, markdown)
- Suggest curl commands or browser developer tools when automated fetching fails

Be efficient in retrieving web content and transforming it into actionable information.''',
        tools=fetch_tools,
    )

    # Perplexity agent
    perplexity_tools = [mcp_toolset_instance_perplexity] if mcp_toolset_instance_perplexity else []
    perplexity_agent = LlmAgent(
        model=model_config_to_use,
        name='perplexity_agent',
        instruction='''You are a Perplexity AI specialist focused on comprehensive research and analysis tasks.

CAPABILITIES:
- Conduct deep research with synthesis from multiple sources
- Find and evaluate APIs, libraries, and technical documentation
- Check code for deprecated features and security issues
- Provide comprehensive analysis with expert-level insights
- Continue conversational research threads

PRINCIPLES:
- Provide thorough, well-researched answers with source attribution
- Focus on actionable insights and practical recommendations
- Compare multiple options and provide pros/cons analysis
- Stay current with latest developments and best practices
- Suggest follow-up research directions and related topics
- If Perplexity tools are unavailable, coordinate with search_agent and fetch_agent for comprehensive research
- When API limits are reached, suggest waiting periods and alternative research approaches
- Provide manual research strategies and source recommendations when automated tools fail
- Suggest academic databases and direct source consultation when AI research tools are down

Be the go-to specialist for deep research and comprehensive analysis that requires expert-level synthesis.''',
        tools=perplexity_tools,
    )
    
    # Import agent_tool for creating the root agent
    from google.adk.tools import agent_tool
    
    # Root agent that can delegate to filesystem, search, and MCP code executor agents
    root_agent = LlmAgent(
        model=model_config_to_use,
        name='assistant',
        instruction='''You are an intelligent daily assistant that can solve complex problems using available tools and custom code.

CORE PRINCIPLES:
1. Take initiative and be proactive in solving problems
2. Break down complex requests into logical steps and execute them
3. Use existing tools when available, write and execute custom code when needed
4. Always find a solution - never give up due to missing tools
5. Coordinate multiple agents for complex workflows
6. Be solution-focused and efficient

AVAILABLE CAPABILITIES:
- Filesystem operations (filesystem_agent) - files, directories, organization
- Web search & content analysis (search_agent) - research, current info
- Code execution (mcp_code_executor_agent) - run any Python code
- Content scraping (content_scraper_agent) - Reddit, RSS, Twitter
- URL fetching (fetch_agent) - web content retrieval
- AI research (perplexity_agent) - comprehensive analysis

AGENTIC BEHAVIOR:
- If no existing tool fits the task, write a custom Python script and execute it
- Proactively suggest improvements and alternatives
- Ask clarifying questions only when truly necessary
- Handle errors gracefully and try alternative approaches
- Remember successful patterns within the conversation
- Always include source URLs when presenting web-sourced information

ERROR RECOVERY PATTERNS:
- When a tool fails, automatically try alternative tools or approaches
- For filesystem operations: use code executor with os/shutil libraries as fallback
- For web content: try fetch_agent → search_agent → custom requests script
- For research: try perplexity_agent → search_agent → custom web scraping
- For code execution: suggest manual execution if service unavailable
- Always explain what went wrong and what alternative approach you're taking
- Learn from failures and suggest preventive measures

APPROACH FOR ANY TASK:
1. Understand the user's goal completely
2. Plan the most efficient solution path
3. Execute using tools or custom code as needed
4. Verify results and present clearly
5. Suggest next steps or related improvements

MULTI-AGENT COORDINATION:
- Data analysis: search → code execution → filesystem
- Content creation: research → analysis → file saving
- Web workflows: fetch → process → save → report

Be the user's reliable daily assistant that gets things done efficiently and proactively.''' ,
        tools=[
            agent_tool.AgentTool(agent=filesystem_agent),
            agent_tool.AgentTool(agent=search_agent),
            agent_tool.AgentTool(agent=mcp_code_executor_agent),
            agent_tool.AgentTool(agent=content_scraper_agent),
            agent_tool.AgentTool(agent=fetch_agent),
            agent_tool.AgentTool(agent=perplexity_agent)
        ],
    )

    runner = Runner(
        app_name='mcp_filesystem_app',
        agent=root_agent,
        # artifact_service=artifacts_service, # Uncomment if you need artifact service
        session_service=session_service,
    )

    print()  # Add blank line for separation between initialized servers and interactive mode
    print_section_header("Google ADK Agent - Interactive Mode", COLOR_GREEN, SYMBOL_THINKING)
    print_status_message("Agent ready! Type 'exit' to quit.", "success")
    print() # Add blank line for separation
    
    conversation_history = []
    stats = ConversationStats()
    
    while True:
      user_input = input("You: ")
      print() # Add blank line for separation after user input
      if user_input.lower() == 'exit':
        stats.print_summary()
        break
      
      # Start timing the request
      stats.start_request()

      # Check if user input is too large and split if necessary
      input_tokens = token_manager.count_tokens(user_input)
      if input_tokens > token_manager.max_context_tokens - token_manager.safety_margin:
        print_status_message(f"Input is very large ({input_tokens:,} tokens). Splitting into chunks...", "warning")
        chunks = token_manager.split_large_message(user_input)
        
        for i, chunk in enumerate(chunks):
          print_status_message(f"Processing chunk {i+1}/{len(chunks)}...", "info")
          content = types.Content(role='user', parts=[types.Part(text=chunk)])
          conversation_history.append(content)
          
          # Check and truncate conversation history if needed
          if token_manager.should_truncate_history(conversation_history):
            print_status_message("Truncating conversation history to manage context window...", "warning")
            conversation_history = token_manager.truncate_conversation_history(conversation_history)
          
          events_async = runner.run_async(
              session_id=session.id, user_id=session.user_id, new_message=content
          )
          
          # Process response for this chunk with error recovery
          response_time = await process_events(events_async, error_recovery, stats)
          print() # Add blank line between chunks
      else:
        content = types.Content(role='user', parts=[types.Part(text=user_input)])
        conversation_history.append(content)
        
        # Check and truncate conversation history if needed
        if token_manager.should_truncate_history(conversation_history):
          print_status_message("Truncating conversation history to manage context window...", "warning")
          conversation_history = token_manager.truncate_conversation_history(conversation_history)

        events_async = runner.run_async(
            session_id=session.id, user_id=session.user_id, new_message=content
        )
        
        # Process response with error recovery
        response_time = await process_events(events_async, error_recovery, stats)
        
        # Show compact stats after each response
        current_tokens = token_manager.count_tokens(str(conversation_history))
        print_session_stats(current_tokens, response_time, stats.message_count)
        print()  # Add blank line before next "You:" prompt

async def process_events(events_async, error_recovery_system: ErrorRecoverySystem, stats: ConversationStats = None):
      response_time = None
      try:
        async for event in events_async:
          has_printed_content = False
          if event.content and event.content.parts:
            for part in event.content.parts:
              if part.text:
                print_section_header("Agent Response", COLOR_GREEN, SYMBOL_THINKING)
                # Print each line of multi-line text with color
                for line in part.text.splitlines():
                  print(f"{COLOR_GREEN}{line}{COLOR_RESET}")
                print() # Add blank line for separation
                has_printed_content = True
              if part.function_call:
                print_section_header(f"Tool Call: {part.function_call.name}", COLOR_YELLOW, SYMBOL_TOOL)
                pretty_print_json_string(part.function_call.args, COLOR_YELLOW)
                print() # Add blank line for separation
                has_printed_content = True
              if part.function_response:
                # Assuming function_response.response might contain a 'name' if it's structured,
                # otherwise, it might be a simple string or dict.
                # For ADK, function_response.name refers to the tool name.
                tool_name_for_response = "UnknownTool" # Default
                if hasattr(part.function_response, 'name') and part.function_response.name:
                    tool_name_for_response = part.function_response.name

                # The actual response content is in part.function_response.response
                # This 'response' field itself can be a dict containing 'content' or other structured data.
                actual_response_data = part.function_response.response
                if isinstance(actual_response_data, dict) and 'content' in actual_response_data:
                    format_tool_response(tool_name_for_response, actual_response_data['content'])
                else:
                    format_tool_response(tool_name_for_response, actual_response_data)
                has_printed_content = True
          
          # Display grounding metadata if available
          if hasattr(event, 'candidates') and event.candidates:
            for candidate in event.candidates:
              if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                grounding = candidate.grounding_metadata
                if hasattr(grounding, 'web_search_queries') and grounding.web_search_queries:
                  print_section_header("Web Search Queries", COLOR_CYAN, SYMBOL_SEARCH)
                  for query in grounding.web_search_queries:
                    print(f"{COLOR_CYAN}  {SYMBOL_SEARCH} {query}{COLOR_RESET}")
                  print() # Add blank line for separation
                  has_printed_content = True
                if hasattr(grounding, 'grounding_chunks') and grounding.grounding_chunks:
                  print_section_header("Grounding Sources", COLOR_CYAN, SYMBOL_INFO)
                  for i, chunk in enumerate(grounding.grounding_chunks):
                      title = "N/A"
                      uri = "N/A"
                      if hasattr(chunk, 'web'):
                          if hasattr(chunk.web, 'title') and chunk.web.title:
                              title = chunk.web.title
                          if hasattr(chunk.web, 'uri') and chunk.web.uri:
                              uri = chunk.web.uri
                      print(f"{COLOR_CYAN}  {SYMBOL_INFO} Source {i+1}: {title[:50]}{'...' if len(title) > 50 else ''}{COLOR_RESET}")
                      print(f"{COLOR_DIM}    {uri}{COLOR_RESET}")
                  print() # Add blank line for separation
                  has_printed_content = True
                
                # Display URL Context Metadata if available
                if hasattr(candidate, 'url_context_metadata') and candidate.url_context_metadata:
                    url_meta_data = candidate.url_context_metadata
                    if hasattr(url_meta_data, 'url_metadata') and url_meta_data.url_metadata:
                        print_section_header("URL Context Metadata", COLOR_BLUE, SYMBOL_INFO)
                        for i, meta_item in enumerate(url_meta_data.url_metadata):
                            retrieved_url = meta_item.retrieved_url if hasattr(meta_item, 'retrieved_url') else "N/A"
                            status = meta_item.url_retrieval_status if hasattr(meta_item, 'url_retrieval_status') else "N/A"
                            # Ensure status is converted to string if it's an enum-like object for printing
                            status_str = str(status) if status != "N/A" else "N/A"
                            status_symbol = SYMBOL_SUCCESS if "success" in status_str.lower() else SYMBOL_WARNING
                            print(f"{COLOR_BLUE}  {status_symbol} URL {i+1}: {retrieved_url[:60]}{'...' if len(retrieved_url) > 60 else ''}{COLOR_RESET}")
                            print(f"{COLOR_DIM}    Status: {status_str}{COLOR_RESET}")
                        print()
                        has_printed_content = True

                # Display rendered search suggestions HTML
                if hasattr(grounding, 'search_entry_point') and \
                   hasattr(grounding.search_entry_point, 'rendered_content') and \
                   grounding.search_entry_point.rendered_content:
                  print(f"{COLOR_CYAN}--- Rendered Search Suggestions (HTML) ---{COLOR_RESET}")
                  # webSearchQueries (printed above) are the text of these suggestions.
                  # This rendered_content is HTML for rich display in a UI.
                  print(f"{COLOR_CYAN}Raw HTML for rich display (first 500 chars):{COLOR_RESET}")
                  html_content = grounding.search_entry_point.rendered_content
                  # Ensure html_content is a string before slicing
                  html_content_str = str(html_content)
                  print(f"{COLOR_MAGENTA}{html_content_str[:500]}{'...' if len(html_content_str) > 500 else ''}{COLOR_RESET}")
                  print() # Add blank line for separation
                  has_printed_content = True
          
          if not has_printed_content: # If no specific part was printed above
            print(f"{COLOR_MAGENTA}--- Event Information ---{COLOR_RESET}")
            # Print event information without attempting JSON formatting
            try:
              event_str = str(event)
              print(f"{COLOR_MAGENTA}{event_str}{COLOR_RESET}")
            except Exception as e:
              print(f"{COLOR_MAGENTA}Error displaying event: {e}{COLOR_RESET}")
            print() # Add blank line for separation
      except Exception as e:
        # Enhanced error handling with recovery suggestions
        context = create_failure_context(e, tool_name="event_processor", user_intent="process_agent_response")
        fallback_result = await error_recovery_system.handle_failure(context)
        
        print_status_message(f"Error processing response: {fallback_result.user_message}", "error")
        if fallback_result.alternative_action:
          print_status_message(f"Suggested action: {fallback_result.alternative_action}", "info")
        print_status_message("Continuing with next request...", "warning")
        print() # Add blank line for separation
      
      # End timing and return response time
      if stats:
        response_time = stats.end_request()
      return response_time


print("Cleanup complete.") # This will be printed after exit_stack.aclose() implicitly

if __name__ == '__main__':
  try:
    asyncio.run(async_main())
  except KeyboardInterrupt:
    print("\nAgent interrupted by user. Goodbye!")
  except Exception as e:
    print(f"An error occurred: {e}")
    print("The agent will restart automatically. Please try your request again.")
