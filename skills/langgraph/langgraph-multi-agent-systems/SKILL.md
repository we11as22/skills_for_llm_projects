---
name: langgraph-multi-agent-systems
description: Design and implement LangGraph multi-agent systems using collaboration, supervisor, and hierarchical team architectures with typed state, tool routing, and operational guardrails. Use when building specialist-agent teams, delegation strategies, inter-agent protocols, or production workflows requiring structured coordination.
---

# LangGraph Multi-Agent Systems

## Overview

Build multi-agent graphs with clear responsibilities, deterministic routing, and safe tool boundaries. Cover three core architectures from the tutorials: collaboration, supervisor, and hierarchical teams.

## Architecture Decision Tree

1. Use collaboration when peers can iterate with minimal central control.
2. Use supervisor when one controller routes tasks to specialists.
3. Use hierarchical teams when domains are large and each team needs its own supervisor.

## Workflow

1. Define agent roles and non-overlapping capability boundaries.
2. Define shared state schema and message protocol.
3. Choose routing strategy and termination conditions.
4. Constrain tool access per agent.
5. Add recursion and loop guards.
6. Add tracing and per-agent metrics.

## Critical Rules

- Never allow unconstrained recursive handoffs.
- Keep one owner for final user response.
- Encode delegation reason in state for observability.
- Add timeout budget for every agent turn.

## Included Resources

- `references/reference.md`: deep design guidance and anti-patterns.
- `references/examples.md`: exact topology patterns and minimal snippets.
- `scripts/scaffold_multi_agent_graph.py`: generates collaboration/supervisor/hierarchy starter code.
- `assets/state-schema.json`: shared graph state contract.

## Output Format

1. Team topology
2. Agent role table
3. Routing policy and stop conditions
4. Failure recovery strategy
5. Test and evaluation checklist
