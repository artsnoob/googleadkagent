import json
import logging # Import logging
import time
import sys
from datetime import datetime
from google.genai import types # Import types for monkeypatching

# --- Monkeypatch google.genai.types.Content.text to suppress warning ---

_original_content_text_property_getter = None # pylint: disable=invalid-name

def _patched_content_text_getter(self_content_obj):
    """
    A patched version of the `google.genai.types.Content.text` property getter.
    This version omits the logging.warning call that produces the
    "Warning: there are non-text parts in the response..." message.
    It replicates the original logic for concatenating text from text parts.
    """
    # Original logic for concatenating text from google.genai.types.Content.text:
    # A Part is considered text if its `is_text` property is True.
    return "".join(part.text for part in self_content_obj.parts if part.is_text)

def apply_genai_content_text_patch():
    """
    Applies the monkeypatch to `google.genai.types.Content.text`.
    This should be called once, early in the application's lifecycle.
    The 'types' alias from 'from google.genai import types' is used here.
    """
    global _original_content_text_property_getter # pylint: disable=global-statement
    # Ensure the Content class and its text property exist and are as expected.
    if hasattr(types, 'Content') and \
       hasattr(types.Content, 'text') and \
       isinstance(getattr(types.Content, 'text'), property):

        # Save the original getter if we ever wanted to restore or call it.
        _original_content_text_property_getter = types.Content.text.fget

        # Replace the 'text' property on the Content class with a new property
        # whose getter is our patched function.
        types.Content.text = property(_patched_content_text_getter)
        # logging.debug("Successfully monkeypatched google.genai.types.Content.text.")
    else:
        # This case should ideally not be reached if the library version is consistent.
        # logging.warning("Failed to apply monkeypatch: google.generativeai.types.Content.text not found or not a property.")
        pass

# Apply the patch immediately after relevant imports.
apply_genai_content_text_patch()

# Define ANSI color codes
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_MAGENTA = "\033[95m"
COLOR_RESET = "\033[0m"
COLOR_BLUE = "\033[94m"
COLOR_RED = "\033[91m"
COLOR_BOLD = "\033[1m"
COLOR_DIM = "\033[2m"

# Unicode symbols for better visual feedback
SYMBOL_SUCCESS = "✓"
SYMBOL_ERROR = "✗"
SYMBOL_WARNING = "⚠"
SYMBOL_INFO = "ℹ"
SYMBOL_THINKING = "🤔"
SYMBOL_TOOL = "🔧"
SYMBOL_SEARCH = "🔍"
SYMBOL_LOADING = "⏳"
SYMBOL_STATS = "📊"

# Box drawing characters for better formatting
BOX_TOP_LEFT = "┌"
BOX_TOP_RIGHT = "┐"
BOX_BOTTOM_LEFT = "└"
BOX_BOTTOM_RIGHT = "┘"
BOX_HORIZONTAL = "─"
BOX_VERTICAL = "│"
BOX_CROSS = "┼"

import time
from datetime import datetime

# Helper function to pretty-print JSON strings
def pretty_print_json_string(data_string, color):
    try:
        # Attempt to parse as JSON if it looks like a dict or list
        if isinstance(data_string, str) and (data_string.strip().startswith('{') or data_string.strip().startswith('[')):
            parsed_json = json.loads(data_string)
            formatted_json = json.dumps(parsed_json, indent=2)
            # Print each line with color
            for line in formatted_json.splitlines():
                print(f"{color}{line}{COLOR_RESET}")
        elif isinstance(data_string, dict) or isinstance(data_string, list): # Already a dict/list
            formatted_json = json.dumps(data_string, indent=2)
            for line in formatted_json.splitlines():
                print(f"{color}{line}{COLOR_RESET}")
        else: # Not JSON or simple string, print as is
            print(f"{color}{data_string}{COLOR_RESET}")
    except json.JSONDecodeError:
        # Not a valid JSON string, print as is
        print(f"{color}{data_string}{COLOR_RESET}")
    except TypeError: # Handles cases where data_string might not be a string initially
        print(f"{color}{str(data_string)}{COLOR_RESET}")

def print_section_header(title, color=COLOR_CYAN, symbol="", width=60):
    """Print a nicely formatted section header"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    header_text = f"{symbol} {title}" if symbol else title
    # Account for the space before header_text, timestamp, space before timestamp, and both vertical bars
    content_width = len(header_text) + len(timestamp) + 3  # 1 space + header + 1 space + timestamp + 1 space
    actual_width = max(width, content_width + 4)  # Ensure minimum width to fit content
    padding = actual_width - content_width - 2  # -2 for the two vertical bars
    
    print(f"{color}{BOX_TOP_LEFT}{BOX_HORIZONTAL * (actual_width-2)}{BOX_TOP_RIGHT}{COLOR_RESET}")
    print(f"{color}{BOX_VERTICAL} {COLOR_BOLD}{header_text}{COLOR_RESET}{' ' * max(0, padding)}{COLOR_DIM}{timestamp} {color}{BOX_VERTICAL}{COLOR_RESET}")
    print(f"{color}{BOX_BOTTOM_LEFT}{BOX_HORIZONTAL * (actual_width-2)}{BOX_BOTTOM_RIGHT}{COLOR_RESET}")

def print_status_message(message, status_type="info", show_time=True):
    """Print a status message with appropriate symbol and color"""
    symbols = {
        "success": (SYMBOL_SUCCESS, COLOR_GREEN),
        "error": (SYMBOL_ERROR, COLOR_RED),
        "warning": (SYMBOL_WARNING, COLOR_YELLOW),
        "info": (SYMBOL_INFO, COLOR_BLUE),
        "thinking": (SYMBOL_THINKING, COLOR_MAGENTA),
        "tool": (SYMBOL_TOOL, COLOR_CYAN),
        "loading": (SYMBOL_LOADING, COLOR_YELLOW)
    }
    
    symbol, color = symbols.get(status_type, (SYMBOL_INFO, COLOR_BLUE))
    timestamp = f"{COLOR_DIM}[{datetime.now().strftime('%H:%M:%S')}]{COLOR_RESET} " if show_time else ""
    
    print(f"{timestamp}{color}{symbol} {message}{COLOR_RESET}")

def print_loading_animation(message="Processing", duration=1.0):
    """Show a simple loading animation"""
    import sys
    import time
    
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for frame in frames:
            sys.stdout.write(f"\r{COLOR_YELLOW}{frame} {message}...{COLOR_RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
            if time.time() >= end_time:
                break
    
    sys.stdout.write(f"\r{COLOR_GREEN}{SYMBOL_SUCCESS} {message} complete!{COLOR_RESET}\n")
    sys.stdout.flush()

def format_tool_response(tool_name, response_data, show_preview=True, max_preview_lines=5):
    """Format tool responses with better visual hierarchy"""
    print_section_header(f"Tool Response: {tool_name}", COLOR_CYAN, SYMBOL_TOOL)
    
    if show_preview and isinstance(response_data, (dict, list)):
        # Show a preview of large responses
        formatted = json.dumps(response_data, indent=2)
        lines = formatted.splitlines()
        
        if len(lines) > max_preview_lines:
            print(f"{COLOR_DIM}Showing first {max_preview_lines} lines (use --full to see complete response):{COLOR_RESET}")
            for line in lines[:max_preview_lines]:
                print(f"{COLOR_CYAN}{line}{COLOR_RESET}")
            print(f"{COLOR_DIM}... {len(lines) - max_preview_lines} more lines{COLOR_RESET}")
        else:
            pretty_print_json_string(response_data, COLOR_CYAN)
    else:
        pretty_print_json_string(response_data, COLOR_CYAN)
    
    print()  # Add spacing

def print_session_stats(token_usage=None, response_time=None, conversation_length=None):
    """Display session statistics in a compact format"""
    stats = []
    
    if token_usage:
        stats.append(f"Tokens: {token_usage:,}")
    if response_time:
        stats.append(f"Response: {response_time:.1f}s")
    if conversation_length:
        stats.append(f"Messages: {conversation_length}")
    
    if stats:
        stats_text = " | ".join(stats)
        print(f"{COLOR_DIM}📊 {stats_text}{COLOR_RESET}")

class ConversationStats:
    """Track conversation statistics"""
    def __init__(self):
        self.start_time = time.time()
        self.message_count = 0
        self.total_tokens = 0
        self.response_times = []
        self.last_request_time = None
    
    def start_request(self):
        """Mark the start of a new request"""
        self.last_request_time = time.time()
        self.message_count += 1
    
    def end_request(self, tokens_used=0):
        """Mark the end of a request and calculate response time"""
        if self.last_request_time:
            response_time = time.time() - self.last_request_time
            self.response_times.append(response_time)
            self.total_tokens += tokens_used
            return response_time
        return None
    
    def get_avg_response_time(self):
        """Calculate average response time"""
        return sum(self.response_times) / len(self.response_times) if self.response_times else 0
    
    def get_session_duration(self):
        """Get total session duration"""
        return time.time() - self.start_time
    
    def print_summary(self):
        """Print a session summary"""
        duration = self.get_session_duration()
        avg_response = self.get_avg_response_time()
        
        print_section_header("Session Summary", COLOR_MAGENTA, "📊")
        print(f"{COLOR_CYAN}  Duration: {duration/60:.1f} minutes{COLOR_RESET}")
        print(f"{COLOR_CYAN}  Messages: {self.message_count}{COLOR_RESET}")
        print(f"{COLOR_CYAN}  Total tokens: {self.total_tokens:,}{COLOR_RESET}")
        print(f"{COLOR_CYAN}  Avg response time: {avg_response:.1f}s{COLOR_RESET}")
        if self.response_times:
            print(f"{COLOR_CYAN}  Fastest response: {min(self.response_times):.1f}s{COLOR_RESET}")
            print(f"{COLOR_CYAN}  Slowest response: {max(self.response_times):.1f}s{COLOR_RESET}")
        print()
