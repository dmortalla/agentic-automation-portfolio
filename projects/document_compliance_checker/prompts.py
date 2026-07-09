"""Prompt builders for the Document Compliance Checker."""

from projects.document_compliance_checker.schemas import ComplianceDocument


def build_compliance_prompt(document: ComplianceDocument) -> str:
    """Build a structured compliance review prompt."""
    return f"""
You are a compliance review agent.

Review the document and return a JSON object with:
- status: one of compliant, needs_review, non_compliant
- risk_level: one of low, medium, high
- confidence: number from 0.0 to 1.0
- summary: concise explanation
- flagged_issues: list of issues
- recommended_actions: list of next actions

Document ID: {document.document_id}
Title: {document.title}
Policy Area: {document.policy_area}
Content:
{document.content}
""".strip()
