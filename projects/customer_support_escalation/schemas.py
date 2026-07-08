"""Schemas for the Customer Support Escalation System."""

from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class TicketCategory(StrEnum):
    """Supported ticket categories."""

    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    PRODUCT = "product"
    GENERAL = "general"


class TicketPriority(StrEnum):
    """Supported ticket priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class SupportTicket(BaseModel):
    """Customer support ticket submitted for agent classification.

    Attributes:
        ticket_id: Unique ticket identifier.
        customer_name: Name of the customer submitting the ticket.
        customer_email: Customer email address.
        subject: Short ticket subject.
        message: Full customer message.
        source: Intake source such as email, form, or webhook.
    """

    ticket_id: str = Field(..., min_length=1)
    customer_name: str = Field(..., min_length=1)
    customer_email: str = Field(..., min_length=3)
    subject: str = Field(..., min_length=1)
    message: str = Field(..., min_length=10)
    source: str = Field(default="email", min_length=1)

    @field_validator(
        "ticket_id",
        "customer_name",
        "customer_email",
        "subject",
        "message",
        "source",
    )
    @classmethod
    def strip_and_validate_not_blank(cls, value: str) -> str:
        """Strip whitespace and reject blank values.

        Args:
            value: Raw string value.

        Returns:
            Cleaned string value.

        Raises:
            ValueError: If the value is blank after stripping whitespace.
        """
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Value must not be blank.")

        return cleaned_value


class TicketClassification(BaseModel):
    """Structured classification result for a support ticket.

    Attributes:
        category: Business category assigned to the ticket.
        priority: Urgency level assigned to the ticket.
        confidence: Model or rule confidence from 0.0 to 1.0.
        reasoning: Short explanation for the classification.
        requires_human_review: Whether a human should review the classification.
    """

    category: TicketCategory
    priority: TicketPriority
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str = Field(..., min_length=10)
    requires_human_review: bool = Field(default=False)

    @field_validator("reasoning")
    @classmethod
    def strip_and_validate_reasoning(cls, value: str) -> str:
        """Strip whitespace and reject blank reasoning.

        Args:
            value: Raw reasoning value.

        Returns:
            Cleaned reasoning value.

        Raises:
            ValueError: If reasoning is blank after stripping whitespace.
        """
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Reasoning must not be blank.")

        return cleaned_value
