# Async Database Examples

## PostgreSQL (asyncpg)

```python
pool = await asyncpg.create_pool(dsn=dsn, min_size=5, max_size=20)
async with pool.acquire() as conn:
    rows = await conn.fetch("SELECT id, name FROM users WHERE active = true")
```

## MongoDB (motor)

```python
client = AsyncIOMotorClient(uri)
docs = await client.app.orders.find({"status": "pending"}).to_list(100)
```

## Redis (redis.asyncio)

```python
redis = Redis.from_url(redis_url)
await redis.set("session:123", "ok", ex=300)
```

## OpenSearch (async)

```python
client = AsyncOpenSearch(hosts=[{"host": "localhost", "port": 9200}])
await client.search(index="products", body={"query": {"match": {"name": "laptop"}}})
```

## Milvus

```python
# Build vector insert/query wrappers in a dedicated repository module.
# Keep embedding model/version stored with each vector record.
```
