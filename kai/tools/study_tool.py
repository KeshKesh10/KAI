"""
Study tool - note taking and AI-powered quiz generation
Uses LLM for quiz creation based on saved notes
"""

import json
import os

class StudyTool:
    """Manages study notes and generates quizzes using LLM"""
    
    def __init__(self, llm=None, data_file="data/notes.json"):
        self.llm = llm
        self.data_file = data_file
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Create data file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({"topics": {}}, f)
    
    def _load_notes(self):
        """Load notes from JSON file"""
        with open(self.data_file, 'r') as f:
            data = json.load(f)
            return data.get("topics", {})
    
    def _save_notes(self, topics):
        """Save notes to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump({"topics": topics}, f, indent=2)
    
    def execute(self, args):
        """Execute study command"""
        parts = args.strip().split(None, 2)
        
        if not parts:
            return "❌ Usage: /study <save|show|list|quiz> [topic] [note]"
        
        action = parts[0].lower()
        
        if action == "save":
            if len(parts) < 3:
                return "❌ Usage: /study save <topic> <note>"
            topic = parts[1]
            note = parts[2]
            return self._save_note(topic, note)
        
        elif action == "show":
            if len(parts) < 2:
                return "❌ Usage: /study show <topic>"
            topic = parts[1]
            return self._show_notes(topic)
        
        elif action == "list":
            return self._list_topics()
        
        elif action == "quiz":
            if len(parts) < 2:
                return "❌ Usage: /study quiz <topic>"
            topic = parts[1]
            return self._generate_quiz(topic)
        
        else:
            return f"❌ Unknown action: {action}\nUse: save, show, list, quiz"
    
    def _save_note(self, topic, note):
        """Save a note under a topic"""
        topics = self._load_notes()
        
        if topic not in topics:
            topics[topic] = []
        
        topics[topic].append(note)
        self._save_notes(topics)
        
        return f"✅ Note saved under '{topic}'"
    
    def _show_notes(self, topic):
        """Show all notes for a topic"""
        topics = self._load_notes()
        
        if topic not in topics:
            return f"❌ No notes found for '{topic}'"
        
        notes = topics[topic]
        output = [f"📚 Notes for '{topic}':\n"]
        
        for i, note in enumerate(notes, 1):
            output.append(f"  {i}. {note}")
        
        return "\n".join(output)
    
    def _list_topics(self):
        """List all topics"""
        topics = self._load_notes()
        
        if not topics:
            return "📚 No study topics yet. Create one with: /study save <topic> <note>"
        
        output = ["📚 Study Topics:\n"]
        for topic, notes in topics.items():
            output.append(f"  • {topic} ({len(notes)} notes)")
        
        return "\n".join(output)
    
    def _generate_quiz(self, topic):
        """Generate quiz questions using LLM"""
        topics = self._load_notes()
        
        if topic not in topics:
            return f"❌ No notes found for '{topic}'. Save notes first."
        
        if not self.llm:
            return "❌ LLM not available. Cannot generate quiz."
        
        notes = topics[topic]
        notes_text = "\n".join(f"- {note}" for note in notes)
        
        prompt = f"""Based on these study notes about {topic}:

{notes_text}

Generate 3 quiz questions to test understanding of this material.
Format each question clearly with the question number.
Keep questions focused and relevant to the notes provided."""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt="You are a helpful study assistant creating quiz questions."
        )
        
        return f"🎯 Quiz for '{topic}':\n\n{response}"
