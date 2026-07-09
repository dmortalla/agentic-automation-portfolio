# Agentic Automation Portfolio Architecture

## 1. Purpose

This repository contains three production-style agentic automation systems:

1. Autonomous Customer Support & Escalation System
2. Autonomous Document Processing & Compliance Checker
3. AI Sales Pipeline Manager

The goal is to demonstrate end-to-end AI engineering skills using reusable architecture, strong testing, clear documentation, and production-inspired workflows.

## 2. Core Architecture

```text
External Trigger
    |
    v
Automation Layer / CLI / Streamlit
    |
    v
Project Workflow
    |
    v
LangGraph Orchestration
    |
    v
Agents + Tools + RAG
    |
    v
LLM Runtime Adapter
    |
    v
Ollama / vLLM / TensorRT-LLM / OpenAI-Compatible Server
```

## 3. Repository Layout

```text
agentic-automation-portfolio/
+-- apps/
+-- data/
+-- docs/
+-- projects/
+-- shared/
+-- tests/
```

## 4. Shared Layer Responsibilities

### shared/config

Owns validated application settings.

### shared/llm_runtime

Owns runtime abstraction for model inference.

Supported providers:

- Ollama
- vLLM
- TensorRT-LLM
- OpenAI-compatible servers

### shared/models

Owns reusable Pydantic models and enums.

### shared/rag

Owns reusable retrieval-augmented generation utilities.

### shared/tools

Owns reusable tool wrappers.

### shared/logging

Owns structured application logging.

### shared/observability

Owns tracing and monitoring hooks.

### shared/utils

Owns general helper functions.

## 5. Project Pattern

Each project follows this layout:

```text
project_name/
+-- agents.py
+-- cli.py
+-- evals.py
+-- graph.py
+-- prompts.py
+-- schemas.py
+-- tools.py
+-- workflow.py
+-- README.md
```

## 6. Runtime Strategy

Runtime selection is controlled through environment variables.

Example:

```env
LLM_PROVIDER=ollama
```

The rest of the application should not call provider-specific APIs directly.
All model calls should go through the runtime adapter layer.

## 7. Observability Strategy

Observability should be optional and config-driven.

Local development should work without external tracing.

Production-style mode may enable:

- LangSmith traces
- Langfuse event tracking
- latency metrics
- error tracking
- agent decision logs

## 8. Testing Strategy

Quality gate before commits:

```powershell
pytest
ruff check .
python -m compileall .
```

A commit should not be made if these checks fail.

## 9. Error Handling Strategy

Expected practices:

- custom exceptions for runtime failures
- validation errors for bad inputs
- clear messages for missing configuration
- safe fallback behavior where appropriate
- no raw stack traces in user-facing app output

## 10. Security Strategy

Rules:

- .env stays ignored
- .env.example contains placeholder values only
- logs must not print API keys
- uploaded/private data goes under ignored folders
- mock tools should be used for portfolio demos unless real credentials are intentionally configured

## 11. Production Readiness Checklist

For every major component:

- [ ] Typed function signatures
- [ ] Google-style docstrings
- [ ] Input validation
- [ ] Exception handling
- [ ] Unit tests
- [ ] Logging where useful
- [ ] Config-driven behavior
- [ ] No hardcoded secrets
- [ ] Lint clean
- [ ] Compile clean
- [ ] Documented usage

## 12. Build Order

Recommended implementation order:

1. Shared settings
2. Runtime adapter interface
3. Runtime provider adapters
4. Runtime factory
5. Shared logging
6. Shared observability no-op hooks
7. Shared RAG utilities
8. Customer Support project
9. Document Compliance project
10. Sales Pipeline project
11. Streamlit dashboard
12. Docker support
13. Final documentation and screenshots

## 13. First Flagship Project

The first implementation target is:

```text
projects/customer_support_escalation/
```

Reason:

- easiest to demo
- strongest recruiter story
- excellent fit for LangGraph
- supports RAG, routing, sentiment, escalation, and human approval
- maps clearly to real business value
