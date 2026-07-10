"""Workflow state for the AI Sales Pipeline Manager."""

from pydantic import Field, field_validator

from projects.sales_pipeline_manager.schemas import (
    ApprovalStatus,
    Lead,
    LeadScore,
)
from shared.state.base import BaseWorkflowState


class SalesPipelineState(BaseWorkflowState):
    """State passed through the Sales Pipeline LangGraph workflow.

    Attributes:
        lead: Original validated lead.
        lead_score: Structured qualification result, when available.
        approval_status: Current human-review status.
        reviewer_feedback: Optional feedback supplied by a reviewer.
        pending_actions: Proposed external actions awaiting approval.
        completed_actions: Approved actions recorded after execution.
        audit_events: Human-readable workflow audit events.
    """

    lead: Lead
    lead_score: LeadScore | None = Field(default=None)
    approval_status: ApprovalStatus = Field(default=ApprovalStatus.PENDING)
    reviewer_feedback: str | None = Field(default=None, min_length=1)
    pending_actions: list[str] = Field(default_factory=list)
    completed_actions: list[str] = Field(default_factory=list)
    audit_events: list[str] = Field(default_factory=list)

    @field_validator("reviewer_feedback")
    @classmethod
    def strip_optional_feedback(cls, value: str | None) -> str | None:
        """Strip reviewer feedback and reject blank strings."""
        if value is None:
            return None

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Reviewer feedback must not be blank when provided.")

        return cleaned_value

    def add_pending_action(self, action: str) -> None:
        """Record an external action that requires human approval."""
        cleaned_action = self._clean_event_text(action, "Pending action")
        self.pending_actions.append(cleaned_action)
        self.add_audit_event(f"Pending action proposed: {cleaned_action}")

    def approve(self, feedback: str | None = None) -> None:
        """Approve pending recommendations without executing them."""
        self.approval_status = ApprovalStatus.APPROVED

        if feedback is not None:
            self.reviewer_feedback = self._clean_event_text(
                feedback,
                "Reviewer feedback",
            )

        self.add_audit_event("Human reviewer approved the recommendations.")

    def request_changes(self, feedback: str) -> None:
        """Request revisions before any external action is allowed."""
        cleaned_feedback = self._clean_event_text(
            feedback,
            "Reviewer feedback",
        )
        self.approval_status = ApprovalStatus.CHANGES_REQUESTED
        self.reviewer_feedback = cleaned_feedback
        self.add_audit_event("Human reviewer requested changes.")

    def reject(self, feedback: str | None = None) -> None:
        """Reject the recommendations and prevent external actions."""
        self.approval_status = ApprovalStatus.REJECTED

        if feedback is not None:
            self.reviewer_feedback = self._clean_event_text(
                feedback,
                "Reviewer feedback",
            )

        self.add_audit_event("Human reviewer rejected the recommendations.")

    def complete_action(self, action: str) -> None:
        """Record an approved action as completed.

        Raises:
            ValueError: If approval has not been granted or the action is unknown.
        """
        if self.approval_status != ApprovalStatus.APPROVED:
            raise ValueError("External actions require human approval.")

        cleaned_action = self._clean_event_text(action, "Completed action")

        if cleaned_action not in self.pending_actions:
            raise ValueError("Only pending actions may be completed.")

        self.pending_actions.remove(cleaned_action)
        self.completed_actions.append(cleaned_action)
        self.add_audit_event(f"Approved action completed: {cleaned_action}")

    def add_audit_event(self, event: str) -> None:
        """Append a cleaned event to the audit trail."""
        cleaned_event = self._clean_event_text(event, "Audit event")
        self.audit_events.append(cleaned_event)

    @staticmethod
    def _clean_event_text(value: str, field_name: str) -> str:
        """Strip workflow text and reject blank values."""
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(f"{field_name} must not be blank.")

        return cleaned_value
