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
    pretty_print_json_string,
)

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
    print(f"{COLOR_MAGENTA}Using OpenRouter model: {args.model_name}{COLOR_RESET}")
  else: # Default to Gemini
    model_config_to_use = args.model_name
    print(f"{COLOR_MAGENTA}Using Gemini model: {args.model_name}{COLOR_RESET}")

  session_service = InMemorySessionService()
  # Artifact service might not be needed for this example
  # artifacts_service = InMemoryArtifactService() # Uncomment if you need artifact service

  session = await session_service.create_session(
      state={}, app_name='mcp_filesystem_app', user_id='user_fs'
  )

  # Create an AsyncExitStack to manage the lifecycle of MCPToolset
  async with AsyncExitStack() as exit_stack:
    try:
      # Instantiate MCPToolset for the filesystem server
      mcp_toolset_instance_filesystem = MCPToolset(
          connection_params=StdioServerParameters(
              command='npx', # Command to run the server
              args=["-y",    # Arguments for the command
                    "@modelcontextprotocol/server-filesystem",
                    # IMPORTANT: This path specifies the folder the filesystem MCP server will operate on.
                    # We are using the agent_files directory.
                    "/Users/milanboonstra/code/googleadkagent/agent_files"],
          )
      )
      # Register the close method of mcp_toolset_instance_filesystem to be called on exit
      exit_stack.push_async_callback(lambda: mcp_toolset_instance_filesystem.close())
    except Exception as e:
      print(f"{COLOR_YELLOW}Warning: Failed to initialize filesystem MCP server: {e}{COLOR_RESET}")
      mcp_toolset_instance_filesystem = None

    # Instantiate MCPToolset for the code executor server
    try:
      code_storage_dir = os.path.join(os.getcwd(), ".mcp_code_storage")
      mcp_toolset_instance_code_executor = MCPToolset(
          connection_params=StdioServerParameters(
              command='env', # Use 'env' to set environment variables
              args=[
                  f"CODE_STORAGE_DIR={code_storage_dir}",
                  "ENV_TYPE=venv",
                  f"VENV_PATH={os.path.join(os.getcwd(), '.mcp_venv')}",
                  "node",
                  "/Users/milanboonstra/code/openaisdkmcp_server_copy/mcp_code_executor/build/index.js"
              ], # Arguments for the command, including env vars and node execution
              env={} # Environment variables are now set in args
          )
      )
      # Register the close method of mcp_toolset_instance_code_executor to be called on exit
      exit_stack.push_async_callback(lambda: mcp_toolset_instance_code_executor.close())
    except Exception as e:
      print(f"{COLOR_YELLOW}Warning: Failed to initialize code executor MCP server: {e}{COLOR_RESET}")
      mcp_toolset_instance_code_executor = None

    # Instantiate MCPToolset for the content scraper server
    try:
      mcp_toolset_instance_content_scraper = MCPToolset(
          connection_params=StdioServerParameters(
              command='node', # Command to run the server
              args=[          # Arguments for the command
                  "/Users/milanboonstra/Documents/Cline/MCP/contentscraper-mcp-server/build/index.js"
              ],
          )
      )
      # Register the close method of mcp_toolset_instance_content_scraper to be called on exit
      exit_stack.push_async_callback(lambda: mcp_toolset_instance_content_scraper.close())
    except Exception as e:
      print(f"{COLOR_YELLOW}Warning: Failed to initialize content scraper MCP server: {e}{COLOR_RESET}")
      mcp_toolset_instance_content_scraper = None

    # Instantiate MCPToolset for the fetch server
    try:
      mcp_toolset_instance_fetch = MCPToolset(
          connection_params=StdioServerParameters(
              command='node', # Command to run the server
              args=[          # Arguments for the command
                  "/Users/milanboonstra/Documents/Cline/MCP/fetch-server/build/index.js"
              ],
          )
      )
      # Register the close method of mcp_toolset_instance_fetch to be called on exit
      exit_stack.push_async_callback(lambda: mcp_toolset_instance_fetch.close())
    except Exception as e:
      print(f"{COLOR_YELLOW}Warning: Failed to initialize fetch MCP server: {e}{COLOR_RESET}")
      mcp_toolset_instance_fetch = None

    # Instantiate MCPToolset for the Perplexity server
    perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
    if not perplexity_api_key:
        print(f"{COLOR_YELLOW}Warning: PERPLEXITY_API_KEY is not set in .env. Perplexity MCP server might fail.{COLOR_RESET}")
    
    try:
      mcp_toolset_instance_perplexity = MCPToolset(
          connection_params=StdioServerParameters(
              command='env', # Use 'env' to set environment variables
              args=[
                  f"PERPLEXITY_API_KEY={perplexity_api_key}", # Pass the API key as an environment variable
                  "node",         # Command to run the server
                  "/Users/milanboonstra/Documents/Cline/MCP/perplexity-mcp/build/index.js"
              ],
              env={} # Environment variables are now set in args
          )
      )
      # Register the close method of mcp_toolset_instance_perplexity to be called on exit
      exit_stack.push_async_callback(lambda: mcp_toolset_instance_perplexity.close())
    except Exception as e:
      print(f"{COLOR_YELLOW}Warning: Failed to initialize Perplexity MCP server: {e}{COLOR_RESET}")
      mcp_toolset_instance_perplexity = None

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
- If filesystem tools are unavailable, inform the user that file operations cannot be performed

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
- If code execution tools are unavailable, inform the user that code execution cannot be performed

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
- If content scraping tools are unavailable, inform the user that scraping cannot be performed

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
- If fetch tools are unavailable, inform the user that web content fetching cannot be performed

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
- If Perplexity tools are unavailable, inform the user that advanced research cannot be performed

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

    print("Running interactive agent. Type 'exit' to quit.")
    print() # Add blank line for separation
    while True:
      user_input = input("You: ")
      print() # Add blank line for separation after user input
      if user_input.lower() == 'exit':
        break

      content = types.Content(role='user', parts=[types.Part(text=user_input)])

      events_async = runner.run_async(
          session_id=session.id, user_id=session.user_id, new_message=content
      )

      try:
        async for event in events_async:
          has_printed_content = False
          if event.content and event.content.parts:
            for part in event.content.parts:
              if part.text:
                print(f"{COLOR_GREEN}--- Agent Response ---{COLOR_RESET}")
                # Print each line of multi-line text with color
                for line in part.text.splitlines():
                  print(f"{COLOR_GREEN}{line}{COLOR_RESET}")
                print() # Add blank line for separation
                has_printed_content = True
              if part.function_call:
                print(f"{COLOR_YELLOW}--- Tool Call: {part.function_call.name} ---{COLOR_RESET}")
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

                print(f"{COLOR_CYAN}--- Tool Response ({tool_name_for_response}) ---{COLOR_RESET}")
                # The actual response content is in part.function_response.response
                # This 'response' field itself can be a dict containing 'content' or other structured data.
                actual_response_data = part.function_response.response
                if isinstance(actual_response_data, dict) and 'content' in actual_response_data:
                    pretty_print_json_string(actual_response_data['content'], COLOR_CYAN)
                else:
                    pretty_print_json_string(actual_response_data, COLOR_CYAN)
                print() # Add blank line for separation
                has_printed_content = True
          
          # Display grounding metadata if available
          if hasattr(event, 'candidates') and event.candidates:
            for candidate in event.candidates:
              if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                grounding = candidate.grounding_metadata
                if hasattr(grounding, 'web_search_queries') and grounding.web_search_queries:
                  print(f"{COLOR_CYAN}--- Web Search Queries ---{COLOR_RESET}")
                  print(f"{COLOR_CYAN}🔍 {', '.join(grounding.web_search_queries)}{COLOR_RESET}")
                  print() # Add blank line for separation
                  has_printed_content = True
                if hasattr(grounding, 'grounding_chunks') and grounding.grounding_chunks:
                  print(f"{COLOR_CYAN}--- Grounding Sources ---{COLOR_RESET}")
                  for i, chunk in enumerate(grounding.grounding_chunks):
                      title = "N/A"
                      uri = "N/A"
                      if hasattr(chunk, 'web'):
                          if hasattr(chunk.web, 'title') and chunk.web.title:
                              title = chunk.web.title
                          if hasattr(chunk.web, 'uri') and chunk.web.uri:
                              uri = chunk.web.uri
                      print(f"{COLOR_CYAN}  Source {i+1}: {title} ({uri}){COLOR_RESET}")
                  print() # Add blank line for separation
                  has_printed_content = True
                
                # Display URL Context Metadata if available
                if hasattr(candidate, 'url_context_metadata') and candidate.url_context_metadata:
                    url_meta_data = candidate.url_context_metadata
                    if hasattr(url_meta_data, 'url_metadata') and url_meta_data.url_metadata:
                        print(f"{COLOR_BLUE}--- URL Context Metadata ---{COLOR_RESET}")
                        for i, meta_item in enumerate(url_meta_data.url_metadata):
                            retrieved_url = meta_item.retrieved_url if hasattr(meta_item, 'retrieved_url') else "N/A"
                            status = meta_item.url_retrieval_status if hasattr(meta_item, 'url_retrieval_status') else "N/A"
                            # Ensure status is converted to string if it's an enum-like object for printing
                            status_str = str(status) if status != "N/A" else "N/A"
                            print(f"{COLOR_BLUE}  URL {i+1}: {retrieved_url} (Status: {status_str}){COLOR_RESET}")
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
            # Attempt to pretty print the event if it's complex, otherwise just str(event)
            try:
              event_str = str(event)
              if '{' in event_str or '[' in event_str: # Basic check for complex structure
                   pretty_print_json_string(event_str, COLOR_MAGENTA)
              else:
                   print(f"{COLOR_MAGENTA}{event_str}{COLOR_RESET}")
            except Exception:
                print(f"{COLOR_MAGENTA}{str(event)}{COLOR_RESET}")
            print() # Add blank line for separation
      
      except Exception as e:
        print(f"{COLOR_YELLOW}Warning: Error processing response: {e}{COLOR_RESET}")
        print(f"{COLOR_YELLOW}Continuing with next request...{COLOR_RESET}")
        print() # Add blank line for separation


  print("Cleanup complete.") # This will be printed after exit_stack.aclose() implicitly

if __name__ == '__main__':
  try:
    asyncio.run(async_main())
  except KeyboardInterrupt:
    print("\nAgent interrupted by user. Goodbye!")
  except Exception as e:
    print(f"An error occurred: {e}")
    print("The agent will restart automatically. Please try your request again.")
