"""
Example scraping patterns for the enhanced code executor agent.
These patterns demonstrate proper script structure and error handling.
"""

SIMPLE_NEWS_SCRAPER = '''
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_hacker_news():
    """Scrape top stories from Hacker News - a simple, reliable target."""
    url = "https://news.ycombinator.com/"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch page: {str(e)}"}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    stories = []
    
    # Hacker News has a simple structure
    story_rows = soup.select('tr.athing')[:10]  # Get top 10 stories
    
    for story in story_rows:
        story_id = story.get('id')
        title_cell = story.select_one('.titleline > a')
        if title_cell:
            title = title_cell.text
            link = title_cell.get('href', '')
            
            # Get metadata from next row
            meta_row = story.find_next_sibling('tr')
            if meta_row:
                score_span = meta_row.select_one('.score')
                score = score_span.text if score_span else 'N/A'
                
                comments_link = meta_row.select_one('a[href*="item?id="]')
                comments = comments_link.text if comments_link else '0 comments'
            else:
                score = 'N/A'
                comments = '0 comments'
            
            stories.append({
                'title': title,
                'link': link,
                'score': score,
                'comments': comments
            })
    
    return {"stories": stories, "count": len(stories)}

# Execute the scraper
result = scrape_hacker_news()
print(json.dumps(result, indent=2))

# Save to markdown file
if 'stories' in result:
    with open('./agent_files/hacker_news_headlines.md', 'w') as f:
        f.write("# Hacker News Top Stories\\n")
        f.write(f"Scraped on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
        
        for i, story in enumerate(result['stories'], 1):
            f.write(f"## {i}. {story['title']}\\n")
            f.write(f"- **Link**: {story['link']}\\n")
            f.write(f"- **Score**: {story['score']}\\n")
            f.write(f"- **Comments**: {story['comments']}\\n\\n")
    
    print(f"\\nSaved {result['count']} stories to ./agent_files/hacker_news_headlines.md")
'''

REDDIT_SCRAPER = '''
import requests
import json
from datetime import datetime

def scrape_reddit_json(subreddit="programming", limit=10):
    """Scrape Reddit using their JSON API - no BeautifulSoup needed."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Python Reddit Scraper)'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return {"error": f"Failed to fetch Reddit data: {str(e)}"}
    
    posts = []
    
    for post in data['data']['children']:
        post_data = post['data']
        posts.append({
            'title': post_data['title'],
            'url': post_data['url'],
            'score': post_data['score'],
            'num_comments': post_data['num_comments'],
            'author': post_data['author'],
            'subreddit': post_data['subreddit'],
            'permalink': f"https://reddit.com{post_data['permalink']}"
        })
    
    return {"posts": posts, "subreddit": subreddit}

# Execute the scraper
result = scrape_reddit_json("technology", 15)
print(json.dumps(result, indent=2))

# Save to markdown
if 'posts' in result:
    with open('./agent_files/reddit_technology.md', 'w') as f:
        f.write(f"# Reddit r/{result['subreddit']} Top Posts\\n")
        f.write(f"Scraped on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
        
        for i, post in enumerate(result['posts'], 1):
            f.write(f"## {i}. {post['title']}\\n")
            f.write(f"- **Author**: u/{post['author']}\\n")
            f.write(f"- **Score**: {post['score']} points\\n")
            f.write(f"- **Comments**: {post['num_comments']}\\n")
            f.write(f"- **Link**: {post['url']}\\n")
            f.write(f"- **Reddit Link**: {post['permalink']}\\n\\n")
    
    print(f"\\nSaved {len(result['posts'])} posts to ./agent_files/reddit_technology.md")
'''

GENERIC_SCRAPER_TEMPLATE = '''
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

def scrape_generic_site(url, title_selector, link_selector=None, summary_selector=None):
    """
    Generic scraper that can work with many sites.
    
    Args:
        url: The URL to scrape
        title_selector: CSS selector for titles
        link_selector: CSS selector for links (optional)
        summary_selector: CSS selector for summaries (optional)
    """
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch page: {str(e)}"}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    items = []
    
    # Find all titles
    titles = soup.select(title_selector)
    
    for i, title_elem in enumerate(titles[:20]):  # Limit to 20 items
        item = {
            'title': title_elem.get_text(strip=True)
        }
        
        # Try to find associated link
        if link_selector:
            # First check if title itself is a link
            if title_elem.name == 'a':
                item['link'] = title_elem.get('href', '')
            else:
                # Look for link in parent or siblings
                link_elem = title_elem.find_parent(link_selector) or title_elem.find_next(link_selector)
                if link_elem:
                    item['link'] = link_elem.get('href', '')
        
        # Try to find summary
        if summary_selector:
            summary_elem = title_elem.find_next(summary_selector)
            if summary_elem:
                item['summary'] = summary_elem.get_text(strip=True)
        
        items.append(item)
    
    return {"items": items, "source": url}

# Example usage - you would replace these selectors with actual ones
# result = scrape_generic_site(
#     "https://example.com",
#     title_selector="h2.article-title",
#     link_selector="a",
#     summary_selector="p.summary"
# )
'''