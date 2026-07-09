"""Tests for the Customer Support CLI."""

from projects.customer_support_escalation.cli import main


def test_cli_main_exists() -> None:
    """CLI should expose a callable main function."""
    assert callable(main)
