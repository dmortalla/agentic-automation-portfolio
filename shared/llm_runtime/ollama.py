"""Ollama runtime adapter."""

import requests

from shared.llm_runtime.base import BaseLLMRuntime, StructuredOutputT
from shared.llm_runtime.exceptions import LLMRuntimeError
from shared.llm_runtime.parsing import parse_and_validate_structured_output


class OllamaRuntime(BaseLLMRuntime):
    """Runtime adapter for Ollama."""

    def __init__(
        self,
        base_url: str,
        model: str,
        timeout_seconds: int = 60,
    ) -> None:
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

    def check_health(self) -> None:
        """Verify Ollama is reachable.

        Raises:
            LLMRuntimeError: If Ollama is unreachable.
        """
        endpoint = f"{self.base_url}/api/tags"

        try:
            response = requests.get(endpoint, timeout=5)
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
        """Generate structured output using Ollama's local API.

        Args:
            prompt: Prompt sent to the model runtime.
            output_model: Pydantic model class used to validate output.

        Returns:
            Validated structured output.

        Raises:
            LLMRuntimeError: If the request, parsing, or validation fails.
        """
        self.check_health()

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
            raw_model_output = response.json()["response"]
        except (KeyError, TypeError) as error:
            raise LLMRuntimeError("Ollama returned invalid structured output.") from error

        return parse_and_validate_structured_output(
            raw_output=raw_model_output,
            output_model=output_model,
            provider_name="Ollama",
        )
