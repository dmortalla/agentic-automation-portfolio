"""Tests for the classifier agent."""

from projects.customer_support_escalation.agents.classifier import (
    ClassifierAgent,
)
from projects.customer_support_escalation.schemas import (
    SupportTicket,
    TicketClassification,
)
from projects.customer_support_escalation.state import (
    CustomerSupportState,
)
from shared.llm_runtime.base import BaseLLMRuntime


class FakeRuntime(BaseLLMRuntime):
    """Simple fake runtime for classifier tests."""

    @property
    def provider_name(self) -> str:
        return "fake"

    def generate_structured(self, prompt, output_model):
        return output_model(
            category="technical",
            priority="high",
            confidence=0.98,
            reasoning="Customer cannot access the application.",
            requires_human_review=False,
        )


def test_classifier_updates_state() -> None:
    """Classifier should populate workflow state."""
    runtime = FakeRuntime()
    agent = ClassifierAgent(runtime)

    ticket = SupportTicket(
        ticket_id="1",
        customer_name="Jane",
        customer_email="jane@example.com",
        subject="Cannot login",
        message="I cannot login after changing my password.",
        source="email",
    )

    state = CustomerSupportState(ticket=ticket)

    updated = agent.run(state)

    assert isinstance(updated.classification, TicketClassification)
    assert updated.classification.category == "technical"
    assert updated.notes == ["Ticket classified."]
