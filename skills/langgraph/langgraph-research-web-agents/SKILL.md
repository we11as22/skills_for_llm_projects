---
name: langgraph-research-web-agents
description: Design and implement LangGraph research and web-navigation agents inspired by STORM, WebVoyager, and advanced benchmark workflows. Use when building autonomous web research loops, browsing-and-action agents, multi-source synthesis pipelines, or benchmark-driven agent systems requiring planning, evidence tracking, and iterative refinement.
---

# LangGraph Research and Web Agents

## Overview

Build advanced autonomous research agents with web interaction, evidence synthesis, and controlled action loops.

## Covered Tutorial Patterns

- STORM-style long-form research synthesis
- WebVoyager-style web navigation/action loops
- Benchmark-driven iterative solving flows (e.g., USACO tutorial pattern)

## Workflow

1. Define task objective and action policy.
2. Split into planner, browser/action, extractor, and synthesizer nodes.
3. Track evidence with source URLs and confidence.
4. Add action budget and safety policy checks.
5. Add final synthesis and citation validation.

## Rules

- Keep browser actions explicit and reversible.
- Add domain allowlist for navigation.
- Require citation-backed synthesis.
- Stop on budget/time cap with partial output.

## Included Resources

- `references/reference.md`: architecture and safety controls.
- `references/examples.md`: web action loop and synthesis patterns.
- `scripts/scaffold_research_agent.py`: generates planner-browser-synthesizer graph skeleton.
- `assets/web-action-schema.json`: structured action contract.

## Output Format

1. Agent architecture and node roles
2. Action policy and limits
3. Evidence tracking schema
4. Synthesis and citation strategy
5. Evaluation and benchmark plan
