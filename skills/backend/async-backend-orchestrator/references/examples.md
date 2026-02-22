# Async Backend Examples

## Task Envelope

```json
{
  "task_id": "task_01",
  "type": "invoice.generate",
  "attempt": 1,
  "idempotency_key": "invoice:2026-01-10:42",
  "payload": { "invoice_id": 42 }
}
```

## Retry Policy

- Attempt 1: immediate
- Attempt 2: +3s
- Attempt 3: +9s
- Attempt 4: +27s
- Then DLQ

## Saga Example

1. Reserve inventory.
2. Charge payment.
3. Confirm order.
4. On payment failure, release inventory.
