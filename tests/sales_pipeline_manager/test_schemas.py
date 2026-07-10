"""Tests for AI Sales Pipeline Manager schemas."""

import pytest
from pydantic import ValidationError

from projects.sales_pipeline_manager.schemas import (
    ApprovalStatus,
    Lead,
    LeadScore,
    LeadSource,
    QualificationDecision,
)


def _valid_lead_data() -> dict[str, object]:
    """Return reusable valid lead input."""
    return {
        "lead_id": "LEAD-001",
        "company_name": "Northstar Analytics",
        "contact_name": "Jordan Lee",
        "contact_email": "jordan@northstar.example",
        "job_title": "VP of Operations",
        "industry": "Analytics",
        "company_size": 250,
        "source": LeadSource.WEBSITE,
        "expressed_need": (
            "The company wants to automate customer-support triage and reporting."
        ),
    }


def test_lead_accepts_valid_data() -> None:
    """Lead should accept complete valid input."""
    lead = Lead(**_valid_lead_data())

    assert lead.lead_id == "LEAD-001"
    assert lead.company_name == "Northstar Analytics"
    assert lead.source == LeadSource.WEBSITE
    assert lead.company_size == 250


def test_lead_strips_text_fields() -> None:
    """Lead should strip leading and trailing whitespace."""
    data = _valid_lead_data()
    data["company_name"] = " Northstar Analytics "
    data["job_title"] = " VP of Operations "

    lead = Lead(**data)

    assert lead.company_name == "Northstar Analytics"
    assert lead.job_title == "VP of Operations"


def test_lead_rejects_blank_required_text() -> None:
    """Lead should reject blank required text fields."""
    data = _valid_lead_data()
    data["company_name"] = "   "

    with pytest.raises(ValidationError):
        Lead(**data)


def test_lead_rejects_blank_optional_text() -> None:
    """Lead should reject blank optional text when supplied."""
    data = _valid_lead_data()
    data["industry"] = "   "

    with pytest.raises(ValidationError):
        Lead(**data)


def test_lead_rejects_non_positive_company_size() -> None:
    """Lead should reject a non-positive company size."""
    data = _valid_lead_data()
    data["company_size"] = 0

    with pytest.raises(ValidationError):
        Lead(**data)


def test_lead_score_accepts_valid_recommendation() -> None:
    """LeadScore should accept a valid human-review recommendation."""
    result = LeadScore(
        score=87,
        decision=QualificationDecision.QUALIFIED,
        reasoning="The lead has a clear need, relevant authority, and strong fit.",
        recommended_next_step="Prepare personalized outreach for human review.",
    )

    assert result.score == 87
    assert result.decision == QualificationDecision.QUALIFIED
    assert result.requires_human_review is True
    assert result.approval_status == ApprovalStatus.PENDING


def test_lead_score_rejects_score_above_one_hundred() -> None:
    """LeadScore should reject scores above 100."""
    with pytest.raises(ValidationError):
        LeadScore(
            score=101,
            decision=QualificationDecision.QUALIFIED,
            reasoning="The lead appears to be an excellent fit for the solution.",
            recommended_next_step="Prepare outreach.",
        )


def test_lead_score_rejects_score_below_zero() -> None:
    """LeadScore should reject scores below zero."""
    with pytest.raises(ValidationError):
        LeadScore(
            score=-1,
            decision=QualificationDecision.DISQUALIFIED,
            reasoning="The lead does not match the current customer profile.",
            recommended_next_step="Close the lead.",
        )


def test_lead_score_accepts_explicit_review_status() -> None:
    """LeadScore should store an explicit human-review status."""
    result = LeadScore(
        score=65,
        decision=QualificationDecision.NURTURE,
        reasoning="The lead has potential but has not demonstrated sufficient urgency.",
        recommended_next_step="Add the lead to a human-reviewed nurture sequence.",
        approval_status=ApprovalStatus.CHANGES_REQUESTED,
    )

    assert result.approval_status == ApprovalStatus.CHANGES_REQUESTED
