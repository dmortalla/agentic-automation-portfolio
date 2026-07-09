"""Command-line interface for the Customer Support Escalation System."""

import argparse

from projects.customer_support_escalation.schemas import SupportTicket
from projects.customer_support_escalation.workflow import classify_support_ticket
from shared.config.settings import Settings
from shared.llm_runtime.base import BaseLLMRuntime
from shared.llm_runtime.exceptions import LLMRuntimeError
from shared.llm_runtime.factory import create_runtime
from shared.models.enums import LLMProvider


class DemoRuntime(BaseLLMRuntime):
    """Deterministic runtime used for demonstrations."""

    @property
    def provider_name(self) -> str:
        """Return the demo provider name."""
        return "demo"

    def generate_structured(self, prompt, output_model):
        """Return a deterministic classification for demo use."""
        return output_model(
            category="technical",
            priority="high",
            confidence=0.98,
            reasoning="Customer cannot access the application after a password reset.",
            requires_human_review=False,
        )


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Customer Support Escalation Demo",
    )

    parser.add_argument(
        "--provider",
        default="demo",
        choices=["demo", "ollama", "vllm", "tensorrt"],
        help="Runtime provider.",
    )

    return parser.parse_args()


def _create_runtime(provider: str) -> BaseLLMRuntime:
    """Create the requested runtime."""
    if provider == "demo":
        return DemoRuntime()

    if provider == "ollama":
        return create_runtime(Settings(llm_provider=LLMProvider.OLLAMA))

    if provider == "vllm":
        return create_runtime(Settings(llm_provider=LLMProvider.VLLM))

    if provider == "tensorrt":
        return create_runtime(Settings(llm_provider=LLMProvider.TENSORRT))

    raise ValueError(f"Unsupported provider: {provider}")


def _run(provider: str) -> int:
    """Run the customer support workflow.

    Args:
        provider: Runtime provider name.

    Returns:
        Process exit code.
    """
    try:
        runtime = _create_runtime(provider)

        ticket = SupportTicket(
            ticket_id="DEMO-001",
            customer_name="Jane Customer",
            customer_email="jane@example.com",
            subject="Cannot log in",
            message="I cannot log in after resetting my password.",
            source="demo",
        )

        result = classify_support_ticket(
            ticket=ticket,
            runtime=runtime,
        )

        print("=" * 60)
        print("Customer Support Classification")
        print("=" * 60)
        print(f"Provider: {runtime.provider_name}")
        print(f"Category: {result.classification.category}")
        print(f"Priority: {result.classification.priority}")
        print(f"Confidence: {result.classification.confidence:.2f}")
        print(f"Reasoning: {result.classification.reasoning}")
        print(f"Human Review: {result.classification.requires_human_review}")
        print("=" * 60)

        return 0

    except LLMRuntimeError as error:
        print(f"Runtime provider error: {error}")
        return 1


def main() -> None:
    """Parse CLI arguments and run the workflow."""
    args = _parse_args()
    raise SystemExit(_run(args.provider))


if __name__ == "__main__":
    main()
