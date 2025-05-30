"""
RSS Scraper Patch Utility
This module provides functions to format and process RSS feed data from the content scraper MCP.
"""

import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def fix_rss_article_urls(articles_data):
    """
    Process RSS article URLs for proper formatting.
    
    Args:
        articles_data (dict): Dictionary of feed names to article lists
        
    Returns:
        dict: Processed articles data with formatted URLs
    """
    fixed_data = {}
    
    for feed_name, articles in articles_data.items():
        fixed_articles = []
        
        for article in articles:
            if isinstance(article, dict) and 'link' in article:
                # Fix the URL
                fixed_url = fix_single_url(article['link'])
                
                # Create a copy of the article with the fixed URL
                fixed_article = article.copy()
                fixed_article['link'] = fixed_url
                fixed_articles.append(fixed_article)
            else:
                # Keep article as-is if it doesn't have expected structure
                fixed_articles.append(article)
        
        fixed_data[feed_name] = fixed_articles
    
    return fixed_data


def fix_single_url(url):
    """
    Fix a single URL that may have incorrect date components.
    
    Args:
        url (str): The URL to fix
        
    Returns:
        str: The fixed URL
    """
    # Since we're in 2025, we no longer need to fix 2025 dates
    # Simply return the URL as-is
    return url


def format_rss_response_with_urls(raw_json_data):
    """
    Format the RSS scraper response to ensure URLs are properly included.
    
    Args:
        raw_json_data (dict): Raw JSON response from RSS scraper
        
    Returns:
        str: Formatted response with proper URLs
    """
    output = "Here's the latest AI news from RSS feeds:\n\n"
    
    for feed_name, articles in raw_json_data.items():
        if not articles or not isinstance(articles, list):
            output += f"**From {feed_name}:**\n*   No recent articles found.\n\n"
            continue
            
        output += f"**From {feed_name}:**\n"
        
        for article in articles[:5]:  # Limit to 5 articles per feed
            if isinstance(article, dict):
                title = article.get('title', 'No Title')
                link = article.get('link', '')
                author = article.get('author', 'Unknown')
                description = article.get('description', '')
                
                # Clean up the description
                if description:
                    # Remove excessive whitespace and truncate
                    description = ' '.join(description.split())
                    if len(description) > 200:
                        description = description[:197] + '...'
                
                # Format the article entry
                output += f"*   **{title}**"
                if link:
                    output += f" ({link})"
                if author and author != 'Unknown':
                    output += f" - by {author}"
                if description:
                    output += f" - {description}"
                output += "\n"
        
        output += "\n"
    
    return output.strip()


def extract_urls_from_rss_response(rss_response_text):
    """
    Extract URLs from an RSS scraper response text.
    
    Args:
        rss_response_text (str): The response text from RSS scraper
        
    Returns:
        list: List of extracted URLs
    """
    # Pattern to match URLs in parentheses (common format in responses)
    url_pattern = r'\(https?://[^\)]+\)'
    
    urls = []
    matches = re.findall(url_pattern, rss_response_text)
    
    for match in matches:
        # Remove the parentheses
        url = match[1:-1]
        urls.append(url)
    
    return urls


# Example usage
if __name__ == "__main__":
    # Example of processing RSS data
    sample_data = {
        "TechCrunch": [
            {
                "title": "AI News Article",
                "link": "https://techcrunch.com/2025/05/30/ai-news-article/",
                "author": "John Doe",
                "description": "Some AI news..."
            }
        ]
    }
    
    fixed_data = fix_rss_article_urls(sample_data)
    print("Processed URLs:")
    print(format_rss_response_with_urls(fixed_data))