# KAI - Kesh, Assistant/Automated, Intelligence

A 100% local LLM-powered assistant with task management and study tools. No external servers, no API keys needed.

## 🎯 What KAI Does

- **Chat naturally** with a built-in local LLM (completely offline capable)
- **Conversational memory** - KAI remembers your conversation context
- **Manage tasks** - add, complete, and track your todos
- **Study tools** - take notes and generate AI quizzes
- **Google Calendar integration** - view, add, and remove calendar events

## 🏗️ Architecture

```
KAI/
├── main.py              # Entry point & chat loop
├── kai/
│   ├── llm.py          # Local AI (transformers-based)
│   ├── router.py       # Command dispatcher
│   ├── memory.py       # Future: conversation history
│   └── tools/
│       ├── task_tool.py   # Task management
│       └── study_tool.py  # Note taking & quizzes
├── data/
│   ├── tasks.json      # Task storage
│   └── notes.json      # Study notes storage
```

## 🚀 Setup

### Prerequisites

1. **Python 3.8+**
2. **PyTorch and Transformers** (downloads on first run)
3. **Google Account** (optional, for calendar features)

### KAI Setup

```bash
# Clone and enter directory
cd /workspaces/KAI  # or your local path

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run KAI
python main.py
```

### Google Calendar Setup (Optional)

To enable calendar features:

1. **Create Google OAuth2 Credentials**:
   - Go to https://console.cloud.google.com/
   - Create a new project
   - Enable Google Calendar API
   - Create OAuth2 Desktop Application credentials
   - Download the credentials as JSON

2. **Add credentials to KAI**:
   ```bash
   mkdir -p data
   mv ~/Downloads/credentials.json data/
   ```

3. **Run KAI** - it will ask for calendar permission on first use:
   ```bash
   python main.py
   ```

4. **Authorize** in the browser window that opens

That's it! Now use `/calendar` commands.

## 💡 Usage

### Commands

```bash
# Task Management
/task add Finish homework
/task list
/task done 1
/task clear

# Study Tools
/study save Calculus Derivative is rate of change
/study show Calculus
/study list
/study quiz Calculus

# Google Calendar
/calendar add Meeting with team Thursday 2pm
/calendar list          # Show next 7 days
/calendar list 30       # Show next 30 days
/calendar remove Meeting with team

# Help
/help
```

### Natural Chat

Just type normally without `/` to chat with the LLM:

```
You: What is a derivative?
KAI: A derivative represents the rate of change...
```

## ⚠️ Important Notes

- **Fully local** - no external services needed
- **First run** will download model (~300MB for distilgpt2)
- **Works offline** - after first download, no internet needed
- **CPU-friendly** - runs on CPU; GPU optional (faster responses)
- Response quality tradeoff - local models are smaller but completely private

## 📋 Models Available

Change the model in `main.py` line 25:

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| `distilgpt2` | 300MB | ⚡⚡⚡ | ⭐⭐ |
| `gpt2` | 500MB | ⚡⚡ | ⭐⭐⭐ |
| `TinyLlama/TinyLlama-1.1B-Chat-v1.0` | 1.1GB | ⚡ | ⭐⭐⭐⭐ |
| `facebook/opt-125m` | 250MB | ⚡⚡⚡ | ⭐⭐ |

## 🎓 Design Philosophy

- **Zero dependencies** - just Python, PyTorch, and Transformers
- **Separation of concerns** - LLM, routing, and tools are isolated
- **Swappable models** - easy to change local models or providers
- **Truly local** - Full control, no cloud dependencies, complete privacy
- **No external servers** - Everything runs on your machine

## 📝 Next Steps

- [x] Add conversation memory (integrated!)
- [ ] Implement more tools
- [ ] Add configuration file
- [ ] Create test suite

## 🛠️ Troubleshooting

**"ModuleNotFoundError: torch"**
- Install: `pip install torch transformers`

**Slow responses**
- Normal on CPU - models are lighter weight than ChatGPT
- Switch to faster model: `distilgpt2` (already default)
- If you have GPU: torch will auto-detect and use it

**Model download errors**
- Ensure internet connection on first run
- Models cache to `~/.cache/huggingface/` after download
- ~5-10 minutes for first model download

**Out of memory**
- Try smaller model: `distilgpt2` or `gpt2`
- Close other applications
- Reduce max_length in kai/llm.py if needed

---

**KAI** - Kesh, Assistant/Automated, Intelligence
