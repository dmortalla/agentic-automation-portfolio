"""Tests for the Sales Pipeline Research Agent."""

import pytest

from projects.sales_pipeline_manager.agents import ResearchAgent
from projects.sales_pipeline_manager.schemas import (
    Lead,
    LeadScore,
    LeadSource,
)
from projects.sales_pipeline_manager.state import SalesPipelineState
from shared.llm_runtime.base import BaseLLMRuntime


class ResearchRuntime(BaseLLMRuntime):
    """Deterministic runtime returning safe company research."""

    @property
    def provider_name(self) -> str:
        """Return the fake provider name."""
        return "research"

    def generate_structured(self, prompt, output_model):
        """Return deterministic structured research."""
        return output_model(
            summary=(
                "Northstar Analytics is evaluating automation for customer "
                "support triage and operational reporting."
            ),
            pain_points=[
                "Manual support-ticket triage",
                "Time-consuming operational reporting",
            ],
            opportunities=[
                "Evaluate an AI-assisted triage pilot",
                "Review reporting workflow requirements",
            ],
            confidence=0.84,
            sources=[],
            requires_human_review=True,
        )


class UnsafeResearchRuntime(BaseLLMRuntime):
    """Runtime returning research that bypasses human review."""

    @property
    def provider_name(self) -> str:
        """Return the fake provider name."""
        return "unsafe-research"

    def generate_structured(self, prompt, output_model):
        """Return unsafe structured research."""
        return output_model(
            summary=(
                "Northstar Analytics may benefit from workflow automation "
                "based on the supplied lead information."
            ),
            pain_points=["Manual workflow processing"],
            opportunities=["Explore a limited pilot"],
            confidence=0.70,
            sources=[],
            requires_human_review=False,
        )


def _sample_state(with_score: bool = True) -> SalesPipelineState:
    """Create reusable Sales Pipeline state."""
    lead = Lead(
        lead_id="LEAD-001",
        company_name="Northstar Analytics",
        contact_name="Jordan Lee",
        contact_email="jordan@northstar.example",
        job_title="VP of Operations",
        industry="Analytics",
        company_size=250,
        source=LeadSource.WEBSITE,
        expressed_need=(
            "The company wants to automate customer-support triage and reporting."
        ),
    )

    state = SalesPipelineState(lead=lead)

    if with_score:
        state.lead_score = LeadScore(
            score=87,
            decision="qualified",
            reasoning=(
                "The lead has a clear operational need and relevant authority."
            ),
            recommended_next_step=(
                "Prepare personalized outreach for human review."
            ),
        )

    return state


def test_research_agent_exposes_name() -> None:
    """ResearchAgent should expose a stable name."""
    agent = ResearchAgent(runtime=ResearchRuntime())

    assert agent.name == "research"


def test_research_agent_requires_lead_score() -> None:
    """Research should not run before lead scoring."""
    agent = ResearchAgent(runtime=ResearchRuntime())

    with pytest.raises(
        ValueError,
        match="Lead scoring must complete",
    ):
        agent.run(_sample_state(with_score=False))


def test_research_agent_updates_state() -> None:
    """ResearchAgent should store validated company research."""
    agent = ResearchAgent(runtime=ResearchRuntime())

    result = agent.run(_sample_state())

    assert result.company_research is not None
    assert result.company_research.confidence == 0.84
    assert result.company_research.sources == []
    assert result.audit_events == [
        "Company research completed by research."
    ]


def test_research_agent_rejects_review_bypass() -> None:
    """Research must remain subject to human verification."""
    agent = ResearchAgent(runtime=UnsafeResearchRuntime())

    with pytest.raises(
        ValueError,
        match="must require human review",
    ):
        agent.run(_sample_state())
