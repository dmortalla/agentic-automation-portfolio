"""Application settings loaded from environment variables.

This module centralizes configuration for all three portfolio projects.
It uses Pydantic Settings so the rest of the codebase does not need to
read environment variables directly.
"""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from shared.models.enums import LLMProvider


class Settings(BaseSettings):
    """Validated application settings.

    Attributes:
        llm_provider: Runtime provider used for model inference.
        ollama_base_url: Base URL for a local Ollama server.
        ollama_model: Ollama model name.
        vllm_base_url: Base URL for a vLLM OpenAI-compatible server.
        vllm_model: vLLM model name.
        tensorrt_base_url: Base URL for a TensorRT-LLM OpenAI-compatible server.
        tensorrt_model: TensorRT-LLM model name.
        langsmith_tracing: Whether LangSmith tracing is enabled.
        langsmith_api_key: Optional LangSmith API key.
        langfuse_public_key: Optional Langfuse public key.
        langfuse_secret_key: Optional Langfuse secret key.
        langfuse_host: Langfuse server URL.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    llm_provider: LLMProvider = Field(default=LLMProvider.OLLAMA)

    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama3.1")

    vllm_base_url: str = Field(default="http://localhost:8000/v1")
    vllm_model: str = Field(default="meta-llama/Llama-3.1-8B-Instruct")

    tensorrt_base_url: str = Field(default="http://localhost:8000/v1")
    tensorrt_model: str = Field(default="meta-llama/Llama-3.1-8B-Instruct")

    langsmith_tracing: bool = Field(default=False)
    langsmith_api_key: str = Field(default="")

    langfuse_public_key: str = Field(default="")
    langfuse_secret_key: str = Field(default="")
    langfuse_host: str = Field(default="http://localhost:3000")

    @field_validator(
        "ollama_base_url",
        "vllm_base_url",
        "tensorrt_base_url",
        "langfuse_host",
    )
    @classmethod
    def validate_url(cls, value: str) -> str:
        """Validate that URL-like settings begin with http or https.

        Args:
            value: URL string from environment or default settings.

        Returns:
            The validated URL string.

        Raises:
            ValueError: If the value does not start with http:// or https://.
        """
        if not value.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return value


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings.

    Returns:
        A validated Settings object.
    """
    return Settings()
