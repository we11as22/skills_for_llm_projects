# Async Backend Reference

## Table of Contents

1. Queue selection
2. Handler design
3. Retry and DLQ
4. Orchestration patterns
5. Operations

## 1. Queue Selection

- Redis streams: simple infra, strong enough for many workloads.
- RabbitMQ: routing flexibility, mature ack model.
- Kafka: high-throughput log-based event streams.
- SQS/PubSub: managed options with cloud-native integration.

## 2. Handler Design

- Validate payload early.
- Make task handlers idempotent.
- Bound execution time.
- Emit task lifecycle events (`queued`, `running`, `retrying`, `done`, `failed`).

## 3. Retry and DLQ

- Retry transient failures only.
- Use exponential backoff with jitter.
- Move poison messages to DLQ after max attempts.
- Keep replay tooling simple and audited.

## 4. Orchestration Patterns

- Saga: distributed state changes with compensations.
- Outbox: transactional event publication.
- Fan-out/fan-in: parallel subtasks with aggregation.

## 5. Operations

- Monitor queue depth, age, throughput, failure rates.
- Alert on consumer lag and retry storms.
- Keep emergency kill-switch for failing task classes.
