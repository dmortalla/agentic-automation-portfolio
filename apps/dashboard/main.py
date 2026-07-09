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


def render_metrics() -> None:
    """Render portfolio status metrics."""
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Tests", "74 passing")
    col2.metric("Runtime Providers", "3")
    col3.metric("Quality Gates", "Ruff / Pytest / Compile")
    col4.metric("CI", "GitHub Actions")


def main() -> None:
    """Render the portfolio dashboard."""
    bootstrap_repo_root()

    from projects.customer_support_escalation.schemas import SupportTicket
    from projects.customer_support_escalation.workflow import classify_support_ticket
    from shared.config.settings import Settings
    from shared.llm_runtime.factory import create_runtime
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
        "LangGraph workflows, structured outputs, and automated quality gates."
    )

    render_metrics()

    st.divider()

    tab_overview, tab_demo, tab_config = st.tabs(
        ["Overview", "Live Customer Support Demo", "Runtime Configuration"]
    )

    with tab_overview:
        st.header("Implemented Vertical Slice")

        st.write(
            "This dashboard demonstrates the completed customer support escalation "
            "vertical slice: form input, Pydantic validation, runtime injection, "
            "LangGraph orchestration, and structured classification output."
        )

        capabilities = [
            "Runtime abstraction",
            "Ollama runtime",
            "vLLM runtime",
            "TensorRT runtime",
            "Runtime contract tests",
            "LangGraph customer-support workflow",
            "Structured Pydantic outputs",
            "GitHub Actions CI",
            "Pre-commit hooks",
        ]

        for capability in capabilities:
            st.success(capability)

    with tab_demo:
        st.header("Live Customer Support Escalation Demo")

        with st.form("support_ticket_form"):
            ticket_id = st.text_input("Ticket ID", value="TICKET-1001")
            customer_name = st.text_input("Customer Name", value="Jordan Lee")
            customer_email = st.text_input(
                "Customer Email",
                value="jordan.lee@example.com",
            )
            subject = st.text_input(
                "Subject",
                value="Account locked after failed login attempts",
            )
            source = st.selectbox("Source", ["email", "web", "chat", "api"])

            message = st.text_area(
                "Customer Message",
                value=(
                    "I cannot access my account after several failed login attempts. "
                    "Password reset is not working, and I need access urgently because "
                    "my billing deadline is today."
                ),
                height=160,
            )

            submitted = st.form_submit_button("Run LangGraph Workflow")

        if submitted:
            try:
                ticket = SupportTicket(
                    ticket_id=ticket_id,
                    customer_name=customer_name,
                    customer_email=customer_email,
                    subject=subject,
                    message=message,
                    source=source,
                )

                runtime = create_runtime(settings)
                final_state = classify_support_ticket(ticket=ticket, runtime=runtime)

                st.success("Workflow completed successfully.")

                st.subheader("Classification")
                st.json(
                    final_state.classification.model_dump()
                    if final_state.classification
                    else {}
                )

                st.subheader("Workflow Notes")
                st.json(final_state.notes)

                st.subheader("Full Final State")
                st.json(final_state.model_dump())

            except Exception as exc:
                st.error("Workflow execution failed.")
                st.exception(exc)

    with tab_config:
        st.header("Runtime Configuration")

        st.json(
            {
                "active_provider": settings.llm_provider.value,
                "available_providers": [provider.value for provider in LLMProvider],
                "ollama_base_url": settings.ollama_base_url,
                "ollama_model": settings.ollama_model,
                "vllm_base_url": settings.vllm_base_url,
                "vllm_model": settings.vllm_model,
                "tensorrt_base_url": settings.tensorrt_base_url,
                "tensorrt_model": settings.tensorrt_model,
            }
        )

        st.header("Next Roadmap")
        st.json(
            [
                "Dashboard polish",
                "Document compliance checker workflow",
                "Sales pipeline manager workflow",
                "Multi-agent expansion",
                "Professional portfolio deliverables",
            ]
        )


if __name__ == "__main__":
    main()
