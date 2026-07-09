"""Workflow state for the Document Compliance Checker."""

from pydantic import Field

from projects.document_compliance_checker.schemas import (
    ComplianceAssessment,
    ComplianceDocument,
)
from shared.state.base import BaseWorkflowState


class DocumentComplianceState(BaseWorkflowState):
    """State passed through the document compliance workflow."""

    document: ComplianceDocument
    assessment: ComplianceAssessment | None = Field(default=None)
    notes: list[str] = Field(default_factory=list)

    def add_note(self, message: str) -> None:
        """Add an internal workflow note."""
        cleaned_message = message.strip()

        if not cleaned_message:
            raise ValueError("Note message must not be blank.")

        self.notes.append(cleaned_message)
