#!/usr/bin/env python3
"""
KAI - Simple conversational loop
Type input → KAI responds → repeat
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat(user_input):
    """Send user input to OpenAI and get response"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are KAI (Kesh, Assistant/Automated, Intelligence), a helpful AI assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

def main():
    """Main conversation loop"""
    print("=" * 50)
    print("KAI - Kesh, Assistant/Automated, Intelligence")
    print("Type 'exit' or 'quit' to end the conversation")
    print("=" * 50)
    print()
    
    while True:
        # Get user input
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye!")
            break
        
        # Check for exit commands
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\nGoodbye!")
            break
        
        # Skip empty input
        if not user_input:
            continue
        
        # Get and print KAI's response
        try:
            response = chat(user_input)
            print(f"\nKAI: {response}\n")
        except Exception as e:
            print(f"\nError: {e}\n")
            print("Make sure your OPENAI_API_KEY is set correctly in .env\n")

if __name__ == "__main__":
    main()
