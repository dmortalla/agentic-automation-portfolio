"""Streamlit dashboard for the Agentic Automation Portfolio."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


def bootstrap_repo_root() -> None:
    """Ensure repo-root packages are importable when Streamlit runs this file."""
    repo_root = Path(__file__).resolve().parents[2]
    repo_root_str = str(repo_root)

    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)


def main() -> None:
    """Render the portfolio dashboard."""
    bootstrap_repo_root()

    from shared.config.settings import Settings
    from shared.models.enums import LLMProvider

    settings = Settings()

    st.set_page_config(
        page_title="Agentic Automation Portfolio",
        page_icon="AI",
        layout="wide",
    )

    st.title("Agentic Automation Portfolio")
    st.caption(
        "Production-style AI automation system with runtime abstraction, "
        "LangGraph workflows, and quality gates."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Tests", "74 passing")
    col2.metric("Runtime Providers", "3")
    col3.metric("Quality Gates", "Ruff / Pytest / Compile")
    col4.metric("CI", "GitHub Actions")

    st.divider()

    st.header("Runtime Configuration")
    st.json(
        {
            "active_provider": settings.llm_provider.value,
            "available_providers": [provider.value for provider in LLMProvider],
        }
    )

    st.header("Implemented Capabilities")

    capabilities = [
        "Runtime abstraction",
        "Ollama runtime",
        "vLLM runtime",
        "TensorRT runtime",
        "Runtime contract tests",
        "LangGraph customer-support workflow",
        "CLI",
        "GitHub Actions CI",
        "Pre-commit hooks",
    ]

    for capability in capabilities:
        st.success(capability)

    st.header("Next Roadmap")
    st.json(
        [
            "Multi-agent expansion",
            "Professional portfolio deliverables",
            "Dashboard polish and live workflow demos",
        ]
    )


if __name__ == "__main__":
    main()
