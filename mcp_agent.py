import asyncio
from contextlib import AsyncExitStack
import os
import argparse
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import threading
import itertools
import time
import sys
import termios
import tty
import logging
import warnings

# Import from our modular components
from mcp_agent_utils import (
    COLOR_GREEN, COLOR_YELLOW, COLOR_RESET, COLOR_CYAN, COLOR_DIM, COLOR_BOLD,
    SYMBOL_THINKING, SYMBOL_LOADING,
    print_section_header, print_status_message, print_session_stats, 
    print_welcome_banner, ConversationStats
)
from token_manager import TokenManager
from error_recovery_system import ErrorRecoverySystem
from mcp_server_init import initialize_all_mcp_servers
from agent_config import create_all_agents
from event_processor import process_events
from conversation_logger import ConversationLogger

# Suppress various warnings from Google ADK and MCP
logging.getLogger('google.adk.tools.mcp_tool.mcp_session_manager').setLevel(logging.ERROR)
logging.getLogger('mcp').setLevel(logging.ERROR)
logging.getLogger('google.adk').setLevel(logging.ERROR)
# Also suppress warnings from any stdio_client related modules
logging.getLogger('mcp.client').setLevel(logging.ERROR)
logging.getLogger('mcp.client.stdio').setLevel(logging.ERROR)
# Suppress root logger warnings as well
logging.getLogger().setLevel(logging.ERROR)

# Also suppress Python warnings
warnings.filterwarnings("ignore")

# Define blue color for URL context metadata
COLOR_BLUE = "\033[94m"

# The apply_genai_content_text_patch() is called within mcp_agent_utils.py upon import.

# Available slash commands
SLASH_COMMANDS = {
    '/save': 'Save the current conversation to a markdown file',
    '/exit': 'Exit the agent',
    '/help': 'Show available commands',
    '/stats': 'Show conversation statistics',
    '/clear': 'Clear the conversation history (start fresh)',
}

# Loading indicator class
class LoadingIndicator:
    def __init__(self):
        self.active = False
        self.thread = None
        self.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.current_frame = 0
        
    def _animate(self):
        while self.active:
            frame = self.frames[self.current_frame]
            sys.stdout.write(f'\r{frame} ')
            sys.stdout.flush()
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            time.sleep(0.1)
        # Clear the spinner more effectively
        sys.stdout.write('\r' + ' ' * 10 + '\r')  # Clear with more spaces
        sys.stdout.flush()
        
    def start(self):
        if not self.active:
            self.active = True
            self.thread = threading.Thread(target=self._animate)
            self.thread.start()
            
    def stop(self):
        if self.active:
            self.active = False
            if self.thread:
                self.thread.join()
            # Ensure the line is completely cleared after stopping
            sys.stdout.write('\r' + ' ' * 20 + '\r')
            sys.stdout.flush()

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
    print_status_message(f"Using OpenRouter model: {args.model_name}", "success", show_time=False)
  else: # Default to Gemini
    model_config_to_use = args.model_name
    print_status_message(f"Using Gemini model: {args.model_name}", "success", show_time=False)

  # Initialize token manager with appropriate context window
  # Gemini 1.5 models have large context windows, adjust as needed
  max_tokens = 1000000 if "1.5" in args.model_name else 120000
  token_manager = TokenManager(model_name=args.model_name, max_context_tokens=max_tokens)
  print_status_message(f"Token manager initialized with {max_tokens:,} max context tokens", "success", show_time=False)
  
  # Initialize error recovery system
  error_recovery = ErrorRecoverySystem()
  print_status_message("Error recovery system initialized", "success", show_time=False)
  
  # Initialize conversation logger
  conversation_logger = ConversationLogger()
  conversation_logger.set_model_info(args.llm_provider, args.model_name)
  print_status_message("Conversation logger initialized", "success", show_time=False)

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
    print_section_header("Google ADK Agent - Interactive Mode", width=50)
    print_status_message("Agent ready! Type '/' to see available commands.", "success", show_time=False)
    print() # Add blank line for separation
    
    conversation_history = []
    stats = ConversationStats()
    loading_indicator = LoadingIndicator()
    
    # Function to get single character input
    def get_char():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char
    
    # Track if suggestions are currently displayed and previous input
    suggestions_displayed = False
    last_slash_input = ""
    
    def clear_suggestions():
        """Clear the command suggestions display"""
        nonlocal suggestions_displayed
        if suggestions_displayed:
            # Save cursor position
            print('\033[s', end='')
            # Move down to start of suggestions
            print(f"\033[{1}B", end='')
            # Clear each suggestion line
            for _ in range(len(SLASH_COMMANDS)+1):
                print('\033[2K')  # Clear entire line
            # Restore cursor position
            print('\033[u', end='')
            suggestions_displayed = False
            sys.stdout.flush()
    
    def show_command_suggestions(current_input):
        """Show command suggestions when user types '/'"""
        nonlocal suggestions_displayed, last_slash_input
        
        # Handle empty input (all backspaced)
        if not current_input:
            clear_suggestions()
            sys.stdout.write('\r' + ' ' * 80 + '\r' + "You: ")
            sys.stdout.flush()
            last_slash_input = ""
            return
        
        if current_input.startswith('/'):
            # Clear current line
            sys.stdout.write('\r' + ' ' * 80 + '\r')
            sys.stdout.write(f"You: {current_input}")
            
            if current_input == '/' and last_slash_input != '/':
                # First time showing all commands
                clear_suggestions()  # Clear any existing suggestions first
                print(f"\n{COLOR_DIM}Available commands:{COLOR_RESET}")
                for cmd, desc in SLASH_COMMANDS.items():
                    print(f"  {COLOR_CYAN}{cmd}{COLOR_RESET} - {COLOR_DIM}{desc}{COLOR_RESET}")
                # Return cursor to input line
                print(f"\033[{len(SLASH_COMMANDS)+2}A", end='')  # Move cursor up
                sys.stdout.write(f"\rYou: {current_input}")
                suggestions_displayed = True
            elif current_input != '/' and (last_slash_input == '/' or suggestions_displayed):
                # Moving from '/' to more specific input
                clear_suggestions()
                sys.stdout.write('\r' + ' ' * 80 + '\r')
                sys.stdout.write(f"You: {current_input}")
                
                # Show matching commands inline only if not an exact match
                if current_input not in SLASH_COMMANDS:
                    matches = [cmd for cmd in SLASH_COMMANDS.keys() if cmd.startswith(current_input) and cmd != current_input]
                    if matches:
                        suggestions = ' | '.join(matches)
                        sys.stdout.write(f" {COLOR_DIM}({suggestions}){COLOR_RESET}")
            elif current_input != '/' and not suggestions_displayed:
                # Just show inline suggestions
                if current_input not in SLASH_COMMANDS:
                    matches = [cmd for cmd in SLASH_COMMANDS.keys() if cmd.startswith(current_input) and cmd != current_input]
                    if matches:
                        suggestions = ' | '.join(matches)
                        sys.stdout.write(f" {COLOR_DIM}({suggestions}){COLOR_RESET}")
            
            last_slash_input = current_input
            sys.stdout.flush()
        else:
            last_slash_input = ""
    
    while True:
      # Enhanced input handling with command suggestions
      user_input = ""
      suggestions_displayed = False  # Reset for each new input
      last_slash_input = ""  # Reset for each new input
      sys.stdout.write("You: ")
      sys.stdout.flush()
      
      # Custom input handling for slash command autocomplete
      while True:
        char = get_char()
        
        if ord(char) == 13:  # Enter key
          # Clear any command suggestions before printing newline
          clear_suggestions()
          print()  # New line
          break
        elif ord(char) == 127 or ord(char) == 8:  # Backspace
          if user_input:
            user_input = user_input[:-1]
            if user_input.startswith('/') or len(user_input) == 0:
              show_command_suggestions(user_input)
            else:
              # Clear suggestions if we backspaced out of a slash command
              clear_suggestions()
              sys.stdout.write('\r' + ' ' * 80 + '\r' + f"You: {user_input}")
              sys.stdout.flush()
        elif ord(char) == 3:  # Ctrl+C
          print("\nExiting...")
          sys.exit(0)
        else:
          user_input += char
          if user_input.startswith('/'):
            show_command_suggestions(user_input)
          else:
            sys.stdout.write(char)
            sys.stdout.flush()
      
      print() # Add blank line for separation after user input
      
      # Handle slash commands
      if user_input.startswith('/'):
        command = user_input.lower().strip()
        
        if command == '/exit':
          stats.print_summary()
          break
        
        elif command == '/save':
          # Save conversation to markdown
          try:
            filepath = conversation_logger.export_to_markdown()
            print_status_message(f"Conversation saved to: {filepath}", "success")
            print()
            continue
          except Exception as e:
            print_status_message(f"Failed to save conversation: {e}", "error")
            print()
            continue
        
        elif command == '/help':
          print(f"{COLOR_BOLD}Available Commands:{COLOR_RESET}")
          for cmd, desc in SLASH_COMMANDS.items():
            print(f"  {COLOR_CYAN}{cmd}{COLOR_RESET} - {desc}")
          print()
          continue
        
        elif command == '/stats':
          stats.print_summary()
          print()
          continue
        
        elif command == '/clear':
          conversation_history = []
          conversation_logger.clear()
          print_status_message("Conversation history cleared.", "success")
          print()
          continue
        
        else:
          print_status_message(f"Unknown command: {command}. Type /help for available commands.", "warning")
          print()
          continue
      
      # Log user message
      conversation_logger.add_user_message(user_input)
      
      # Start timing the request
      stats.start_request()
      
      # Start loading indicator
      loading_indicator.start()

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
          response_time = await process_events(events_async, error_recovery, stats, conversation_logger, loading_indicator)
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
        response_time = await process_events(events_async, error_recovery, stats, conversation_logger, loading_indicator)
        
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
