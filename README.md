# 🦀 ClawFeed - AI-Powered Threat Intel Dashboard

Real-Time IT Threat & Innovation Feed mit 5 Kategorien, betrieben von AI Agents via Tavily Search API.

**Live:** https://clawfeed.netlify.app

---

## 🎯 Die 5 Kategorien

| Kategorie | Icon | Beschreibung |
|-----------|------|--------------|
| **SECURITY** | 🔒 | CVEs, Vulnerabilities, Security Patches, Breaches |
| **ZERODAY** | 💣 | Unpatched Exploits, Active Threats, Ransomware |
| **CLOUD** | ☁️ | Kubernetes, AWS, Azure, GCP, Infrastructure |
| **AI** | 🤖 | LLMs, AI Models, Jailbreaks, AI Safety |
| **HARDWARE** | ⚙️ | CPU/GPU Exploits, Side-Channels, Microarchitecture |

---

## ⚙️ Tech Stack

- **Frontend:** Vanilla HTML/CSS/JavaScript (kein Build-Step)
- **Data:** JavaScript file (`news-data.js`)
- **Fetching:** Tavily Search API (4x täglich automatisch)
- **Bot:** Python 3 CLI für manuelles News-Management
- **Hosting:** Netlify / GitHub Pages / beliebiges static Hosting

---

## 🚀 Quick Start

```bash
# Lokal starten
python3 -m http.server 8000
# → http://localhost:8000
```

---

## 🤖 AI Agent Operation

### News automatisch fetchen (4x täglich)

```bash
# Cron: 0:00, 6:00, 12:00, 18:00
cd /home/dobby/projects/clawfeed
python3 scripts/fetch-news.py
```

### Manuell News hinzufügen

```bash
python3 scripts/news-bot.py add \
  "CVE-2026-XXXX: Critical RCE in OpenSSL" \
  "Remote code execution vulnerability..." \
  SECURITY CRITICAL \
  --tags openssl rce patch \
  --source "NVD"
```

### Weitere Bot Commands

```bash
python3 scripts/news-bot.py list                    # Alle News
python3 scripts/news-bot.py list --category SECURITY # Nach Kategorie
python3 scripts/news-bot.py stats                   # Statistiken
python3 scripts/news-bot.py remove 5                 # News #5 löschen
python3 scripts/news-bot.py reset --confirm          # Alles löschen
```

---

## 📁 Projektstruktur

```
clawfeed/
├── index.html                      # Hauptseite
├── src/
│   ├── styles/
│   │   ├── main.css               # CRT Design
│   │   └── dashboard.css           # Modal Styles
│   ├── js/
│   │   ├── app.js                 # App Logik
│   │   └── utils.js                # Utilities
│   └── data/
│       └── news-data.js            # News Daten
├── scripts/
│   ├── fetch-news.py              # Tavily Fetcher (PRIMÄR)
│   └── news-bot.py                # CLI Bot
├── netlify.toml                   # Netlify Config
├── AI_AGENT_GUIDE.md              # Detaillierte AI Dokumentation
└── README.md                      # Diese Datei
```

---

## 🔄 Automation

### Tavily Search API

Der Fetcher nutzt Tavily statt RSS-Feeds für bessere Results:

- HTML Cleaning automatisch
- Globale Deduplication
- Relevanz-basiertes Ranking
- 3 Queries pro Kategorie, top 5 Results pro Query

### Cron Setup

```bash
# ClawFeed - Fetch news 4x daily
0 0,6,12,18 * * * cd /home/dobby/projects/clawfeed && python3 scripts/fetch-news.py
```

---

## 🌐 Deployment

### Netlify (empfohlen)

1. GitHub Repo verbinden: `https://github.com/KrabbiAI/clawfeed`
2. Automatisches Deployment bei jedem Push

### GitHub Pages

1. Settings → Pages → Source: `main` branch
2. Fertig unter: `https://KrabbiAI.github.io/clawfeed`

---

## 📊 Features

✅ CRT Terminal Aesthetic mit Scanlines  
✅ 5 Kategorie Dashboards  
✅ Prioritäts-Filter (CRITICAL/WARNING/INFO)  
✅ AI Agent-optimiertes CLI  
✅ Tavily-powered automatic fetching  
✅ Mobile Responsive  
✅ Keine externen Dependencies  
✅ Sofort einsatzbereit  

---

Made with ❤️ by Krabbi 🦀
