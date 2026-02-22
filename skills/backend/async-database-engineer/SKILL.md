---
name: async-database-engineer
description: Design and implement asynchronous data layers for relational, document, key-value, graph, search, and vector databases, including PostgreSQL, MySQL, MongoDB, Redis, OpenSearch, and Milvus. Use when building backend persistence, selecting datastore types, defining async access patterns, tuning queries, or generating production-ready multi-database code examples.
---

# Async Database Engineer

## Overview

Implement robust async database access across heterogeneous storage systems. Choose the right database per workload and enforce resilient patterns for pooling, retries, observability, and migration.

## Workflow

1. Map workload types: transactional, analytical, search, vector, cache, graph.
2. Select datastore per workload and SLA.
3. Define async client lifecycle and pooling rules.
4. Add repository layer with typed DTO/model mapping.
5. Add retries/timeouts only for transient operations.
6. Add health checks, metrics, and query tracing.
7. Validate index strategy and migration flow.

## Core Rules

- Keep one source-of-truth store per domain aggregate.
- Use cache/search/vector stores as derived views, not authoritative writes.
- Never share connection objects across incompatible event loops.
- Always close async clients on shutdown.
- Implement idempotent writes where retries may happen.

## Supported Datastores

- Relational: PostgreSQL, MySQL, SQLite, SQL Server.
- Document: MongoDB.
- Key-value/cache: Redis.
- Search: OpenSearch/Elasticsearch.
- Vector: Milvus (and compatible patterns for Qdrant/pgvector).
- Graph/time-series: Neo4j, TimescaleDB, ClickHouse (via async drivers/adapters).

## Implementation Assets

- Use `scripts/generate_async_db_starter.py` to scaffold async client layer for multiple engines.
- Use `references/reference.md` for driver choices, pooling, and reliability patterns.
- Use `references/examples.md` for practical snippets per datastore.
- Use `assets/dsn-examples.env` for DSN conventions.

## Output Format

1. Workload-to-database matrix
2. Async access layer design
3. Indexing and consistency plan
4. Failure and retry strategy
5. Migration and observability checklist
