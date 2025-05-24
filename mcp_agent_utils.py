import json
import logging # Import logging
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
