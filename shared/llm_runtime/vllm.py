"""vLLM runtime adapter.

This adapter targets vLLM's OpenAI-compatible API server.
"""

import requests

from shared.llm_runtime.base import BaseLLMRuntime, StructuredOutputT
from shared.llm_runtime.exceptions import LLMRuntimeError


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
                "    python -m vllm.entrypoints.openai.api_server "
                "--model <model_name>"
            ) from error

    def generate_structured(
        self,
        prompt: str,
        output_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Generate structured output.

        Raises:
            LLMRuntimeError: Always for now; structured generation is added next.
        """
        self.check_health()

        raise LLMRuntimeError("vLLM structured generation is not implemented yet.")
