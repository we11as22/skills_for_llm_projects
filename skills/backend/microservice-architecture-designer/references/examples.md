# Microservice Architecture Examples

## Example 1: E-commerce Service Split

- `gateway`: authentication, rate limiting, request routing.
- `catalog`: product metadata and search index publish events.
- `orders`: order lifecycle and payment orchestration.
- `inventory`: stock reservation and release.
- `notifications`: email/webhook events.

Event flow:

1. `orders` emits `order.created`.
2. `inventory` reserves stock and emits `inventory.reserved`.
3. `orders` confirms payment and emits `order.confirmed`.
4. `notifications` sends customer updates.

## Example 2: Monolith Strangler Migration

1. Introduce API gateway in front of monolith.
2. Extract read-only catalog first.
3. Extract write-heavy order flow second.
4. Move async integrations to broker.
5. Decommission monolith modules gradually.

## Example 3: Docker Compose Layout

```yaml
services:
  gateway:
    build: ./services/gateway
  users:
    build: ./services/users
  postgres:
    image: postgres:16
  redis:
    image: redis:7
  rabbitmq:
    image: rabbitmq:3-management
```
