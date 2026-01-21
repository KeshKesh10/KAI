#!/usr/bin/env python3
"""
KAI - Kesh, Assistant/Automated, Intelligence
Main entry point for the KAI assistant
100% Local AI - No external servers required
"""

import sys
from kai.llm import KaiLLM
from kai.router import CommandRouter
from kai.memory import Memory

def print_banner():
    """Display welcome banner"""
    print("=" * 60)
    print("  KAI - Kesh, Assistant/Automated, Intelligence")
    print("  100% Local AI Assistant (No External Servers)")
    print("=" * 60)
    print("\n💡 Type /help for commands or just chat naturally")
    print("   Type 'exit', 'quit', or 'bye' to exit\n")

def main():
    """Main conversation loop"""
    
    # Initialize Local KAI
    llm = KaiLLM(model="distilgpt2")
    
    # Check if model loaded
    if not llm.is_available():
        print("⚠️  WARNING: KAI model failed to load!")
        print("   Install required packages:")
        print("   pip install torch transformers")
        print("\n   Continuing anyway (commands will work, chat won't)...\n")
    
    # Initialize router and memory
    router = CommandRouter(llm=llm)
    memory = Memory()
    
    # Display banner
    print_banner()
    
    # Main loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for empty input
            if not user_input:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Goodbye!\n")
                break
            
            # Route command or send to LLM
            if router.is_command(user_input):
                # Execute command
                response = router.route(user_input)
            else:
                # Store user message in memory
                memory.add_message("user", user_input)
                
                # Build conversation context from memory
                messages = [
                    {"role": "system", "content": "You are KAI (Kesh, Assistant/Automated, Intelligence), a helpful and friendly AI assistant."}
                ]
                
                # Add conversation history
                for msg in memory.get_history(limit=10):
                    messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Send to LLM for conversation
                response = llm.chat(messages)
                
                # Store assistant response in memory
                memory.add_message("assistant", response)
            
            # Display response
            print(f"\nKAI: {response}\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        
        except EOFError:
            print("\n\n👋 Goodbye!\n")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
