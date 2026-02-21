# Multi-Agent Systems Reference

## Table of Contents

1. Collaboration pattern
2. Supervisor pattern
3. Hierarchical teams
4. State protocol
5. Reliability and security

## 1. Collaboration Pattern

Use when agents are peers:

- Agent A works partial solution.
- Agent B critiques/extends.
- Loop until done criteria met.

Best for ideation and low-risk iterative tasks.

## 2. Supervisor Pattern

Use when central orchestration is required:

- Supervisor classifies subtask.
- Routes to specialist agent.
- Collects outputs and decides next step.

Best for deterministic control, SLAs, and safety oversight.

## 3. Hierarchical Teams

Use for complex organizations:

- Global supervisor routes to team supervisors.
- Team supervisors route to local specialists.
- Local summaries bubble upward.

Best for large domain decomposition and reusable subteams.

## 4. State Protocol

Required fields:

- `messages`
- `current_agent`
- `delegation_chain`
- `task_status`
- `final_answer`

## 5. Reliability and Security

- Add max-steps guard.
- Add allowlist for tool calls by role.
- Store audit trail of routing decisions.
- Enforce content policy checks before final answer.
