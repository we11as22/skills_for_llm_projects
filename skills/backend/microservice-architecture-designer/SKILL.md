---
name: microservice-architecture-designer
description: Design production-ready microservice architectures with clear bounded contexts, synchronous and asynchronous communication patterns, service contracts, data ownership, Dockerfiles, and docker-compose orchestration. Use when planning a new microservice system, refactoring a monolith, defining service boundaries, creating deployment topology, or generating architecture blueprints and starter code.
---

# Microservice Architecture Designer

## Overview

Design reliable microservice systems with explicit boundaries, deployment artifacts, and operational guardrails. Produce actionable architecture outputs that include Dockerfiles, docker-compose stacks, contracts, and migration plans.

## Workflow

1. Capture goals, scale, latency, data consistency rules, and compliance constraints.
2. Split domains by bounded context and map ownership per service.
3. Choose communication style per interaction: REST/gRPC for request-response, broker for events and decoupling.
4. Define API and event contracts before implementation.
5. Assign one primary datastore per service and document integration patterns.
6. Add resilience controls: retries, circuit breakers, timeouts, idempotency keys, DLQ.
7. Add observability: structured logs, metrics, tracing, health checks.
8. Produce runnable container artifacts and local compose topology.

## Architecture Rules

- Keep each service independently deployable.
- Avoid shared service databases.
- Use schema/versioned contracts for external APIs and events.
- Keep synchronous chains short to reduce cascading latency.
- Prefer eventual consistency with compensating actions for cross-service workflows.
- Include migration and rollback plans for every contract change.

## Deliverables

- Service catalog: purpose, owner, API surface, events, SLO.
- Context map and dependency graph.
- `docker-compose.yml` for local integration.
- Service `Dockerfile` patterns with multi-stage builds.
- Security baseline: secrets, mTLS/API auth, network segmentation.
- Runbook for failures and scaling strategy.

## Implementation Assets

- Use `scripts/scaffold_microservices.py` to generate a starter FastAPI microservice workspace with Dockerfiles and compose stack.
- Use `references/reference.md` for architecture checklists and production decisions.
- Use `references/examples.md` for monolith-to-microservices migration and event choreography examples.
- Use `assets/templates/docker-compose.base.yml` and `assets/templates/service.Dockerfile` as copyable templates.

## Output Format

When producing architecture output, include these sections in order:

1. System goals and constraints
2. Proposed service boundaries
3. Communication matrix (sync vs async)
4. Data ownership and consistency model
5. Docker and deployment topology
6. Reliability and observability controls
7. Risks and phased rollout plan
