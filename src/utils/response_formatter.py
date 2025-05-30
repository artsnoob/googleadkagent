"""
Enhanced response formatting utilities for better readability.
Improves formatting for news, weather, and other content types.
"""

import re
import textwrap
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

# Import color constants from mcp_agent_utils
from .mcp_agent_utils import (
    COLOR_GREEN, COLOR_YELLOW, COLOR_CYAN, COLOR_MAGENTA, COLOR_RESET,
    COLOR_BLUE, COLOR_DIM, COLOR_BOLD, COLOR_RED, COLOR_GRAY,
    SYMBOL_INFO, SYMBOL_SUCCESS, SYMBOL_WARNING, SYMBOL_SEARCH,
    BOX_HORIZONTAL, BOX_VERTICAL, BOX_TOP_LEFT, BOX_TOP_RIGHT,
    BOX_BOTTOM_LEFT, BOX_BOTTOM_RIGHT
)


class ResponseFormatter:
    """Enhanced formatter for agent responses with improved visual hierarchy."""
    
    def __init__(self, max_line_width: int = 80, indent_size: int = 2):
        self.max_line_width = max_line_width
        self.indent_size = indent_size
        self.url_pattern = re.compile(r'https?://[^\s]+')
        self.reddit_pattern = re.compile(r'(r/\w+)')
        self.twitter_pattern = re.compile(r'(@\w+)')
        
    def format_response(self, text: str) -> str:
        """Main entry point for formatting agent responses."""
        # Detect content type and apply appropriate formatting
        if self._is_news_content(text):
            return self._format_news_content(text)
        elif self._is_weather_content(text):
            return self._format_weather_content(text)
        elif self._contains_urls(text):
            return self._format_content_with_urls(text)
        else:
            return self._format_general_content(text)
    
    def _is_news_content(self, text: str) -> bool:
        """Check if the content appears to be news."""
        news_indicators = [
            'reddit', 'r/', 'news', 'article', 'post', 
            'published', 'reported', 'announcement', 'update'
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in news_indicators)
    
    def _is_weather_content(self, text: str) -> bool:
        """Check if the content appears to be weather information."""
        weather_indicators = [
            'weather', 'temperature', 'forecast', 'rain', 
            'sunny', 'cloudy', 'humidity', '°C', '°F'
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in weather_indicators)
    
    def _contains_urls(self, text: str) -> bool:
        """Check if the content contains URLs."""
        return bool(self.url_pattern.search(text))
    
    def _format_news_content(self, text: str) -> str:
        """Format news content with better structure."""
        lines = text.split('\n')
        formatted_lines = []
        current_item = []
        item_count = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_item:
                    # Process accumulated item
                    formatted_lines.extend(self._format_news_item(current_item, item_count))
                    current_item = []
                    item_count += 1
                continue
            
            # Check if this line starts a new item (contains title indicators)
            if self._is_news_title(line) and current_item:
                # Process previous item
                formatted_lines.extend(self._format_news_item(current_item, item_count))
                current_item = [line]
                item_count += 1
            else:
                current_item.append(line)
        
        # Process last item
        if current_item:
            formatted_lines.extend(self._format_news_item(current_item, item_count))
        
        return '\n'.join(formatted_lines)
    
    def _is_news_title(self, line: str) -> bool:
        """Determine if a line is likely a news title."""
        # Titles often start with capital letters, are relatively short,
        # and don't contain URLs
        if self.url_pattern.search(line):
            return False
        if len(line) > 100:
            return False
        # Check if line starts with a capital letter or number
        return bool(re.match(r'^[A-Z0-9]', line))
    
    def _format_news_item(self, item_lines: List[str], item_number: int) -> List[str]:
        """Format a single news item."""
        formatted = []
        
        # Add minimal separator between items (not for the first one)
        if item_number > 0:
            formatted.append("")  # Just one blank line between items
        
        # Extract title, content, and URL
        title = ""
        content_lines = []
        url = ""
        
        for line in item_lines:
            urls = self.url_pattern.findall(line)
            if urls:
                url = urls[0]
                # Remove URL from line
                line_without_url = self.url_pattern.sub('', line).strip()
                if line_without_url:
                    content_lines.append(line_without_url)
            elif not title and self._is_news_title(line):
                title = line
            else:
                content_lines.append(line)
        
        # Format title with bullet point
        if title:
            formatted.append(f"{COLOR_GREEN}• {title}{COLOR_RESET}")
        
        # Format content inline (no extra spacing)
        if content_lines:
            for line in content_lines:
                # Keep content compact
                line = self._highlight_special_content(line)
                formatted.append(f"  {line}")
        
        # Format URL inline with content
        if url:
            formatted.append(f"  {COLOR_BLUE}{url}{COLOR_RESET}")
        
        return formatted
    
    def _format_weather_content(self, text: str) -> str:
        """Format weather content with better visual structure."""
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines for more compact display
            
            # Check if this is a section header
            if self._is_weather_section_header(line):
                if formatted_lines:  # Add single blank line before new sections
                    formatted_lines.append("")
                formatted_lines.append(f"{COLOR_CYAN}{line}:{COLOR_RESET}")
            else:
                # Format weather data
                line = self._format_weather_line(line)
                formatted_lines.append(f"  {line}")
        
        return '\n'.join(formatted_lines)
    
    def _is_weather_section_header(self, line: str) -> bool:
        """Check if a line is a weather section header."""
        headers = [
            'current conditions', 'forecast', 'today', 'tomorrow',
            'week ahead', 'daily forecast', 'hourly forecast'
        ]
        line_lower = line.lower()
        return any(header in line_lower for header in headers)
    
    def _format_weather_line(self, line: str) -> str:
        """Format individual weather data lines."""
        # Add weather emoji
        weather_emoji = {
            'sunny': '☀️', 'clear': '☀️',
            'cloudy': '☁️', 'overcast': '☁️',
            'rain': '🌧️', 'showers': '🌦️',
            'snow': '❄️', 'thunderstorm': '⛈️',
            'fog': '🌫️', 'wind': '💨'
        }
        
        line_lower = line.lower()
        for condition, emoji in weather_emoji.items():
            if condition in line_lower:
                line = f"{emoji} {line}"
                break
        
        # Highlight temperature
        line = re.sub(r'(\d+°[CF])', f'{COLOR_YELLOW}\\1{COLOR_RESET}', line)
        
        # Highlight percentages
        line = re.sub(r'(\d+%)', f'{COLOR_CYAN}\\1{COLOR_RESET}', line)
        
        return line
    
    def _format_content_with_urls(self, text: str) -> str:
        """Format content that contains URLs."""
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            urls = self.url_pattern.findall(line)
            if urls:
                # Put URL on next line without extra spacing
                for url in urls:
                    line_without_url = line.replace(url, '').strip()
                    if line_without_url:
                        formatted_lines.append(line_without_url)
                    formatted_lines.append(f"{COLOR_BLUE}{url}{COLOR_RESET}")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_general_content(self, text: str) -> str:
        """Format general content with basic improvements."""
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append("")
                continue
            
            # Highlight special content
            line = self._highlight_special_content(line)
            
            # Wrap long lines
            wrapped = self._wrap_text(line, self.max_line_width)
            formatted_lines.extend(wrapped)
        
        return '\n'.join(formatted_lines)
    
    def _highlight_special_content(self, line: str) -> str:
        """Highlight special content like Reddit/Twitter handles."""
        # Highlight Reddit subreddits
        line = self.reddit_pattern.sub(f'{COLOR_CYAN}\\1{COLOR_RESET}', line)
        
        # Highlight Twitter handles
        line = self.twitter_pattern.sub(f'{COLOR_BLUE}\\1{COLOR_RESET}', line)
        
        return line
    
    def _format_url(self, url: str) -> str:
        """Format URL for better readability."""
        # For now, return the full URL to ensure users can access it
        # We can add shortening logic later if needed
        return url
    
    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        """Wrap text to specified width while preserving formatting."""
        # Don't wrap if text contains ANSI escape codes (colors)
        if '\033[' in text:
            return [text]
        
        return textwrap.wrap(text, width=max_width, break_long_words=False, break_on_hyphens=False)


# Global formatter instance
response_formatter = ResponseFormatter()


def format_agent_response(text: str) -> str:
    """Convenience function to format agent responses."""
    return response_formatter.format_response(text)