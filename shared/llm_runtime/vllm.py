"""vLLM runtime adapter."""

from shared.llm_runtime.base import BaseLLMRuntime, StructuredOutputT
from shared.llm_runtime.exceptions import LLMRuntimeError


class VLLMRuntime(BaseLLMRuntime):
    """Runtime adapter for vLLM OpenAI-compatible inference."""

    def __init__(self, base_url: str, model: str) -> None:
        """Initialize the vLLM runtime adapter.

        Args:
            base_url: vLLM OpenAI-compatible server base URL.
            model: vLLM model name.
        """
        self.base_url = base_url
        self.model = model

    @property
    def provider_name(self) -> str:
        """Return the runtime provider name."""
        return "vllm"

    def generate_structured(
        self,
        prompt: str,
        output_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Generate structured output.

        Raises:
            LLMRuntimeError: Always for now because live vLLM calls are added later.
        """
        raise LLMRuntimeError("vLLM structured generation is not implemented yet.")
