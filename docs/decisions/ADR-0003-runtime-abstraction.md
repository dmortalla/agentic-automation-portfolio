# ADR-0003: Use Runtime Adapter Abstraction

## Status

Accepted

## Context

The portfolio should support local and production-style model inference. The user may run locally with Ollama or use vLLM/TensorRT-LLM for higher-performance serving.

## Decision

Create a shared LLM runtime adapter layer. Application code will call a common interface instead of provider-specific APIs.

## Consequences

### Positive

- Provider changes do not require rewriting agents.
- Ollama can be used for local development.
- vLLM can be used for production-style serving.
- TensorRT-LLM can be documented as an advanced GPU deployment option.

### Tradeoffs

- Requires a small amount of upfront abstraction.
- Provider-specific advanced features may need adapter extensions later.
