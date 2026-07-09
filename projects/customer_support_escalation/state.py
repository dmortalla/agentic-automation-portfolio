"""Workflow state for the Customer Support Escalation System."""

from pydantic import Field

from projects.customer_support_escalation.schemas import SupportTicket, TicketClassification
from shared.state.base import BaseWorkflowState


class CustomerSupportState(BaseWorkflowState):
    """State passed through the customer support LangGraph workflow.

    Attributes:
        ticket: Original support ticket submitted to the workflow.
        classification: Structured classification result, if available.
        notes: Internal workflow notes useful for debugging and review.
    """

    ticket: SupportTicket
    classification: TicketClassification | None = Field(default=None)
    notes: list[str] = Field(default_factory=list)

    def add_note(self, message: str) -> None:
        """Add an internal workflow note.

        Args:
            message: Note message to record.

        Raises:
            ValueError: If the message is blank.
        """
        cleaned_message = message.strip()

        if not cleaned_message:
            raise ValueError("Note message must not be blank.")

        self.notes.append(cleaned_message)
