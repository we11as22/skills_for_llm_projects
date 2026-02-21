---
name: llm-async-structured-output
description: Build asynchronous LLM integrations with retries, timeout control, circuit-safe patterns, and strict structured output validated by JSON Schema. Use when implementing LLM features in production, orchestrating concurrent LLM tasks, enforcing output contracts, or creating resilient async pipelines for generation, extraction, and decision support.
---

# LLM Async Structured Output

## Overview

Implement production LLM workflows with asynchronous execution, deterministic output contracts, and robust failure handling. Prioritize typed outputs and traceable behavior over ad-hoc text parsing.

## Workflow

1. Define task contract with JSON Schema.
2. Build async request pipeline with bounded concurrency.
3. Add timeouts, retries with jitter, and fallback strategy.
4. Validate model output against schema.
5. Store raw response + validated artifact for debugging.
6. Add evaluation hooks and error taxonomy.

## Reliability Rules

- Use explicit deadline per request.
- Retry only transient failures (429/5xx/network).
- Apply idempotency keys where supported.
- Keep prompts versioned and traceable.
- Validate every structured response before downstream use.

## Implementation Assets

- Use `scripts/create_async_llm_stack.py` to scaffold resilient async LLM client code.
- Use `references/reference.md` for retries, concurrency, and schema patterns.
- Use `references/examples.md` for extraction and classification flows.
- Use `assets/base-response-schema.json` as a strict output contract seed.

## Output Format

1. Task and schema definition
2. Async execution and concurrency model
3. Retry/timeout/fallback policy
4. Validation and parsing plan
5. Evaluation and observability checklist
