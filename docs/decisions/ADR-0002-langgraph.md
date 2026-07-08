# ADR-0002: Use LangGraph for Agent Orchestration

## Status

Accepted

## Context

The systems require stateful workflows, routing, multi-agent coordination, and human approval gates.

## Decision

Use LangGraph as the orchestration framework for agent workflows.

## Consequences

### Positive

- Supports stateful workflow design.
- Makes routing logic explicit.
- Fits multi-agent and approval workflows.
- Improves reliability compared with loose agent loops.

### Tradeoffs

- Requires upfront graph design.
- Adds complexity compared with a single function pipeline.
