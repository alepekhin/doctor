"""Comprehensive tests for Doctor - Medical Data Analysis CLI."""
import pytest
import json
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.getcwd())

import api_client
from models import ModelManager, DEFAULT_MODELS
from disclaimer import get_disclaimer, format_result, is_disclaimer_present
from analyzers import JSONAnalyzer, ImageAnalyzer, AnalysisEngine


# ==================== shared fixtures ====================


@pytest.fixture
def model_manager():
    """Create ModelManager instance."""
    return ModelManager()


@pytest.fixture
def api_client_instance():
    """Create API client instance."""
    return api_client.OllamaApiClient()


# ==================== api_client tests ====================


class TestOllamaApiClient:
    """Test Ollama API client functionality."""

    @pytest.fixture
    def client(self):
        """Create client fixture."""
        return api_client.OllamaApiClient()

    @pytest.fixture
    def mock_response(self):
        """Mock successful response."""
        return {
            "response": "Medical analysis concluded. All test results within normal limits.",
            "done": True
        }

    @pytest.fixture
    def mock_json_response(self):
        """Mock JSON response."""
        return {
            "response": '{"extracted": true}',
            "done": True
        }

    def test_generate_basic(self, client, mock_response):
        """Test basic generate call."""
        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status.return_value = None

            result = client.generate(
                prompt="Test prompt",
                model="test-model",
                system_prompt=""
            )

            assert result == mock_response["response"]
            mock_post.assert_called_once()

    def test_generate_with_system_prompt(self, client, mock_response):
        """Test generate with system prompt."""
        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status.return_value = None

            result = client.generate(
                prompt="Test",
                model="test",
                system_prompt="You are medical assistant"
            )

            call_args = mock_post.call_args
            assert "system" in call_args[1]["json"]
            assert call_args[1]["json"]["system"] == "You are medical assistant"

    def test_generate_stream(self, client):
        """Test streaming generation."""
        with patch("requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__.return_value = mock_response
            mock_response.__exit__.return_value = False
            mock_response.raise_for_status.return_value = None
            mock_response.iter_lines.return_value = iter([
                '{"response":"part1"}',
                '{"response":"part2"}',
                '{"response":"part3"}'
            ])
            mock_post.return_value = mock_response

            responses = list(client.stream_generate("test", "test-model", ""))

            assert responses == ["part1", "part2", "part3"]

    def test_generate_error_handling(self, client):
        """Test error handling when all retries are exhausted."""
        client._max_retries = 0
        with patch("requests.post") as mock_post:
            mock_post.side_effect = Exception("Connection error")

            with pytest.raises(RuntimeError):
                client.generate("test", "test-model")

            error_msg = client.get_last_error()
            assert error_msg is not None
            assert "Connection error" in error_msg

    def test_retry_logic(self, client):
        """Test that generate recovers when a retry succeeds."""
        client._max_retries = 3
        with patch("requests.post") as mock_post, patch("api_client.time.sleep"):
            call_count = {"n": 0}

            def side_effect(*args, **kwargs):
                call_count["n"] += 1
                if call_count["n"] <= 2:
                    raise Exception("Connection error")
                mock = MagicMock()
                mock.json.return_value = {"response": "success"}
                return mock

            mock_post.side_effect = side_effect

            result = client.generate("test", "test-model")

            assert result == "success"

    def test_get_context(self, client):
        """Test get_context method."""
        with patch("requests.post") as mock_post:
            mock_response = {"context": []}
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status.return_value = None

            result = client.get_context()

            assert result == []


# ==================== data flow tests ====================


class TestDataFlow:
    """Test complete data flow scenarios."""

    @pytest.fixture
    def mock_json_data(self):
        """Mock JSON test data."""
        return {
            "report_section": "Biochemistry",
            "description": "Laboratory test results",
            "results": [
                {
                    "test_name": "ALT",
                    "test_name_russian": "аланинаминотрансфераза",
                    "result": 40.45,
                    "unit": "Ед/л",
                    "reference_interval": "0 - 41"
                }
            ]
        }

    @pytest.fixture
    def mock_gemma4_response(self):
        """Mock gemma4 image to JSON response."""
        return json.dumps({
            "report_section": "Biochemistry",
            "results": [
                {
                    "test_name": "Total Bilirubin",
                    "result": 9.94,
                    "unit": "мкмоль/л",
                    "reference_interval": "3.4 - 20.5"
                }
            ]
        })

    @pytest.fixture
    def mock_omnicoder_response(self):
        """Mock omnicoder analysis response."""
        return "All biochemical markers are within normal reference limits."

    def test_json_analysis_flow(self, mock_json_data, mock_omnicoder_response):
        """Test complete JSON analysis flow."""
        client = api_client.OllamaApiClient()

        with patch.object(client, "generate") as mock_gen:
            mock_gen.return_value = mock_omnicoder_response

            result = JSONAnalyzer.analyze(mock_json_data, client)

            assert "All biochemical markers" in result

    def test_image_analysis_flow(self, mock_gemma4_response, mock_omnicoder_response):
        """Test complete image analysis flow."""
        client = api_client.OllamaApiClient()
        mock_gen = MagicMock()
        mock_gen.side_effect = [mock_gemma4_response, mock_omnicoder_response]

        with patch.object(ImageAnalyzer, "_call_gemma4", return_value=mock_gemma4_response):
            with patch.object(JSONAnalyzer, "analyze", return_value=mock_omnicoder_response) as mock_analyze:
                result = ImageAnalyzer.analyze("test.jpg", client)

                assert "All biochemical markers" in result
                mock_analyze.assert_called_once()

    def test_image_analysis_invalid_json(self, api_client_instance):
        """Test image analysis with non-JSON gemma4 output."""
        raw_text = "No clear table found in image"
        with patch.object(ImageAnalyzer, "_call_gemma4", return_value=raw_text):
            with patch.object(JSONAnalyzer, "analyze", return_value="Fallback conclusion") as mock_analyze:
                result = ImageAnalyzer.analyze("test.jpg", api_client_instance)
                assert result == "Fallback conclusion"
                mock_analyze.assert_called_once()


# ==================== model manager tests ====================


class TestModelManager:
    """Test model manager functionality."""

    def test_get_default_models(self, model_manager):
        """Test default model names."""
        models = model_manager.get_default_models()

        assert "omnicoder" in models
        assert "gemma4" in models

    def test_get_model_for_json(self, model_manager):
        """Test model selection for JSON file."""
        model = model_manager.get_model_for_input("test.json")

        assert model == DEFAULT_MODELS["omnicoder"]

    def test_get_model_for_image(self, model_manager):
        """Test model selection for image file."""
        model = model_manager.get_model_for_input("test.jpg")

        assert model == DEFAULT_MODELS["gemma4"]

    def test_get_model_for_png(self, model_manager):
        """Test model selection for PNG image."""
        model = model_manager.get_model_for_input("test.png")

        assert model == DEFAULT_MODELS["gemma4"]

    def test_get_model_for_unknown(self, model_manager):
        """Test model selection for unknown file type."""
        model = model_manager.get_model_for_input("test.txt")

        assert model == DEFAULT_MODELS["omnicoder"]

    def test_get_model_for_png_uppercase(self, model_manager):
        """Test model selection for uppercase PNG extension."""
        model = model_manager.get_model_for_input("test.PNG")

        assert model == DEFAULT_MODELS["gemma4"]


# ==================== disclaimer tests ====================


class TestDisclaimer:
    """Test disclaimer functionality."""

    def test_get_disclaimer(self):
        """Test disclaimer content."""
        disclaimer = get_disclaimer()

        assert "Medical Disclaimer" in disclaimer
        assert "AI-generated" in disclaimer

    def test_format_result(self):
        """Test result formatting."""
        analysis = "Medical analysis complete"
        result = format_result(analysis)

        assert "Medical Analysis Result:" in result
        assert "Medical Disclaimer" in result

    def test_is_disclaimer_present(self):
        """Test disclaimer detection."""
        with_result = "Medical Disclaimer: This is AI"
        without_result = "Just text"

        assert is_disclaimer_present(with_result) is True
        assert is_disclaimer_present(without_result) is False


# ==================== analysis engine tests ====================


class TestAnalysisEngine:
    """Test analysis engine."""

    def test_analyze_json_file(self, model_manager, tmp_path):
        """Test JSON file analysis."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"results": [{"result": 42, "reference_interval": "0-41"}]}')

        engine = AnalysisEngine(model_manager)

        with patch.object(engine.model_manager, "get_model_for_input", return_value="m1"):
            with patch.object(engine.model_manager, "ensure_model_loaded", return_value=True):
                with patch("api_client.OllamaApiClient") as mock_client_cls:
                    mock_client = MagicMock()
                    mock_client.generate.return_value = "Conclusion"
                    mock_client_cls.return_value = mock_client

                    result = engine.analyze_file(str(json_file))

                    assert "Conclusion" in result
                    assert "Medical Disclaimer" in result

    def test_analyze_image_file(self, model_manager, tmp_path):
        """Test image file analysis."""
        img_file = tmp_path / "test.jpg"
        img_file.write_text("fake image")

        engine = AnalysisEngine(model_manager)

        with patch.object(engine.model_manager, "get_model_for_input", return_value="gemma4:latest"):
            with patch.object(engine.model_manager, "ensure_model_loaded", return_value=True):
                with patch("analyzers.ImageAnalyzer.analyze", return_value="Image conclusion") as mock_analyze:
                    result = engine.analyze_file(str(img_file))

                    assert "Image conclusion" in result
                    assert "Medical Disclaimer" in result
                    mock_analyze.assert_called_once()

    def test_file_not_found(self, model_manager):
        """Test error when file does not exist."""
        engine = AnalysisEngine(model_manager)

        with pytest.raises(FileNotFoundError):
            engine.analyze_file("nonexistent.json")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])