#!/usr/bin/env python3
"""
ClawFeed News Fetcher via Tavily Search API
Fetches top news for each category using Tavily
"""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from tavily import TavilyClient

# Category search queries for Tavily
CATEGORY_QUERIES = {
    'SECURITY': [
        'cybersecurity vulnerability CVE 2026',
        'data breach malware ransomware 2026',
        'security patch update enterprise',
    ],
    'ZERODAY': [
        'zero day exploit vulnerability active 2026',
        'unpatched vulnerability exploited 2026',
        'ransomware attack critical infrastructure 2026',
    ],
    'CLOUD': [
        'kubernetes aws azure gcp cloud 2026',
        'devops infrastructure cloud native 2026',
        'cloud security outage incident 2026',
    ],
    'AI': [
        'artificial intelligence LLM GPT Claude 2026',
        'AI model release safety 2026',
        'machine learning breakthrough research 2026',
    ],
    'HARDWARE': [
        'CPU GPU processor chip architecture 2026',
        'Intel AMD NVIDIA hardware 2026',
        'semiconductor chip manufacturing 2026',
    ]
}

DATA_FILE = Path(__file__).parent.parent / 'src' / 'data' / 'news-data.js'
MAX_ITEMS_PER_CATEGORY = 10
MAX_SEARCH_RESULTS = 5  # per query

# Initialize Tavily
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY', '')
if not TAVILY_API_KEY:
    # Try to load from credentials.json
    cred_file = Path.home() / '.openclaw' / 'workspace' / 'credentials.json'
    if cred_file.exists():
        creds = json.loads(cred_file.read_text())
        TAVILY_API_KEY = creds.get('tavily', {}).get('api_key', '')


def search_tavily(query, max_results=5):
    """Search using Tavily API"""
    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        result = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_answer=False,
            include_raw_content=False
        )
        return result.get('results', [])
    except Exception as e:
        print(f"  Tavily error for '{query}': {e}")
        return []


def determine_priority(title, description):
    """Determine priority based on keywords"""
    text = (title + ' ' + description).lower()
    critical_keywords = [
        'critical', 'zero-day', 'zeroday', 'active exploit', 'ransomware',
        'breach', 'data leak', 'vulnerability', 'cve', 'urgent',
        'immediate', 'active threat', 'in the wild', 'being exploited'
    ]
    warning_keywords = [
        'vulnerability', 'patch', 'update', 'warning', ' flaw', 'issue',
        'important', 'released', 'announced'
    ]
    
    for kw in critical_keywords:
        if kw in text:
            return 'CRITICAL'
    for kw in warning_keywords:
        if kw in text:
            return 'WARNING'
    return 'INFO'


def determine_tags(title, description, category):
    """Generate tags based on content"""
    text = (title + ' ' + description).lower()
    tags = []
    
    if category == 'SECURITY':
        if any(x in text for x in ['cve', 'vulnerability', 'exploit']): tags.append('vulnerability')
        if 'patch' in text or 'update' in text: tags.append('patch')
        if 'breach' in text or 'leak' in text: tags.append('breach')
        if 'ransomware' in text: tags.append('ransomware')
        if 'malware' in text: tags.append('malware')
    elif category == 'ZERODAY':
        if 'zero-day' in text or 'zeroday' in text: tags.append('zeroday')
        if 'exploit' in text: tags.append('exploit')
        if 'ransomware' in text: tags.append('ransomware')
        if 'active' in text or 'wild' in text: tags.append('active-threat')
    elif category == 'CLOUD':
        if 'kubernetes' in text or 'k8s' in text: tags.append('kubernetes')
        if 'aws' in text or 'amazon' in text: tags.append('aws')
        if 'azure' in text or 'microsoft' in text: tags.append('azure')
        if 'gcp' in text or 'google cloud' in text: tags.append('gcp')
        if 'docker' in text or 'container' in text: tags.append('containers')
    elif category == 'AI':
        if any(x in text for x in ['llm', 'gpt', 'claude', 'gemini', 'openai']): tags.append('llm')
        if 'model' in text: tags.append('model')
        if 'safety' in text or 'alignment' in text: tags.append('safety')
        if 'research' in text or 'paper' in text: tags.append('research')
    elif category == 'HARDWARE':
        if 'cpu' in text: tags.append('cpu')
        if 'gpu' in text: tags.append('gpu')
        if 'intel' in text: tags.append('intel')
        if 'amd' in text: tags.append('amd')
        if 'nvidia' in text: tags.append('nvidia')
        if 'chip' in text or 'semiconductor' in text: tags.append('chip')
    
    if not tags:
        tags = [category.lower()]
    
    return tags[:4]


def load_news():
    """Load existing news from JS file"""
    if not DATA_FILE.exists():
        return []
    try:
        content = DATA_FILE.read_text()
        start = content.find('[')
        end = content.rfind(']') + 1
        if start >= 0 and end > start:
            return json.loads(content[start:end])
    except:
        pass
    return []


def save_news(news):
    """Save news to JS file"""
    js_content = f"const newsData = {json.dumps(news, indent=4)};\n"
    DATA_FILE.write_text(js_content)
    print(f"✓ Saved {len(news)} items to {DATA_FILE}")


def clean_text(text, max_len=300):
    """Clean HTML and truncate"""
    if not text:
        return ''
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_len]


def fetch_all():
    """Fetch news for all categories using Tavily"""
    all_news = {}
    
    print("Searching with Tavily...")
    for category, queries in CATEGORY_QUERIES.items():
        print(f"  {category}: {len(queries)} queries")
        all_news[category] = []
        seen_titles = set()
        
        for query in queries:
            results = search_tavily(query, max_results=MAX_SEARCH_RESULTS)
            for r in results:
                title = clean_text(r.get('title', ''), 200)
                if not title or title.lower() in seen_titles:
                    continue
                seen_titles.add(title.lower())
                
                description = clean_text(r.get('description', ''), 300)
                url = r.get('url', '')
                
                all_news[category].append({
                    'title': title,
                    'description': description,
                    'link': url,
                    'category': category,
                    'source': clean_text(r.get('source', url[:50]), 50)
                })
    
    return all_news


def main():
    print(f"=== ClawFeed Fetcher (Tavily) === {datetime.now().isoformat()}")
    
    if not TAVILY_API_KEY:
        print("✗ No Tavily API key found!")
        print("  Set TAVILY_API_KEY env var or add to credentials.json")
        return
    
    # Load existing news (for deduplication)
    existing = load_news()
    existing_titles = {item['title'].lower() for item in existing}
    
    # Fetch fresh news
    all_news = fetch_all()
    
    # Select top items per category, excluding already-added
    new_items = []
    next_id = max([item['id'] for item in existing], default=0) + 1
    
    for category in ['SECURITY', 'ZERODAY', 'CLOUD', 'AI', 'HARDWARE']:
        items = all_news.get(category, [])
        count = 0
        for item in items:
            if count >= MAX_ITEMS_PER_CATEGORY:
                break
            if item['title'].lower() not in existing_titles:
                priority = determine_priority(item['title'], item['description'])
                tags = determine_tags(item['title'], item['description'], category)
                new_items.append({
                    'id': next_id,
                    'title': item['title'],
                    'description': item['description'],
                    'category': category,
                    'priority': priority,
                    'tags': tags,
                    'source': item['source'],
                    'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                    'link': item.get('link', '')
                })
                next_id += 1
                count += 1
    
    # Combine: new items first, then existing
    combined = new_items + existing
    
    # Keep max 100 items total
    if len(combined) > 100:
        combined = combined[:100]
    
    save_news(combined)
    print(f"\n=== Summary ===")
    print(f"New items added: {len(new_items)}")
    print(f"Total items: {len(combined)}")
    for cat in ['SECURITY', 'ZERODAY', 'CLOUD', 'AI', 'HARDWARE']:
        count = sum(1 for i in combined if i['category'] == cat)
        print(f"  {cat}: {count}")


if __name__ == '__main__':
    main()
