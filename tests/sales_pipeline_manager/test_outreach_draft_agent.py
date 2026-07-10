"""Tests for the Sales Pipeline Outreach Draft Agent."""

import pytest

from projects.sales_pipeline_manager.agents import OutreachDraftAgent
from projects.sales_pipeline_manager.schemas import (
    ApprovalStatus,
    CompanyResearch,
    Lead,
    LeadScore,
    LeadSource,
    OutreachTone,
)
from projects.sales_pipeline_manager.state import SalesPipelineState
from shared.llm_runtime.base import BaseLLMRuntime


class OutreachRuntime(BaseLLMRuntime):
    """Deterministic runtime returning a safe outreach draft."""

    @property
    def provider_name(self) -> str:
        """Return the fake provider name."""
        return "outreach"

    def generate_structured(self, prompt, output_model):
        """Return deterministic structured outreach."""
        return output_model(
            subject="Exploring support-triage automation at Northstar",
            body=(
                "Hi Jordan, I noticed Northstar Analytics is exploring ways "
                "to automate customer-support triage and operational reporting. "
                "A limited pilot could help your team assess whether AI-assisted "
                "routing reduces manual work while preserving human oversight. "
                "Would a short exploratory conversation be useful?"
            ),
            personalization_summary=[
                "Northstar Analytics is evaluating support-triage automation.",
                "Jordan Lee is the VP of Operations.",
            ],
            call_to_action="Offer a short exploratory conversation.",
            tone=OutreachTone.CONSULTATIVE,
            confidence=0.88,
            requires_human_review=True,
            approval_status=ApprovalStatus.PENDING,
        )


class UnsafeOutreachRuntime(BaseLLMRuntime):
    """Runtime returning outreach that bypasses review."""

    @property
    def provider_name(self) -> str:
        """Return the fake provider name."""
        return "unsafe-outreach"

    def generate_structured(self, prompt, output_model):
        """Return an unsafe outreach result."""
        return output_model(
            subject="Immediate automation opportunity",
            body=(
                "Hi Jordan, Northstar Analytics should immediately deploy "
                "our solution. This message has already been approved and sent."
            ),
            personalization_summary=[
                "The lead expressed interest in workflow automation."
            ],
            call_to_action="Book a meeting immediately.",
            tone=OutreachTone.PROFESSIONAL,
            confidence=0.70,
            requires_human_review=False,
            approval_status=ApprovalStatus.PENDING,
        )


def _sample_state(
    *,
    with_score: bool = True,
    with_research: bool = True,
) -> SalesPipelineState:
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

    if with_research:
        state.company_research = CompanyResearch(
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
            ],
            confidence=0.84,
            sources=[],
        )

    return state


def test_outreach_agent_exposes_name() -> None:
    """OutreachDraftAgent should expose a stable name."""
    agent = OutreachDraftAgent(runtime=OutreachRuntime())

    assert agent.name == "outreach_draft"


def test_outreach_agent_requires_lead_score() -> None:
    """Outreach drafting should require completed lead scoring."""
    agent = OutreachDraftAgent(runtime=OutreachRuntime())

    with pytest.raises(
        ValueError,
        match="Lead scoring must complete",
    ):
        agent.run(
            _sample_state(
                with_score=False,
                with_research=False,
            )
        )


def test_outreach_agent_requires_company_research() -> None:
    """Outreach drafting should require completed research."""
    agent = OutreachDraftAgent(runtime=OutreachRuntime())

    with pytest.raises(
        ValueError,
        match="Company research must complete",
    ):
        agent.run(_sample_state(with_research=False))


def test_outreach_agent_updates_state() -> None:
    """OutreachDraftAgent should store a pending review draft."""
    agent = OutreachDraftAgent(runtime=OutreachRuntime())

    result = agent.run(_sample_state())

    assert result.outreach_draft is not None
    assert result.outreach_draft.tone == OutreachTone.CONSULTATIVE
    assert result.outreach_draft.approval_status == ApprovalStatus.PENDING
    assert result.approval_status == ApprovalStatus.PENDING
    assert result.pending_actions == [
        "Review personalized outreach draft before sending."
    ]
    assert result.completed_actions == []
    assert result.audit_events == [
        (
            "Pending action proposed: "
            "Review personalized outreach draft before sending."
        ),
        "Outreach draft created by outreach_draft.",
    ]


def test_outreach_agent_rejects_review_bypass() -> None:
    """Outreach drafts must remain subject to human approval."""
    agent = OutreachDraftAgent(runtime=UnsafeOutreachRuntime())

    with pytest.raises(
        ValueError,
        match="must require human review",
    ):
        agent.run(_sample_state())
