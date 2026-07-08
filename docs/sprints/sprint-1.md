# Sprint 1: Customer Support MVP

## Goal

Deliver the first vertical slice of the Customer Support Escalation System.

## User Story

As a support representative, I want to submit a customer ticket so that an AI classifier can categorize it.

## Scope

- Ticket schema
- Classification schema
- Classifier agent
- LangGraph workflow
- CLI runner
- Unit tests
- Logging
- Error handling

## Out of Scope

- RAG response drafting
- Sentiment analysis
- Escalation logic
- Supervisor approval
- Streamlit UI

## Definition of Done

- CLI can classify a sample ticket
- Graph workflow executes successfully
- Tests cover schema validation and workflow behavior
- Quality gate passes
- Documentation updated
- Git commit completed

## Risks

- LangGraph integration complexity
- Runtime adapter not fully implemented yet
- Need to keep MVP small and avoid overbuilding
