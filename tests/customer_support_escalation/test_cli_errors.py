"""Tests for CLI error handling."""

from projects.customer_support_escalation.cli import _run


def test_run_returns_success_for_demo_provider() -> None:
    """Demo provider should run successfully."""
    exit_code = _run("demo")

    assert exit_code == 0


def test_run_returns_failure_for_stubbed_ollama_provider() -> None:
    """Stubbed Ollama provider should return a clean failure code."""
    exit_code = _run("ollama")

    assert exit_code == 1
