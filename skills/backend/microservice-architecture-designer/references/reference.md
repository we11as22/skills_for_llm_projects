# Microservice Architecture Reference

## Table of Contents

1. Service boundary heuristics
2. Communication decisions
3. Data and consistency patterns
4. Docker and compose standards
5. Reliability baseline
6. Security baseline
7. Observability baseline

## 1. Service Boundary Heuristics

- Split by business capability and change cadence, not by technical layers.
- Keep write model ownership inside one service.
- Keep team cognitive load low: each service should be understandable by one team.
- Extract services only when autonomy or scaling benefit is clear.

## 2. Communication Decisions

- Use REST/gRPC for user-facing queries and strict request-response flows.
- Use event brokers (RabbitMQ/Kafka/NATS) for fan-out, decoupling, and async workflows.
- Enforce deadlines and retries with exponential backoff for sync calls.
- Use idempotency keys for externally triggered operations.

## 3. Data and Consistency Patterns

- Database per service.
- Use outbox pattern for reliable event publication.
- Use saga pattern for cross-service transactions.
- Use CQRS read models where cross-service query composition is expensive.

## 4. Docker and Compose Standards

- Multi-stage Dockerfile with non-root runtime user.
- Healthcheck in each container.
- `depends_on` + health checks for startup ordering in local environments.
- Separate infra services (db, cache, broker) from business services.

## 5. Reliability Baseline

- Timeouts on every network call.
- Retries only for transient errors.
- Circuit breaker on unstable upstreams.
- Dead-letter queue for poison messages.
- Correlation IDs propagated across services.

## 6. Security Baseline

- Never bake secrets into images.
- Prefer secret manager or injected env vars.
- Enforce least-privilege DB users per service.
- Restrict internal admin endpoints.

## 7. Observability Baseline

- Structured logs (JSON).
- Request and trace IDs in logs.
- Metrics: latency, throughput, error rate, saturation.
- Distributed tracing across sync and async paths.
