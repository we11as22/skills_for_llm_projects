# LLM Async Reference

## Table of Contents

1. Async orchestration model
2. Retry policy
3. Structured output strategy
4. Safety and reliability
5. Evaluation loop

## 1. Async Orchestration Model

- Use semaphore-based concurrency limits.
- Batch independent requests when possible.
- Keep end-to-end request deadline shorter than user timeout budget.

## 2. Retry Policy

- Retry classes: timeouts, connection reset, 429, 5xx.
- Avoid retry on validation failures unless prompt/model fallback changes.
- Add bounded exponential backoff with jitter.

## 3. Structured Output Strategy

- Use JSON Schema with strict required fields.
- Validate output before business logic.
- Log schema validation errors with prompt/model version.

## 4. Safety and Reliability

- Add prompt injection guards for retrieval contexts.
- Sanitize high-risk tool arguments.
- Keep model-generated decisions auditable.

## 5. Evaluation Loop

- Build golden datasets per use case.
- Track exact-match/field-level accuracy and latency/cost.
- Run regression checks before prompt/model changes.
