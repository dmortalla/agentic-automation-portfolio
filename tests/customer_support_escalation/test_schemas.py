"""Tests for Customer Support schemas."""

import pytest
from pydantic import ValidationError

from projects.customer_support_escalation.schemas import SupportTicket


def test_support_ticket_accepts_valid_data() -> None:
    """SupportTicket should accept valid ticket data."""
    ticket = SupportTicket(
        ticket_id="TICKET-001",
        customer_name="Jane Customer",
        customer_email="jane@example.com",
        subject="Cannot log in",
        message="I cannot log in to my account after resetting my password.",
        source="email",
    )

    assert ticket.ticket_id == "TICKET-001"
    assert ticket.customer_name == "Jane Customer"
    assert ticket.source == "email"


def test_support_ticket_strips_whitespace() -> None:
    """SupportTicket should strip leading and trailing whitespace."""
    ticket = SupportTicket(
        ticket_id=" TICKET-002 ",
        customer_name=" John Customer ",
        customer_email=" john@example.com ",
        subject=" Billing issue ",
        message=" I was charged twice for my monthly subscription. ",
        source=" form ",
    )

    assert ticket.ticket_id == "TICKET-002"
    assert ticket.customer_name == "John Customer"
    assert ticket.source == "form"


def test_support_ticket_rejects_blank_required_field() -> None:
    """SupportTicket should reject blank required fields."""
    with pytest.raises(ValidationError):
        SupportTicket(
            ticket_id="   ",
            customer_name="Jane Customer",
            customer_email="jane@example.com",
            subject="Cannot log in",
            message="I cannot log in to my account after resetting my password.",
            source="email",
        )


def test_support_ticket_rejects_short_message() -> None:
    """SupportTicket should reject messages that are too short."""
    with pytest.raises(ValidationError):
        SupportTicket(
            ticket_id="TICKET-003",
            customer_name="Jane Customer",
            customer_email="jane@example.com",
            subject="Help",
            message="Too short",
            source="email",
        )
