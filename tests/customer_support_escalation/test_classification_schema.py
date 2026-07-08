"""Tests for Customer Support classification schemas."""

import pytest
from pydantic import ValidationError

from projects.customer_support_escalation.schemas import (
    TicketCategory,
    TicketClassification,
    TicketPriority,
)


def test_ticket_classification_accepts_valid_data() -> None:
    """TicketClassification should accept valid classification data."""
    classification = TicketClassification(
        category="technical",
        priority="high",
        confidence=0.91,
        reasoning="The customer cannot access the application after a password reset.",
        requires_human_review=True,
    )

    assert classification.category == TicketCategory.TECHNICAL
    assert classification.priority == TicketPriority.HIGH
    assert classification.confidence == 0.91
    assert classification.requires_human_review is True


def test_ticket_classification_strips_reasoning_whitespace() -> None:
    """TicketClassification should strip reasoning whitespace."""
    classification = TicketClassification(
        category="billing",
        priority="medium",
        confidence=0.75,
        reasoning=" Customer reports a duplicate subscription charge. ",
    )

    assert classification.reasoning == "Customer reports a duplicate subscription charge."


def test_ticket_classification_rejects_invalid_category() -> None:
    """TicketClassification should reject unsupported categories."""
    with pytest.raises(ValidationError):
        TicketClassification(
            category="refund",
            priority="medium",
            confidence=0.75,
            reasoning="Customer is asking for a refund on a duplicate charge.",
        )


def test_ticket_classification_rejects_invalid_priority() -> None:
    """TicketClassification should reject unsupported priorities."""
    with pytest.raises(ValidationError):
        TicketClassification(
            category="billing",
            priority="critical",
            confidence=0.75,
            reasoning="Customer is blocked by a billing issue.",
        )


def test_ticket_classification_rejects_confidence_below_zero() -> None:
    """TicketClassification should reject confidence below 0.0."""
    with pytest.raises(ValidationError):
        TicketClassification(
            category="technical",
            priority="high",
            confidence=-0.01,
            reasoning="Customer cannot access the product.",
        )


def test_ticket_classification_rejects_confidence_above_one() -> None:
    """TicketClassification should reject confidence above 1.0."""
    with pytest.raises(ValidationError):
        TicketClassification(
            category="technical",
            priority="high",
            confidence=1.01,
            reasoning="Customer cannot access the product.",
        )


def test_ticket_classification_rejects_short_reasoning() -> None:
    """TicketClassification should reject short reasoning."""
    with pytest.raises(ValidationError):
        TicketClassification(
            category="general",
            priority="low",
            confidence=0.5,
            reasoning="short",
        )
