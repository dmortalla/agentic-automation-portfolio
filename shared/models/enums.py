"""Shared enum definitions for the agentic automation portfolio."""

from enum import StrEnum


class LLMProvider(StrEnum):
    """Supported LLM runtime providers."""

    OLLAMA = "ollama"
    VLLM = "vllm"
    TENSORRT = "tensorrt"
    OPENAI = "openai"
