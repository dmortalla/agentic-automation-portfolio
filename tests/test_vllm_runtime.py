"""Tests for vLLM runtime adapter."""

import json
from unittest.mock import Mock, patch

import pytest
import requests
from pydantic import BaseModel, Field

from shared.llm_runtime.exceptions import LLMRuntimeError
from shared.llm_runtime.vllm import VLLMRuntime


class ExampleOutput(BaseModel):
    """Example structured output."""

    label: str
    confidence: float = Field(..., ge=0.0, le=1.0)


def _runtime() -> VLLMRuntime:
    """Create a reusable vLLM runtime."""
    return VLLMRuntime(
        base_url="http://localhost:8000/v1",
        model="meta-llama/Llama-3.1-8B-Instruct",
    )


def test_vllm_runtime_exposes_provider_name() -> None:
    """vLLM runtime should expose provider name."""
    assert _runtime().provider_name == "vllm"


def test_vllm_health_check_passes() -> None:
    """Healthy vLLM server should not raise."""
    response = Mock()
    response.raise_for_status.return_value = None

    with patch("shared.llm_runtime.vllm.requests.get", return_value=response):
        _runtime().check_health()


def test_vllm_health_check_reports_unavailable_server() -> None:
    """Unavailable vLLM server should raise friendly error."""
    with patch(
        "shared.llm_runtime.vllm.requests.get",
        side_effect=requests.ConnectionError,
    ):
        with pytest.raises(LLMRuntimeError, match="vLLM is not reachable"):
            _runtime().check_health()


def test_vllm_generates_structured_output() -> None:
    """vLLM runtime should parse and validate structured output."""
    health_response = Mock()
    health_response.raise_for_status.return_value = None

    generate_response = Mock()
    generate_response.raise_for_status.return_value = None
    generate_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "label": "technical",
                            "confidence": 0.98,
                        }
                    )
                }
            }
        ]
    }

    with patch("shared.llm_runtime.vllm.requests.get", return_value=health_response):
        with patch("shared.llm_runtime.vllm.requests.post", return_value=generate_response):
            result = _runtime().generate_structured(
                prompt="Classify this ticket.",
                output_model=ExampleOutput,
            )

    assert result.label == "technical"
    assert result.confidence == 0.98


def test_vllm_normalizes_percentage_confidence() -> None:
    """vLLM runtime should convert percentage confidence to decimal confidence."""
    health_response = Mock()
    health_response.raise_for_status.return_value = None

    generate_response = Mock()
    generate_response.raise_for_status.return_value = None
    generate_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "label": "technical",
                            "confidence": 85,
                        }
                    )
                }
            }
        ]
    }

    with patch("shared.llm_runtime.vllm.requests.get", return_value=health_response):
        with patch("shared.llm_runtime.vllm.requests.post", return_value=generate_response):
            result = _runtime().generate_structured(
                prompt="Classify this ticket.",
                output_model=ExampleOutput,
            )

    assert result.confidence == 0.85


def test_vllm_rejects_blank_prompt() -> None:
    """vLLM runtime should reject blank prompts."""
    health_response = Mock()
    health_response.raise_for_status.return_value = None

    with patch("shared.llm_runtime.vllm.requests.get", return_value=health_response):
        with pytest.raises(LLMRuntimeError, match="Prompt must not be blank"):
            _runtime().generate_structured(
                prompt="   ",
                output_model=ExampleOutput,
            )


def test_vllm_wraps_request_errors() -> None:
    """vLLM runtime should convert request failures to LLMRuntimeError."""
    health_response = Mock()
    health_response.raise_for_status.return_value = None

    with patch("shared.llm_runtime.vllm.requests.get", return_value=health_response):
        with patch(
            "shared.llm_runtime.vllm.requests.post",
            side_effect=requests.RequestException("request failed"),
        ):
            with pytest.raises(LLMRuntimeError, match="vLLM request failed"):
                _runtime().generate_structured(
                    prompt="Classify this ticket.",
                    output_model=ExampleOutput,
                )


def test_vllm_rejects_invalid_json_response() -> None:
    """vLLM runtime should reject malformed model output."""
    health_response = Mock()
    health_response.raise_for_status.return_value = None

    generate_response = Mock()
    generate_response.raise_for_status.return_value = None
    generate_response.json.return_value = {
        "choices": [{"message": {"content": "not-json"}}]
    }

    with patch("shared.llm_runtime.vllm.requests.get", return_value=health_response):
        with patch("shared.llm_runtime.vllm.requests.post", return_value=generate_response):
            with pytest.raises(LLMRuntimeError, match="invalid structured output"):
                _runtime().generate_structured(
                    prompt="Classify this ticket.",
                    output_model=ExampleOutput,
                )


def test_vllm_rejects_schema_invalid_response() -> None:
    """vLLM runtime should reject output that does not match schema."""
    health_response = Mock()
    health_response.raise_for_status.return_value = None

    generate_response = Mock()
    generate_response.raise_for_status.return_value = None
    generate_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "label": "technical",
                            "confidence": "not-a-number",
                        }
                    )
                }
            }
        ]
    }

    with patch("shared.llm_runtime.vllm.requests.get", return_value=health_response):
        with patch("shared.llm_runtime.vllm.requests.post", return_value=generate_response):
            with pytest.raises(LLMRuntimeError, match="schema validation"):
                _runtime().generate_structured(
                    prompt="Classify this ticket.",
                    output_model=ExampleOutput,
                )
