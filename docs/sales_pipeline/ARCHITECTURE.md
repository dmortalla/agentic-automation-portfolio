# AI Sales Pipeline Manager Architecture

## 1. Purpose

The AI Sales Pipeline Manager is a production-style, human-in-the-loop workflow for:

- Lead qualification
- Organization research
- Personalized outreach drafting
- Follow-up planning
- CRM change recommendations
- Human review and approval

The system may analyze, rank, draft, and recommend actions autonomously.

It must not perform irreversible external actions without explicit human approval.

## 2. Business Goal

Reduce manual effort required to:

- Evaluate incoming leads
- Research target organizations
- Prepare personalized outreach
- Plan follow-ups
- Maintain CRM records

The workflow improves sales-team productivity while preserving human control over external communication and business-system changes.

## 3. Safety Boundary

The workflow may:

- Calculate lead scores
- Summarize organization research
- Draft email outreach
- Recommend follow-up dates
- Recommend CRM updates

Human approval is required before:

- Sending email
- Creating or modifying CRM records
- Scheduling external meetings
- Triggering external automation
- Performing irreversible business actions

## 4. High-Level Architecture

~~~mermaid
flowchart LR
    TRIGGER[Lead Trigger] --> INTAKE[Lead Intake]
    INTAKE --> SCORE[Lead Scoring Agent]
    SCORE --> RESEARCH[Research Agent]
    RESEARCH --> OUTREACH[Outreach Draft Agent]
    OUTREACH --> FOLLOWUP[Follow-Up Planning Agent]
    FOLLOWUP --> CRM[CRM Recommendation Agent]
    CRM --> REVIEW[Human Approval Gate]

    REVIEW -->|Approve| EXECUTE[Approved Action Tools]
    REVIEW -->|Edit| OUTREACH
    REVIEW -->|Reject| AUDIT[Audit Trail]
    EXECUTE --> AUDIT
~~~

## 5. Architectural Layers

### Presentation and Trigger Layer

Potential entry points include:

- CLI
- Streamlit dashboard
- REST API
- n8n webhook
- CRM-created-lead event
- Lead-response event

Entry points call the workflow and do not contain agent logic.

### Application Layer

The application layer:

- Validates incoming lead data
- Creates the initial workflow state
- Invokes the compiled LangGraph workflow
- Returns the final structured state
- Surfaces actions requiring approval

### Orchestration Layer

LangGraph manages:

- Node execution order
- Shared state
- Conditional routing
- Approval interruption
- Retry paths
- Failure handling
- Resume-after-approval behavior

### Agent Layer

Planned agents:

1. Lead Scoring Agent
2. Research Agent
3. Outreach Draft Agent
4. Follow-Up Planning Agent
5. CRM Recommendation Agent

Each agent performs one focused task and updates shared state.

### Tool Layer

LangChain-compatible tools may include:

- Approved search tools
- Organization-data lookup
- Email-draft formatting
- CRM read tools
- CRM write tools
- Calendar and reminder tools

Write-capable tools remain unavailable until approval is granted.

### Runtime Layer

Agents depend on the shared runtime abstraction rather than provider-specific APIs.

Supported runtimes include:

- Deterministic demo runtime
- Ollama
- vLLM
- TensorRT-LLM

Provider selection remains configuration-driven.

### Observability Layer

Planned observability includes:

- LangSmith workflow traces
- Langfuse latency and cost metrics
- Structured application logs
- Agent decision records
- Approval and rejection events
- External-action audit records

## 6. Proposed Workflow State

The shared state will eventually contain:

- Original lead
- Lead score
- Qualification result
- Organization research
- Outreach draft
- Follow-up recommendation
- CRM recommendation
- Approval status
- Reviewer feedback
- Pending external actions
- Completed actions
- Errors
- Audit events

## 7. Initial Vertical Slice

~~~mermaid
flowchart LR
    START --> LEAD[Validated Lead]
    LEAD --> SCORE[Lead Scoring Agent]
    SCORE --> REVIEW[Human Review Required]
    REVIEW --> END
~~~

The first slice will:

- Accept a validated lead
- Produce a structured lead score
- Produce a qualification recommendation
- Require human review
- Avoid all external side effects

## 8. Initial Data Contracts

The first implementation will define:

- Lead
- LeadScore
- QualificationDecision
- ApprovalStatus
- SalesPipelineState

All LLM-produced values must be validated through Pydantic before entering trusted workflow state.

## 9. Error-Handling Strategy

Expected failures include:

- Invalid lead data
- Runtime connection errors
- Invalid structured model output
- Research-tool failures
- CRM-tool failures
- Approval timeouts
- Rejected or edited recommendations

Expected failures must be translated into domain-appropriate errors and recorded in workflow state.

## 10. Testing Strategy

The implementation will include:

- Schema validation tests
- State transition tests
- Agent unit tests
- Runtime-independent tests using fake runtimes
- LangGraph execution tests
- Human-approval routing tests
- Tool-permission tests
- CLI and dashboard smoke tests
- Audit-record tests

## 11. Non-Goals for the First Slice

The first slice will not:

- Send email
- Write to Salesforce or HubSpot
- Scrape arbitrary websites
- Schedule external meetings
- Trigger autonomous follow-ups
- Use live credentials
- Perform irreversible actions

## 12. Implementation Sequence

1. Schemas and enums
2. Typed workflow state
3. Lead Scoring Agent
4. Initial LangGraph graph
5. Workflow runner
6. Deterministic CLI demo
7. Human approval node
8. Research Agent
9. Outreach Draft Agent
10. Follow-Up Planning Agent
11. CRM Recommendation Agent
12. Mock external-action tools
13. Streamlit review interface
14. n8n trigger examples
15. LangSmith and Langfuse integration
16. Optional sandboxed external integrations

## 13. Definition of Done

The Sales Pipeline Manager is complete when:

- All planned agents are implemented
- LangGraph routing is tested
- Human approval is enforced before external actions
- Runtime selection works through the shared platform
- Mocked demonstrations run without credentials
- Optional sandbox integrations are documented
- Observability captures decisions and approvals
- Quality gates pass
- Architecture and usage documentation are current
