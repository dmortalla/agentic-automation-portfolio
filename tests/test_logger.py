"""Tests for shared logging utilities."""

import logging

import pytest

from shared.logging.logger import DEFAULT_LOG_FORMAT, get_logger


def test_get_logger_returns_logger() -> None:
    """get_logger should return a configured Logger instance."""
    logger = get_logger("test_logger")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"


def test_get_logger_adds_handler() -> None:
    """get_logger should attach at least one handler."""
    logger = get_logger("test_logger_with_handler")

    assert len(logger.handlers) >= 1


def test_get_logger_reuses_handlers() -> None:
    """Calling get_logger twice should not duplicate handlers."""
    logger_one = get_logger("test_logger_reuse")
    handler_count = len(logger_one.handlers)

    logger_two = get_logger("test_logger_reuse")

    assert len(logger_two.handlers) == handler_count


def test_empty_logger_name_raises_error() -> None:
    """An empty logger name should fail fast."""
    with pytest.raises(ValueError):
        get_logger("")


def test_default_log_format_is_defined() -> None:
    """The default log format should include useful fields."""
    assert "%(levelname)s" in DEFAULT_LOG_FORMAT
    assert "%(name)s" in DEFAULT_LOG_FORMAT
    assert "%(message)s" in DEFAULT_LOG_FORMAT
