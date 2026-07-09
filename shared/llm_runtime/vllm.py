"""vLLM runtime adapter.

This adapter targets vLLM's OpenAI-compatible API server.
"""

import requests

from shared.llm_runtime.base import BaseLLMRuntime, StructuredOutputT
from shared.llm_runtime.exceptions import LLMRuntimeError
from shared.llm_runtime.parsing import parse_and_validate_structured_output


class VLLMRuntime(BaseLLMRuntime):
    """Runtime adapter for vLLM OpenAI-compatible inference."""

    def __init__(self, base_url: str, model: str, timeout_seconds: int = 60) -> None:
        """Initialize the vLLM runtime adapter.

        Args:
            base_url: vLLM OpenAI-compatible server base URL.
            model: vLLM model name.
            timeout_seconds: HTTP request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    @property
    def provider_name(self) -> str:
        """Return the runtime provider name."""
        return "vllm"

    def check_health(self) -> None:
        """Verify the vLLM server is reachable.

        Raises:
            LLMRuntimeError: If the vLLM server is unreachable.
        """
        endpoint = f"{self.base_url}/models"

        try:
            response = requests.get(endpoint, timeout=5)
            response.raise_for_status()
        except requests.RequestException as error:
            raise LLMRuntimeError(
                "vLLM is not reachable.\n\n"
                "Start the vLLM OpenAI-compatible server, then try again.\n\n"
                "Example:\n"
                "    python -m vllm.entrypoints.openai.api_server --model <model_name>"
            ) from error

    def generate_structured(
        self,
        prompt: str,
        output_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Generate structured output using vLLM's OpenAI-compatible API.

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

        endpoint = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": output_model.__name__,
                    "schema": output_model.model_json_schema(),
                },
            },
        }

        try:
            response = requests.post(
                endpoint,
                json=payload,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            raise LLMRuntimeError(f"vLLM request failed: {error}") from error

        try:
            raw_model_output = response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise LLMRuntimeError("vLLM returned invalid structured output.") from error

        return parse_and_validate_structured_output(
            raw_output=raw_model_output,
            output_model=output_model,
            provider_name="vLLM",
        )
