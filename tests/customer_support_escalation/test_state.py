"""Tests for Customer Support workflow state."""

import pytest

from projects.customer_support_escalation.schemas import SupportTicket, TicketClassification
from projects.customer_support_escalation.state import CustomerSupportState
from shared.state.base import WorkflowStatus


def _sample_ticket() -> SupportTicket:
    """Create a reusable valid support ticket for tests."""
    return SupportTicket(
        ticket_id="TICKET-001",
        customer_name="Jane Customer",
        customer_email="jane@example.com",
        subject="Cannot log in",
        message="I cannot log in to my account after resetting my password.",
        source="email",
    )


def test_customer_support_state_starts_pending() -> None:
    """CustomerSupportState should start with pending status."""
    state = CustomerSupportState(ticket=_sample_ticket())

    assert state.status == WorkflowStatus.PENDING
    assert state.classification is None
    assert state.errors == []
    assert state.notes == []


def test_customer_support_state_accepts_classification() -> None:
    """CustomerSupportState should store a classification result."""
    classification = TicketClassification(
        category="technical",
        priority="high",
        confidence=0.91,
        reasoning="The customer cannot access the application after password reset.",
        requires_human_review=True,
    )
    state = CustomerSupportState(ticket=_sample_ticket(), classification=classification)

    assert state.classification == classification


def test_add_note_records_clean_note() -> None:
    """add_note should strip whitespace and store the note."""
    state = CustomerSupportState(ticket=_sample_ticket())

    state.add_note(" Classification completed. ")

    assert state.notes == ["Classification completed."]


def test_add_note_rejects_blank_note() -> None:
    """add_note should reject blank note messages."""
    state = CustomerSupportState(ticket=_sample_ticket())

    with pytest.raises(ValueError):
        state.add_note("   ")


def test_add_error_records_error_and_marks_failed() -> None:
    """add_error should record an error and mark the state as failed."""
    state = CustomerSupportState(ticket=_sample_ticket())

    state.add_error(" Classifier failed. ")

    assert state.errors == ["Classifier failed."]
    assert state.status == WorkflowStatus.FAILED


def test_add_error_rejects_blank_error() -> None:
    """add_error should reject blank error messages."""
    state = CustomerSupportState(ticket=_sample_ticket())

    with pytest.raises(ValueError):
        state.add_error("   ")
