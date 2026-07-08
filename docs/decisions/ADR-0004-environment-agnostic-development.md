# ADR-0004: Use Environment-Agnostic Local Development

## Status

Accepted

## Context

Developers may use different Python environment managers depending on their background and tooling. Backend engineers often prefer Python virtual environments, while ML and AI engineers often use Conda for scientific, GPU, and native dependency workflows.

This project should be easy to clone, install, test, and run regardless of whether the developer prefers `.venv`, Conda, Docker, or a future CI environment.

## Decision

The repository will remain environment-agnostic.

The project supports:

- Python virtual environments
- Conda environments
- Future Docker-based development
- Future CI/CD environments

The only hard requirement is a compatible Python version with the required dependencies installed.

## Recommended Setup Options

### Option 1: Python virtual environment

- python -m venv .venv
- .\.venv\Scripts\Activate.ps1
- pip install -r requirements.txt

### Option 2: Conda environment

- conda create -n agentic_automation_env python=3.13
- conda activate agentic_automation_env
- pip install -r requirements.txt

## Consequences

### Positive

- Reduces friction for different types of engineers.
- Keeps the repository portable.
- Avoids forcing one environment manager on all users.
- Supports backend, ML, and DevOps workflows.
- Makes the project easier to evaluate, clone, and run.

### Tradeoffs

- Documentation must clearly show multiple setup paths.
- Environment checks should validate capabilities rather than assuming a specific tool.
- Developers must avoid committing environment-specific files.

## Engineering Principle

Optimize for the next engineer.

The project should be easy for another developer to understand, configure, test, and extend.
