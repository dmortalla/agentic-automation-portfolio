"""Tests for Ollama runtime adapter."""

import json
from unittest.mock import Mock, patch

import pytest
import requests
from pydantic import BaseModel

from shared.llm_runtime.exceptions import LLMRuntimeError
from shared.llm_runtime.ollama import OllamaRuntime


class ExampleOutput(BaseModel):
    """Example structured output."""

    label: str
    score: float


def test_ollama_runtime_generates_structured_output() -> None:
    """OllamaRuntime should parse and validate structured output."""
    runtime = OllamaRuntime(
        base_url="http://localhost:11434",
        model="llama3.1",
    )

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "response": json.dumps({"label": "technical", "score": 0.98})
    }

    with patch("shared.llm_runtime.ollama.requests.post", return_value=mock_response) as mock_post:
        result = runtime.generate_structured(
            prompt="Classify this ticket.",
            output_model=ExampleOutput,
        )

    assert result.label == "technical"
    assert result.score == 0.98
    mock_post.assert_called_once()


def test_ollama_runtime_rejects_blank_prompt() -> None:
    """OllamaRuntime should reject blank prompts."""
    runtime = OllamaRuntime(
        base_url="http://localhost:11434",
        model="llama3.1",
    )

    with pytest.raises(LLMRuntimeError):
        runtime.generate_structured(
            prompt="   ",
            output_model=ExampleOutput,
        )


def test_ollama_runtime_wraps_request_errors() -> None:
    """OllamaRuntime should convert request errors into LLMRuntimeError."""
    runtime = OllamaRuntime(
        base_url="http://localhost:11434",
        model="llama3.1",
    )

    with patch(
        "shared.llm_runtime.ollama.requests.post",
        side_effect=requests.RequestException("connection failed"),
    ):
        with pytest.raises(LLMRuntimeError, match="Ollama request failed"):
            runtime.generate_structured(
                prompt="Classify this ticket.",
                output_model=ExampleOutput,
            )


def test_ollama_runtime_rejects_invalid_json_response() -> None:
    """OllamaRuntime should reject malformed model output."""
    runtime = OllamaRuntime(
        base_url="http://localhost:11434",
        model="llama3.1",
    )

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"response": "not-json"}

    with patch("shared.llm_runtime.ollama.requests.post", return_value=mock_response):
        with pytest.raises(LLMRuntimeError, match="invalid structured output"):
            runtime.generate_structured(
                prompt="Classify this ticket.",
                output_model=ExampleOutput,
            )


def test_ollama_runtime_rejects_schema_invalid_response() -> None:
    """OllamaRuntime should reject output that does not match schema."""
    runtime = OllamaRuntime(
        base_url="http://localhost:11434",
        model="llama3.1",
    )

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "response": json.dumps({"label": "technical", "score": "not-a-number"})
    }

    with patch("shared.llm_runtime.ollama.requests.post", return_value=mock_response):
        with pytest.raises(LLMRuntimeError, match="schema validation"):
            runtime.generate_structured(
                prompt="Classify this ticket.",
                output_model=ExampleOutput,
            )
