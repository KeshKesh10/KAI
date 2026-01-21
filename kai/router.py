"""
Command router - parses and dispatches commands to appropriate tools
No LLM calls here - pure routing logic
"""

from kai.tools.task_tool import TaskTool
from kai.tools.study_tool import StudyTool
from kai.tools.calendar_tool import CalendarTool

class CommandRouter:
    """Routes commands to appropriate tools"""
    
    def __init__(self, llm=None):
        self.task_tool = TaskTool()
        self.study_tool = StudyTool(llm)
        self.calendar_tool = CalendarTool()
        self.commands = {
            "/task": self.task_tool,
            "/study": self.study_tool,
            "/calendar": self.calendar_tool,
            "/help": self._show_help
        }
    
    def is_command(self, text):
        """Check if input starts with a command"""
        return text.strip().startswith("/")
    
    def route(self, command_text):
        """
        Parse and execute command
        
        Args:
            command_text: Full command string (e.g., "/task add Do homework")
            
        Returns:
            Command output as string
        """
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
    
    def _show_help(self):
        """Show available commands"""
        return """
📋 KAI Commands:

Task Management:
  /task add <description>    - Add a new task
  /task list                 - Show all tasks
  /task done <number>        - Mark task as complete
  /task clear                - Clear all tasks

Study Tools:
  /study save <topic> <note> - Save study note
  /study show <topic>        - Show notes for topic
  /study list                - List all topics
  /study quiz <topic>        - Get AI-generated quiz

Calendar (Google Calendar):
  /calendar add <title> [description] - Add event to calendar
  /calendar list [days]               - Show upcoming events (default: 7 days)
  /calendar remove <title>            - Delete event from calendar

General:
  /help                      - Show this help message
  exit, quit, bye            - Exit KAI

💡 Anything without / will be sent to the LLM for conversation.

📅 Calendar Setup:
   1. Create Google OAuth2 credentials at: https://console.cloud.google.com/
   2. Download credentials.json and place in data/ folder
   3. Run KAI - it will ask for calendar permission
   4. Grant access and you're ready to use /calendar commands!
"""
