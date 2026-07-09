"""Tests for the Document Compliance Checker vertical slice."""

from __future__ import annotations

from typing import TypeVar

import pytest
from pydantic import BaseModel

from projects.document_compliance_checker.schemas import (
    ComplianceAssessment,
    ComplianceDocument,
    ComplianceRiskLevel,
    ComplianceStatus,
)
from projects.document_compliance_checker.workflow import check_document_compliance
from shared.llm_runtime.base import BaseLLMRuntime


StructuredOutputT = TypeVar("StructuredOutputT", bound=BaseModel)


class FakeComplianceRuntime(BaseLLMRuntime):
    """Deterministic runtime for compliance workflow tests."""

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "fake-compliance-runtime"

    def generate_structured(
        self,
        prompt: str,
        output_model: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Return a deterministic structured compliance assessment."""
        assert "Review the document" in prompt

        return output_model(
            status=ComplianceStatus.NEEDS_REVIEW,
            risk_level=ComplianceRiskLevel.MEDIUM,
            confidence=0.91,
            summary="The document needs review due to missing approval language.",
            flagged_issues=["Missing approval clause."],
            recommended_actions=["Add explicit approval and review requirements."],
        )


def test_check_document_compliance_completes_workflow() -> None:
    """Workflow should return a validated final state with an assessment."""
    document = ComplianceDocument(
        document_id="DOC-1001",
        title="Vendor Data Handling Policy",
        content=(
            "This policy describes how vendor data should be handled, stored, "
            "reviewed, and protected before external sharing or processing."
        ),
        policy_area="data_privacy",
    )

    final_state = check_document_compliance(
        document=document,
        runtime=FakeComplianceRuntime(),
    )

    assert final_state.assessment is not None
    assert isinstance(final_state.assessment, ComplianceAssessment)
    assert final_state.assessment.status == ComplianceStatus.NEEDS_REVIEW
    assert final_state.assessment.risk_level == ComplianceRiskLevel.MEDIUM
    assert final_state.notes == ["Document compliance assessment completed."]


def test_check_document_compliance_rejects_missing_document() -> None:
    """Workflow should reject a missing document."""
    with pytest.raises(ValueError, match="Document must not be None."):
        check_document_compliance(
            document=None,  # type: ignore[arg-type]
            runtime=FakeComplianceRuntime(),
        )


def test_check_document_compliance_rejects_missing_runtime() -> None:
    """Workflow should reject a missing runtime."""
    document = ComplianceDocument(
        document_id="DOC-1002",
        title="Security Policy",
        content=(
            "This security policy defines access rules, audit expectations, "
            "and control ownership for sensitive operational systems."
        ),
    )

    with pytest.raises(ValueError, match="Runtime must not be None."):
        check_document_compliance(
            document=document,
            runtime=None,  # type: ignore[arg-type]
        )
