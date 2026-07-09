"""Runtime contract tests."""

from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel, Field

from shared.llm_runtime.base import BaseLLMRuntime


StructuredOutputT = TypeVar("StructuredOutputT", bound=BaseModel)


class ContractResponse(BaseModel):
    """Structured response used to validate runtime contract behavior."""

    answer: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)


class FakeRuntime(BaseLLMRuntime):
    """Deterministic runtime used to test the runtime contract itself."""

    @property
    def provider_name(self) -> str:
        """Return fake provider name."""
        return "fake"

    def generate_structured(
        self,
        prompt: str,
        output_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Return a validated structured response."""
        assert prompt.strip()

        return output_model(
            answer="Runtime contract satisfied.",
            confidence=0.95,
        )


def test_runtime_contract_generate_structured_returns_pydantic_model() -> None:
    """Every runtime must return an instance of the requested Pydantic model."""
    runtime = FakeRuntime()

    result = runtime.generate_structured(
        prompt="Return an answer and confidence score.",
        output_model=ContractResponse,
    )

    assert isinstance(result, ContractResponse)
    assert result.answer
    assert 0.0 <= result.confidence <= 1.0


def test_runtime_contract_requires_provider_name() -> None:
    """Every runtime must expose a non-empty provider name."""
    runtime = FakeRuntime()

    assert isinstance(runtime.provider_name, str)
    assert runtime.provider_name.strip()
