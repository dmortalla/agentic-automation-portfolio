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
    """Validated lead submitted to the sales pipeline.

    Attributes:
        lead_id: Unique lead identifier.
        company_name: Organization associated with the lead.
        contact_name: Primary contact name.
        contact_email: Primary contact email address.
        job_title: Contact's role, when known.
        industry: Organization industry, when known.
        company_size: Approximate employee count, when known.
        source: Channel through which the lead was acquired.
        expressed_need: Business need or problem described by the lead.
    """

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
    """Structured lead-scoring result.

    Attributes:
        score: Qualification score from 0 to 100.
        decision: Recommended qualification outcome.
        reasoning: Explanation supporting the score and decision.
        recommended_next_step: Safe recommended action for a reviewer.
        requires_human_review: Whether a reviewer must approve progression.
        approval_status: Current human-review status.
    """

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
