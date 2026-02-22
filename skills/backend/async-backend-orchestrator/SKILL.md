---
name: async-backend-orchestrator
description: Design and implement complex asynchronous backend logic with queues, workers, orchestration, retries, idempotency, and failure recovery. Use when building long-running workflows, background processing, event-driven systems, distributed task execution, or resilient queue-based architectures.
---

# Async Backend Orchestrator

## Overview

Build backend systems where complex work is processed asynchronously with strong delivery guarantees and operational control. Focus on queue topology, worker safety, and consistent outcomes.

## Workflow

1. Model workflows as explicit state transitions.
2. Split fast request path from heavy background work.
3. Choose queue technology by delivery guarantees and scale.
4. Define idempotency keys and deduplication strategy.
5. Add retries with capped exponential backoff and DLQ.
6. Add observability for queue lag and worker failures.
7. Add replay and compensation procedures.

## Queue and Worker Rules

- Keep handlers idempotent.
- Persist task state transitions.
- Use explicit task timeouts and visibility windows.
- Limit concurrency per task class.
- Guard external side effects with exactly-once semantics where possible.

## Implementation Assets

- Use `scripts/scaffold_async_backend.py` to generate API + worker + queue starter.
- Use `references/reference.md` for reliability and orchestration patterns.
- Use `references/examples.md` for saga/outbox and retry patterns.
- Use `assets/task-contract.json` for task envelope schema.

## Output Format

1. Workflow/state model
2. Queue topology and task contract
3. Worker concurrency/retry config
4. Failure recovery and DLQ strategy
5. Metrics, alerts, and runbook
