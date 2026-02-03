#!/usr/bin/env python3
"""
Pre-load facts into KAI
Use this to teach KAI about yourself before you start chatting
"""

import json
import os
from datetime import datetime

FACTS_FILE = "data/facts.json"

def load_facts():
    """Load existing facts"""
    if os.path.exists(FACTS_FILE):
        with open(FACTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_facts(facts):
    """Save facts to file"""
    os.makedirs(os.path.dirname(FACTS_FILE), exist_ok=True)
    with open(FACTS_FILE, 'w') as f:
        json.dump(facts, f, indent=2)

def add_fact(key, value):
    """Add a single fact"""
    facts = load_facts()
    facts[key] = {
        "value": value,
        "learned_at": datetime.now().isoformat()
    }
    save_facts(facts)
    print(f"✅ Added: {key} = {value}")

def bulk_add_facts(facts_dict):
    """Add multiple facts at once"""
    facts = load_facts()
    timestamp = datetime.now().isoformat()
    
    for key, value in facts_dict.items():
        facts[key] = {
            "value": value,
            "learned_at": timestamp
        }
    
    save_facts(facts)
    print(f"✅ Added {len(facts_dict)} facts to KAI's memory")

def list_facts():
    """Show all stored facts"""
    facts = load_facts()
    
    if not facts:
        print("📋 No facts stored yet")
        return
    
    print("\n📚 Facts KAI knows about you:")
    print("=" * 50)
    for key, data in facts.items():
        print(f"  • {key}: {data['value']}")
    print()

def clear_all_facts():
    """Clear all facts (use carefully!)"""
    confirm = input("⚠️  Clear ALL facts? This cannot be undone! (yes/no): ")
    if confirm.lower() == "yes":
        save_facts({})
        print("✅ All facts cleared")
    else:
        print("❌ Cancelled")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("KAI - Pre-load Personal Information")
    print("=" * 60 + "\n")
    
    # Example: Add your personal information here
    my_info = {
        "user_name": "Kesh",
        "full_name": "Rakesh Olanda",
        "age": "25",  # Change to your age
        "occupation": "Software Engineer",  # Change to your job
        "location": "California",  # Change to your location
        "favorite_subject": "Computer Science",
        "goals": "Build AI projects and learn machine learning",
        "hobbies": "Coding, reading, hiking",
        "programming_languages": "Python, JavaScript, Java",
        "learning_currently": "AI and Machine Learning",
    }
    
    print("Adding your personal information to KAI...\n")
    bulk_add_facts(my_info)
    
    print("\n" + "=" * 60)
    list_facts()
    print("=" * 60)
    
    print("\nNow when you chat with KAI, it will know these facts about you!")
    print("Try asking: 'What do you know about me?'\n")
