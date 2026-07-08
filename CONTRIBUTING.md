# Contributing Guide

This repository is developed using production-style engineering practices.

## Development Workflow

1. Create or select a scoped task.
2. Update documentation when architecture changes.
3. Write typed Python code with Google-style docstrings.
4. Add or update tests.
5. Run the quality gate.
6. Commit only when all checks pass.

## Quality Gate

Run before every commit:

- pytest
- ruff check .
- python -m compileall shared projects apps tests

## Code Standards

- Prefer small, testable functions.
- Use Pydantic for structured data.
- Use custom exceptions for expected failure modes.
- Keep prompts outside agent logic.
- Keep provider-specific LLM calls inside runtime adapters.
- Do not commit secrets or private data.

## Definition of Done

A task is complete only when:

- Requirements are implemented
- Tests pass
- Lint check passes
- Compile check passes
- Documentation is updated
- Git commit is complete
