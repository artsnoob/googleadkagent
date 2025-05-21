import asyncio
from contextlib import AsyncExitStack
import os # Import os
from dotenv import load_dotenv # Import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types
from rich.console import Console # Import Console

# Initialize Console
console = Console()

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
                  "."],
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

    console.print("Running interactive agent. Type 'exit' to quit.")
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
              console.print(f"[green]Agent Response: {part.text}[/green]")
            if part.function_call:
              console.print(f"[dim yellow]Interpreter: The agent is about to ask an external tool ([bold]{part.function_call.name}[/bold]) to perform an action.[/dim yellow]")
              console.print(f"[yellow]Agent is attempting to use the [bold]{part.function_call.name}[/bold] tool with the following parameters:[/yellow]")
              console.print(part.function_call.args)
            if part.function_response:
              console.print(f"[cyan]Tool [bold]{part.function_response.name}[/bold] responded:[/cyan]")
              response_data = part.function_response.response # This is usually a dict

              is_error = isinstance(response_data, dict) and "error" in response_data # A common pattern
              if is_error:
                  console.print(f"[red]Error reported by tool:[/red]")
                  console.print(response_data['error'])
              
              # Print the full response for transparency. Rich will format it.
              console.print(response_data)

              # Add interpretive context after processing the response
              if is_error:
                  console.print(f"[dim red]Interpreter: The tool ([bold]{part.function_response.name}[/bold]) reported an issue, as detailed above.[/dim red]")
              else:
                  console.print(f"[dim cyan]Interpreter: The tool ([bold]{part.function_response.name}[/bold]) has completed its execution and provided a response.[/dim cyan]")
        else:
          console.print(f"Event received: {event}")

  console.print("Cleanup complete.") # This will be printed after exit_stack.aclose() implicitly

if __name__ == '__main__':
  try:
    asyncio.run(async_main())
  except Exception as e:
    console.print(f"[red]An error occurred: {e}[/red]")
