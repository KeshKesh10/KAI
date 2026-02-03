"""Local LLM with fallback to rule-based responses"""

try:
    import torch
    from transformers import pipeline
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("⚠️  torch/transformers not available - using rule-based responses")

class KaiLLM:
    
    def __init__(self, model="distilgpt2"):
        self.model_name = model
        self.available = False
        
        if TORCH_AVAILABLE:
            try:
                import torch
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
                
                print(f"🤖 Loading model: {model}...")
                self.generator = pipeline(
                    "text-generation",
                    model=model,
                    device=0 if self.device == "cuda" else -1,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                )
                self.available = True
                print("✅ Ready!")
            except Exception as e:
                print(f"⚠️  Using rule-based mode: {e}")
                self.generator = None
        else:
            print("ℹ️  Using rule-based conversational mode")
            self.generator = None
    
    def generate(self, prompt, system_prompt=None, max_length=150):
        """
        Generate text response
        
        Args:
            prompt: User's input text
            system_prompt: Optional system context
            max_length: Max tokens to generate
            
        Returns:
            Generated text response
        """
        if not self.available:
            # Use simple rule-based responses
            return self._generate_rule_based(prompt)
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        
        try:
            result = self.generator(
                full_prompt,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.95,
                do_sample=True
            )
            
            response = result[0]["generated_text"]
            # Remove the prompt from response
            if full_prompt in response:
                response = response[len(full_prompt):].strip()
            
            return response.strip()
        
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"
    
    def _generate_rule_based(self, prompt):
        """Conversational rule-based responses when LLM not available"""
        prompt_lower = prompt.lower().strip()
        
        # Greetings
        if prompt_lower in ['hi', 'hello', 'hey', 'hola', 'greetings', 'yo']:
            return "Hey there! 👋 I'm KAI, your personal assistant. I can help you manage tasks, take study notes, or just chat. What would you like to do?"
        
        # How are you / What are you
        if any(phrase in prompt_lower for phrase in ['how are you', 'how r u', 'how are u']):
            return "I'm doing great, thanks for asking! 😊 I'm here and ready to help. What's on your mind?"
        
        if any(phrase in prompt_lower for phrase in ['what are you', 'who are you', 'what r u', 'who r u']):
            return "I'm KAI - your personal AI assistant! I help with tasks, studying, scheduling, and general conversation. I run 100% locally on your machine. Want to know what I can do?"
        
        # Name questions
        if any(phrase in prompt_lower for phrase in ['my name is', "i'm ", "i am "]):
            # Extract name
            import re
            match = re.search(r'(?:my name is|i\'m|i am)\s+(\w+)', prompt_lower)
            if match:
                name = match.group(1).capitalize()
                return f"Nice to meet you, {name}! 😊 I'll remember that. How can I help you today?"
            return "Nice to meet you! How can I help you today?"
        
        if any(phrase in prompt_lower for phrase in ['what is my name', 'my name', 'who am i', 'do you know me', 
                                                       'what do you know about me', 'tell me about me']):
            return "I store facts about you in my memory! To see what I know, check data/facts.json or use the load_facts.py script to see and add more information about yourself."
        
        # Capability questions
        if any(phrase in prompt_lower for phrase in ['what can you do', 'capabilities', 'features', 'help me']):
            return "I can help you with:\n• Managing tasks and to-dos\n• Taking study notes and quizzes\n• Scheduling (with Google Calendar)\n• General conversation\n\nJust talk naturally! Say things like 'add a task' or 'show my tasks'. What would you like help with?"
        
        # Yes/No responses
        if prompt_lower in ['yes', 'yeah', 'yep', 'sure', 'ok', 'okay', 'y']:
            return "Great! What would you like to do?"
        
        if prompt_lower in ['no', 'nope', 'nah', 'n']:
            return "No worries! Let me know if you need anything else."
        
        # Thank you
        if any(phrase in prompt_lower for phrase in ['thank', 'thanks', 'thx']):
            return "You're welcome! Happy to help! 😊"
        
        # Math
        if "2+2" in prompt_lower or "2 + 2" in prompt_lower:
            return "2 + 2 = 4! 🧮 Need help with other calculations?"
        
        # Jokes
        if "joke" in prompt_lower or "funny" in prompt_lower:
            jokes = [
                "Why did the AI go to school? To improve its learning model! 😄",
                "What do you call an AI that tells jokes? A funny bot! 🤖",
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡"
            ]
            import random
            return random.choice(jokes)
        
        # Weather
        if "weather" in prompt_lower:
            return "I can't check live weather data, but I hope it's nice where you are! ☀️ Want me to help with anything else?"
        
        # Food
        if "food" in prompt_lower or "eat" in prompt_lower:
            return "Food is fuel for the body and soul! 🍕 Are you looking for meal planning or recipe ideas? I can help you organize that!"
        
        # Time/Date
        if any(phrase in prompt_lower for phrase in ['what time', 'what date', 'today']):
            from datetime import datetime
            now = datetime.now()
            return f"It's {now.strftime('%A, %B %d, %Y at %I:%M %p')}. ⏰"
        
        # Empty or short inputs
        if not prompt_lower or len(prompt_lower) < 2:
            return "I'm listening! What would you like to talk about?"
        
        # Random terminal commands
        if any(cmd in prompt_lower for cmd in ['ls', 'cd', 'pwd', 'mkdir']):
            return "I see you're thinking about terminal commands! I'm designed for natural conversation. Try asking me to add tasks or notes instead! 😊"
        
        # General conversation - more contextual
        if '?' in prompt:
            return "That's a great question! I'm running in basic mode without the full AI model, so my responses are limited. I'm best at managing tasks, notes, and schedules. Want to try one of those?"
        
        # Default friendly responses
        responses = [
            "Interesting! I'm running in basic conversational mode. For better responses, you can install torch. Meanwhile, I'm great at tasks and notes - want to try?",
            "I hear you! I can help best with tasks, studying, and organization. What would you like to work on?",
            "Got it! While I'm limited without the full AI model, I can still help you stay organized. Need to add a task or note?",
            "I see! Want to put that into a task or note so you remember it later?",
        ]
        
        import random
        return random.choice(responses)
    
    def chat(self, messages):
        """
        Chat-style interface with better context handling
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            
        Returns:
            Generated text response
        """
        system_prompt = None
        conversation_history = ""
        user_prompt = ""
        
        # Extract system prompt and build conversation context
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            elif msg["role"] == "user":
                user_prompt = msg["content"]
            else:
                # Add to conversation history
                conversation_history += f"{msg['role'].capitalize()}: {msg['content']}\n"
        
        # Build better prompt that includes conversation flow
        if conversation_history:
            full_prompt = f"{system_prompt}\n\n{conversation_history}User: {user_prompt}\nAssistant:"
        else:
            full_prompt = f"{system_prompt}\n\nUser: {user_prompt}\nAssistant:"
        
        return self.generate(user_prompt, system_prompt, max_length=200)
    
    def is_available(self):
        """Check if model loaded successfully"""
        return self.available
