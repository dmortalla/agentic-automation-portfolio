"""Abstract LLM runtime contract.

This module defines the interface that all model runtime adapters must
implement.

Business logic should depend on this interface, not on provider-specific
clients such as Ollama, vLLM, TensorRT-LLM, or OpenAI-compatible SDKs.
"""

from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel


StructuredOutputT = TypeVar("StructuredOutputT", bound=BaseModel)


class BaseLLMRuntime(ABC):
    """Abstract base class for LLM runtime adapters.

    Runtime adapters translate application-level generation requests into
    provider-specific calls. Agents and workflows should depend on this
    interface so provider changes remain configuration-driven.

    This class should not depend on business-domain models such as support
    tickets, leads, or compliance documents.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the runtime provider name."""

    @abstractmethod
    def generate_structured(
        self,
        prompt: str,
        output_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Generate a structured response validated by a Pydantic model.

        Args:
            prompt: Prompt sent to the model runtime.
            output_model: Pydantic model class used to validate output.

        Returns:
            Validated structured output.

        Raises:
            LLMRuntimeError: If generation or validation fails.
        """
