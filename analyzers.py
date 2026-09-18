"""Data analysis module for medical data."""
from typing import Dict, Any
import json
import os
import re


class JSONAnalyzer:
    """Analyze JSON medical data with omnicoder model."""
    
    @staticmethod
    def analyze(data: Dict[str, Any], client) -> str:
        """Analyze JSON data and return medical conclusion."""
        if not data.get("results"):
            return "No test results found in the data."
        
        prompt = json.dumps(data, ensure_ascii=False)
        
        model = "carstenuhlig/omnicoder-2-9b:latest"
        response = client.generate(
            prompt=prompt,
            model=model,
            system_prompt="Analyze these medical lab test results and provide a concise clinical conclusion. Summarize normal and abnormal findings."
        )
        
        return response


class ImageAnalyzer:
    """Analyze medical images and convert to insights."""
    
    @staticmethod
    def _call_gemma4(image_path: str, client) -> str:
        """Call gemma4 model to extract JSON from image."""
        model = "gemma4:latest"

        prompt = (
            "Extract table data from this medical image and return it as valid JSON. "
            "Format: {\"report_section\": \"<section>\", \"results\": [{\"test_name\": \"...\", "
            "\"result\": <number>, \"unit\": \"...\", \"reference_interval\": \"low - high\"}]}. "
            "Output only the JSON, no other text."
        )

        response = client.generate(
            prompt=prompt,
            model=model,
            system_prompt="You are a medical data extraction tool. Return only JSON data.",
            images=[image_path]
        )

        return response

    @staticmethod
    def _extract_json(text: str) -> dict:
        """Extract a JSON dict from model output, handling markdown wrappers."""
        text = text.strip()
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        if text.startswith("{") and text.endswith("}"):
            return json.loads(text)
        raise json.JSONDecodeError("No JSON object found", text, 0)

    @staticmethod
    def analyze(image_path: str, client) -> str:
        """Analyze image file and return medical conclusion."""
        gemma4_response = ImageAnalyzer._call_gemma4(image_path, client)

        if not gemma4_response:
            return "Failed to process image - unable to extract data."

        try:
            data = ImageAnalyzer._extract_json(gemma4_response)
        except (json.JSONDecodeError, ValueError):
            data = {"description": "Medical image data",
                    "text_output": gemma4_response}

        conclusion = JSONAnalyzer.analyze(data, client)

        return conclusion


class AnalysisEngine:
    """Unified analysis engine that routes to appropriate analyzer."""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
    
    def analyze_file(self, filepath: str) -> str:
        """Analyze file based on type."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        model = self.model_manager.get_model_for_input(filepath)
        
        if not self.model_manager.ensure_model_loaded(model):
            pass
        
        from api_client import OllamaApiClient
        client = OllamaApiClient()
        
        if filepath.endswith(".json"):
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
            conclusion = JSONAnalyzer.analyze(data, client)
        else:
            conclusion = ImageAnalyzer.analyze(filepath, client)

        from disclaimer import get_disclaimer
        return conclusion + get_disclaimer()


__all__ = ["JSONAnalyzer", "ImageAnalyzer", "AnalysisEngine"]
