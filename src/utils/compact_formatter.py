"""
Compact response formatter for cleaner, more readable agent output.
"""

import re
from typing import List, Tuple
from .mcp_agent_utils import COLOR_GREEN, COLOR_BLUE, COLOR_CYAN, COLOR_RESET, COLOR_YELLOW


class CompactFormatter:
    """Streamlined formatter for agent responses - minimal but effective."""
    
    def __init__(self):
        self.url_pattern = re.compile(r'https?://[^\s]+')
        
    def format(self, text: str) -> str:
        """Format agent response with minimal but effective styling."""
        lines = text.split('\n')
        formatted_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip multiple consecutive empty lines
            if not line:
                if i == 0 or (i > 0 and lines[i-1].strip()):
                    formatted_lines.append("")
                continue
            
            # Handle lines with asterisks (news items)
            if line.startswith('*'):
                formatted_line = self._format_news_line(line)
                formatted_lines.append(formatted_line)
            # Handle section headers (lines ending with :)
            elif line.endswith(':') and not self.url_pattern.search(line):
                if formatted_lines and formatted_lines[-1] != "":
                    formatted_lines.append("")
                formatted_lines.append(f"{COLOR_CYAN}{line}{COLOR_RESET}")
            # Handle lines that are just URLs
            elif self.url_pattern.match(line):
                formatted_lines.append(f"  {COLOR_BLUE}{line}{COLOR_RESET}")
            # Handle regular lines
            else:
                formatted_lines.append(self._format_regular_line(line))
        
        # Remove trailing empty lines
        while formatted_lines and formatted_lines[-1] == "":
            formatted_lines.pop()
            
        return '\n'.join(formatted_lines)
    
    def _format_news_line(self, line: str) -> str:
        """Format a news item line starting with asterisk."""
        # Remove the asterisk
        line = line[1:].strip()
        
        # Check if line contains URL in parentheses
        url_match = re.search(r'\((https?://[^\)]+)\)', line)
        if url_match:
            url = url_match.group(1)
            # Split title and URL
            title = line[:url_match.start()].strip()
            # Format as bullet point with title and URL on same line
            return f"{COLOR_GREEN}• {title}{COLOR_RESET} {COLOR_BLUE}{url}{COLOR_RESET}"
        else:
            # Just a title, no URL
            return f"{COLOR_GREEN}• {line}{COLOR_RESET}"
    
    def _format_regular_line(self, line: str) -> str:
        """Format a regular line with URL detection."""
        urls = self.url_pattern.findall(line)
        
        if urls:
            # If the line contains URLs, highlight them
            for url in urls:
                line = line.replace(url, f"{COLOR_BLUE}{url}{COLOR_RESET}")
        
        # Highlight temperatures
        line = re.sub(r'(\d+°[CF])', f'{COLOR_YELLOW}\\1{COLOR_RESET}', line)
        
        # Highlight subreddits
        line = re.sub(r'(r/\w+)', f'{COLOR_CYAN}\\1{COLOR_RESET}', line)
        
        return line


# Create global instance
compact_formatter = CompactFormatter()


def format_compact(text: str) -> str:
    """Format text in a compact, readable way."""
    return compact_formatter.format(text)