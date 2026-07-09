"""Tests for the Customer Support workflow runner."""

import pytest

from projects.customer_support_escalation.schemas import SupportTicket
from projects.customer_support_escalation.state import CustomerSupportState
from projects.customer_support_escalation.workflow import classify_support_ticket
from shared.llm_runtime.base import BaseLLMRuntime


class FakeRuntime(BaseLLMRuntime):
    """Fake runtime used to test workflow execution."""

    @property
    def provider_name(self) -> str:
        """Return fake provider name."""
        return "fake"

    def generate_structured(self, prompt, output_model):
        """Return deterministic classification output."""
        return output_model(
            category="technical",
            priority="high",
            confidence=0.98,
            reasoning="Customer cannot access the application.",
            requires_human_review=False,
        )


def _sample_ticket() -> SupportTicket:
    """Create reusable support ticket."""
    return SupportTicket(
        ticket_id="TICKET-001",
        customer_name="Jane Customer",
        customer_email="jane@example.com",
        subject="Cannot login",
        message="I cannot login after changing my password.",
        source="email",
    )


def test_classify_support_ticket_returns_final_state() -> None:
    """Workflow runner should return final CustomerSupportState."""
    result = classify_support_ticket(
        ticket=_sample_ticket(),
        runtime=FakeRuntime(),
    )

    assert isinstance(result, CustomerSupportState)
    assert result.classification is not None
    assert result.classification.category == "technical"
    assert result.notes == ["Ticket classified."]


def test_classify_support_ticket_rejects_missing_ticket() -> None:
    """Workflow runner should reject missing ticket."""
    with pytest.raises(ValueError):
        classify_support_ticket(ticket=None, runtime=FakeRuntime())


def test_classify_support_ticket_rejects_missing_runtime() -> None:
    """Workflow runner should reject missing runtime."""
    with pytest.raises(ValueError):
        classify_support_ticket(ticket=_sample_ticket(), runtime=None)
