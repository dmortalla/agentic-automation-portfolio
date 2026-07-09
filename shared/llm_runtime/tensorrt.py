"""TensorRT-LLM runtime adapter."""

from shared.llm_runtime.base import BaseLLMRuntime, StructuredOutputT
from shared.llm_runtime.exceptions import LLMRuntimeError


class TensorRTRuntime(BaseLLMRuntime):
    """Runtime adapter for TensorRT-LLM OpenAI-compatible inference."""

    def __init__(self, base_url: str, model: str) -> None:
        """Initialize the TensorRT-LLM runtime adapter.

        Args:
            base_url: TensorRT-LLM OpenAI-compatible server base URL.
            model: TensorRT-LLM model name.
        """
        self.base_url = base_url
        self.model = model

    @property
    def provider_name(self) -> str:
        """Return the runtime provider name."""
        return "tensorrt"

    def generate_structured(
        self,
        prompt: str,
        output_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Generate structured output.

        Raises:
            LLMRuntimeError: Always for now because live TensorRT-LLM calls are added later.
        """
        raise LLMRuntimeError("TensorRT-LLM structured generation is not implemented yet.")
