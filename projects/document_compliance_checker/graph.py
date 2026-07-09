"""LangGraph workflow for the Document Compliance Checker."""

from langgraph.graph import END, START, StateGraph

from projects.document_compliance_checker.agents.checker import ComplianceCheckerAgent
from projects.document_compliance_checker.state import DocumentComplianceState
from shared.llm_runtime.base import BaseLLMRuntime


def build_document_compliance_graph(runtime: BaseLLMRuntime):
    """Build the document compliance LangGraph workflow."""
    checker_agent = ComplianceCheckerAgent(runtime=runtime)

    def checker_node(state: DocumentComplianceState) -> DocumentComplianceState:
        """Run the compliance checker node."""
        return checker_agent.run(state)

    graph = StateGraph(DocumentComplianceState)

    graph.add_node("compliance_checker", checker_node)
    graph.add_edge(START, "compliance_checker")
    graph.add_edge("compliance_checker", END)

    return graph.compile()
