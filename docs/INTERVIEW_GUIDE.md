# Interview Guide

## Elevator Pitch

I built a production-style agentic automation platform containing three reusable business workflows: customer support escalation, document compliance checking, and human-in-the-loop sales pipeline management.

The platform uses LangGraph for stateful orchestration, Pydantic for validated structured outputs, and a provider-agnostic runtime layer supporting Demo, Ollama, vLLM, and TensorRT-LLM implementations.

## Architecture Summary

The application separates:

- Presentation
- Workflow execution
- Agent orchestration
- Business agents
- Runtime infrastructure
- Structured data contracts

This means model providers can be replaced without rewriting business workflows or LangGraph orchestration.

## Why LangGraph?

LangGraph makes workflow state, routing, retries, and human approval points explicit.

I selected it because these applications require controlled business workflows rather than unconstrained autonomous agent loops.

## Why Dependency Injection?

Agents receive a `BaseLLMRuntime` dependency instead of creating provider-specific clients.

This allows:

- Runtime replacement through configuration
- Deterministic testing with fake runtimes
- Local execution with Ollama
- Higher-throughput deployment with vLLM or TensorRT-LLM
- Business logic that remains independent of infrastructure

## Why Pydantic?

Every model-generated business object is validated before it enters the workflow.

Examples include:

- Ticket classifications
- Confidence scores
- Compliance findings
- Lead-scoring recommendations

This prevents arbitrary unvalidated model text from becoming trusted application state.

## Why Multiple Runtime Providers?

The runtime layer demonstrates that the orchestration architecture is genuinely provider-independent.

Supported implementations include:

- Demo runtime for deterministic testing
- Ollama for local inference
- vLLM for OpenAI-compatible high-throughput serving
- TensorRT-LLM for optimized NVIDIA inference

## What Did Real Model Integration Reveal?

The Ollama model returned confidence as `85` instead of `0.85`.

Rather than weakening the schema, I added controlled normalization for numeric confidence percentages while preserving strict Pydantic validation.

This is an example of making an AI system tolerant of reasonable output variation without accepting invalid business data.

## Why Human-in-the-Loop Sales Automation?

The Sales Pipeline Manager drafts outreach and recommends CRM or follow-up actions.

It does not send messages or mutate external business systems without human approval.

That design balances automation with:

- Operational safety
- Auditability
- Brand protection
- Responsible AI governance

## Testing Strategy

The repository includes:

- Schema validation tests
- Agent unit tests
- Workflow tests
- LangGraph routing tests
- Runtime adapter tests
- Runtime contract tests
- CLI tests
- Shared parsing tests

The standard quality gate runs Ruff, Pytest, and Python compilation checks.

## CI/CD Practices

GitHub Actions runs the repository quality gate automatically.

Pre-commit hooks catch common problems before code is committed.

Development uses short-lived branches, focused commits, and merges into a protected conceptual `main` branch.

## Strong Interview Statement

I implemented a provider-agnostic runtime layer with dependency injection. The application orchestrates agents using LangGraph and validates structured outputs with Pydantic. It supports deterministic testing, local inference with Ollama, and production-oriented runtimes such as vLLM and TensorRT-LLM without changing the orchestration layer.

## Lessons Learned

- Build the smallest complete vertical slice first.
- Define data contracts before implementing agents.
- Let concrete duplication reveal the correct abstraction.
- Treat model output as untrusted input.
- Keep external business actions behind explicit approval gates.
- Maintain documentation as part of the product.
