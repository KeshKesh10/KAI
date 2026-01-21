"""
Task management tool
Handles task CRUD operations with JSON storage
"""

import json
import os
from datetime import datetime

class TaskTool:
    """Manages tasks with local JSON storage"""
    
    def __init__(self, data_file="data/tasks.json"):
        self.data_file = data_file
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Create data file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({"tasks": []}, f)
    
    def _load_tasks(self):
        """Load tasks from JSON file"""
        with open(self.data_file, 'r') as f:
            data = json.load(f)
            return data.get("tasks", [])
    
    def _save_tasks(self, tasks):
        """Save tasks to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump({"tasks": tasks}, f, indent=2)
    
    def execute(self, args):
        """Execute task command"""
        parts = args.strip().split(None, 1)
        
        if not parts:
            return "❌ Usage: /task <add|list|done|clear> [args]"
        
        action = parts[0].lower()
        params = parts[1] if len(parts) > 1 else ""
        
        if action == "add":
            return self._add_task(params)
        elif action == "list":
            return self._list_tasks()
        elif action == "done":
            return self._complete_task(params)
        elif action == "clear":
            return self._clear_tasks()
        else:
            return f"❌ Unknown action: {action}\nUse: add, list, done, clear"
    
    def _add_task(self, description):
        """Add a new task"""
        if not description:
            return "❌ Task description cannot be empty"
        
        tasks = self._load_tasks()
        task = {
            "id": len(tasks) + 1,
            "description": description,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        tasks.append(task)
        self._save_tasks(tasks)
        
        return f"✅ Task added: {description}"
    
    def _list_tasks(self):
        """List all tasks"""
        tasks = self._load_tasks()
        
        if not tasks:
            return "📋 No tasks yet. Add one with: /task add <description>"
        
        output = ["📋 Your Tasks:\n"]
        for task in tasks:
            status = "✓" if task["completed"] else "○"
            output.append(f"  {status} {task['id']}. {task['description']}")
        
        return "\n".join(output)
    
    def _complete_task(self, task_id_str):
        """Mark a task as complete"""
        if not task_id_str:
            return "❌ Specify task number: /task done <number>"
        
        try:
            task_id = int(task_id_str)
        except ValueError:
            return "❌ Task number must be an integer"
        
        tasks = self._load_tasks()
        
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self._save_tasks(tasks)
                return f"✅ Task completed: {task['description']}"
        
        return f"❌ Task {task_id} not found"
    
    def _clear_tasks(self):
        """Clear all tasks"""
        self._save_tasks([])
        return "✅ All tasks cleared"
