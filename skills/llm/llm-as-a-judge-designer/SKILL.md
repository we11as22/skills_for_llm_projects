---
name: llm-as-a-judge-designer
description: Design LLM-as-a-Judge systems with strict structured output, weighted criteria, calibration workflows, and audit-ready evaluation reports. Use when building automatic quality evaluation for LLM outputs, benchmarking prompts/models, scoring agent traces, or enforcing release gates with rubric-based decisions.
---

# LLM-as-a-Judge Designer

## Overview

Implement robust judge pipelines that produce strict JSON outputs across detailed quality criteria and can be calibrated against human labels.

## Workflow

1. Define evaluation scope and critical failure classes.
2. Define rubric with weighted criteria.
3. Define strict JSON Schema for judge output.
4. Build async evaluation runner with retries/timeouts.
5. Add calibration against human-rated benchmark set.
6. Set release gates and monitoring thresholds.

## Judge Criteria (Baseline)

- Task success
- Factuality/grounding
- Instruction following
- Safety/policy compliance
- Completeness
- Clarity/structure
- Citation quality (if required)
- Tool-use correctness (for agents)

## Core Rules

- Keep rubric criteria non-overlapping.
- Always require textual evidence/explanation per score.
- Separate critical-fail conditions from weighted aggregate.
- Version rubric and schema together.

## Included Resources

- `references/reference.md`: judge system architecture and calibration methods.
- `references/examples.md`: rubric and scoring examples.
- `scripts/run_llm_judge.py`: async judge runner with schema validation.
- `assets/judge-output-schema.json`: strict judge output contract.

## Output Format

1. Rubric definition
2. Schema definition
3. Evaluation pipeline
4. Calibration and threshold policy
5. Reporting format and release gate
