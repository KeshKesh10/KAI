#!/usr/bin/env python3
"""KAI - Local AI Assistant"""

from kai.llm import KaiLLM
from kai.router import CommandRouter
from kai.memory import Memory

def print_banner():
    print("=" * 60)
    print("  KAI - Your Local AI Assistant")
    print("=" * 60)
    print("\n💬 Chat naturally - I'll help with tasks, study, and more!")
    print("   Type 'exit' to quit\n")

def main():
    # Initialize
    llm = KaiLLM()
    router = CommandRouter(llm=llm)
    memory = Memory()
    
    print_banner()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Goodbye!\n")
                break
            
            # Route to appropriate handler
            if router.is_command(user_input):
                response = router.route(user_input)
            else:
                intent_response = router.route(user_input)
                
                if intent_response:
                    response = intent_response
                else:
                    # Conversational response
                    memory.add_message("user", user_input)
                    
                    messages = [{"role": "system", "content": "You are KAI, a helpful AI assistant."}]
                    
                    facts_context = memory.get_facts_context()
                    if facts_context:
                        messages.append({"role": "system", "content": facts_context})
                    
                    for msg in memory.get_history(limit=10):
                        messages.append({"role": msg["role"], "content": msg["content"]})
                    
                    response = llm.chat(messages)
                    memory.add_message("assistant", response)
            
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
