"""Command router - Natural language to tool routing"""

from kai.tools.task_tool import TaskTool
from kai.tools.study_tool import StudyTool
from kai.tools.calendar_tool import CalendarTool

class CommandRouter:
    
    def __init__(self, llm=None):
        self.task_tool = TaskTool()
        self.study_tool = StudyTool(llm)
        self.calendar_tool = CalendarTool()
        self.llm = llm
        self.commands = {
            "/task": self.task_tool,
            "/study": self.study_tool,
            "/calendar": self.calendar_tool,
            "/help": self._show_help
        }
        
        self.task_keywords = ["task", "todo", "do", "add", "complete", "done", "check", "mark", "finish"]
        self.study_keywords = ["study", "note", "quiz", "learn", "save", "learning", "remember"]
        self.calendar_keywords = ["calendar", "event", "meeting", "schedule", "remind", "when", "appointment", 
                                  "my schedule", "what's my schedule", "what is my schedule", "upcoming"]
        self.help_keywords = ["help", "what can you do", "commands", "how do i", "capabilities", "list commands"]
        
        self.conversational_only = ["hi", "hello", "hey", "how are you", "who are you", "what are you", 
                                    "yes", "no", "yeah", "nope", "thank", "thanks", "weather", "joke", 
                                    "my name", "i'm", "i am", "food", "what time"]
    
    def is_command(self, text):
        """Check if input starts with a command"""
        return text.strip().startswith("/")
    
    def detect_intent(self, text):
        """
        Detect user intent from natural language
        Can use LLM for smarter detection if available
        
        Args:
            text: User input text
            
        Returns:
            Tuple of (intent_type, action, params) or None
        """
        text_lower = text.lower()
        
        # Quick keyword check first (faster)
        quick_intent = self._quick_intent_check(text_lower)
        if quick_intent:
            return quick_intent
        
        # If LLM available and no quick match, use smarter detection
        if self.llm and self.llm.is_available():
            return self._llm_intent_detection(text)
        
        return None
    
    def _quick_intent_check(self, text_lower):
        """Fast keyword-based intent detection"""
        # First check if it's purely conversational
        if any(phrase in text_lower for phrase in self.conversational_only):
            return None  # Let LLM handle it conversationally
        
        # Help detection
        if any(keyword in text_lower for keyword in self.help_keywords):
            return ("help", None, None)
        
        # Task detection - but be smart about it
        if any(keyword in text_lower for keyword in self.task_keywords):
            # Make sure it's actually about tasks, not just contains "do"
            if len(text_lower.split()) < 3 and text_lower in ["do", "done"]:
                return None  # Too vague
            return self._parse_task_intent(text_lower)
        
        # Study detection
        if any(keyword in text_lower for keyword in self.study_keywords):
            return self._parse_study_intent(text_lower)
        
        # Calendar detection
        if any(keyword in text_lower for keyword in self.calendar_keywords):
            return self._parse_calendar_intent(text_lower)
        
        return None
    
    def _llm_intent_detection(self, text):
        """Use LLM to intelligently detect intent"""
        intent_prompt = f"""Given this user message, what is their primary intent?
Message: "{text}"

Respond with ONLY one of: TASK, STUDY, CALENDAR, HELP, or CHAT

Then on next line add the action if applicable (add, list, done, save, quiz, show, schedule, remove, etc)
Then on next line add any parameters"""
        
        response = self.llm.generate(intent_prompt, max_length=50)
        lines = response.strip().split('\n')
        
        if not lines:
            return None
        
        intent_type = lines[0].strip().lower()
        action = lines[1].strip().lower() if len(lines) > 1 else ""
        params = lines[2].strip() if len(lines) > 2 else ""
        
        if intent_type in ["task", "study", "calendar", "help"]:
            return (intent_type, action, params)
        
        return None
    
    def _parse_task_intent(self, text):
        """Parse natural language task intent"""
        text_lower = text.lower()
        
        if any(w in text_lower for w in ["list", "show", "my tasks", "all tasks"]):
            return ("task", "list", "")
        elif any(w in text_lower for w in ["clear", "delete all", "clear all"]):
            return ("task", "clear", "")
        elif any(w in text_lower for w in ["complete", "done", "mark", "finish"]):
            # Try to extract task number
            import re
            match = re.search(r'\b(\d+)\b', text)
            task_id = match.group(1) if match else ""
            return ("task", "done", task_id)
        elif any(w in text_lower for w in ["add", "create", "new task"]):
            # Extract task description
            import re
            # Remove common prefixes
            desc = re.sub(r"^(add|create|new task|i need to|please add|can you add)\s*", "", text, flags=re.IGNORECASE).strip()
            return ("task", "add", desc)
        elif any(w in text_lower for w in ["do", "need to", "remember"]):
            # Simple task addition
            return ("task", "add", text)
        
        return ("task", "list", "")  # Default to list
    
    def _parse_study_intent(self, text):
        """Parse natural language study intent"""
        text_lower = text.lower()
        
        if any(w in text_lower for w in ["list", "show all", "my topics"]):
            return ("study", "list", "")
        elif any(w in text_lower for w in ["quiz", "test", "question"]):
            import re
            match = re.search(r'about\s+(\w+)|on\s+(\w+)|for\s+(\w+)', text)
            topic = ""
            if match:
                topic = match.group(1) or match.group(2) or match.group(3)
            return ("study", "quiz", topic)
        elif any(w in text_lower for w in ["save", "note", "remember"]):
            import re
            # Try to extract: "save note about [topic]" or "note about [topic]: [content]"
            match = re.search(r'(?:about|on|for)\s+(\w+)[:\s]+(.+)', text)
            if match:
                topic = match.group(1)
                note = match.group(2)
                return ("study", "save", f"{topic} {note}")
            return ("study", "list", "")
        elif any(w in text_lower for w in ["show", "recall", "get notes"]):
            import re
            match = re.search(r'(?:about|on|for)\s+(\w+)', text)
            topic = match.group(1) if match else ""
            return ("study", "show", topic)
        
        return ("study", "list", "")
    
    def _parse_calendar_intent(self, text):
        """Parse natural language calendar intent"""
        text_lower = text.lower()
        
        if any(w in text_lower for w in ["add", "schedule", "create event", "book"]):
            return ("calendar", "add", text)
        elif any(w in text_lower for w in ["list", "show", "upcoming", "what's", "my schedule", "schedule", "events"]):
            return ("calendar", "list", "")
        elif any(w in text_lower for w in ["remove", "delete", "cancel"]):
            return ("calendar", "remove", text)
        
        return ("calendar", "list", "")
    
    def route(self, command_text):
        """
        Parse and execute command or natural language
        
        Args:
            command_text: Full command string or natural language
            
        Returns:
            Command output as string
        """
        # Check if explicit command
        if self.is_command(command_text):
            return self._route_command(command_text)
        
        # Try natural language intent detection
        intent = self.detect_intent(command_text)
        if intent:
            intent_type, action, params = intent
            return self._execute_intent(intent_type, action, params)
        
        # If no intent detected, return None so LLM handles it
        return None
    
    def _route_command(self, command_text):
        """Handle explicit /command syntax"""
        parts = command_text.strip().split(None, 1)
        
        if not parts:
            return self._show_help()
        
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command in self.commands:
            tool = self.commands[command]
            if callable(tool):
                return tool()
            else:
                return tool.execute(args)
        else:
            return f"❌ Unknown command: {command}\nType /help for available commands"
    
    def _execute_intent(self, intent_type, action, params):
        """Execute detected intent"""
        if intent_type == "help":
            return self._show_help()
        elif intent_type == "task":
            return self.task_tool.execute(f"{action} {params}".strip())
        elif intent_type == "study":
            return self.study_tool.execute(f"{action} {params}".strip())
        elif intent_type == "calendar":
            return self.calendar_tool.execute(f"{action} {params}".strip())
        
        return None
    
    def _show_help(self):
        """Show available commands and natural language examples"""
        return """
🎯 What I Can Help You With:

📝 Task Management - Just say things like:
  • "Add make dinner to my tasks"
  • "Show my to-do list"
  • "I'm done with task 3"
  • "Clear all my tasks"

📚 Study Tools - Try natural phrases like:
  • "Save a note about Python"
  • "Show my biology notes"
  • "Give me a quiz on history"
  • "What topics have I studied?"

📅 Calendar - Speak naturally:
  • "Schedule a meeting on Friday"
  • "What's my calendar look like?"
  • "Remove that dentist appointment"
  • "Add a reminder for tomorrow"

💬 Everything Else:
  • Just chat with me naturally! I can discuss anything.
  • Type 'exit', 'quit', or 'bye' to leave

⚡ Or use classic commands with /:
  /task add <description>     /study save <topic> <note>     /calendar list
"""
