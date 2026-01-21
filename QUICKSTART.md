# KAI Quick Start Guide

## ✅ What's Included

- ✅ Full project structure ready
- ✅ Commands system working (tasks, notes, calendar)
- ✅ Local AI model ready to download
- ✅ Optional Google Calendar integration

## 🚀 Installation (5 minutes)

### Step 1: Install Dependencies

```bash
cd /workspaces/KAI
source venv/bin/activate  # Already created in Codespaces
pip install -r requirements.txt
```

This installs PyTorch, Transformers, and Google Calendar API (~500MB download).

### Step 2: Run KAI

```bash
python main.py
```

**First run**: Model downloads automatically (~300MB, takes ~5 mins)

That's it! Everything runs locally with no external servers.

---

## 🎮 Using KAI

### Try These Commands:

```bash
# Get help
/help

# Task management (works immediately)
/task add Finish math homework
/task add Study for test
/task list
/task done 1

# Study tools (works immediately)
/study save Calculus Derivative measures rate of change
/study save Calculus Integral measures area under curve
/study show Calculus
/study quiz Calculus

# Google Calendar (requires setup - see below)
/calendar list
/calendar add Team meeting at 2pm
/calendar remove Team meeting

# Natural conversation (after model loads)
What is calculus?
Explain derivatives simply
Tell me a joke
```

---

## 📅 Google Calendar Setup (Optional)

Want to use `/calendar` commands? Follow these steps:

### Step 1: Create Google Credentials

1. Go to https://console.cloud.google.com/
2. Create a new project (name it "KAI" or anything)
3. Search for "Google Calendar API" and enable it
4. Click "Create Credentials" → OAuth 2.0 → Desktop Application
5. Download as JSON

### Step 2: Add to KAI

```bash
mkdir -p data
# Move your downloaded credentials.json to data/
cp ~/Downloads/credentials.json data/
```

### Step 3: Authorize KAI

Run KAI and it will open a browser asking for calendar permission:

```bash
python main.py
```

Click "Allow" and you're done! 

Now you can use:
- `/calendar list` - See your upcoming events
- `/calendar add Event Name` - Add events
- `/calendar remove Event Name` - Delete events

---

## 🔍 Project Structure

```
KAI/
├── main.py                     # Run this → python main.py
├── kai/
│   ├── llm.py                 # Local AI (transformers)
│   ├── router.py              # Command routing
│   └── tools/
│       ├── task_tool.py       # Tasks
│       ├── study_tool.py      # Notes & quizzes
│       └── calendar_tool.py   # Google Calendar
├── data/
│   ├── tasks.json             # Your tasks
│   ├── notes.json             # Your notes
│   ├── credentials.json       # Google OAuth (optional)
│   └── google_token.json      # Cached Google auth (auto-created)
```

---

## ✨ What's Special About This Version

✅ **No external servers** - everything runs locally  
✅ **No API keys** - completely private  
✅ **Fully integrated AI** - built-in local model  
✅ **Google Calendar** - integrated if you want it  
✅ **Works offline** - after first download  
✅ **Fast setup** - just pip install and run  

---

## 📊 Model Options

Want faster or better responses? Edit `main.py` line 25:

```python
llm = KaiLLM(model="distilgpt2")  # Fast (default)
# or
llm = KaiLLM(model="gpt2")  # Better quality
# or
llm = KaiLLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")  # Best quality
```

**First time with new model?** It auto-downloads (~300MB-1.1GB)

---

## 🐛 Troubleshooting

**"torch not found"**
```bash
pip install torch transformers
```

**"Slow responses"**
- Normal on CPU! First response loads model into memory
- Subsequent responses are faster
- Switch to `distilgpt2` if using larger model

**"Memory issues"**
- Restart KAI
- Use smaller model: `distilgpt2`

**"Google Calendar commands not working"**
- Check: `ls data/credentials.json` - file should exist
- Delete `data/google_token.json` and rerun - it will re-authorize
- Check error message has a link to https://accounts.google.com - follow it

---

## 🎯 Next Steps

1. Run: `python main.py`
2. Try: `/help` to see all commands
3. Try: `/task list` to see tasks
4. Try: `/calendar list` (if set up)
5. Chat naturally (no "/" prefix) for AI responses

Done! You're running KAI. 🚀
