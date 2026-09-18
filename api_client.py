import requests
import json
import time
import base64
import os
from typing import Optional, Generator, List, Union


class OllamaApiClient:
    """Ollama API client for medical data analysis."""

    def __init__(self, host: str = "http://127.0.0.1:11434", timeout: Optional[int] = None):
        self.host = host
        self.timeout = timeout if timeout is not None else self._default_timeout()
        self._last_error = None
        self._retry_count = 0
        self._max_retries = 3

    @staticmethod
    def _default_timeout() -> int:
        """Read timeout_seconds from config/models.json, default 300."""
        config_path = os.path.join(os.getcwd(), "config", "models.json")
        try:
            with open(config_path, "r") as f:
                data = json.load(f)
                return int(data.get("timeout_seconds", 300))
        except Exception:
            return 300

    def _url(self) -> str:
        return f"{self.host}/api/generate"

    def _base_payload(self, prompt: str, model: str, stream: bool, system_prompt: str) -> dict:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {"temperature": 0.7, "top_p": 0.9}
        }
        if system_prompt:
            payload["system"] = system_prompt
        return payload

    @staticmethod
    def _encode_images(images: Optional[List[str]]) -> Optional[List[str]]:
        """Encode any local file paths in the images list to base64 strings."""
        if not images:
            return None
        encoded = []
        for img in images:
            if os.path.exists(img):
                with open(img, "rb") as f:
                    encoded.append(base64.b64encode(f.read()).decode())
            else:
                encoded.append(img)
        return encoded

    def _handle_error(self, error: Exception) -> bool:
        """Record an error and decide whether to retry.

        Returns True if a retry should be attempted, False otherwise.
        """
        self._retry_count += 1
        self._last_error = error

        if self._retry_count <= self._max_retries:
            print(f"Retrying... ({self._retry_count}/{self._max_retries})")
            time.sleep(0.5 * self._retry_count)
            return True

        self._last_error = error
        return False

    def generate(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "",
        context: Optional[int] = None,
        images: Optional[List[str]] = None
    ) -> str:
        """Generate text from Ollama (non-streaming) with retries."""
        payload = self._base_payload(prompt, model, False, system_prompt)
        if context is not None:
            payload["context"] = context
        img_data = self._encode_images(images)
        if img_data:
            payload["images"] = img_data

        while True:
            try:
                response = requests.post(self._url(), json=payload, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                self._retry_count = 0
                return data.get("response", "")
            except Exception as e:
                if not self._handle_error(e):
                    raise RuntimeError(f"Failed after {self._max_retries} attempts: {e}")

    def stream_generate(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "",
        context: Optional[int] = None,
        images: Optional[List[str]] = None
    ) -> Generator[str, None, None]:
        """Stream text generation from Ollama."""
        payload = self._base_payload(prompt, model, True, system_prompt)
        if context is not None:
            payload["context"] = context
        img_data = self._encode_images(images)
        if img_data:
            payload["images"] = img_data

        while True:
            try:
                with requests.post(
                    self._url(), json=payload, timeout=self.timeout, stream=True
                ) as response:
                    response.raise_for_status()
                    for line in response.iter_lines(decode_unicode=True):
                        if line:
                            data = json.loads(line)
                            yield data.get("response", "")
                self._retry_count = 0
                return
            except Exception as e:
                if not self._handle_error(e):
                    raise RuntimeError(f"Failed after {self._max_retries} attempts: {e}")
                yield ""

    def get_last_error(self) -> Optional[str]:
        """Get the last error message."""
        return str(self._last_error) if self._last_error else None

    def get_context(self) -> Optional[list]:
        """Get current conversation context."""
        try:
            response = requests.post(
                self._url(),
                json={"model": "test", "prompt": "", "stream": False},
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json().get("context")
        except Exception:
            return None