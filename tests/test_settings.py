"""Tests for application settings."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from shared.config.settings import Settings
from shared.models.enums import LLMProvider


def test_default_settings_use_ollama(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Default settings should use Ollama as the local development provider."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)

    settings = Settings()

    assert settings.llm_provider == LLMProvider.OLLAMA
    assert settings.ollama_base_url == "http://localhost:11434"
    assert settings.ollama_model == "llama3.1"


def test_settings_accept_vllm_provider(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Settings should accept vLLM as a supported provider."""
    monkeypatch.chdir(tmp_path)

    settings = Settings(llm_provider=LLMProvider.VLLM)

    assert settings.llm_provider == LLMProvider.VLLM


def test_invalid_provider_raises_validation_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Unsupported LLM providers should fail environment validation."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LLM_PROVIDER", "bad_provider")

    with pytest.raises(ValidationError):
        Settings()
