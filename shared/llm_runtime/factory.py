"""Factory for creating configured LLM runtime adapters."""

from shared.config.settings import Settings, get_settings
from shared.llm_runtime.base import BaseLLMRuntime
from shared.llm_runtime.exceptions import UnsupportedLLMProviderError
from shared.llm_runtime.ollama import OllamaRuntime
from shared.llm_runtime.tensorrt import TensorRTRuntime
from shared.llm_runtime.vllm import VLLMRuntime
from shared.models.enums import LLMProvider


def create_runtime(settings: Settings | None = None) -> BaseLLMRuntime:
    """Create an LLM runtime adapter from application settings.

    Args:
        settings: Optional settings object. If omitted, cached app settings are used.

    Returns:
        Configured LLM runtime adapter.

    Raises:
        UnsupportedLLMProviderError: If the configured provider is unsupported.
    """
    resolved_settings = settings or get_settings()

    if resolved_settings.llm_provider == LLMProvider.OLLAMA:
        return OllamaRuntime(
            base_url=resolved_settings.ollama_base_url,
            model=resolved_settings.ollama_model,
        )

    if resolved_settings.llm_provider == LLMProvider.VLLM:
        return VLLMRuntime(
            base_url=resolved_settings.vllm_base_url,
            model=resolved_settings.vllm_model,
        )

    if resolved_settings.llm_provider == LLMProvider.TENSORRT:
        return TensorRTRuntime(
            base_url=resolved_settings.tensorrt_base_url,
            model=resolved_settings.tensorrt_model,
        )

    raise UnsupportedLLMProviderError(
        f"Unsupported LLM provider: {resolved_settings.llm_provider}"
    )
