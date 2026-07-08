# Product Requirements Document

## Product

Agentic Automation Portfolio

## Problem

Modern businesses need AI systems that do more than answer questions. They need systems that can classify, retrieve context, use tools, make decisions, escalate safely, and operate inside real workflows.

## Goal

Build a production-style portfolio of three agentic automation systems:

1. Customer Support Escalation
2. Document Compliance Checking
3. Sales Pipeline Management

## Success Criteria

- End-to-end workflows run locally
- Agent orchestration uses LangGraph
- Shared tooling is reusable across projects
- Runtime can switch between Ollama, vLLM, TensorRT-LLM, or OpenAI-compatible servers
- Tests and quality gates pass before every commit
- Documentation explains architecture, decisions, and delivery process

## Out of Scope for v1

- Real customer data
- Production credentials
- Paid CRM/email integrations by default
- Fully managed cloud deployment
