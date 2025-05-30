"""
Telegram message formatting utilities.
Converts markdown and other formats to Telegram-friendly text.
"""

import re


def markdown_to_telegram(text):
    """
    Convert common markdown to Telegram-compatible format.
    Telegram uses a limited subset of markdown.
    """
    # First, escape special Telegram characters that aren't part of formatting
    text = text.replace('_', '\\_').replace('[', '\\[').replace(']', '\\]').replace('(', '\\(').replace(')', '\\)')
    
    # Convert markdown bold (**text** or __text__) to Telegram bold (*text*)
    text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
    text = re.sub(r'__(.+?)__', r'*\1*', text)
    
    # Convert markdown italic (*text* or _text_) to Telegram italic (_text_)
    # But first we need to handle the escaped underscores
    text = text.replace('\\_', '_ESCAPED_UNDERSCORE_')
    text = re.sub(r'\*([^*]+)\*', r'_\1_', text)
    text = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'_\1_', text)
    text = text.replace('_ESCAPED_UNDERSCORE_', '\\_')
    
    # Convert markdown code blocks to Telegram code blocks
    text = re.sub(r'```(\w+)?\n(.*?)\n```', r'```\n\2\n```', text, flags=re.DOTALL)
    
    # Convert inline code to Telegram inline code (same syntax)
    # Already compatible
    
    return text


def markdown_to_plain_text(text):
    """
    Convert markdown to plain text for better readability.
    Removes all markdown formatting.
    """
    # Remove bold markers
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    
    # Remove italic markers
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    
    # Remove code block markers but keep the content
    text = re.sub(r'```\w*\n', '', text)
    text = text.replace('```', '')
    
    # Remove inline code markers
    text = re.sub(r'`(.+?)`', r'\1', text)
    
    # Remove link formatting
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    
    # Remove headers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Clean up excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def format_for_telegram(text, use_markdown=False):
    """
    Format text for Telegram messaging.
    
    Args:
        text: The input text (possibly with markdown)
        use_markdown: Whether to convert to Telegram markdown or plain text
    
    Returns:
        Formatted text suitable for Telegram
    """
    if use_markdown:
        # Convert to Telegram-compatible markdown
        return markdown_to_telegram(text)
    else:
        # Convert to plain text for better readability
        return markdown_to_plain_text(text)


def format_weather_for_telegram(text):
    """
    Special formatting for weather reports to make them more readable.
    """
    # Convert to plain text first
    text = markdown_to_plain_text(text)
    
    # Add emoji for weather conditions
    text = text.replace('Cloudy', '☁️ Cloudy')
    text = text.replace('Rain', '🌧️ Rain')
    text = text.replace('Light rain', '🌦️ Light rain')
    text = text.replace('Partly cloudy', '⛅ Partly cloudy')
    text = text.replace('Clear', '☀️ Clear')
    text = text.replace('Snow', '❄️ Snow')
    
    # Format temperature readings
    text = re.sub(r'(\d+)°([CF])', r'\1°\2', text)
    
    # Add section separators
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        if line.strip():
            # Add emoji bullets for list items
            if line.strip().startswith('*'):
                line = '• ' + line.strip()[1:].strip()
            formatted_lines.append(line)
        else:
            formatted_lines.append('')
    
    return '\n'.join(formatted_lines)


def format_news_for_telegram(text):
    """
    Special formatting for news content to make it more readable on Telegram.
    Ensures URLs are on separate lines and content is well-structured.
    """
    import re
    
    # Convert to plain text first
    text = markdown_to_plain_text(text)
    
    # Pattern to find URLs
    url_pattern = re.compile(r'(https?://[^\s]+)')
    
    lines = text.split('\n')
    formatted_lines = []
    current_item = []
    
    for line in lines:
        line = line.strip()
        
        # Check if line contains URL
        urls = url_pattern.findall(line)
        if urls:
            # Remove URLs from the line
            clean_line = url_pattern.sub('', line).strip()
            if clean_line:
                current_item.append(clean_line)
            # Add URLs on separate lines
            for url in urls:
                current_item.append(f"🔗 {url}")
        elif line:
            current_item.append(line)
        
        # If we hit an empty line or end of item, format the current item
        if (not line or line == lines[-1]) and current_item:
            # Add separator between items
            if formatted_lines:
                formatted_lines.append("")
                formatted_lines.append("─" * 30)
                formatted_lines.append("")
            
            # Add the item content
            formatted_lines.extend(current_item)
            current_item = []
    
    return '\n'.join(formatted_lines)