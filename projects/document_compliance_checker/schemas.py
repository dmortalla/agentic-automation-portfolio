"""Schemas for the Document Compliance Checker."""

from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class ComplianceStatus(StrEnum):
    """Supported compliance statuses."""

    COMPLIANT = "compliant"
    NEEDS_REVIEW = "needs_review"
    NON_COMPLIANT = "non_compliant"


class ComplianceRiskLevel(StrEnum):
    """Supported compliance risk levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ComplianceDocument(BaseModel):
    """Document submitted for compliance review."""

    document_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=25)
    policy_area: str = Field(default="general", min_length=1)

    @field_validator("document_id", "title", "content", "policy_area")
    @classmethod
    def strip_and_validate_not_blank(cls, value: str) -> str:
        """Strip whitespace and reject blank values."""
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Value must not be blank.")

        return cleaned_value


class ComplianceAssessment(BaseModel):
    """Structured compliance assessment."""

    status: ComplianceStatus
    risk_level: ComplianceRiskLevel
    confidence: float = Field(..., ge=0.0, le=1.0)
    summary: str = Field(..., min_length=10)
    flagged_issues: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)

    @field_validator("summary")
    @classmethod
    def strip_and_validate_summary(cls, value: str) -> str:
        """Strip whitespace and reject blank summaries."""
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Summary must not be blank.")

        return cleaned_value
