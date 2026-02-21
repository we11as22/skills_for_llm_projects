---
name: langgraph-planning-reasoning
description: Design and implement LangGraph planning and reasoning architectures including plan-and-execute, ReWOO, LLM Compiler, LATS, reflection, reflexion, and self-discover patterns. Use when tasks require multi-step decomposition, dependency-aware execution, iterative self-critique, or search over candidate reasoning trajectories.
---

# LangGraph Planning and Reasoning

## Overview

Build advanced agent graphs for difficult tasks that need explicit plans, dependency management, and iterative improvement loops.

## Covered Tutorial Patterns

- Plan-and-Execute
- ReWOO (planner-executor-solver)
- LLM Compiler (planner, task fetching, joiner)
- LATS (tree search)
- Reflection and Reflexion loops
- Self-discover prompting structure

## Workflow

1. Define task objective and final success checks.
2. Choose decomposition style (linear plan, DAG plan, or search tree).
3. Define worker tools and action constraints.
4. Define critique/join strategy.
5. Add step budget, recursion limits, and fallback exits.
6. Add replay traces and evaluation metrics.

## Critical Rules

- Keep planner output machine-parseable.
- Separate planning from execution state.
- Add dependency validation before task execution.
- Cap reflection depth to avoid infinite loops.

## Included Resources

- `references/reference.md`: pattern-by-pattern architecture guidance.
- `references/examples.md`: snippet-level execution flows.
- `scripts/scaffold_planning_graphs.py`: generates starter templates for core planning architectures.
- `assets/plan-schema.json`: plan and task schema.

## Output Format

1. Chosen planning architecture
2. Graph node definitions
3. Plan format and dependency policy
4. Critique/repair strategy
5. Runtime and evaluation controls
