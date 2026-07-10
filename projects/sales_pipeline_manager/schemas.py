"""Validated schemas for the AI Sales Pipeline Manager."""

from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class LeadSource(StrEnum):
    """Supported lead acquisition sources."""

    WEBSITE = "website"
    REFERRAL = "referral"
    EVENT = "event"
    OUTBOUND = "outbound"
    PARTNER = "partner"
    OTHER = "other"


class QualificationDecision(StrEnum):
    """Supported lead qualification recommendations."""

    QUALIFIED = "qualified"
    NURTURE = "nurture"
    DISQUALIFIED = "disqualified"


class ApprovalStatus(StrEnum):
    """Human-review status for recommended sales actions."""

    PENDING = "pending"
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    REJECTED = "rejected"


class Lead(BaseModel):
    """Validated lead submitted to the sales pipeline."""

    lead_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    contact_name: str = Field(..., min_length=1)
    contact_email: str = Field(..., min_length=3)
    job_title: str | None = Field(default=None, min_length=1)
    industry: str | None = Field(default=None, min_length=1)
    company_size: int | None = Field(default=None, ge=1)
    source: LeadSource = Field(default=LeadSource.OTHER)
    expressed_need: str = Field(..., min_length=10)

    @field_validator(
        "lead_id",
        "company_name",
        "contact_name",
        "contact_email",
        "expressed_need",
    )
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        """Strip required text fields and reject blank values."""
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Value must not be blank.")

        return cleaned_value

    @field_validator("job_title", "industry")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        """Strip optional text fields and reject blank strings."""
        if value is None:
            return None

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Optional text must not be blank when provided.")

        return cleaned_value


class LeadScore(BaseModel):
    """Structured lead-scoring result."""

    score: int = Field(..., ge=0, le=100)
    decision: QualificationDecision
    reasoning: str = Field(..., min_length=10)
    recommended_next_step: str = Field(..., min_length=5)
    requires_human_review: bool = Field(default=True)
    approval_status: ApprovalStatus = Field(default=ApprovalStatus.PENDING)

    @field_validator("reasoning", "recommended_next_step")
    @classmethod
    def strip_recommendation_text(cls, value: str) -> str:
        """Strip recommendation text and reject blank values."""
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Recommendation text must not be blank.")

        return cleaned_value


class CompanyResearch(BaseModel):
    """Structured company research produced for a qualified lead.

    Attributes:
        summary: Evidence-based organization summary.
        pain_points: Relevant business problems inferred from supplied facts.
        opportunities: Potential areas where the solution may help.
        confidence: Research confidence between 0.0 and 1.0.
        sources: Approved source names or references, when available.
        requires_human_review: Whether a human must verify the research.
    """

    summary: str = Field(..., min_length=20)
    pain_points: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)
    sources: list[str] = Field(default_factory=list)
    requires_human_review: bool = Field(default=True)

    @field_validator("summary")
    @classmethod
    def strip_summary(cls, value: str) -> str:
        """Strip and validate the research summary."""
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Research summary must not be blank.")

        return cleaned_value

    @field_validator("pain_points", "opportunities", "sources")
    @classmethod
    def clean_text_lists(cls, values: list[str]) -> list[str]:
        """Strip list entries and reject blank items."""
        cleaned_values = [value.strip() for value in values]

        if any(not value for value in cleaned_values):
            raise ValueError("Research list entries must not be blank.")

        return cleaned_values
