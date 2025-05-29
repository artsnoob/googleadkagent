"""
Terminal input handling with autocomplete support.
Handles low-level terminal operations and command suggestions.
"""
import sys
import termios
import tty
from typing import Optional, Tuple, Dict
from ..utils.mcp_agent_utils import COLOR_DIM, COLOR_CYAN, COLOR_RESET

class InputHandler:
    """Handles terminal input with autocomplete and command suggestions."""
    
    def __init__(self, commands: Dict[str, str]):
        self.commands = commands
        self.suggestions_displayed = False
        self.last_slash_input = ""
    
    def get_char(self) -> str:
        """Get a single character from stdin without echo."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char
    
    def clear_suggestions(self):
        """Clear the command suggestions display."""
        if self.suggestions_displayed:
            # Save cursor position
            print('\033[s', end='')
            # Move down to start of suggestions
            print(f"\033[{1}B", end='')
            # Clear each suggestion line
            for _ in range(len(self.commands) + 1):
                print('\033[2K')  # Clear entire line
            # Restore cursor position
            print('\033[u', end='')
            self.suggestions_displayed = False
            sys.stdout.flush()
    
    def show_command_suggestions(self, current_input: str):
        """Show command suggestions when user types '/'."""
        # Handle empty input (all backspaced)
        if not current_input:
            self.clear_suggestions()
            sys.stdout.write('\r' + ' ' * 80 + '\r' + "You: ")
            sys.stdout.flush()
            self.last_slash_input = ""
            return
        
        if current_input.startswith('/'):
            # Clear current line
            sys.stdout.write('\r' + ' ' * 80 + '\r')
            sys.stdout.write(f"You: {current_input}")
            
            if current_input == '/' and self.last_slash_input != '/':
                # First time showing all commands
                self.clear_suggestions()  # Clear any existing suggestions first
                print(f"\n{COLOR_DIM}Available commands:{COLOR_RESET}")
                for cmd, desc in self.commands.items():
                    print(f"  {COLOR_CYAN}{cmd}{COLOR_RESET} - {COLOR_DIM}{desc}{COLOR_RESET}")
                # Return cursor to input line
                print(f"\033[{len(self.commands)+2}A", end='')  # Move cursor up
                sys.stdout.write(f"\rYou: {current_input}")
                self.suggestions_displayed = True
            elif current_input != '/' and (self.last_slash_input == '/' or self.suggestions_displayed):
                # Moving from '/' to more specific input
                self.clear_suggestions()
                sys.stdout.write('\r' + ' ' * 80 + '\r')
                sys.stdout.write(f"You: {current_input}")
                
                # Show matching commands inline only if not an exact match
                if current_input not in self.commands:
                    matches = [cmd for cmd in self.commands.keys() 
                             if cmd.startswith(current_input) and cmd != current_input]
                    if matches:
                        suggestions = ' | '.join(matches)
                        sys.stdout.write(f" {COLOR_DIM}({suggestions}){COLOR_RESET}")
            elif current_input != '/' and not self.suggestions_displayed:
                # Just show inline suggestions
                if current_input not in self.commands:
                    matches = [cmd for cmd in self.commands.keys() 
                             if cmd.startswith(current_input) and cmd != current_input]
                    if matches:
                        suggestions = ' | '.join(matches)
                        sys.stdout.write(f" {COLOR_DIM}({suggestions}){COLOR_RESET}")
            
            self.last_slash_input = current_input
            sys.stdout.flush()
        else:
            self.last_slash_input = ""
    
    def get_user_input(self) -> str:
        """Get user input with command autocomplete support."""
        user_input = ""
        self.suggestions_displayed = False  # Reset for each new input
        self.last_slash_input = ""  # Reset for each new input
        sys.stdout.write("You: ")
        sys.stdout.flush()
        
        while True:
            char = self.get_char()
            
            if ord(char) == 13:  # Enter key
                # Clear any command suggestions before printing newline
                self.clear_suggestions()
                print()  # New line
                break
            elif ord(char) == 127 or ord(char) == 8:  # Backspace
                if user_input:
                    user_input = user_input[:-1]
                    if user_input.startswith('/') or len(user_input) == 0:
                        self.show_command_suggestions(user_input)
                    else:
                        # Clear suggestions if we backspaced out of a slash command
                        self.clear_suggestions()
                        sys.stdout.write('\r' + ' ' * 80 + '\r' + f"You: {user_input}")
                        sys.stdout.flush()
            elif ord(char) == 3:  # Ctrl+C
                print("\nExiting...")
                sys.exit(0)
            else:
                user_input += char
                if user_input.startswith('/'):
                    self.show_command_suggestions(user_input)
                else:
                    sys.stdout.write(char)
                    sys.stdout.flush()
        
        print()  # Add blank line for separation after user input
        return user_input