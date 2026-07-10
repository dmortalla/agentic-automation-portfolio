# Project Status

## Current State

- Repository: agentic-automation-portfolio
- Branch: main
- Remote: origin/main
- Latest verified test count: 77 passed
- Quality gate:
  1. ruff check .
  2. pytest
  3. python -m compileall shared projects apps tests scripts

## Completed

- Architecture documentation and ADRs
- Environment-agnostic setup
- GitHub Flow workflow
- GitHub Actions CI
- Pre-commit hooks
- Shared settings
- Shared logging
- Runtime abstraction
- Runtime factory
- Demo runtime
- Ollama runtime
- vLLM runtime
- TensorRT runtime productionization
- Runtime contract tests
- Shared runtime parsing utilities
- Customer Support LangGraph workflow
- Customer Support CLI
- Streamlit dashboard
- Dashboard runtime switching
- Live customer support dashboard demo
- Document Compliance vertical slice
- Sales Pipeline vertical slice
- Human-in-the-loop Sales Pipeline positioning

## Current Architecture

The repository is organized as a production-style AI automation platform:

- shared/ contains reusable infrastructure
- projects/ contains business workflows
- apps/ contains user-facing apps
- tests/ contains unit and contract tests
- docs/ contains architecture, ADRs, roadmap, and status
- scripts/ contains developer tooling

## Current Project Positioning

The Sales Pipeline Manager keeps the stable internal folder name:

- projects/sales_pipeline_manager/

It is positioned externally as a human-in-the-loop AI sales automation workflow.

The system drafts and recommends actions but does not send emails or update CRM records without human approval.

## Next Recommended Work

1. Clean up stale local feature branches that are already merged.
2. Run full quality gate.
3. Review README and portfolio-facing documentation.
4. Add or update Interview Guide.
5. Continue production hardening and dashboard polish.

## Stale Local Branches to Review

These branches appear merged into main and may be deleted locally after verification:

- ci/github-actions
- chore/pre-commit-hooks
- test/runtime-contract-tests
- feature/streamlit-dashboard
- feature/dashboard-live-workflow-demo
- feature/dashboard-live-customer-support-demo
- feature/dashboard-v3-runtime-switching
- feature/document-compliance-vertical-slice
- feature/sales-pipeline-vertical-slice
- feature/tensorrt-runtime-productionization
