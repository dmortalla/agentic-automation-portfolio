"""Tests for the Sales Pipeline Lead Scoring Agent."""

import pytest

from projects.sales_pipeline_manager.agents import LeadScoringAgent
from projects.sales_pipeline_manager.schemas import (
    ApprovalStatus,
    Lead,
    LeadSource,
)
from projects.sales_pipeline_manager.state import SalesPipelineState
from shared.llm_runtime.base import BaseLLMRuntime


class SuccessfulRuntime(BaseLLMRuntime):
    """Deterministic runtime returning a safe lead score."""

    @property
    def provider_name(self) -> str:
        """Return the fake provider name."""
        return "successful"

    def generate_structured(self, prompt, output_model):
        """Return a deterministic validated lead score."""
        return output_model(
            score=87,
            decision="qualified",
            reasoning=(
                "The lead has a clear operational need, relevant authority, "
                "and an appropriate company profile."
            ),
            recommended_next_step=(
                "Prepare personalized outreach for human review."
            ),
            requires_human_review=True,
            approval_status="pending",
        )


class UnsafeReviewRuntime(BaseLLMRuntime):
    """Runtime returning a result that bypasses review."""

    @property
    def provider_name(self) -> str:
        """Return the fake provider name."""
        return "unsafe-review"

    def generate_structured(self, prompt, output_model):
        """Return an unsafe result."""
        return output_model(
            score=87,
            decision="qualified",
            reasoning=(
                "The lead appears suitable for the product and has a clear need."
            ),
            recommended_next_step="Send outreach immediately.",
            requires_human_review=False,
            approval_status="pending",
        )


class UnsafeStatusRuntime(BaseLLMRuntime):
    """Runtime returning a prematurely approved result."""

    @property
    def provider_name(self) -> str:
        """Return the fake provider name."""
        return "unsafe-status"

    def generate_structured(self, prompt, output_model):
        """Return an improperly approved result."""
        return output_model(
            score=87,
            decision="qualified",
            reasoning=(
                "The lead appears suitable for the product and has a clear need."
            ),
            recommended_next_step="Prepare outreach for review.",
            requires_human_review=True,
            approval_status="approved",
        )


def _sample_state() -> SalesPipelineState:
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

    return SalesPipelineState(lead=lead)


def test_lead_scoring_agent_exposes_name() -> None:
    """LeadScoringAgent should expose a stable agent name."""
    agent = LeadScoringAgent(runtime=SuccessfulRuntime())

    assert agent.name == "lead_scoring"


def test_lead_scoring_agent_updates_state() -> None:
    """LeadScoringAgent should store a validated recommendation."""
    state = _sample_state()
    agent = LeadScoringAgent(runtime=SuccessfulRuntime())

    result = agent.run(state)

    assert result.lead_score is not None
    assert result.lead_score.score == 87
    assert result.lead_score.decision == "qualified"
    assert result.approval_status == ApprovalStatus.PENDING
    assert result.pending_actions == [
        "Prepare personalized outreach for human review."
    ]
    assert result.completed_actions == []
    assert result.audit_events == [
        (
            "Pending action proposed: "
            "Prepare personalized outreach for human review."
        ),
        "Lead scored by lead_scoring: 87/100.",
    ]


def test_lead_scoring_agent_rejects_review_bypass() -> None:
    """Agent should reject recommendations that disable human review."""
    state = _sample_state()
    agent = LeadScoringAgent(runtime=UnsafeReviewRuntime())

    with pytest.raises(
        ValueError,
        match="must require human review",
    ):
        agent.run(state)


def test_lead_scoring_agent_rejects_premature_approval() -> None:
    """Agent should reject recommendations that begin approved."""
    state = _sample_state()
    agent = LeadScoringAgent(runtime=UnsafeStatusRuntime())

    with pytest.raises(
        ValueError,
        match="must begin as pending",
    ):
        agent.run(state)
