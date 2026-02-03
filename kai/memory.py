"""Conversation memory and facts storage"""

import json
import os
from datetime import datetime

class Memory:
    """Conversation and fact memory handler"""
    
    def __init__(self, history_file="data/conversation_history.json", facts_file="data/facts.json"):
        self.history = []
        self.facts = {}  # Long-term facts about user
        self.history_file = history_file
        self.facts_file = facts_file
        self._load_persistent_data()
    
    def _load_persistent_data(self):
        """Load history and facts from disk"""
        # Load conversation history
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []
        
        # Load facts
        if os.path.exists(self.facts_file):
            try:
                with open(self.facts_file, 'r') as f:
                    self.facts = json.load(f)
            except:
                self.facts = {}
    
    def _save_persistent_data(self):
        """Save history and facts to disk"""
        os.makedirs(os.path.dirname(self.history_file) or "data", exist_ok=True)
        
        # Save conversation history (keep last 100 messages)
        with open(self.history_file, 'w') as f:
            json.dump(self.history[-100:], f, indent=2)
        
        # Save facts
        with open(self.facts_file, 'w') as f:
            json.dump(self.facts, f, indent=2)
    
    def add_message(self, role, content):
        """Add a message to history and save"""
        self.history.append({
            "role": role, 
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self._save_persistent_data()
    
    def add_fact(self, key, value):
        """Store a persistent fact about the user"""
        self.facts[key] = {
            "value": value,
            "learned_at": datetime.now().isoformat()
        }
        self._save_persistent_data()
    
    def get_fact(self, key):
        """Retrieve a stored fact"""
        if key in self.facts:
            return self.facts[key]["value"]
        return None
    
    def get_facts_context(self):
        """Get facts formatted for LLM context"""
        if not self.facts:
            return ""
        
        facts_list = []
        for key, data in self.facts.items():
            facts_list.append(f"- {key}: {data['value']}")
        
        return "Facts I know about you:\n" + "\n".join(facts_list)
    
    def get_history(self, limit=10):
        """Get recent conversation history"""
        return self.history[-limit:]
    
    def clear(self):
        """Clear session conversation history (but keep facts)"""
        self.history = []
        self._save_persistent_data()
    
    def clear_all(self):
        """Clear everything including facts"""
        self.history = []
        self.facts = {}
        self._save_persistent_data()
