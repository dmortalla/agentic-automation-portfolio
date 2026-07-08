"""Shared logging utilities for the agentic automation portfolio.

This module provides one standard way to create loggers across the project.
Centralized logging helps keep CLI runs, Streamlit demos, tests, and future
production deployments consistent.
"""

import logging
import sys


DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Create or return a configured logger.

    Args:
        name: Logger name, usually __name__ from the calling module.
        level: Logging level. Defaults to logging.INFO.

    Returns:
        A configured logging.Logger instance.

    Raises:
        ValueError: If the logger name is empty.
    """
    if not name or not name.strip():
        raise ValueError("Logger name must not be empty.")

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
