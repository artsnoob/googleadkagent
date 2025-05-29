"""
Refactored MCP Agent with better separation of concerns.
This is the core orchestrator that coordinates all components.
"""
import asyncio
from contextlib import AsyncExitStack
import argparse
from typing import Optional, Dict, Any
import logging
import warnings

from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Import configurations
from ..config.settings import get_config, ModelConfig

# Import UI components
from ..ui.loading_indicator import LoadingIndicator
from ..cli.command_handler import CommandHandler
from ..cli.input_handler import InputHandler

# Import core components
from .enhanced_token_manager import SmartTokenManager
from .enhanced_error_recovery import EnhancedErrorRecoverySystem
from ..mcp.mcp_server_init import initialize_all_mcp_servers
from ..agents.enhanced_agent_config import create_all_agents

# Import processors
from ..processors.enhanced_event_processor import process_events
from ..processors.conversation_logger import ConversationLogger
from ..processors.intelligent_conversation_manager import IntelligentConversationManager

# Import utilities
from ..utils.mcp_agent_utils import (
    print_section_header, print_status_message, print_session_stats,
    print_welcome_banner, ConversationStats
)

# Configure logging
def configure_logging():
    """Configure logging to suppress unwanted messages."""
    loggers_to_suppress = [
        'google.adk.tools.mcp_tool.mcp_session_manager',
        'mcp', 'google.adk', 'mcp.client', 'mcp.client.stdio'
    ]
    for logger_name in loggers_to_suppress:
        logging.getLogger(logger_name).setLevel(logging.ERROR)
    
    logging.getLogger().setLevel(logging.ERROR)
    warnings.filterwarnings("ignore")


class MCPAgent:
    """Main orchestrator for the MCP Agent."""
    
    def __init__(self, config: Optional[Any] = None):
        """Initialize the MCP Agent with configuration."""
        self.config = config or get_config()
        self.token_manager: Optional[SmartTokenManager] = None
        self.error_recovery: Optional[EnhancedErrorRecoverySystem] = None
        self.conversation_logger: Optional[ConversationLogger] = None
        self.conversation_manager: Optional[IntelligentConversationManager] = None
        self.command_handler: Optional[CommandHandler] = None
        self.input_handler: Optional[InputHandler] = None
        self.stats = ConversationStats()
        self.conversation_history = []
        
    def _initialize_components(self, model_config: ModelConfig):
        """Initialize all agent components."""
        # Enhanced token manager
        self.token_manager = SmartTokenManager(
            model_name=model_config.name,
            max_context_tokens=model_config.max_context_tokens
        )
        print_status_message(
            f"Smart token manager initialized with {model_config.max_context_tokens:,} max context tokens",
            "success", show_time=False
        )
        
        # Enhanced error recovery
        if self.config.enable_error_recovery:
            self.error_recovery = EnhancedErrorRecoverySystem()
            print_status_message("Enhanced error recovery system initialized", "success", show_time=False)
        
        # Conversation logger
        if self.config.enable_conversation_logging:
            self.conversation_logger = ConversationLogger()
            self.conversation_logger.set_model_info(model_config.provider, model_config.name)
            print_status_message("Conversation logger initialized", "success", show_time=False)
            
            # Intelligent conversation manager
            self.conversation_manager = IntelligentConversationManager(self.conversation_logger)
            print_status_message("Intelligent conversation manager initialized", "success", show_time=False)
        
        # Command handler
        self.command_handler = CommandHandler(self.conversation_logger)
        
        # Input handler
        self.input_handler = InputHandler(self.command_handler.get_commands())
    
    def _get_model_config(self, args: argparse.Namespace) -> tuple:
        """Determine model configuration from arguments."""
        model_config = ModelConfig(
            provider=args.llm_provider,
            name=args.model_name
        )
        
        if model_config.provider == "openrouter":
            llm_config = LiteLlm(model=model_config.name)
            print_status_message(f"Using OpenRouter model: {model_config.name}", "success", show_time=False)
        else:
            llm_config = model_config.name
            print_status_message(f"Using Gemini model: {model_config.name}", "success", show_time=False)
        
        return llm_config, model_config
    
    async def _handle_user_input(self, user_input: str, runner: Runner, session: Any) -> bool:
        """
        Process user input and return whether to continue the conversation.
        
        Returns:
            bool: True to continue, False to exit
        """
        # Handle slash commands
        if self.command_handler.is_command(user_input):
            context = {
                'conversation_history': self.conversation_history,
                'stats': self.stats
            }
            should_continue, _ = await self.command_handler.handle_command(user_input, context)
            return should_continue
        
        # Log user message
        if self.conversation_logger:
            self.conversation_logger.add_user_message(user_input)
        
        # Start timing the request
        self.stats.start_request()
        
        # Process the message
        loading_indicator = LoadingIndicator() if self.config.show_loading_indicator else None
        if loading_indicator:
            loading_indicator.start()
        
        try:
            # Check token limits and handle large inputs
            input_tokens = self.token_manager.count_tokens(user_input)
            if input_tokens > self.token_manager.max_context_tokens - self.token_manager.safety_margin:
                await self._handle_large_input(user_input, runner, session, loading_indicator)
            else:
                await self._handle_normal_input(user_input, runner, session, loading_indicator)
            
            # Show stats if enabled
            if self.config.show_token_stats:
                current_tokens = self.token_manager.count_tokens(str(self.conversation_history))
                response_time = self.stats.get_last_response_time()
                print_session_stats(current_tokens, response_time, self.stats.message_count)
            
            print()  # Blank line before next prompt
            
        finally:
            if loading_indicator:
                loading_indicator.stop()
        
        return True
    
    async def _handle_large_input(self, user_input: str, runner: Runner, 
                                  session: Any, loading_indicator: Optional[LoadingIndicator]):
        """Handle inputs that exceed token limits."""
        input_tokens = self.token_manager.count_tokens(user_input)
        print_status_message(
            f"Input is very large ({input_tokens:,} tokens). Splitting into chunks...",
            "warning"
        )
        
        chunks = self.token_manager.split_large_message(user_input)
        for i, chunk in enumerate(chunks):
            print_status_message(f"Processing chunk {i+1}/{len(chunks)}...", "info")
            await self._process_chunk(chunk, runner, session, loading_indicator)
            print()  # Blank line between chunks
    
    async def _handle_normal_input(self, user_input: str, runner: Runner,
                                   session: Any, loading_indicator: Optional[LoadingIndicator]):
        """Handle normal-sized inputs."""
        await self._process_chunk(user_input, runner, session, loading_indicator)
    
    async def _process_chunk(self, text: str, runner: Runner,
                             session: Any, loading_indicator: Optional[LoadingIndicator]):
        """Process a single chunk of text."""
        content = types.Content(role='user', parts=[types.Part(text=text)])
        self.conversation_history.append(content)
        
        # Check and truncate history if needed
        if self.token_manager.should_truncate_history(self.conversation_history):
            print_status_message(
                "Truncating conversation history to manage context window...",
                "warning"
            )
            self.conversation_history = self.token_manager.truncate_conversation_history(
                self.conversation_history
            )
        
        # Run the agent
        events_async = runner.run_async(
            session_id=session.id,
            user_id=session.user_id,
            new_message=content
        )
        
        # Process response
        await process_events(
            events_async,
            self.error_recovery,
            self.stats,
            self.conversation_logger,
            loading_indicator
        )
    
    async def run(self, args: argparse.Namespace):
        """Main entry point for running the agent."""
        # Configure logging
        configure_logging()
        
        # Get model configuration
        llm_config, model_config = self._get_model_config(args)
        
        # Initialize components
        self._initialize_components(model_config)
        
        # Validate configuration
        warnings = self.config.validate()
        for warning in warnings:
            print_status_message(warning, "warning", show_time=False)
        
        # Initialize session
        session_service = InMemorySessionService()
        session = await session_service.create_session(
            state={}, app_name='mcp_filesystem_app', user_id='user_fs'
        )
        
        # Print welcome banner
        print_welcome_banner()
        
        # Initialize MCP servers and agents
        async with AsyncExitStack() as exit_stack:
            # Initialize MCP servers
            mcp_servers = await initialize_all_mcp_servers(self.error_recovery, exit_stack)
            
            # Create agents
            agents = create_all_agents(llm_config, mcp_servers)
            root_agent = agents['root']
            
            # Create runner
            runner = Runner(
                app_name='mcp_filesystem_app',
                agent=root_agent,
                session_service=session_service,
            )
            
            # Start interactive mode
            print()
            print_section_header("Google ADK Agent - Interactive Mode", width=50)
            print_status_message(
                "Agent ready! Type '/' to see available commands.",
                "success", show_time=False
            )
            print()
            
            # Main conversation loop
            while True:
                user_input = self.input_handler.get_user_input()
                
                should_continue = await self._handle_user_input(user_input, runner, session)
                if not should_continue:
                    break
        
        print("Cleanup complete.")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Run ADK Agent with selectable LLM provider and model."
    )
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
        help="The model name to use. For Gemini, e.g., 'gemini-2.5-flash-preview-05-20'. "
             "For OpenRouter, e.g., 'openrouter/anthropic/claude-3-haiku'."
    )
    return parser


async def main():
    """Main entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    agent = MCPAgent()
    await agent.run(args)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAgent interrupted by user. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("The agent will restart automatically. Please try your request again.")