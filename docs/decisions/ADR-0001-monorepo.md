# ADR-0001: Use a Monorepo

## Status

Accepted

## Context

The portfolio contains three related agentic automation systems that share configuration, logging, runtime adapters, RAG utilities, tools, and documentation standards.

## Decision

Use a single monorepo with reusable shared modules and separate project folders.

## Consequences

### Positive

- Shared infrastructure avoids duplication.
- One polished GitHub repository tells a stronger portfolio story.
- Common quality gates apply to all projects.
- Recruiters can review one cohesive system.

### Tradeoffs

- Repository structure is larger.
- Clear boundaries are required to avoid coupling between projects.
