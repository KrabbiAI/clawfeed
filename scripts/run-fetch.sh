#!/bin/bash
# ClawFeed Cron Trigger - Spawns subagent to fetch and update news
# Run 4x daily: 00:00, 06:00, 12:00, 18:00

export CLAWFEEd_ROOT="/home/dobby/projects/clawfeed"

echo "[$(date)] ClawFeed fetch triggered"

# Spawn subagent to run the fetch
openclaw sessions spawn \
  --runtime subagent \
  --mode run \
  --task "Run: cd /home/dobby/projects/clawfeed && python3 scripts/fetch-news.py" \
  --label "clawfeed-fetch-$(date +%H%M)" 2>/dev/null || \
python3 /home/dobby/projects/clawfeed/scripts/fetch-news.py

echo "[$(date)] ClawFeed fetch complete"
