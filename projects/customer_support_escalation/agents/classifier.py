"""Classifier agent."""

from projects.customer_support_escalation.agents.base import (
    BaseCustomerSupportAgent,
)
from projects.customer_support_escalation.prompts import (
    build_classification_prompt,
)
from projects.customer_support_escalation.state import (
    CustomerSupportState,
)
from shared.llm_runtime.base import BaseLLMRuntime
from projects.customer_support_escalation.schemas import (
    TicketClassification,
)


class ClassifierAgent(BaseCustomerSupportAgent):
    """AI agent responsible for ticket classification."""

    def __init__(self, runtime: BaseLLMRuntime) -> None:
        """Initialize the classifier agent.

        Args:
            runtime: Runtime used to perform structured generation.
        """
        self._runtime = runtime

    @property
    def name(self) -> str:
        """Return the agent name."""
        return "classifier"

    def run(
        self,
        state: CustomerSupportState,
    ) -> CustomerSupportState:
        """Run ticket classification."""
        prompt = build_classification_prompt(state.ticket)

        classification = self._runtime.generate_structured(
            prompt=prompt,
            output_model=TicketClassification,
        )

        state.classification = classification
        state.add_note("Ticket classified.")

        return state
