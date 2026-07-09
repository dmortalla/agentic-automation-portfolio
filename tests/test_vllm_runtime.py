"""Tests for vLLM runtime adapter health checks."""

from unittest.mock import Mock, patch

import pytest
import requests

from shared.llm_runtime.exceptions import LLMRuntimeError
from shared.llm_runtime.vllm import VLLMRuntime


def test_vllm_runtime_exposes_provider_name() -> None:
    """vLLM runtime should expose provider name."""
    runtime = VLLMRuntime(
        base_url="http://localhost:8000/v1",
        model="meta-llama/Llama-3.1-8B-Instruct",
    )

    assert runtime.provider_name == "vllm"


def test_vllm_health_check_passes() -> None:
    """Healthy vLLM server should not raise."""
    runtime = VLLMRuntime(
        base_url="http://localhost:8000/v1",
        model="meta-llama/Llama-3.1-8B-Instruct",
    )

    response = Mock()
    response.raise_for_status.return_value = None

    with patch("shared.llm_runtime.vllm.requests.get", return_value=response):
        runtime.check_health()


def test_vllm_health_check_reports_unavailable_server() -> None:
    """Unavailable vLLM server should raise friendly error."""
    runtime = VLLMRuntime(
        base_url="http://localhost:8000/v1",
        model="meta-llama/Llama-3.1-8B-Instruct",
    )

    with patch(
        "shared.llm_runtime.vllm.requests.get",
        side_effect=requests.ConnectionError,
    ):
        with pytest.raises(LLMRuntimeError, match="vLLM is not reachable"):
            runtime.check_health()
