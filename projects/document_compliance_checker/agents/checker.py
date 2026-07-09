"""Compliance checker agent."""

from projects.document_compliance_checker.prompts import build_compliance_prompt
from projects.document_compliance_checker.schemas import ComplianceAssessment
from projects.document_compliance_checker.state import DocumentComplianceState
from shared.llm_runtime.base import BaseLLMRuntime


class ComplianceCheckerAgent:
    """AI agent responsible for document compliance assessment."""

    def __init__(self, runtime: BaseLLMRuntime) -> None:
        """Initialize the compliance checker agent."""
        self._runtime = runtime

    @property
    def name(self) -> str:
        """Return the agent name."""
        return "compliance_checker"

    def run(self, state: DocumentComplianceState) -> DocumentComplianceState:
        """Run document compliance assessment."""
        prompt = build_compliance_prompt(state.document)

        assessment = self._runtime.generate_structured(
            prompt=prompt,
            output_model=ComplianceAssessment,
        )

        state.assessment = assessment
        state.add_note("Document compliance assessment completed.")

        return state
