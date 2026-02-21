# LLM Async Examples

## Example 1: Structured Extraction Contract

```json
{
  "type": "object",
  "required": ["invoice_id", "amount", "currency"],
  "properties": {
    "invoice_id": { "type": "string" },
    "amount": { "type": "number" },
    "currency": { "type": "string" }
  },
  "additionalProperties": false
}
```

## Example 2: Async Batch

```python
semaphore = asyncio.Semaphore(10)
results = await asyncio.gather(*(run_one(item, semaphore) for item in items))
```

## Example 3: Validation Gate

```python
jsonschema.validate(instance=parsed, schema=schema)
```
