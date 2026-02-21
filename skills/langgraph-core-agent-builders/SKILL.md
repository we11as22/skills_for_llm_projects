---
name: langgraph-core-agent-builders
description: Build foundational LangGraph applications from core tutorial patterns including introduction flows, information-gather prompting, code-assistant pipelines, and customer-support orchestration. Use when starting new LangGraph projects, defining typed state graphs, implementing core nodes, or scaffolding production-ready single-agent and tool-agent apps.
---

# LangGraph Core Agent Builders

## Overview

Implement baseline LangGraph applications with strong fundamentals: typed state, predictable transitions, clear tool boundaries, and deterministic prompts.

## Covered Tutorial Patterns

- Introductory state graph patterns
- Prompt generation from information gathering
- Code assistant workflow graph
- Customer support agent flow

## Workflow

1. Define graph state schema.
2. Define core nodes (collect context, call model, call tools, finalize answer).
3. Define routing conditions and stop criteria.
4. Add structured output model and validation.
5. Add logging/tracing and basic tests.

## Rules

- Keep each node single-purpose.
- Keep prompt templates versioned.
- Validate tool arguments before invocation.
- Store conversation summary for long interactions.

## Included Resources

- `references/reference.md`: foundational patterns and pitfalls.
- `references/examples.md`: minimal core graph templates.
- `scripts/scaffold_core_agent_graph.py`: generate starter graph package.
- `assets/core-state-schema.json`: state schema baseline.

## Output Format

1. Graph purpose and scope
2. State schema and nodes
3. Routing logic
4. Prompt/tool contracts
5. Validation and observability plan
