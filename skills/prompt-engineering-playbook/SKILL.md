---
name: prompt-engineering-playbook
description: Design, debug, and optimize prompts for reliable LLM behavior across extraction, reasoning, coding, and agent workflows. Use when building prompt templates, adding guardrails, defining evaluation criteria, reducing hallucinations, or establishing prompt versioning and experimentation practices.
---

# Prompt Engineering Playbook

## Overview

Create prompt systems that are testable, versioned, and aligned with measurable task outcomes. Focus on prompt structure, instruction clarity, context control, and evaluation loops.

## Workflow

1. Define task objective and success metric.
2. Encode role, constraints, and output contract.
3. Add high-signal context only.
4. Provide examples only when they improve consistency.
5. Add refusal/safety boundaries.
6. Evaluate on golden cases and iterate.

## Prompt Rules

- Put non-negotiable constraints early.
- Make output format explicit and machine-parseable.
- Avoid conflicting instructions.
- Keep context concise and relevant.
- Version prompts and compare with offline tests.

## Implementation Assets

- Use `scripts/prompt_linter.py` to lint templates for common quality issues.
- Use `references/reference.md` for prompt design patterns.
- Use `references/examples.md` for before/after prompt rewrites.
- Use `assets/prompt-template.md` as a baseline template.

## Output Format

1. Task contract
2. Prompt template
3. Expected output schema
4. Evaluation plan
5. Iteration log
