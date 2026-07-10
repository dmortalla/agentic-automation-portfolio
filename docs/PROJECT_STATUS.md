# Project Status

## Repository State

- Repository: `agentic-automation-portfolio`
- Default branch: `main`
- Remote branch: `origin/main`
- Latest verified test count: **77 passed**
- Architecture status: **Frozen**
- Development phase: **Professionalization and production hardening**

## Standard Quality Gate

Run before every commit:

1. `ruff check .`
2. `pytest`
3. `python -m compileall shared projects apps tests scripts`

Run an application smoke test when a user-facing entry point changes.

## Completed Platform Capabilities

- Production-style monorepo architecture
- Environment-agnostic local development
- Validated Pydantic settings
- Shared structured logging
- Provider-agnostic LLM runtime interface
- Runtime factory with dependency injection
- Demo runtime
- Real Ollama runtime
- Real vLLM OpenAI-compatible runtime
- TensorRT-LLM runtime productionization
- Shared structured-output parsing and validation
- Confidence normalization
- Runtime contract tests
- GitHub Actions quality-gate workflow
- Pre-commit hooks
- Architecture Decision Records
- Mermaid architecture documentation
- GitHub Flow development process

## Completed Applications

### Customer Support and Escalation

- Validated support ticket schema
- Structured classification schema
- Typed LangGraph workflow state
- Classifier agent
- Prompt builder
- LangGraph orchestration
- Workflow runner
- CLI runtime selection
- Real Ollama execution
- Streamlit dashboard demo
- Dashboard runtime switching

### Document Compliance Checker

- Initial end-to-end vertical slice
- Project-specific workflow structure
- Tests integrated into the repository quality gate

### AI Sales Pipeline Manager

- Initial end-to-end vertical slice
- Stable internal module path: `projects/sales_pipeline_manager/`
- Human-in-the-loop product positioning
- External actions require review and approval

## Sales Pipeline Safety Model

The AI Sales Pipeline Manager may:

- Score and rank leads
- Research organizations
- Draft personalized outreach
- Recommend CRM changes
- Recommend follow-up timing

The workflow must require human approval before:

- Sending external email
- Updating CRM records
- Scheduling external follow-up
- Triggering other irreversible business actions

## Current Architecture

```mermaid
flowchart TB
    UI[CLI and Streamlit Apps]
    WORKFLOW[Workflow Runners]
    GRAPH[LangGraph Orchestration]
    AGENTS[Project Agents]
    RUNTIME[Provider-Agnostic Runtime Layer]
    MODELS[Pydantic Structured Outputs]

    UI --> WORKFLOW
    WORKFLOW --> GRAPH
    GRAPH --> AGENTS
    AGENTS --> RUNTIME
    RUNTIME --> MODELS

    RUNTIME --> DEMO[Demo Runtime]
    RUNTIME --> OLLAMA[Ollama]
    RUNTIME --> VLLM[vLLM]
    RUNTIME --> TRT[TensorRT-LLM]
Repository Structure
shared/ — reusable infrastructure
projects/ — business workflows
apps/ — user-facing applications
tests/ — unit, integration, and contract tests
scripts/ — developer automation
docs/ — architecture, ADRs, roadmap, and status
.github/ — CI workflows and repository automation
Next Recommended Work
Clean up merged local branch references.
Add the interview and engineering-decision documentation.
Review and modernize the root README.
Confirm all three applications have runnable demo paths.
Add production-readiness checks for each application.
Add screenshots and portfolio assets.
Prepare the first formal release.
Source of Truth

This document must be updated after:

Major milestones
Completed vertical slices
Architecture changes
Chat or engineer handoffs
Significant roadmap changes
