"""Base agent contract for the Customer Support Escalation System."""

from abc import ABC, abstractmethod

from projects.customer_support_escalation.state import CustomerSupportState


class BaseCustomerSupportAgent(ABC):
    """Abstract base class for customer support workflow agents.

    Agents receive a CustomerSupportState, perform one focused task, and
    return the updated state. This keeps agent behavior consistent across
    classifier, sentiment, escalation, RAG, and supervisor nodes.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the human-readable agent name."""

    @abstractmethod
    def run(self, state: CustomerSupportState) -> CustomerSupportState:
        """Run the agent against the current workflow state.

        Args:
            state: Current customer support workflow state.

        Returns:
            Updated customer support workflow state.
        """
