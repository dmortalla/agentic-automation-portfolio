"""Prompt builders for the AI Sales Pipeline Manager."""

from projects.sales_pipeline_manager.schemas import Lead


def build_lead_scoring_prompt(lead: Lead) -> str:
    """Build a structured lead-qualification prompt.

    Args:
        lead: Validated sales lead.

    Returns:
        Prompt requesting a structured LeadScore response.
    """
    company_size = (
        str(lead.company_size)
        if lead.company_size is not None
        else "Unknown"
    )
    job_title = lead.job_title or "Unknown"
    industry = lead.industry or "Unknown"

    return f"""
You are a business-to-business sales qualification specialist.

Evaluate the lead using the supplied facts only. Do not invent missing
information.

Lead details:
- Company: {lead.company_name}
- Contact: {lead.contact_name}
- Job title: {job_title}
- Industry: {industry}
- Company size: {company_size}
- Lead source: {lead.source.value}
- Expressed need: {lead.expressed_need}

Return a structured qualification result containing:
- score: integer from 0 to 100
- decision: qualified, nurture, or disqualified
- reasoning: concise evidence-based explanation
- recommended_next_step: safe recommendation for a human reviewer
- requires_human_review: always true
- approval_status: pending

Do not recommend sending email or updating a CRM without human approval.
""".strip()
