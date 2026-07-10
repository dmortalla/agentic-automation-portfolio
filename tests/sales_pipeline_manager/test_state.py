"""Tests for AI Sales Pipeline Manager workflow state."""

import pytest
from pydantic import ValidationError

from projects.sales_pipeline_manager.schemas import (
    ApprovalStatus,
    Lead,
    LeadSource,
)
from projects.sales_pipeline_manager.state import SalesPipelineState
from shared.state.base import WorkflowStatus


def _sample_lead() -> Lead:
    """Create a reusable valid lead."""
    return Lead(
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


def test_state_starts_pending_and_requires_review() -> None:
    """Sales pipeline state should begin safely with no approved actions."""
    state = SalesPipelineState(lead=_sample_lead())

    assert state.status == WorkflowStatus.PENDING
    assert state.approval_status == ApprovalStatus.PENDING
    assert state.lead_score is None
    assert state.pending_actions == []
    assert state.completed_actions == []
    assert state.audit_events == []


def test_add_pending_action_records_audit_event() -> None:
    """Proposed actions should remain pending and be audited."""
    state = SalesPipelineState(lead=_sample_lead())

    state.add_pending_action(" Draft personalized outreach. ")

    assert state.pending_actions == ["Draft personalized outreach."]
    assert state.audit_events == [
        "Pending action proposed: Draft personalized outreach."
    ]


def test_complete_action_requires_human_approval() -> None:
    """External actions must not complete before human approval."""
    state = SalesPipelineState(lead=_sample_lead())
    state.add_pending_action("Update CRM lead status.")

    with pytest.raises(ValueError, match="require human approval"):
        state.complete_action("Update CRM lead status.")


def test_approved_pending_action_can_be_completed() -> None:
    """An approved pending action should move to completed actions."""
    state = SalesPipelineState(lead=_sample_lead())
    state.add_pending_action("Update CRM lead status.")
    state.approve("Approved after reviewing the recommendation.")

    state.complete_action("Update CRM lead status.")

    assert state.approval_status == ApprovalStatus.APPROVED
    assert state.pending_actions == []
    assert state.completed_actions == ["Update CRM lead status."]
    assert state.reviewer_feedback == (
        "Approved after reviewing the recommendation."
    )


def test_request_changes_records_feedback() -> None:
    """Reviewers should be able to request revisions."""
    state = SalesPipelineState(lead=_sample_lead())

    state.request_changes(" Make the outreach less promotional. ")

    assert state.approval_status == ApprovalStatus.CHANGES_REQUESTED
    assert state.reviewer_feedback == "Make the outreach less promotional."
    assert state.audit_events == ["Human reviewer requested changes."]


def test_blank_reviewer_feedback_is_rejected() -> None:
    """Blank reviewer feedback should fail validation."""
    with pytest.raises(ValidationError):
        SalesPipelineState(
            lead=_sample_lead(),
            reviewer_feedback="   ",
        )
