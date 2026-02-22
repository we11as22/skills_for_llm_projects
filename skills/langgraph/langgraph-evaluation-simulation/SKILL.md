---
name: langgraph-evaluation-simulation
description: Design and run LangGraph evaluation pipelines using simulation-based testing, synthetic users, scenario datasets, and LLM/human judging loops. Use when validating assistant quality before release, benchmarking architecture variants, stress-testing safety behavior, or implementing continuous evaluation for graph-based agents.
---

# LangGraph Evaluation and Simulation

## Overview

Evaluate agent behavior systematically with simulated users, reproducible scenarios, and structured judge outputs.

## Covered Tutorial Patterns

- Multi-agent simulation for chatbot evaluation
- LangSmith-style simulation benchmarking loops

## Workflow

1. Define test scenarios and expected outcomes.
2. Build simulated user personas and interaction policies.
3. Run assistant under simulation at scale.
4. Judge outputs with structured criteria.
5. Aggregate metrics and error taxonomy.
6. Feed failures into prompt/graph/tool iteration backlog.

## Quality Rules

- Separate functional success from style quality.
- Track policy/safety failures explicitly.
- Keep judge schema stable and versioned.
- Include adversarial and edge-case scenarios.

## Included Resources

- `references/reference.md`: evaluation architecture and metric taxonomy.
- `references/examples.md`: scenario formats and scorecards.
- `scripts/scaffold_simulation_harness.py`: async simulation and scoring starter.
- `assets/eval-schema.json`: structured evaluation output schema.

## Output Format

1. Evaluation objective and scope
2. Dataset/persona design
3. Judge criteria and schema
4. Result metrics and error clusters
5. Recommended remediation plan
