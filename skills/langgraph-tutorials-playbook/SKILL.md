---
name: langgraph-tutorials-playbook
description: Navigate and apply the full LangGraph tutorials set as production design patterns. Use when selecting the right LangGraph architecture, mapping tutorial patterns to real requirements, planning implementation phases, or generating starter graphs and decision records from the official tutorial families.
---

# LangGraph Tutorials Playbook

## Overview

Map project requirements to the correct LangGraph architecture family and produce implementation-ready plans. Use this skill as the top-level router before choosing a deeper specialized LangGraph skill.

## Workflow

1. Capture workload goals: latency, cost, reliability, autonomy level, human oversight.
2. Select tutorial family (core, multi-agent, RAG, planning/reasoning, evaluation, research/web).
3. Choose concrete architecture pattern from the matrix in `references/tutorial-map.md`.
4. Generate project skeleton and ADR checklist with `scripts/generate_langgraph_adr.py`.
5. Decompose into incremental milestones: baseline graph -> safety gates -> eval harness -> production rollout.

## Selection Rules

- Choose single-agent graph first when tool orchestration is simple.
- Choose supervisor/hierarchy when multiple specialists need routing and control.
- Choose adaptive/corrective/self-RAG when retrieval quality is uncertain.
- Choose plan/execute or ReWOO for long multi-step tasks with dependencies.
- Add simulation + judge loops before production release.

## Included Resources

- Read `references/tutorial-map.md` for full tutorial-to-pattern coverage.
- Read `references/reference.md` for decision criteria and anti-patterns.
- Read `references/examples.md` for requirement-to-architecture mapping.
- Use `assets/adr-template.md` to document architecture decisions.
- Use `scripts/generate_langgraph_adr.py` to generate ADR scaffold quickly.

## Output Format

1. Requirement summary
2. Chosen tutorial family and exact pattern
3. Graph topology outline
4. Safety/evaluation plan
5. Phase-by-phase implementation roadmap
