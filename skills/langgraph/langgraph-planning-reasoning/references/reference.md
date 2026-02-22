# Planning and Reasoning Reference

## Table of Contents

1. Plan-and-execute
2. ReWOO
3. LLM compiler
4. Reflection and reflexion
5. LATS
6. Self-discover

## 1. Plan-and-Execute

- Planner emits ordered tasks.
- Executor runs tasks sequentially.
- Re-plan node adjusts unfinished steps.

## 2. ReWOO

- Planner creates steps with symbolic references.
- Executor resolves tool calls and fills references.
- Solver composes final answer from resolved steps.

## 3. LLM Compiler

- Planner emits DAG-like task list.
- Task fetching unit dispatches ready tasks.
- Joiner aggregates results and decides completion.

## 4. Reflection and Reflexion

- Generate draft.
- Critique quality and identify issues.
- Revise with bounded loop count.

## 5. LATS

- Build candidate reasoning tree.
- Score nodes with heuristic/judge.
- Expand top candidates until budget exhausted.

## 6. Self-discover

- Choose reasoning modules dynamically.
- Compose module sequence per task characteristics.
