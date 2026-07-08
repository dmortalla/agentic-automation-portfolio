"""Schemas for the Customer Support Escalation System."""

from pydantic import BaseModel, Field, field_validator


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
