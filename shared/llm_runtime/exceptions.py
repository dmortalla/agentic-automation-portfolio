"""Custom exceptions for LLM runtime adapters."""


class LLMRuntimeError(Exception):
    """Base exception for LLM runtime errors."""


class UnsupportedLLMProviderError(LLMRuntimeError):
    """Raised when an unsupported LLM provider is requested."""


class LLMConfigurationError(LLMRuntimeError):
    """Raised when LLM runtime configuration is invalid."""
