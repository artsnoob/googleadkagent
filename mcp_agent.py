import asyncio
from contextlib import AsyncExitStack
import os
import argparse
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Import from our modular components
from mcp_agent_utils import (
    COLOR_GREEN, COLOR_YELLOW, COLOR_RESET, SYMBOL_THINKING,
    print_section_header, print_status_message, print_session_stats, 
    print_welcome_banner, ConversationStats
)
from token_manager import TokenManager
from error_recovery_system import ErrorRecoverySystem
from mcp_server_init import initialize_all_mcp_servers
from agent_config import create_all_agents
from event_processor import process_events

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

  # Print welcome banner
  print_welcome_banner()
  
  # Create an AsyncExitStack to manage the lifecycle of MCPToolset
  async with AsyncExitStack() as exit_stack:
    # Initialize all MCP servers
    mcp_servers = await initialize_all_mcp_servers(error_recovery, exit_stack)

    # Create all agents using the configuration module
    agents = create_all_agents(model_config_to_use, mcp_servers)
    root_agent = agents['root']

    runner = Runner(
        app_name='mcp_filesystem_app',
        agent=root_agent,
        # artifact_service=artifacts_service, # Uncomment if you need artifact service
        session_service=session_service,
    )

    print()  # Add blank line for separation between initialized servers and interactive mode
    print_section_header("Google ADK Agent - Interactive Mode", COLOR_GREEN, SYMBOL_THINKING, width=50)
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


print("Cleanup complete.") # This will be printed after exit_stack.aclose() implicitly

if __name__ == '__main__':
  try:
    asyncio.run(async_main())
  except KeyboardInterrupt:
    print("\nAgent interrupted by user. Goodbye!")
  except Exception as e:
    print(f"An error occurred: {e}")
    print("The agent will restart automatically. Please try your request again.")
