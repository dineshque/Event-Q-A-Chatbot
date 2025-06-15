"""Interface for local LLM using Ollama."""

import requests
import json
from typing import List, Dict

class OllamaLLM:
    """Interface for Ollama local LLM."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        self.base_url = base_url
        self.model = model
        self.generate_url = f"{base_url}/api/generate"
    
    def is_available(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_response(self, prompt: str, context_chunks: List[Dict[str, any]]) -> str:
        """Generate response using retrieved context."""
        # Prepare context from retrieved chunks
        context = "\n\n".join([chunk['text'] for chunk in context_chunks])
        
        # Create prompt with context
        full_prompt = self._create_prompt(prompt, context)
        
        # Prepare request data
        # data = {
        #     "model": self.model,
        #     "prompt": full_prompt,
        #     "stream": False,
        #     "options": {
        #         "temperature": 0.7,
        #         "top_p": 0.9,
        #         "max_tokens": 500
        #     }
        # }
        data = {
        "model": self.model,
        "prompt": full_prompt,
        "stream": True,  # Enable streaming
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 500
        }
    }
        
        try:
            response = requests.post(
                self.generate_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                timeout=300,  # Longer timeout for streaming
                stream=True
            )
            
            if response.status_code == 200:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        if 'response' in chunk:
                            full_response += chunk['response']
                        if chunk.get('done', False):
                            break
                return full_response
        # ... error handling ...
        
        except Exception as e:
            return f"Error connecting to LLM: {str(e)}"
    
    def _create_prompt(self, question: str, context: str) -> str:
        """Create a well-structured prompt for the LLM."""
        prompt = f"""You are an AI assistant helping users with questions about an event. Use only the provided context to answer questions accurately and concisely.

Context Information:
{context}

Question: {question}

Instructions:
- Answer based only on the provided context
- If the context doesn't contain enough information, say so
- Be specific and cite relevant details from the context
- Keep responses clear and concise

Answer:"""
        
        return prompt
