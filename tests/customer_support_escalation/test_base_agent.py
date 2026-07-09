"""Tests for Customer Support base agent contract."""

import pytest

from projects.customer_support_escalation.agents.base import BaseCustomerSupportAgent
from projects.customer_support_escalation.schemas import SupportTicket
from projects.customer_support_escalation.state import CustomerSupportState


class ExampleAgent(BaseCustomerSupportAgent):
    """Concrete test agent used to verify the base contract."""

    @property
    def name(self) -> str:
        """Return the test agent name."""
        return "example_agent"

    def run(self, state: CustomerSupportState) -> CustomerSupportState:
        """Add a note and return updated state."""
        state.add_note("Example agent ran.")
        return state


def _sample_state() -> CustomerSupportState:
    """Create a reusable valid workflow state for tests."""
    ticket = SupportTicket(
        ticket_id="TICKET-001",
        customer_name="Jane Customer",
        customer_email="jane@example.com",
        subject="Cannot log in",
        message="I cannot log in to my account after resetting my password.",
        source="email",
    )
    return CustomerSupportState(ticket=ticket)


def test_base_agent_cannot_be_instantiated() -> None:
    """The abstract base agent should not be directly instantiable."""
    with pytest.raises(TypeError):
        BaseCustomerSupportAgent()


def test_concrete_agent_returns_name() -> None:
    """A concrete agent should expose a name."""
    agent = ExampleAgent()

    assert agent.name == "example_agent"


def test_concrete_agent_runs_and_updates_state() -> None:
    """A concrete agent should accept and return workflow state."""
    agent = ExampleAgent()
    state = _sample_state()

    updated_state = agent.run(state)

    assert updated_state.notes == ["Example agent ran."]
