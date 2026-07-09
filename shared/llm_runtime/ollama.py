"""Ollama runtime adapter.

This adapter represents the local-development Ollama runtime. It satisfies
the BaseLLMRuntime contract so agents can depend on a common interface
without importing Ollama-specific clients.
"""

from pydantic import BaseModel

from shared.llm_runtime.base import BaseLLMRuntime, StructuredOutputT
from shared.llm_runtime.exceptions import LLMRuntimeError


class OllamaRuntime(BaseLLMRuntime):
    """Runtime adapter for Ollama-compatible local inference."""

    def __init__(self, base_url: str, model: str) -> None:
        """Initialize the Ollama runtime adapter.

        Args:
            base_url: Ollama server base URL.
            model: Ollama model name.
        """
        self.base_url = base_url
        self.model = model

    @property
    def provider_name(self) -> str:
        """Return the runtime provider name."""
        return "ollama"

    def generate_structured(
        self,
        prompt: str,
        output_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Generate structured output.

        Args:
            prompt: Prompt sent to the model runtime.
            output_model: Pydantic model class used to validate output.

        Raises:
            LLMRuntimeError: Always for now because live Ollama calls are added later.
        """
        raise LLMRuntimeError("Ollama structured generation is not implemented yet.")
