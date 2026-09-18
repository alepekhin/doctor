import requests
import json
import os
from typing import Dict, Optional


OMNICODER = "carstenuhlig/omnicoder-2-9b:latest"
GEMMA4 = "gemma4:latest"
DEFAULT_MODELS = {
    "omnicoder": OMNICODER,
    "gemma4": GEMMA4
}


class ModelManager:
    """Manage model routing and detection for Ollama."""
    
    def __init__(self):
        self._models: Dict[str, str] = {}
        self._config_path = "config/models.json"
        self._loaded = False
    
    def load_config(self) -> None:
        """Load model configuration from file."""
        if os.path.exists(self._config_path):
            try:
                with open(self._config_path, 'r') as f:
                    data = json.load(f)
                    self._models.update(data.get("models", {}))
                    self._loaded = True
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")
                self._loaded = False
    
    def check_env_override(self) -> None:
        """Check for environment variable overrides."""
        env_models = os.environ.get("OLLAMA_MODELS_OVERRIDE")
        if env_models:
            try:
                with open(os.path.join(os.getcwd(), env_models), 'r') as f:
                    data = json.load(f)
                    self._models.update(data.get("models", {}))
                    self._loaded = True
            except:
                self._loaded = False
    
    def get_available_models(self) -> list:
        """Query Ollama for available models."""
        if not self._loaded:
            self.load_config()
            self.check_env_override()
        
        url = "http://127.0.0.1:11434/api/tags"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            models = response.json()
            return [m.get("name") for m in models.get("models", [])]
        except:
            return []
    
    def get_model_for_input(self, filepath: str) -> str:
        """Get appropriate model for input file type."""
        # JSON file → omnicoder
        if filepath.endswith(".json"):
            return self._models.get("omnicoder", OMNICODER)
        
        # Image file → gemma4
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"]
        if any(filepath.lower().endswith(ext) for ext in image_extensions):
            return self._models.get("gemma4", GEMMA4)
        
        # Default to omnicoder for unknown types
        return self._models.get("omnicoder", OMNICODER)
    
    def ensure_model_loaded(self, model_name: str) -> bool:
        """Ensure model is loaded in Ollama."""
        url = f"http://127.0.0.1:11434/api/generate"
        payload = {"model": model_name, "prompt": "ping", "stream": False}
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Could not load model {model_name}: {e}")
            return False
    
    def list_models(self) -> None:
        """Print available models."""
        available = self.get_available_models()
        print(f"Available Ollama models:")
        for model in available:
            print(f"  - {model}")
        
        if not available:
            print("  (Checking Ollama models...)\n  This may take a moment.")
    
    def get_default_models(self) -> dict:
        """Get default model names."""
        return DEFAULT_MODELS