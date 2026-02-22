#!/usr/bin/env python3
"""Generate a polyglot async database starter package."""

from __future__ import annotations

import argparse
from pathlib import Path

INIT_TEMPLATE = """\"\"\"Async DB starter package.\"\"\"
"""

POSTGRES_TEMPLATE = """from __future__ import annotations

import asyncpg


class PostgresClient:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(dsn=self._dsn, min_size=2, max_size=20)

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()

    async def fetch_users(self) -> list[dict]:
        if self._pool is None:
            raise RuntimeError("Pool is not initialized")
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("SELECT id, email FROM users LIMIT 100")
        return [dict(row) for row in rows]
"""

MONGO_TEMPLATE = """from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorClient


class MongoClient:
    def __init__(self, uri: str) -> None:
        self._client = AsyncIOMotorClient(uri)

    async def fetch_orders(self) -> list[dict]:
        return await self._client.app.orders.find({"status": "open"}).to_list(100)

    async def close(self) -> None:
        self._client.close()
"""

REDIS_TEMPLATE = """from __future__ import annotations

from redis.asyncio import Redis


class RedisCache:
    def __init__(self, url: str) -> None:
        self._redis = Redis.from_url(url)

    async def set_cache(self, key: str, value: str, ttl_seconds: int = 60) -> None:
        await self._redis.set(key, value, ex=ttl_seconds)

    async def get_cache(self, key: str) -> str | None:
        value = await self._redis.get(key)
        if value is None:
            return None
        return value.decode() if isinstance(value, bytes) else str(value)

    async def close(self) -> None:
        await self._redis.close()
"""

OPENSEARCH_TEMPLATE = """from __future__ import annotations

from opensearchpy import AsyncOpenSearch


class SearchClient:
    def __init__(self, host: str, port: int) -> None:
        self._client = AsyncOpenSearch(hosts=[{"host": host, "port": port}])

    async def search_products(self, text: str) -> dict:
        query = {"query": {"multi_match": {"query": text, "fields": ["name^2", "description"]}}}
        return await self._client.search(index="products", body=query)

    async def close(self) -> None:
        await self._client.close()
"""

MILVUS_TEMPLATE = """from __future__ import annotations

# Note: pymilvus async support varies by version. Use async APIs when available,
# otherwise isolate sync client calls in worker threads/processes.


class MilvusVectorStore:
    def __init__(self, uri: str, collection: str) -> None:
        self.uri = uri
        self.collection = collection

    async def upsert_embeddings(self, rows: list[dict]) -> None:
        # Replace with actual async/sync Milvus calls for your environment.
        _ = rows

    async def similarity_search(self, embedding: list[float], top_k: int = 10) -> list[dict]:
        _ = embedding
        return [{"id": "demo", "score": 0.99, "top_k": top_k}]
"""

README_TEMPLATE = """# Async DB Starter

Generated clients:
- `postgres.py`
- `mongo.py`
- `redis_cache.py`
- `search.py` (OpenSearch)
- `vector.py` (Milvus pattern)

Integrate by wiring `connect()`/`close()` into application startup/shutdown hooks.
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output directory")
    args = parser.parse_args()

    root = args.output / "db_clients"
    write(root / "__init__.py", INIT_TEMPLATE)
    write(root / "postgres.py", POSTGRES_TEMPLATE)
    write(root / "mongo.py", MONGO_TEMPLATE)
    write(root / "redis_cache.py", REDIS_TEMPLATE)
    write(root / "search.py", OPENSEARCH_TEMPLATE)
    write(root / "vector.py", MILVUS_TEMPLATE)
    write(args.output / "README.md", README_TEMPLATE)

    print(f"Async DB starter generated in {args.output}")


if __name__ == "__main__":
    main()
