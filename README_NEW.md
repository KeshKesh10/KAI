# KAI - Local AI Assistant

A 100% local conversational AI assistant with task management, study tools, and calendar integration.

## Quick Start

```bash
cd /Users/rakesholanda/Downloads/KAI
python3 main.py
```

That's it! No API keys, no external servers.

## Features

- 🗣️ **Natural conversation** - No commands needed, just chat
- ✅ **Task management** - Add, complete, and track to-dos
- 📚 **Study tools** - Take notes and generate quizzes
- 📅 **Calendar** - Google Calendar integration (optional)
- 🧠 **Memory** - Remembers facts about you between sessions
- 🔒 **100% Local** - All data stays on your machine

## Usage Examples

```
You: hi
You: add finish project to my tasks
You: show my tasks
You: save a note about Python
You: what's my schedule
You: tell me a joke
```

## Pre-load Your Information

```bash
python3 load_facts.py
```

Edit `load_facts.py` to add your personal info (name, goals, etc.)

## Setup Calendar (Optional)

```bash
python3 setup_calendar.py
```

Follow [CALENDAR_SETUP.md](CALENDAR_SETUP.md) for Google Calendar connection.

## Project Structure

```
kai/
  ├── llm.py           # AI engine (with rule-based fallback)
  ├── router.py        # Intent detection & routing
  ├── memory.py        # Persistent storage
  └── tools/           # Task, study, calendar tools
data/                  # Your private data (JSON files)
main.py               # Run this to start KAI
```

## Documentation

- [CONVERSATIONAL_GUIDE.md](CONVERSATIONAL_GUIDE.md) - How to chat with KAI
- [MEMORY_GUIDE.md](MEMORY_GUIDE.md) - How KAI learns & remembers
- [CALENDAR_SETUP.md](CALENDAR_SETUP.md) - Google Calendar setup

## Privacy

- All data stored locally in `data/` folder
- No external API calls
- No telemetry
- You own your data

---

Made with ❤️ - 100% local, 100% yours
