import asyncio
from contextlib import AsyncExitStack
import os # Import os
from dotenv import load_dotenv # Import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types

# Define ANSI color codes
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"

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
    # Instantiate MCPToolset directly
    mcp_toolset_instance = MCPToolset(
        connection_params=StdioServerParameters(
            command='npx', # Command to run the server
            args=["-y",    # Arguments for the command
                  "@modelcontextprotocol/server-filesystem",
                  # IMPORTANT: This path specifies the folder the filesystem MCP server will operate on.
                  # We are using the current working directory for simplicity.
                  "/Users/milanboonstra/code/googleadkagent"],
        )
    )
    # Register the close method of mcp_toolset_instance to be called on exit
    # Use push_async_callback for coroutines
    exit_stack.push_async_callback(mcp_toolset_instance.close)

    # The tools are now available via mcp_toolset_instance.get_tools()
    # However, the LlmAgent expects a list of tools directly.
    # MCPToolset itself acts as a toolset that the LlmAgent can use.
    root_agent = LlmAgent(
        model='gemini-2.5-flash-preview-04-17', # Adjust model name if needed based on availability
        name='filesystem_assistant',
        instruction='Help user interact with the local filesystem using available tools.',
        tools=[mcp_toolset_instance], # Provide the MCPToolset instance directly
    )

    runner = Runner(
        app_name='mcp_filesystem_app',
        agent=root_agent,
        # artifact_service=artifacts_service, # Uncomment if you need artifact service
        session_service=session_service,
    )

    print("Running interactive agent. Type 'exit' to quit.")
    while True:
      user_input = input("You: ")
      if user_input.lower() == 'exit':
        break

      content = types.Content(role='user', parts=[types.Part(text=user_input)])

      events_async = runner.run_async(
          session_id=session.id, user_id=session.user_id, new_message=content
      )

      async for event in events_async:
        if event.content and event.content.parts:
          for part in event.content.parts:
            if part.text:
              print(f"{COLOR_GREEN}Agent Response: {part.text}{COLOR_RESET}")
            if part.function_call:
              print(f"{COLOR_YELLOW}Tool Call: {part.function_call.name}({part.function_call.args}){COLOR_RESET}")
            if part.function_response:
              print(f"{COLOR_CYAN}Tool Response: {part.function_response.response}{COLOR_RESET}")
        else:
          print(f"Event received: {event}")

  print("Cleanup complete.") # This will be printed after exit_stack.aclose() implicitly

if __name__ == '__main__':
  try:
    asyncio.run(async_main())
  except Exception as e:
    print(f"An error occurred: {e}")
