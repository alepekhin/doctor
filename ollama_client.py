"""Ollama client for medical analysis."""
import requests
import sys

OLLAMA_URL = "http://localhost:11434/api/chat"


class OllamaClient:
    """Ollama API client."""
    
    def __init__(self, model: str = "carstenuhlig/omnicoder-2-9b:latest"):
        self.model = model
        self._check_connection()
    
    def _check_connection(self):
        """Verify Ollama is running."""
        try:
            requests.get(OLLAMA_URL, timeout=5)
        except Exception as e:
            print(f"Error: Could not connect to Ollama",
                  file=sys.stderr)
            print(f"  {e}", file=sys.stderr)
            print(f"Run 'ollama serve' to start", file=sys.stderr)
            sys.exit(1)
    
    def chat(self, messages: list[dict]) -> dict:
        """Send prompt to Ollama."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()
    
    def generate(self, prompt: str) -> str:
        """Generate response for prompt."""
        return self.chat([{"role": "user", "content": prompt}])["message"]["content"]