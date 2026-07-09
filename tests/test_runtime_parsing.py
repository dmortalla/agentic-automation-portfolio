"""Tests for shared runtime parsing utilities."""

import pytest
from pydantic import BaseModel, Field

from shared.llm_runtime.exceptions import LLMRuntimeError
from shared.llm_runtime.parsing import (
    normalize_confidence,
    parse_and_validate_structured_output,
    parse_json_object,
)


class ExampleOutput(BaseModel):
    """Example output model."""

    label: str
    confidence: float = Field(..., ge=0.0, le=1.0)


def test_parse_json_object_returns_dict() -> None:
    """parse_json_object should parse valid JSON objects."""
    result = parse_json_object(
        raw_output='{"label": "technical"}',
        provider_name="TestProvider",
    )

    assert result == {"label": "technical"}


def test_parse_json_object_rejects_invalid_json() -> None:
    """parse_json_object should reject malformed JSON."""
    with pytest.raises(LLMRuntimeError, match="invalid structured output"):
        parse_json_object(
            raw_output="not-json",
            provider_name="TestProvider",
        )


def test_parse_json_object_rejects_non_object_json() -> None:
    """parse_json_object should reject JSON arrays."""
    with pytest.raises(LLMRuntimeError, match="invalid structured output"):
        parse_json_object(
            raw_output='["not", "an", "object"]',
            provider_name="TestProvider",
        )


def test_normalize_confidence_converts_percentage() -> None:
    """normalize_confidence should convert 85 to 0.85."""
    payload = {"confidence": 85}

    result = normalize_confidence(payload)

    assert result["confidence"] == 0.85


def test_normalize_confidence_keeps_decimal() -> None:
    """normalize_confidence should preserve already normalized confidence."""
    payload = {"confidence": 0.85}

    result = normalize_confidence(payload)

    assert result["confidence"] == 0.85


def test_parse_and_validate_structured_output_returns_model() -> None:
    """parse_and_validate_structured_output should return validated model."""
    result = parse_and_validate_structured_output(
        raw_output='{"label": "technical", "confidence": 85}',
        output_model=ExampleOutput,
        provider_name="TestProvider",
    )

    assert result.label == "technical"
    assert result.confidence == 0.85


def test_parse_and_validate_structured_output_raises_validation_error() -> None:
    """parse_and_validate_structured_output should report schema validation errors."""
    with pytest.raises(LLMRuntimeError, match="schema validation"):
        parse_and_validate_structured_output(
            raw_output='{"label": "technical", "confidence": "bad"}',
            output_model=ExampleOutput,
            provider_name="TestProvider",
        )
