"""Tests for Ollama health checking."""

from unittest.mock import Mock, patch

import pytest
import requests

from shared.llm_runtime.exceptions import LLMRuntimeError
from shared.llm_runtime.ollama import OllamaRuntime


def test_health_check_passes() -> None:
    """Healthy server should not raise."""

    runtime = OllamaRuntime(
        base_url="http://localhost:11434",
        model="llama3.1",
    )

    response = Mock()
    response.raise_for_status.return_value = None

    with patch(
        "shared.llm_runtime.ollama.requests.get",
        return_value=response,
    ):
        runtime.check_health()


def test_health_check_reports_unavailable_server() -> None:
    """Unavailable server should raise friendly error."""

    runtime = OllamaRuntime(
        base_url="http://localhost:11434",
        model="llama3.1",
    )

    with patch(
        "shared.llm_runtime.ollama.requests.get",
        side_effect=requests.ConnectionError,
    ):
        with pytest.raises(
            LLMRuntimeError,
            match="Ollama is not reachable",
        ):
            runtime.check_health()
