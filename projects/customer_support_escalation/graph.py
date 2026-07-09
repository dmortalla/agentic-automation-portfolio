"""LangGraph workflow for the Customer Support Escalation System."""

from langgraph.graph import END, START, StateGraph

from projects.customer_support_escalation.agents.classifier import ClassifierAgent
from projects.customer_support_escalation.state import CustomerSupportState
from shared.llm_runtime.base import BaseLLMRuntime


def build_customer_support_graph(runtime: BaseLLMRuntime):
    """Build the initial customer support LangGraph workflow.

    Args:
        runtime: LLM runtime used by workflow agents.

    Returns:
        Compiled LangGraph application.

    The initial graph is intentionally small:

        START -> classifier -> END

    Future nodes will include sentiment, RAG, escalation, and supervisor review.
    """
    classifier_agent = ClassifierAgent(runtime=runtime)

    def classifier_node(state: CustomerSupportState) -> CustomerSupportState:
        """Run the classifier agent node."""
        return classifier_agent.run(state)

    graph = StateGraph(CustomerSupportState)

    graph.add_node("classifier", classifier_node)
    graph.add_edge(START, "classifier")
    graph.add_edge("classifier", END)

    return graph.compile()
