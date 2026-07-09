"""Tests for the abstract LLM runtime contract."""

import pytest
from pydantic import BaseModel

from shared.llm_runtime.base import BaseLLMRuntime


class ExampleOutput(BaseModel):
    """Example structured output used for runtime contract tests."""

    message: str


class ExampleRuntime(BaseLLMRuntime):
    """Concrete runtime used to verify the abstract contract."""

    @property
    def provider_name(self) -> str:
        """Return the test provider name."""
        return "example"

    def generate_structured(
        self,
        prompt: str,
        output_model: type[ExampleOutput],
    ) -> ExampleOutput:
        """Return a deterministic structured response for tests."""
        return output_model(message=f"Processed: {prompt}")


def test_base_runtime_cannot_be_instantiated() -> None:
    """BaseLLMRuntime should not be directly instantiable."""
    with pytest.raises(TypeError):
        BaseLLMRuntime()


def test_concrete_runtime_exposes_provider_name() -> None:
    """Concrete runtimes should expose a provider name."""
    runtime = ExampleRuntime()

    assert runtime.provider_name == "example"


def test_concrete_runtime_generates_structured_output() -> None:
    """Concrete runtimes should return validated structured output."""
    runtime = ExampleRuntime()

    result = runtime.generate_structured("hello", ExampleOutput)

    assert isinstance(result, ExampleOutput)
    assert result.message == "Processed: hello"
