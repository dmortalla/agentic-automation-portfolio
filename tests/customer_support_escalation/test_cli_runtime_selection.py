"""Tests for CLI runtime selection."""

from projects.customer_support_escalation.cli import DemoRuntime, _create_runtime


def test_demo_runtime_is_selected() -> None:
    """Demo provider should return DemoRuntime."""
    runtime = _create_runtime("demo")

    assert isinstance(runtime, DemoRuntime)
    assert runtime.provider_name == "demo"


def test_ollama_runtime_is_selected() -> None:
    """Ollama provider should build an Ollama runtime."""
    runtime = _create_runtime("ollama")

    assert runtime.provider_name == "ollama"


def test_vllm_runtime_is_selected() -> None:
    """vLLM provider should build a vLLM runtime."""
    runtime = _create_runtime("vllm")

    assert runtime.provider_name == "vllm"


def test_tensorrt_runtime_is_selected() -> None:
    """TensorRT provider should build a TensorRT runtime."""
    runtime = _create_runtime("tensorrt")

    assert runtime.provider_name == "tensorrt"
