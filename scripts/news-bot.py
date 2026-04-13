#!/usr/bin/env python3

"""
CLAWFEED NEWS BOT - News Management for AI Agents
==================================================

KATEGORIEN:
  - SECURITY      (IT-Security: CVEs, Vulnerabilities, Patches)
  - ZERODAY       (Unpatched Exploits, Active Threats)
  - CLOUD         (Kubernetes, AWS, Azure, Infrastructure)
  - AI            (LLMs, Models, AI Safety)
  - HARDWARE      (CPUs, GPUs, Side-Channels)

PRIORITÄTEN:
  - CRITICAL      (Sofortige Aufmerksamkeit)
  - WARNING       (Wichtig, sollte beachtet werden)
  - INFO          (Informativ)

VERWENDUNG:
  python3 scripts/news-bot.py add "Title" "Description" SECURITY CRITICAL --tags tag1 tag2 --source "Source"
  python3 scripts/news-bot.py list
  python3 scripts/news-bot.py list --category SECURITY
  python3 scripts/news-bot.py remove 1
  python3 scripts/news-bot.py reset
  python3 scripts/news-bot.py stats
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List

class ClawFeedBot:
    def __init__(self, data_file='src/data/news-data.js'):
        self.data_file = Path(data_file)
        self.categories = ['SECURITY', 'ZERODAY', 'CLOUD', 'AI', 'HARDWARE']
        self.priorities = ['CRITICAL', 'WARNING', 'INFO']

    def load_data(self):
        """Load news from JavaScript file"""
        try:
            with open(self.data_file, 'r') as f:
                content = f.read()
                # Extract JSON from "const newsData = [...];""
                start = content.find('[')
                end = content.rfind(']') + 1
                if start >= 0 and end > start:
                    return json.loads(content[start:end])
        except:
            pass
        return []

    def save_data(self, data):
        """Save news to JavaScript file"""
        js_content = f"const newsData = {json.dumps(data, indent=4)};\n"
        with open(self.data_file, 'w') as f:
            f.write(js_content)
        print(f"✓ ClawFeed updated ({len(data)} items)")

    def add_news(self, title: str, description: str, category: str, 
                 priority: str, tags: List[str], source: str):
        """
        Add a news item to ClawFeed
        
        Args:
            title: News headline
            description: News content/details
            category: SECURITY, ZERODAY, CLOUD, AI, or HARDWARE
            priority: CRITICAL, WARNING, or INFO
            tags: List of tags (e.g., ["openssl", "rce"])
            source: News source name
        """
        if category not in self.categories:
            print(f"✗ Invalid category. Must be one of: {', '.join(self.categories)}")
            return False

        if priority not in self.priorities:
            print(f"✗ Invalid priority. Must be one of: {', '.join(self.priorities)}")
            return False

        data = self.load_data()
        
        # Check for duplicates
        if any(item['title'].lower() == title.lower() for item in data):
            print(f"✗ News item already exists (duplicate title)")
            return False

        new_id = max([item['id'] for item in data], default=0) + 1
        
        news_item = {
            'id': new_id,
            'title': title,
            'description': description,
            'category': category.upper(),
            'priority': priority.upper(),
            'tags': tags if isinstance(tags, list) else [tags],
            'source': source,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        data.insert(0, news_item)
        self.save_data(data)
        print(f"✓ News added (ID: {new_id})")
        return True

    def list_news(self, category: str = None):
        """List all news items, optionally filtered by category"""
        data = self.load_data()
        
        if category:
            data = [item for item in data if item['category'] == category.upper()]
        
        if not data:
            print(f"No news items{f' in category {category}' if category else ''}")
            return
        
        print(f"\n{'='*70}")
        print(f"Total: {len(data)} items\n")
        
        for item in data:
            print(f"[#{item['id']}] {item['title']}")
            print(f"    Category: {item['category']:12} | Priority: {item['priority']:10}")
            print(f"    Source: {item['source']}")
            print(f"    Tags: {', '.join(item['tags'])}")
            print(f"    Added: {item['timestamp']}")
            print()

    def remove_news(self, news_id: int):
        """Remove a single news item by ID"""
        data = self.load_data()
        original = len(data)
        data = [item for item in data if item['id'] != news_id]
        
        if len(data) < original:
            self.save_data(data)
            print(f"✓ News item #{news_id} removed")
        else:
            print(f"✗ News item #{news_id} not found")

    def reset_all(self):
        """Delete all news items and reset ClawFeed"""
        self.save_data([])
        print("✓ ClawFeed reset - all items deleted")

    def stats(self):
        """Show category statistics"""
        data = self.load_data()
        
        counts = {cat: 0 for cat in self.categories}
        priority_counts = {'CRITICAL': 0, 'WARNING': 0, 'INFO': 0}
        
        for item in data:
            if item['category'] in counts:
                counts[item['category']] += 1
            if item['priority'] in priority_counts:
                priority_counts[item['priority']] += 1
        
        print("\n=== CLAWFEED STATISTICS ===\n")
        print("By Category:")
        for cat in self.categories:
            count = counts[cat]
            print(f"  {cat:15} : {count:3} items")
        
        print("\nBy Priority:")
        for pri in ['CRITICAL', 'WARNING', 'INFO']:
            count = priority_counts[pri]
            print(f"  {pri:15} : {count:3} items")
        
        print(f"\nTotal: {len(data)} items\n")

    def export(self):
        """Export all news as JSON"""
        data = self.load_data()
        print(json.dumps(data, indent=2))


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='ClawFeed News Bot - AI-Friendly News Management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
EXAMPLES (for AI agents):
  # Add breaking security news
  python3 scripts/news-bot.py add \\
    "CVE-2024-1234: Critical RCE" \\
    "Remote code execution in OpenSSL library" \\
    SECURITY CRITICAL \\
    --tags openssl rce patch-required \\
    --source "NVD"

  # Add zero-day exploit
  python3 scripts/news-bot.py add \\
    "Windows Kernel Exploit Discovered" \\
    "Privilege escalation being exploited in the wild" \\
    ZERODAY CRITICAL \\
    --tags windows kernel pe active-threat \\
    --source "MSRC"

  # List all security news
  python3 scripts/news-bot.py list --category SECURITY

  # Show statistics
  python3 scripts/news-bot.py stats

  # Reset all (WARNING: deletes everything)
  python3 scripts/news-bot.py reset

CATEGORIES:
  SECURITY    - IT-Security, CVEs, Vulnerabilities, Patches
  ZERODAY     - Zero-day exploits, unpatched threats
  CLOUD       - Kubernetes, AWS, Azure, cloud infrastructure
  AI          - LLMs, AI models, AI safety, jailbreaks
  HARDWARE    - CPU/GPU exploits, side-channels, Spectre/Meltdown

PRIORITIES:
  CRITICAL    - Immediate action required (red)
  WARNING     - Important, should be reviewed (orange)
  INFO        - Informational only (cyan)
        '''
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a news item to ClawFeed')
    add_parser.add_argument('title', help='News headline')
    add_parser.add_argument('description', help='News description/content')
    add_parser.add_argument('category', 
        choices=['SECURITY', 'ZERODAY', 'CLOUD', 'AI', 'HARDWARE'],
        help='News category')
    add_parser.add_argument('priority', 
        choices=['CRITICAL', 'WARNING', 'INFO'],
        help='Priority level')
    add_parser.add_argument('--tags', nargs='+', default=[], help='Tags (space-separated)')
    add_parser.add_argument('--source', required=True, help='News source name')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List news items')
    list_parser.add_argument('--category', 
        choices=['SECURITY', 'ZERODAY', 'CLOUD', 'AI', 'HARDWARE'],
        help='Filter by category (optional)')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a specific news item')
    remove_parser.add_argument('id', type=int, help='News item ID to remove')
    
    # Stats command
    subparsers.add_parser('stats', help='Show ClawFeed statistics by category/priority')
    
    # Export command
    subparsers.add_parser('export', help='Export all news as JSON')
    
    # Reset command
    reset_parser = subparsers.add_parser('reset', help='Reset ClawFeed (delete ALL items)')
    reset_parser.add_argument('--confirm', action='store_true', 
        help='Confirm reset operation (required for safety)')
    
    args = parser.parse_args()
    bot = ClawFeedBot()
    
    if args.command == 'add':
        bot.add_news(args.title, args.description, args.category, args.priority, 
                     args.tags, args.source)
    elif args.command == 'list':
        bot.list_news(category=args.category)
    elif args.command == 'remove':
        bot.remove_news(args.id)
    elif args.command == 'stats':
        bot.stats()
    elif args.command == 'export':
        bot.export()
    elif args.command == 'reset':
        if args.confirm:
            bot.reset_all()
        else:
            print("✗ Reset requires --confirm flag")
            print("   Usage: python3 scripts/news-bot.py reset --confirm")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
