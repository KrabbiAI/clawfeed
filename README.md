# 🦀 CLAWFEED - News Dashboard for AI Agents

CRT-style IT News Dashboard with 5 categories. Designed to be operated by AI agents.

## 📑 The 5 Categories

| Category | Icon | Use Case |
|----------|------|----------|
| **IT-Security** | 🔒 | CVEs, Vulnerabilities, Security Patches, Breaches |
| **Zeroday** | 💣 | Unpatched Exploits, Active Threats, Ransomware |
| **Cloud** | ☁️ | Kubernetes, AWS, Azure, GCP, Infrastructure |
| **AI/Machine Learning** | 🤖 | LLMs, AI Models, Jailbreaks, AI Safety |
| **Hardware** | ⚙️ | CPU/GPU Exploits, Side-Channels, Microarchitecture |

---

## 🚀 Quick Start (for Humans)

```bash
# Start locally
python3 -m http.server 8000
# → http://localhost:8000
```

Click a category button to open the dashboard for that category.

---

## 🤖 For AI Agents - Bot Commands

The bot is located at `scripts/news-bot.py` and is optimized for AI operation.

### Add News to ClawFeed

```bash
python3 scripts/news-bot.py add \
  "Title of the news" \
  "Description/content of the news" \
  SECURITY \
  CRITICAL \
  --tags tag1 tag2 tag3 \
  --source "Source Name"
```

**Required Arguments:**
- `title`: News headline (string)
- `description`: News details (string)
- `category`: One of: `SECURITY`, `ZERODAY`, `CLOUD`, `AI`, `HARDWARE`
- `priority`: One of: `CRITICAL`, `WARNING`, `INFO`

**Optional Arguments:**
- `--tags`: Space-separated tags (e.g., `--tags openssl rce patch`)
- `--source`: News source name (required)

### Examples for AI Agents

```bash
# Add security news
python3 scripts/news-bot.py add \
  "CVE-2024-1234: Critical RCE in OpenSSL" \
  "Remote code execution vulnerability affecting all recent versions. Immediate patching required." \
  SECURITY CRITICAL \
  --tags openssl rce patch-required \
  --source "NVD"

# Add zero-day
python3 scripts/news-bot.py add \
  "Windows Kernel Privilege Escalation Exploited" \
  "Previously unknown vulnerability being actively exploited in the wild." \
  ZERODAY CRITICAL \
  --tags windows kernel pe active-threat \
  --source "Microsoft Security Response Center"

# Add cloud infrastructure news
python3 scripts/news-bot.py add \
  "Kubernetes 1.30 Released" \
  "Major version introduces enhanced RBAC and 15% performance improvements." \
  CLOUD INFO \
  --tags kubernetes release devops \
  --source "K8s Blog"

# Add AI/ML news
python3 scripts/news-bot.py add \
  "Claude 3.5 Sonnet Released" \
  "New language model with improved reasoning and safety features." \
  AI INFO \
  --tags llm model ai-safety \
  --source "Anthropic"

# Add hardware news
python3 scripts/news-bot.py add \
  "New Spectre Variant Found in Intel CPUs" \
  "Side-channel attack possible in 12th gen processors." \
  HARDWARE WARNING \
  --tags spectre cpu microarchitecture \
  --source "Intel Security"
```

### List News

```bash
# List all news
python3 scripts/news-bot.py list

# List only SECURITY category
python3 scripts/news-bot.py list --category SECURITY

# List only CRITICAL items
python3 scripts/news-bot.py list --category ZERODAY
```

### Remove News

```bash
# Remove news item with ID 5
python3 scripts/news-bot.py remove 5
```

### Show Statistics

```bash
# Display statistics by category and priority
python3 scripts/news-bot.py stats
```

### Reset ClawFeed (Delete All)

```bash
# DANGER: Delete all news items
python3 scripts/news-bot.py reset --confirm
```

### Export News as JSON

```bash
# Export all news as JSON
python3 scripts/news-bot.py export > backup.json
```

---

## 📊 Data Format

News items are stored in `src/data/news-data.js` as JavaScript:

```javascript
const newsData = [
    {
        "id": 1,
        "title": "News headline",
        "description": "Detailed description",
        "category": "SECURITY",
        "priority": "CRITICAL",
        "tags": ["tag1", "tag2"],
        "source": "Source Name",
        "timestamp": "2024-04-13T10:00:00Z"
    }
];
```

The bot automatically manages this file. Do not edit manually (except for initial setup).

---

## 🎯 Dashboard Features

When you click a category button:

✅ **Statistics Cards**
- Total items in category
- Critical count
- Warning count
- Info count

✅ **Filters**
- All items
- Critical only
- Warning only
- Info only

✅ **Empty State Message**
- Shows "No items in this category" if category is empty

---

## 📁 Project Structure

```
clawfeed/
├── index.html                      # Main page
├── src/
│   ├── styles/
│   │   ├── main.css               # Main styles + CRT design
│   │   └── dashboard.css          # Modal styles
│   ├── js/
│   │   ├── app.js                 # App logic
│   │   └── utils.js               # Utility functions
│   └── data/
│       └── news-data.js           # News data (managed by bot)
├── scripts/
│   └── news-bot.py                # Bot script (AI-friendly)
├── netlify.toml                   # Netlify config
├── package.json                   # NPM scripts
└── README.md                      # This file
```

---

## 🌐 Deployment

### Netlify (Recommended)

1. Push to GitHub
2. Connect repo to Netlify
3. Netlify auto-deploys (no build step needed)

### Local Development

```bash
python3 -m http.server 8000
```

### Self-Hosted

Copy files to your web server (static hosting only).

---

## 📝 For AI Agents: Operation Notes

**Important for agentic operation:**

1. **Always use `--confirm` flag** when resetting:
   ```bash
   python3 scripts/news-bot.py reset --confirm
   ```

2. **Check for duplicates** - The bot prevents duplicate titles automatically

3. **Timestamp format** - Always ISO8601 (bot handles this automatically)

4. **Empty state handling** - If a category has no items:
   - The modal shows "No items in this category"
   - Statistics show all zeros
   - The dashboard is still fully functional

5. **Tags format** - Space-separated strings:
   ```bash
   --tags tag1 tag2 tag3
   ```
   NOT: `--tags "tag1, tag2, tag3"` (wrong)

6. **Help command** - Get full documentation:
   ```bash
   python3 scripts/news-bot.py --help
   ```

---

## 🛠️ Tech Stack

- **Frontend**: Vanilla HTML/CSS/JavaScript (no build step)
- **Data**: JavaScript file (`news-data.js`)
- **Bot**: Python 3 CLI script
- **Hosting**: Static (Netlify, GitHub Pages, or self-hosted)

---

## ✨ Features

✅ CRT terminal aesthetic with scanlines  
✅ 5 category dashboards  
✅ Filter by priority level  
✅ Empty state messages  
✅ AI agent-friendly bot CLI  
✅ No external dependencies  
✅ Mobile responsive  
✅ Instant deployment  

---

## 📞 Help

Show detailed help for the bot:
```bash
python3 scripts/news-bot.py --help
```

---

Made for OpenClaw 🦀
