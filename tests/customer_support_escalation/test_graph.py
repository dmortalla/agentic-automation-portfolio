"""Tests for the Customer Support LangGraph workflow."""

from projects.customer_support_escalation.graph import build_customer_support_graph
from projects.customer_support_escalation.schemas import SupportTicket
from projects.customer_support_escalation.state import CustomerSupportState
from shared.llm_runtime.base import BaseLLMRuntime


class FakeRuntime(BaseLLMRuntime):
    """Fake runtime used to test graph execution."""

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


def _sample_state() -> CustomerSupportState:
    """Create reusable test workflow state."""
    ticket = SupportTicket(
        ticket_id="TICKET-001",
        customer_name="Jane Customer",
        customer_email="jane@example.com",
        subject="Cannot login",
        message="I cannot login after changing my password.",
        source="email",
    )
    return CustomerSupportState(ticket=ticket)


def test_customer_support_graph_executes_classifier_node() -> None:
    """Graph should execute classifier node and update state."""
    graph = build_customer_support_graph(runtime=FakeRuntime())
    state = _sample_state()

    result = graph.invoke(state)

    assert result["classification"] is not None
    assert result["classification"].category == "technical"
    assert result["notes"] == ["Ticket classified."]
