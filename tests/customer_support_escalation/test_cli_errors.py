"""Tests for CLI error handling."""

from projects.customer_support_escalation import cli
from projects.customer_support_escalation.cli import _run
from shared.llm_runtime.base import BaseLLMRuntime
from shared.llm_runtime.exceptions import LLMRuntimeError


class FailingRuntime(BaseLLMRuntime):
    """Runtime that always fails for CLI error testing."""

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "failing"

    def generate_structured(self, prompt, output_model):
        """Raise a runtime error."""
        raise LLMRuntimeError("Test runtime failure.")


def test_run_returns_success_for_demo_provider() -> None:
    """Demo provider should run successfully."""
    exit_code = _run("demo")

    assert exit_code == 0


def test_run_returns_failure_for_runtime_error(monkeypatch) -> None:
    """Runtime errors should return a clean failure code."""

    def fake_create_runtime(provider: str) -> BaseLLMRuntime:
        return FailingRuntime()

    monkeypatch.setattr(cli, "_create_runtime", fake_create_runtime)

    exit_code = _run("ollama")

    assert exit_code == 1
