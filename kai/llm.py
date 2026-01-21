"""
LLM wrapper for local AI integration (using transformers)
KAI - local AI that runs without external servers
"""

import torch
from transformers import pipeline

class KaiLLM:
    """Local LLM client using transformers"""
    
    def __init__(self, model="distilgpt2"):
        """
        Initialize local LLM
        
        Args:
            model: Hugging Face model ID (default: distilgpt2 - fast, lightweight)
                   Other options:
                   - "TinyLlama/TinyLlama-1.1B-Chat-v1.0" (better responses, ~1.1B)
                   - "gpt2" (classic, ~124M)
                   - "facebook/opt-125m" (compact, ~125M)
        """
        self.model_name = model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        try:
            print(f"🤖 Loading KAI model: {model} (device: {self.device})...")
            self.generator = pipeline(
                "text-generation",
                model=model,
                device=0 if self.device == "cuda" else -1,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            self.available = True
            print(f"✅ KAI ready!")
        except Exception as e:
            print(f"⚠️  Warning: Could not load model: {e}")
            self.available = False
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
            return "❌ Error: KAI model not loaded. Install transformers: pip install transformers torch"
        
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
    
    def chat(self, messages):
        """
        Chat-style interface
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            
        Returns:
            Generated text response
        """
        system_prompt = None
        user_prompt = ""
        
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            elif msg["role"] == "user":
                user_prompt = msg["content"]
        
        return self.generate(user_prompt, system_prompt)
    
    def is_available(self):
        """Check if model loaded successfully"""
        return self.available
