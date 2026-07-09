"""Command-line interface for the Customer Support Escalation System."""

from projects.customer_support_escalation.schemas import SupportTicket
from projects.customer_support_escalation.workflow import classify_support_ticket
from shared.llm_runtime.factory import create_runtime


def main() -> None:
    """Run a simple demonstration of the customer support workflow."""
    ticket = SupportTicket(
        ticket_id="DEMO-001",
        customer_name="Jane Customer",
        customer_email="jane@example.com",
        subject="Cannot log in",
        message="I cannot log in after resetting my password.",
        source="demo",
    )

    runtime = create_runtime()

    result = classify_support_ticket(
        ticket=ticket,
        runtime=runtime,
    )

    print("=" * 60)
    print("Customer Support Classification")
    print("=" * 60)
    print(f"Category : {result.classification.category}")
    print(f"Priority : {result.classification.priority}")
    print(f"Confidence : {result.classification.confidence:.2f}")
    print(f"Reasoning : {result.classification.reasoning}")
    print(f"Human Review : {result.classification.requires_human_review}")
    print("=" * 60)


if __name__ == "__main__":
    main()
