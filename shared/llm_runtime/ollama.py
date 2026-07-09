"""Ollama runtime adapter.

This adapter calls Ollama's local HTTP API and requests structured output
using the Pydantic model JSON schema.
"""

import json

import requests
from pydantic import ValidationError

from shared.llm_runtime.base import BaseLLMRuntime, StructuredOutputT
from shared.llm_runtime.exceptions import LLMRuntimeError


class OllamaRuntime(BaseLLMRuntime):
    """Runtime adapter for Ollama-compatible local inference."""

    def __init__(self, base_url: str, model: str, timeout_seconds: int = 60) -> None:
        """Initialize the Ollama runtime adapter.

        Args:
            base_url: Ollama server base URL.
            model: Ollama model name.
            timeout_seconds: HTTP request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    @property
    def provider_name(self) -> str:
        """Return the runtime provider name."""
        return "ollama"

    def generate_structured(
        self,
        prompt: str,
        output_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Generate structured output using Ollama's local API.

        Args:
            prompt: Prompt sent to the model runtime.
            output_model: Pydantic model class used to validate output.

        Returns:
            Validated structured output.

        Raises:
            LLMRuntimeError: If Ollama request, JSON parsing, or validation fails.
        """
        if not prompt.strip():
            raise LLMRuntimeError("Prompt must not be blank.")

        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": output_model.model_json_schema(),
        }

        try:
            response = requests.post(
                endpoint,
                json=payload,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            raise LLMRuntimeError(f"Ollama request failed: {error}") from error

        try:
            response_payload = response.json()
            raw_model_output = response_payload["response"]
            parsed_output = json.loads(raw_model_output)
        except (KeyError, json.JSONDecodeError, TypeError) as error:
            raise LLMRuntimeError("Ollama returned invalid structured output.") from error

        try:
            return output_model.model_validate(parsed_output)
        except ValidationError as error:
            raise LLMRuntimeError("Ollama output failed schema validation.") from error
