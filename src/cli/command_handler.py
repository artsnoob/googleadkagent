"""
Slash command handling for the Google ADK Agent.
Separates command processing logic from the main agent loop.
"""
from typing import Dict, Callable, Optional, Tuple
from ..utils.mcp_agent_utils import (
    COLOR_BOLD, COLOR_CYAN, COLOR_RESET,
    print_status_message
)
from ..processors.conversation_logger import ConversationLogger

class CommandHandler:
    """Handles slash commands with a registry-based approach."""
    
    def __init__(self, conversation_logger: ConversationLogger):
        self.conversation_logger = conversation_logger
        self.commands: Dict[str, Dict[str, any]] = {
            '/save': {
                'description': 'Save the current conversation to a markdown file',
                'handler': self._handle_save
            },
            '/exit': {
                'description': 'Exit the agent',
                'handler': self._handle_exit
            },
            '/help': {
                'description': 'Show available commands',
                'handler': self._handle_help
            },
            '/stats': {
                'description': 'Show conversation statistics',
                'handler': self._handle_stats
            },
            '/clear': {
                'description': 'Clear the conversation history (start fresh)',
                'handler': self._handle_clear
            },
        }
    
    def get_commands(self) -> Dict[str, str]:
        """Get command descriptions for display."""
        return {cmd: info['description'] for cmd, info in self.commands.items()}
    
    def is_command(self, user_input: str) -> bool:
        """Check if input is a slash command."""
        return user_input.startswith('/')
    
    def get_matching_commands(self, partial: str) -> list:
        """Get commands that match a partial input."""
        if not partial.startswith('/'):
            return []
        return [cmd for cmd in self.commands.keys() 
                if cmd.startswith(partial) and cmd != partial]
    
    async def handle_command(self, command: str, context: dict) -> Tuple[bool, Optional[str]]:
        """
        Handle a slash command.
        
        Args:
            command: The command string
            context: Dictionary containing conversation_history, stats, etc.
            
        Returns:
            Tuple of (should_continue, optional_message)
            should_continue: False if we should exit the main loop
        """
        command = command.lower().strip()
        
        if command not in self.commands:
            print_status_message(
                f"Unknown command: {command}. Type /help for available commands.", 
                "warning"
            )
            print()
            return True, None
        
        handler = self.commands[command]['handler']
        return await handler(context)
    
    async def _handle_save(self, context: dict) -> Tuple[bool, Optional[str]]:
        """Handle /save command."""
        try:
            filepath = self.conversation_logger.export_to_markdown()
            print_status_message(f"Conversation saved to: {filepath}", "success")
            print()
            return True, None
        except Exception as e:
            print_status_message(f"Failed to save conversation: {e}", "error")
            print()
            return True, None
    
    async def _handle_exit(self, context: dict) -> Tuple[bool, Optional[str]]:
        """Handle /exit command."""
        if 'stats' in context:
            context['stats'].print_summary()
        return False, "exit"
    
    async def _handle_help(self, context: dict) -> Tuple[bool, Optional[str]]:
        """Handle /help command."""
        print(f"{COLOR_BOLD}Available Commands:{COLOR_RESET}")
        for cmd, desc in self.get_commands().items():
            print(f"  {COLOR_CYAN}{cmd}{COLOR_RESET} - {desc}")
        print()
        return True, None
    
    async def _handle_stats(self, context: dict) -> Tuple[bool, Optional[str]]:
        """Handle /stats command."""
        if 'stats' in context:
            context['stats'].print_summary()
        print()
        return True, None
    
    async def _handle_clear(self, context: dict) -> Tuple[bool, Optional[str]]:
        """Handle /clear command."""
        if 'conversation_history' in context:
            context['conversation_history'].clear()
        self.conversation_logger.clear()
        print_status_message("Conversation history cleared.", "success")
        print()
        return True, None
    
    def register_command(self, command: str, description: str, handler: Callable):
        """Register a new command dynamically."""
        self.commands[command] = {
            'description': description,
            'handler': handler
        }