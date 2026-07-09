"""Workflow runner for the Customer Support Escalation System."""

from projects.customer_support_escalation.graph import build_customer_support_graph
from projects.customer_support_escalation.schemas import SupportTicket
from projects.customer_support_escalation.state import CustomerSupportState
from shared.llm_runtime.base import BaseLLMRuntime
from shared.logging.logger import get_logger

logger = get_logger(__name__)


def classify_support_ticket(
    ticket: SupportTicket,
    runtime: BaseLLMRuntime,
) -> CustomerSupportState:
    """Classify a support ticket through the LangGraph workflow.

    Args:
        ticket: Support ticket to classify.
        runtime: Runtime used by workflow agents.

    Returns:
        Final customer support workflow state.

    Raises:
        ValueError: If ticket or runtime is missing.
    """
    if ticket is None:
        raise ValueError("Ticket must not be None.")

    if runtime is None:
        raise ValueError("Runtime must not be None.")

    logger.info("Starting customer support classification workflow.")

    initial_state = CustomerSupportState(ticket=ticket)
    graph = build_customer_support_graph(runtime=runtime)

    result = graph.invoke(initial_state)

    final_state = CustomerSupportState.model_validate(result)

    logger.info("Customer support classification workflow completed.")

    return final_state
