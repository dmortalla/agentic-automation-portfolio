"""Shared parsing utilities for LLM runtime adapters."""

import json
from typing import Any

from pydantic import BaseModel, ValidationError

from shared.llm_runtime.exceptions import LLMRuntimeError


def parse_json_object(raw_output: str, provider_name: str) -> dict[str, Any]:
    """Parse a raw model response into a JSON object.

    Args:
        raw_output: Raw text returned by the model.
        provider_name: Runtime provider name used in error messages.

    Returns:
        Parsed JSON object.

    Raises:
        LLMRuntimeError: If the raw output is not valid JSON or not an object.
    """
    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as error:
        raise LLMRuntimeError(
            f"{provider_name} returned invalid structured output."
        ) from error

    if not isinstance(parsed, dict):
        raise LLMRuntimeError(
            f"{provider_name} returned invalid structured output."
        )

    return parsed


def normalize_confidence(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize common confidence formats in model output.

    Args:
        payload: Parsed structured model output.

    Returns:
        Payload with confidence normalized if needed.
    """
    confidence = payload.get("confidence")

    if isinstance(confidence, int | float) and 1 < confidence <= 100:
        payload["confidence"] = confidence / 100

    return payload


def validate_structured_output(
    payload: dict[str, Any],
    output_model: type[BaseModel],
    provider_name: str,
) -> BaseModel:
    """Validate structured output against a Pydantic model.

    Args:
        payload: Parsed structured model output.
        output_model: Pydantic model class used for validation.
        provider_name: Runtime provider name used in error messages.

    Returns:
        Validated Pydantic model instance.

    Raises:
        LLMRuntimeError: If validation fails.
    """
    try:
        return output_model.model_validate(payload)
    except ValidationError as error:
        raise LLMRuntimeError(
            f"{provider_name} output failed schema validation: {error}"
        ) from error


def parse_and_validate_structured_output(
    raw_output: str,
    output_model: type[BaseModel],
    provider_name: str,
) -> BaseModel:
    """Parse, normalize, and validate a structured model response.

    Args:
        raw_output: Raw model output string.
        output_model: Pydantic model class used for validation.
        provider_name: Runtime provider name used in error messages.

    Returns:
        Validated Pydantic model instance.
    """
    parsed = parse_json_object(raw_output=raw_output, provider_name=provider_name)
    normalized = normalize_confidence(parsed)

    return validate_structured_output(
        payload=normalized,
        output_model=output_model,
        provider_name=provider_name,
    )
