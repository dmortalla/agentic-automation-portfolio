"""Prompt builders for the AI Sales Pipeline Manager."""

from projects.sales_pipeline_manager.schemas import Lead, LeadScore


def build_lead_scoring_prompt(lead: Lead) -> str:
    """Build a structured lead-qualification prompt."""
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


def build_company_research_prompt(
    lead: Lead,
    lead_score: LeadScore,
) -> str:
    """Build a constrained company-research prompt.

    The prompt permits analysis only from supplied lead facts. Live search
    providers may be added later behind approved tools.
    """
    return f"""
You are a business research specialist supporting a human sales reviewer.

Use only the supplied lead information and qualification result. Do not
claim that you searched the web, and do not invent company facts.

Company: {lead.company_name}
Industry: {lead.industry or "Unknown"}
Company size: {lead.company_size or "Unknown"}
Expressed need: {lead.expressed_need}
Qualification score: {lead_score.score}
Qualification decision: {lead_score.decision.value}
Qualification reasoning: {lead_score.reasoning}

Return structured research containing:
- summary: evidence-based organization and opportunity summary
- pain_points: likely pain points supported by supplied information
- opportunities: safe areas for further human investigation
- confidence: decimal from 0.0 to 1.0
- sources: empty unless approved sources were explicitly supplied
- requires_human_review: always true

Do not recommend contacting the lead or changing a CRM record.
""".strip()
