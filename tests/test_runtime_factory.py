"""Tests for the LLM runtime factory."""

import pytest

from shared.config.settings import Settings
from shared.llm_runtime.exceptions import UnsupportedLLMProviderError
from shared.llm_runtime.factory import create_runtime
from shared.llm_runtime.ollama import OllamaRuntime
from shared.llm_runtime.tensorrt import TensorRTRuntime
from shared.llm_runtime.vllm import VLLMRuntime
from shared.models.enums import LLMProvider


def test_create_runtime_returns_ollama_runtime() -> None:
    """Factory should return OllamaRuntime when provider is Ollama."""
    settings = Settings(llm_provider=LLMProvider.OLLAMA)

    runtime = create_runtime(settings)

    assert isinstance(runtime, OllamaRuntime)
    assert runtime.provider_name == "ollama"
    assert runtime.base_url == settings.ollama_base_url
    assert runtime.model == settings.ollama_model


def test_create_runtime_returns_vllm_runtime() -> None:
    """Factory should return VLLMRuntime when provider is vLLM."""
    settings = Settings(llm_provider=LLMProvider.VLLM)

    runtime = create_runtime(settings)

    assert isinstance(runtime, VLLMRuntime)
    assert runtime.provider_name == "vllm"
    assert runtime.base_url == settings.vllm_base_url
    assert runtime.model == settings.vllm_model


def test_create_runtime_returns_tensorrt_runtime() -> None:
    """Factory should return TensorRTRuntime when provider is TensorRT."""
    settings = Settings(llm_provider=LLMProvider.TENSORRT)

    runtime = create_runtime(settings)

    assert isinstance(runtime, TensorRTRuntime)
    assert runtime.provider_name == "tensorrt"
    assert runtime.base_url == settings.tensorrt_base_url
    assert runtime.model == settings.tensorrt_model


def test_create_runtime_rejects_openai_until_adapter_exists() -> None:
    """Factory should fail clearly for providers not implemented yet."""
    settings = Settings(llm_provider=LLMProvider.OPENAI)

    with pytest.raises(UnsupportedLLMProviderError):
        create_runtime(settings)
