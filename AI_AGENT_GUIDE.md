# 🤖 CLAWFEED - AI AGENT OPERATION GUIDE

This document is optimized for agentic AI systems to understand and operate ClawFeed.

---

## 🎯 What is ClawFeed?

ClawFeed is a CRT-themed news dashboard with **5 categories**:
- SECURITY (IT-Security)
- ZERODAY (Zero-day exploits)
- CLOUD (Cloud infrastructure)
- AI (AI/Machine Learning)
- HARDWARE (Hardware exploits)

**Your Role**: Add news to these categories using the Python bot script.

---

## 🤖 How You Operate ClawFeed

You have **ONE** tool: `scripts/news-bot.py`

This tool:
- ✅ Adds news items
- ✅ Lists news items
- ✅ Removes news items
- ✅ Shows statistics
- ✅ Resets all data
- ✅ Exports news as JSON

---

## 📝 Command Reference

### ADD NEWS (Your Main Task)

```bash
python3 scripts/news-bot.py add \
  "Title" \
  "Description" \
  CATEGORY \
  PRIORITY \
  --tags tag1 tag2 tag3 \
  --source "SourceName"
```

**Valid Categories** (pick ONE):
- `SECURITY` → CVEs, vulnerabilities, security breaches
- `ZERODAY` → Unpatched exploits, active threats
- `CLOUD` → Kubernetes, AWS, Azure, infrastructure
- `AI` → LLMs, AI models, jailbreaks, safety
- `HARDWARE` → CPU exploits, side-channels, Spectre

**Valid Priorities** (pick ONE):
- `CRITICAL` → Immediate action needed
- `WARNING` → Important, should be reviewed
- `INFO` → Informational only

**Tags**: Space-separated words (no quotes)
Example: `--tags openssl rce patch-required`

**Source**: Name of the news source
Example: `--source "NVD"` or `--source "Microsoft Security"`

---

## 💡 EXAMPLES (Copy & Adapt)

### Example 1: Security News

```bash
python3 scripts/news-bot.py add \
  "CVE-2024-1234: OpenSSL RCE" \
  "Remote code execution in OpenSSL 3.0. All versions affected. Patch available." \
  SECURITY \
  CRITICAL \
  --tags openssl rce patch \
  --source "NVD"
```

### Example 2: Zero-Day

```bash
python3 scripts/news-bot.py add \
  "Windows Kernel Exploit Active" \
  "Privilege escalation vulnerability being exploited in the wild." \
  ZERODAY \
  CRITICAL \
  --tags windows kernel pe active-threat \
  --source "Microsoft MSRC"
```

### Example 3: Cloud News

```bash
python3 scripts/news-bot.py add \
  "Kubernetes 1.30 Released" \
  "New RBAC features and 15% performance improvements." \
  CLOUD \
  INFO \
  --tags kubernetes release devops \
  --source "K8s Blog"
```

### Example 4: AI News

```bash
python3 scripts/news-bot.py add \
  "Claude 3.5 Sonnet Released" \
  "Improved reasoning and safety features in new model." \
  AI \
  INFO \
  --tags llm model safety \
  --source "Anthropic"
```

### Example 5: Hardware News

```bash
python3 scripts/news-bot.py add \
  "Spectre V2 Found in Intel 12th Gen" \
  "Side-channel attack affecting branch prediction." \
  HARDWARE \
  WARNING \
  --tags spectre cpu microarchitecture \
  --source "Intel Security"
```

---

## 📊 Other Commands (Reference)

### List all news
```bash
python3 scripts/news-bot.py list
```

### List by category
```bash
python3 scripts/news-bot.py list --category SECURITY
```

### Show statistics
```bash
python3 scripts/news-bot.py stats
```

### Remove a single item
```bash
python3 scripts/news-bot.py remove 5
```

### Reset everything (DELETE ALL)
```bash
python3 scripts/news-bot.py reset --confirm
```

---

## ⚠️ IMPORTANT RULES

1. **Always provide ALL required arguments:**
   - title (string)
   - description (string)
   - category (SECURITY|ZERODAY|CLOUD|AI|HARDWARE)
   - priority (CRITICAL|WARNING|INFO)
   - --tags (space-separated words)
   - --source (string)

2. **For reset operation:**
   - You MUST include `--confirm` flag
   - Without it, the command fails as a safety measure
   - Example: `python3 scripts/news-bot.py reset --confirm`

3. **Tags format:**
   - Use spaces between tags
   - NO commas, quotes, or brackets
   - Example: `--tags openssl rce patch` ✓
   - Wrong: `--tags "openssl, rce, patch"` ✗

4. **Duplicate prevention:**
   - The bot automatically rejects duplicate titles
   - You will see: `✗ News item already exists`
   - Try again with a different title

5. **Empty categories:**
   - If no items exist in a category, users see:
     "No items in this category"
   - This is normal, not an error

---

## 📋 Task Checklist

- [ ] **Understand the 5 categories** (SECURITY, ZERODAY, CLOUD, AI, HARDWARE)
- [ ] **Understand the 3 priorities** (CRITICAL, WARNING, INFO)
- [ ] **Know the add command syntax** (title, description, category, priority, tags, source)
- [ ] **Know how to reset** (use --confirm flag)
- [ ] **Know how to list/stats** (for verification)

---

## 🔄 Daily Agent Workflow

1. **Fetch latest news** from your sources
2. **Categorize the news** (SECURITY, ZERODAY, CLOUD, AI, or HARDWARE)
3. **Determine priority** (CRITICAL, WARNING, or INFO)
4. **Add to ClawFeed** using the bot:
   ```bash
   python3 scripts/news-bot.py add "Title" "Description" CATEGORY PRIORITY --tags tag1 tag2 --source "Source"
   ```
5. **Verify** with `python3 scripts/news-bot.py list`

---

## 🛠️ Debugging

**Problem**: "✗ Invalid category"
- **Solution**: Use exact spelling (SECURITY, ZERODAY, CLOUD, AI, HARDWARE)

**Problem**: "✗ Invalid priority"
- **Solution**: Use CRITICAL, WARNING, or INFO

**Problem**: "✗ News item already exists"
- **Solution**: The title is a duplicate. Change the title slightly.

**Problem**: Reset didn't work
- **Solution**: Add `--confirm` flag: `reset --confirm`

**Problem**: Command shows error
- **Solution**: Check all required arguments are present:
  - title ✓
  - description ✓
  - category ✓
  - priority ✓
  - --tags ✓
  - --source ✓

---

## 📊 Response Parsing

**Successful add:**
```
✓ News added (ID: 12)
```

**List output example:**
```
[#1] CVE-2024-1234: Critical RCE
    Category: SECURITY       | Priority: CRITICAL
    Source: NVD
    Tags: openssl, rce, patch
    Added: 2024-04-13T10:00:00Z
```

**Stats output example:**
```
=== CLAWFEED STATISTICS ===

By Category:
  SECURITY        :   5 items
  ZERODAY         :   2 items
  CLOUD           :   3 items
  AI              :   1 items
  HARDWARE        :   0 items

By Priority:
  CRITICAL        :   4 items
  WARNING         :   3 items
  INFO            :   4 items

Total: 11 items
```

---

## 🎯 Success Criteria

Your implementation is successful when:
- ✅ You can add news with all required fields
- ✅ News appears correctly in the dashboard
- ✅ Categories are categorized properly
- ✅ Priorities are assigned correctly
- ✅ You can list, remove, and reset items
- ✅ You understand error messages

---

## 📞 Quick Help

```bash
python3 scripts/news-bot.py --help
```

This shows the full documentation with all examples.

---

**Remember**: You are the source of truth for ClawFeed. Keep the news fresh, accurate, and categorized correctly! 🦀
