"""Agents for the AI Sales Pipeline Manager."""

from projects.sales_pipeline_manager.prompts import (
    build_company_research_prompt,
    build_lead_scoring_prompt,
)
from projects.sales_pipeline_manager.schemas import (
    ApprovalStatus,
    CompanyResearch,
    LeadScore,
)
from projects.sales_pipeline_manager.state import SalesPipelineState
from shared.llm_runtime.base import BaseLLMRuntime


class LeadScoringAgent:
    """Agent that evaluates and qualifies a validated sales lead."""

    def __init__(self, runtime: BaseLLMRuntime) -> None:
        """Initialize the lead-scoring agent."""
        self._runtime = runtime

    @property
    def name(self) -> str:
        """Return the agent name."""
        return "lead_scoring"

    def run(self, state: SalesPipelineState) -> SalesPipelineState:
        """Score the current lead and update workflow state."""
        prompt = build_lead_scoring_prompt(state.lead)

        lead_score = self._runtime.generate_structured(
            prompt=prompt,
            output_model=LeadScore,
        )

        if not lead_score.requires_human_review:
            raise ValueError(
                "Lead-scoring recommendations must require human review."
            )

        if lead_score.approval_status != ApprovalStatus.PENDING:
            raise ValueError(
                "New lead-scoring recommendations must begin as pending."
            )

        state.lead_score = lead_score
        state.approval_status = ApprovalStatus.PENDING
        state.add_pending_action(lead_score.recommended_next_step)
        state.add_audit_event(
            f"Lead scored by {self.name}: {lead_score.score}/100."
        )

        return state


class ResearchAgent:
    """Agent that produces constrained company research."""

    def __init__(self, runtime: BaseLLMRuntime) -> None:
        """Initialize the research agent."""
        self._runtime = runtime

    @property
    def name(self) -> str:
        """Return the agent name."""
        return "research"

    def run(self, state: SalesPipelineState) -> SalesPipelineState:
        """Research the scored lead and update workflow state.

        Raises:
            ValueError: If lead scoring has not completed or review is bypassed.
        """
        if state.lead_score is None:
            raise ValueError(
                "Lead scoring must complete before company research."
            )

        prompt = build_company_research_prompt(
            lead=state.lead,
            lead_score=state.lead_score,
        )

        research = self._runtime.generate_structured(
            prompt=prompt,
            output_model=CompanyResearch,
        )

        if not research.requires_human_review:
            raise ValueError(
                "Company research must require human review."
            )

        state.company_research = research
        state.add_audit_event(
            f"Company research completed by {self.name}."
        )

        return state
