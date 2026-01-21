"""
Memory module - for future conversation history tracking
Not implemented yet (Phase 1 focuses on stateless interaction)
"""

class Memory:
    """Conversation memory handler"""
    
    def __init__(self):
        self.history = []
    
    def add_message(self, role, content):
        """Add a message to history"""
        self.history.append({"role": role, "content": content})
    
    def get_history(self, limit=10):
        """Get recent conversation history"""
        return self.history[-limit:]
    
    def clear(self):
        """Clear conversation history"""
        self.history = []
