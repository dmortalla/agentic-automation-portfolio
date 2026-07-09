"""Tests for Ollama output normalization."""

import json
from unittest.mock import Mock, patch

from pydantic import BaseModel, Field

from shared.llm_runtime.ollama import OllamaRuntime


class ConfidenceOutput(BaseModel):
    """Output with normalized confidence."""

    confidence: float = Field(..., ge=0.0, le=1.0)


def test_ollama_normalizes_percentage_confidence() -> None:
    """OllamaRuntime should convert percentage confidence to decimal confidence."""
    runtime = OllamaRuntime(
        base_url="http://localhost:11434",
        model="qwen2.5-coder:7b",
    )

    health_response = Mock()
    health_response.raise_for_status.return_value = None

    generate_response = Mock()
    generate_response.raise_for_status.return_value = None
    generate_response.json.return_value = {
        "response": json.dumps({"confidence": 85})
    }

    with patch("shared.llm_runtime.ollama.requests.get", return_value=health_response):
        with patch("shared.llm_runtime.ollama.requests.post", return_value=generate_response):
            result = runtime.generate_structured(
                prompt="Return confidence.",
                output_model=ConfidenceOutput,
            )

    assert result.confidence == 0.85
