"""Workflow runner for the Document Compliance Checker."""

from projects.document_compliance_checker.graph import build_document_compliance_graph
from projects.document_compliance_checker.schemas import ComplianceDocument
from projects.document_compliance_checker.state import DocumentComplianceState
from shared.llm_runtime.base import BaseLLMRuntime
from shared.logging.logger import get_logger

logger = get_logger(__name__)


def check_document_compliance(
    document: ComplianceDocument,
    runtime: BaseLLMRuntime,
) -> DocumentComplianceState:
    """Check a document through the LangGraph compliance workflow."""
    if document is None:
        raise ValueError("Document must not be None.")

    if runtime is None:
        raise ValueError("Runtime must not be None.")

    logger.info("Starting document compliance workflow.")

    initial_state = DocumentComplianceState(document=document)
    graph = build_document_compliance_graph(runtime=runtime)

    result = graph.invoke(initial_state)
    final_state = DocumentComplianceState.model_validate(result)

    logger.info("Document compliance workflow completed.")

    return final_state
