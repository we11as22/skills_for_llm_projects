# Async Database Reference

## Table of Contents

1. Driver selection
2. Connection lifecycle
3. Per-database best practices
4. Retry and timeout policy
5. Schema/index strategy

## 1. Driver Selection

- PostgreSQL: `asyncpg` or SQLAlchemy 2 async.
- MySQL: `aiomysql` / SQLAlchemy async.
- SQLite: `aiosqlite` (light workloads).
- MongoDB: `motor`.
- Redis: `redis.asyncio`.
- OpenSearch: `opensearch-py` async client.
- Milvus: `pymilvus` async APIs where available or worker-offloaded sync calls.

## 2. Connection Lifecycle

- Initialize pools in app startup hooks.
- Inject connections/sessions per request/task scope.
- Close pools/clients on shutdown.
- Expose readiness checks for downstream dependency health.

## 3. Per-Database Best Practices

### PostgreSQL

- Use transactions for multi-step writes.
- Prefer prepared statements for hot paths.
- Monitor slow query log and lock contention.

### MongoDB

- Avoid unbounded array growth in documents.
- Design compound indexes to match query shapes.
- Keep document size under operational limits.

### Redis

- Use expirations for cache keys.
- Use Lua/scripts for atomic read-modify-write logic where needed.
- Separate cache DB namespace from queue or lock data.

### OpenSearch

- Tune shard/replica count by index size and query profile.
- Keep mappings explicit for predictable relevance.
- Use bulk API for ingestion.

### Milvus

- Version embedding models and vector dimensions.
- Use metadata filtering before ANN search when possible.
- Rebuild/reindex vectors on model upgrades.

## 4. Retry and Timeout Policy

- Timeout every external call.
- Retry only transient network/overload classes.
- Never retry non-idempotent writes without safeguards.

## 5. Schema and Index Strategy

- Keep migration scripts deterministic and reversible.
- Co-locate migration history with application versioning.
- Benchmark index impact on both read and write workloads.
