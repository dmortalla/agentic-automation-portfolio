"""Ollama runtime adapter."""

import json

import requests
from pydantic import ValidationError

from shared.llm_runtime.base import BaseLLMRuntime, StructuredOutputT
from shared.llm_runtime.exceptions import LLMRuntimeError


class OllamaRuntime(BaseLLMRuntime):
    """Runtime adapter for Ollama."""

    def __init__(
        self,
        base_url: str,
        model: str,
        timeout_seconds: int = 60,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    @property
    def provider_name(self) -> str:
        return "ollama"

    def check_health(self) -> None:
        """Verify Ollama is reachable."""

        endpoint = f"{self.base_url}/api/tags"

        try:
            response = requests.get(
                endpoint,
                timeout=5,
            )
            response.raise_for_status()

        except requests.RequestException as error:
            raise LLMRuntimeError(
                "Ollama is not reachable.\n\n"
                "Start the server with:\n"
                "    ollama serve\n\n"
                "Verify with:\n"
                "    ollama list"
            ) from error

    def generate_structured(
        self,
        prompt: str,
        output_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Generate structured output."""

        self.check_health()

        if not prompt.strip():
            raise LLMRuntimeError(
                "Prompt must not be blank."
            )

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
            raise LLMRuntimeError(
                f"Ollama request failed: {error}"
            ) from error

        try:
            raw = response.json()["response"]
            parsed = json.loads(raw)

            if (
                isinstance(parsed, dict)
                and isinstance(parsed.get("confidence"), int | float)
                and 1 < parsed["confidence"] <= 100
            ):
                parsed["confidence"] = parsed["confidence"] / 100

        except (
            KeyError,
            TypeError,
            json.JSONDecodeError,
        ) as error:
            raise LLMRuntimeError(
                "Ollama returned invalid structured output."
            ) from error

        try:
            return output_model.model_validate(parsed)

        except ValidationError as error:
            raise LLMRuntimeError(
                f"Ollama output failed schema validation: {error}"
            ) from error
