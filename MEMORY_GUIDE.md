# KAI Memory & Learning System

## Yes, KAI Learns! 🧠

KAI has **persistent memory** that saves between sessions:

### What KAI Remembers

1. **Facts about you** → `data/facts.json`
   - Your name, age, occupation, goals, hobbies, etc.
   - Anything you explicitly tell KAI
   - Added manually or learned from conversations

2. **Conversation history** → `data/conversation_history.json`
   - Last 100 messages
   - Full context of what you discussed
   - Used to maintain conversation flow

3. **Tasks** → `data/tasks.json`
   - Your to-do list
   - Completed/incomplete status
   - Created dates

4. **Study notes** → `data/notes.json`
   - Notes organized by topic
   - Used for generating quizzes

## Pre-Loading Information into KAI

### Method 1: Use the Script (Easiest)

```bash
# Edit load_facts.py with your information
nano load_facts.py  # or any editor

# Run it
python3 load_facts.py
```

Edit the `my_info` dictionary in [load_facts.py](load_facts.py):

```python
my_info = {
    "user_name": "Your Name",
    "age": "Your Age",
    "occupation": "Your Job",
    "location": "Your City",
    "goals": "What you want to achieve",
    "hobbies": "What you enjoy",
    # Add anything you want!
}
```

### Method 2: Tell KAI Directly

Just chat with KAI and tell it:

```
You: My name is Kesh
You: I'm learning machine learning
You: I love coding in Python
You: Remember my birthday is March 15th
```

KAI will automatically store important facts from conversations!

### Method 3: Edit JSON Directly

Edit `data/facts.json`:

```json
{
  "favorite_food": {
    "value": "Pizza",
    "learned_at": "2026-02-03T15:00:00"
  },
  "pet_name": {
    "value": "Max",
    "learned_at": "2026-02-03T15:00:00"
  }
}
```

## How KAI Uses Facts

When you chat, KAI sees your stored facts:

```
You: What do you know about me?
KAI: [Shows facts from data/facts.json]

You: Help me with my goals
KAI: [Refers to your stored goals]

You: What am I learning?
KAI: [Knows from facts you're learning ML]
```

## View Your Stored Data

```bash
# See what KAI knows about you
cat data/facts.json

# See conversation history
cat data/conversation_history.json

# See your tasks
cat data/tasks.json

# See study notes
cat data/notes.json
```

## Learning Over Time

KAI learns by:

1. **Extracting facts** from conversations
2. **Storing them permanently** in JSON files
3. **Using them in future conversations** for context
4. **Never forgetting** unless you clear the files

### What Gets Remembered

✅ Your name, preferences, goals
✅ Things you explicitly share
✅ Past conversations (last 100 messages)
✅ Tasks and notes you create

### What Doesn't Get Remembered

❌ Things outside KAI's scope
❌ Conversations older than 100 messages
❌ Data if you delete the JSON files

## Privacy

- **100% Local** - Everything stored on your machine
- **No cloud sync** - Never leaves your computer
- **Full control** - You can view/edit/delete all data
- **Portable** - Copy the `data/` folder to backup

## Advanced: Managing Facts

### List all facts
```python
python3 load_facts.py
```

### Add a single fact
```python
from load_facts import add_fact
add_fact("favorite_color", "Blue")
```

### Clear everything (careful!)
```bash
rm -rf data/
# KAI will recreate empty files on next run
```

## Tips for Better Learning

1. **Be explicit** - "My name is X" is better than "I'm X"
2. **Pre-load facts** - Use load_facts.py before first use
3. **Update regularly** - Run load_facts.py when things change
4. **Ask KAI** - "What do you know about me?" to verify

---

**Your data is yours!** All files are in `data/` - back them up, edit them, or delete them anytime.
