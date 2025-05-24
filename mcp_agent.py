import asyncio
from contextlib import AsyncExitStack
import os # Import os
from dotenv import load_dotenv # Import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types # Still needed for types.Content, types.Part
from google.adk.tools import google_search
# Import from our new utils file
from mcp_agent_utils import (
    COLOR_GREEN,
    COLOR_YELLOW,
    COLOR_CYAN,
    COLOR_MAGENTA,
    COLOR_RESET,
    pretty_print_json_string
)
# The apply_genai_content_text_patch() is called within mcp_agent_utils.py upon import.



# Load environment variables from .env file
load_dotenv()



# --- Main Execution Logic ---
async def async_main():
  session_service = InMemorySessionService()
  # Artifact service might not be needed for this example
  # artifacts_service = InMemoryArtifactService() # Uncomment if you need artifact service

  session = await session_service.create_session(
      state={}, app_name='mcp_filesystem_app', user_id='user_fs'
  )

  # Create an AsyncExitStack to manage the lifecycle of MCPToolset
  async with AsyncExitStack() as exit_stack:
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
    exit_stack.push_async_callback(mcp_toolset_instance_filesystem.close)

    # Instantiate MCPToolset for the code executor server
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
    exit_stack.push_async_callback(mcp_toolset_instance_code_executor.close)

    # Create separate agents due to ADK limitations:
    # Built-in tools (like google_search) cannot be combined with other tools in the same agent
    
    # Filesystem agent with MCP toolset
    filesystem_agent = LlmAgent(
        model='gemini-2.5-flash-preview-04-17',
        name='filesystem_agent',
        instruction='You are a specialist in filesystem operations. Help users interact with the local filesystem using available tools. When asked to save a file, use the "agent_files" directory.',
        tools=[mcp_toolset_instance_filesystem],
    )
    
    # Search agent with Google Search
    search_agent = LlmAgent(
        model='gemini-2.5-flash-preview-04-17',
        name='search_agent', 
        instruction='You are a specialist in web search. Help users find current information from the web.',
        tools=[google_search],
    )

    # MCP Code Executor agent
    mcp_code_executor_agent = LlmAgent(
        model='gemini-2.5-flash-preview-04-17',
        name='mcp_code_executor_agent',
        instruction='You are a specialist in code execution using the MCP code executor server. Help users run code via this server.',
        tools=[mcp_toolset_instance_code_executor],
    )
    
    # Import agent_tool for creating the root agent
    from google.adk.tools import agent_tool
    
    # Root agent that can delegate to filesystem, search, and MCP code executor agents
    root_agent = LlmAgent(
        model='gemini-2.5-flash-preview-04-17',
        name='assistant',
        instruction='You are a helpful assistant that can interact with the local filesystem, search the web for current information, and execute code via an MCP server. Delegate filesystem tasks to the filesystem_agent, web search tasks to the search_agent, and MCP-based code execution to mcp_code_executor_agent.',
        tools=[
            agent_tool.AgentTool(agent=filesystem_agent),
            agent_tool.AgentTool(agent=search_agent),
            agent_tool.AgentTool(agent=mcp_code_executor_agent)
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
                print(f"{COLOR_CYAN}📚 Found {len(grounding.grounding_chunks)} source(s){COLOR_RESET}")
                # Optionally, print details of each chunk if needed
                # for i, chunk_info in enumerate(grounding.grounding_chunks):
                # print(f"{COLOR_CYAN} Source {i+1}: {chunk_info}{COLOR_RESET}")
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


  print("Cleanup complete.") # This will be printed after exit_stack.aclose() implicitly

if __name__ == '__main__':
  try:
    asyncio.run(async_main())
  except Exception as e:
    print(f"An error occurred: {e}")
