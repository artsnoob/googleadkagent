"""
Loading indicator for showing progress during async operations.
"""
import sys
import threading
import time
from typing import List

class LoadingIndicator:
    """Animated loading indicator for terminal UI."""
    
    def __init__(self, frames: List[str] = None, interval: float = 0.1):
        """
        Initialize loading indicator.
        
        Args:
            frames: List of animation frames. Defaults to spinner frames.
            interval: Time between frames in seconds.
        """
        self.frames = frames or ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.interval = interval
        self.active = False
        self.thread = None
        self.current_frame = 0
        
    def _animate(self):
        """Animation loop running in separate thread."""
        while self.active:
            frame = self.frames[self.current_frame]
            sys.stdout.write(f'\r{frame} ')
            sys.stdout.flush()
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            time.sleep(self.interval)
        # Clear the spinner more effectively
        sys.stdout.write('\r' + ' ' * 10 + '\r')  # Clear with more spaces
        sys.stdout.flush()
        
    def start(self):
        """Start the loading indicator animation."""
        if not self.active:
            self.active = True
            self.thread = threading.Thread(target=self._animate)
            self.thread.daemon = True  # Make thread daemon for clean exit
            self.thread.start()
            
    def stop(self):
        """Stop the loading indicator animation."""
        if self.active:
            self.active = False
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=1.0)  # Add timeout to prevent hanging
            # Ensure the line is completely cleared after stopping
            sys.stdout.write('\r' + ' ' * 20 + '\r')
            sys.stdout.flush()
    
    def __enter__(self):
        """Context manager support."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.stop()


class ProgressIndicator(LoadingIndicator):
    """Enhanced loading indicator with progress messages."""
    
    def __init__(self, message: str = "Processing", **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.progress_text = ""
    
    def _animate(self):
        """Animation loop with progress message."""
        while self.active:
            frame = self.frames[self.current_frame]
            display_text = f'\r{frame} {self.message}'
            if self.progress_text:
                display_text += f': {self.progress_text}'
            display_text += ' ' * 20  # Padding to clear previous text
            sys.stdout.write(display_text)
            sys.stdout.flush()
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            time.sleep(self.interval)
        # Clear the line
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.flush()
    
    def update_progress(self, text: str):
        """Update the progress text shown next to the spinner."""
        self.progress_text = text