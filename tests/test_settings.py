"""Tests for application settings."""

import pytest
from pydantic import ValidationError

from shared.config.settings import Settings
from shared.models.enums import LLMProvider


def test_default_settings_use_ollama() -> None:
    """Default settings should use Ollama as the local development provider."""
    settings = Settings()

    assert settings.llm_provider == LLMProvider.OLLAMA
    assert settings.ollama_base_url == "http://localhost:11434"
    assert settings.ollama_model == "llama3.1"


def test_settings_accept_vllm_provider() -> None:
    """Settings should accept vLLM as a supported provider."""
    settings = Settings(llm_provider="vllm")

    assert settings.llm_provider == LLMProvider.VLLM


def test_invalid_provider_raises_validation_error() -> None:
    """Unsupported LLM providers should fail validation."""
    with pytest.raises(ValidationError):
        Settings(llm_provider="bad_provider")


def test_invalid_url_raises_validation_error() -> None:
    """Invalid runtime URLs should fail validation."""
    with pytest.raises(ValidationError):
        Settings(ollama_base_url="localhost:11434")
