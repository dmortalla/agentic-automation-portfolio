"""Prompt builders for the Customer Support Escalation System."""

from projects.customer_support_escalation.schemas import SupportTicket


def build_classification_prompt(ticket: SupportTicket) -> str:
    """Build the prompt used by the classifier agent.

    Args:
        ticket: Customer support ticket.

    Returns:
        Prompt instructing the LLM to classify the ticket.
    """
    return f"""
You are an expert customer support triage assistant.

Classify the following support ticket.

Subject:
{ticket.subject}

Message:
{ticket.message}

Return a structured classification.

Category:
Priority:
Confidence:
Reasoning:
Requires Human Review:
""".strip()
