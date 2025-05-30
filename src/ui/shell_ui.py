"""Clean UI module for AgentSH with minimal terminal design."""
import sys
import time
from typing import Optional
from ..utils.mcp_agent_utils import (
    COLOR_CYAN, COLOR_RESET, COLOR_DIM
)

class ShellUI:
    """Clean, minimal UI components for the agent shell interface."""
    
    # Standard width for all UI elements
    WIDTH = 50
    
    @staticmethod
    def print_banner():
        """Print clean AgentSH banner."""
        # Simple top border
        border = "=" * ShellUI.WIDTH
        print(f"\n{COLOR_CYAN}{border}{COLOR_RESET}")
        
        # Simple centered title
        title = "AgentSH"
        print(f"{COLOR_CYAN}{title:^{ShellUI.WIDTH}}{COLOR_RESET}")
        
        # Simple bottom border
        print(f"{COLOR_CYAN}{border}{COLOR_RESET}")
        print()
    
    @staticmethod
    def print_processing(message: str = "Processing"):
        """Print simple processing indicator."""
        print(f"{COLOR_DIM}{message}...{COLOR_RESET}")
        print()
    
    @staticmethod
    def format_response_header(response_type: str = "Response"):
        """Format simple response header."""
        # No header in minimal design - responses speak for themselves
        pass
    
    @staticmethod
    def format_response(content: str):
        """Format response content with minimal styling."""
        # Just return the content as-is for clean appearance
        return content