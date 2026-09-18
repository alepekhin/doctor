"""Live integration tests against a running Ollama server.

These tests require a running Ollama instance with the models configured in
config/models.json. They are skipped automatically if Ollama is unreachable.
"""
import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import OllamaApiClient
from models import ModelManager
from analyzers import AnalysisEngine

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOOD_JSON = os.path.join(PROJECT_DIR, "blood.json")
BLOOD_JPG = os.path.join(PROJECT_DIR, "blood.jpg")
OLLAMA_HOST = "http://127.0.0.1:11434"


def ollama_is_up() -> bool:
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not ollama_is_up(), reason="Ollama server is not running"
)


@pytest.fixture(scope="module")
def model_manager():
    manager = ModelManager()
    manager.load_config()
    return manager


def test_ollama_has_required_models(model_manager):
    """All required models must be present on the Ollama instance."""
    available = model_manager.get_available_models()
    models = model_manager.get_default_models()
    for name in {models["omnicoder"], models["gemma4"]}:
        assert name in available, f"Missing required model: {name}"


def test_live_json_analysis(model_manager):
    """End-to-end analysis of blood.json against live Ollama."""
    engine = AnalysisEngine(model_manager)
    result = engine.analyze_file(BLOOD_JSON)

    assert result, "Analysis returned empty result"
    assert "Medical Disclaimer" in result
    assert "ALT" in result or "АЛТ" in result


def test_live_image_analysis(model_manager):
    """End-to-end analysis of blood.jpg against live Ollama."""
    engine = AnalysisEngine(model_manager)
    result = engine.analyze_file(BLOOD_JPG)

    assert result, "Analysis returned empty result"
    assert "Medical Disclaimer" in result


def test_live_client_generate(model_manager):
    """The API client can generate text via the live server."""
    client = OllamaApiClient()
    response = client.generate(
        prompt="Say OK",
        model=model_manager.get_default_models()["omnicoder"],
        system_prompt="Be very concise. Reply with just OK.",
    )
    assert response.strip(), "Empty response from Ollama"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])