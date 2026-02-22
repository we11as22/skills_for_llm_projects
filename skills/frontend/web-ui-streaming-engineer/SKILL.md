---
name: web-ui-streaming-engineer
description: Build web UI progress streaming architectures and implementations using SSE, WebSocket, and Socket.IO with clear decision criteria, backend patterns, and frontend integration. Use when implementing live progress, notifications, collaborative updates, long-running task feedback, or deciding between SSE and bidirectional socket protocols.
---

# Web UI Streaming Engineer

## Overview

Design and implement real-time UX with the right transport per interaction model. Provide deterministic backend contracts and resilient frontend state handling for progress streams.

## Decision Rules

- Use SSE for server-to-client progress, logs, and token streams.
- Use WebSocket/Socket.IO for bidirectional collaboration, chat, and live control channels.
- Use polling only as compatibility fallback.

## Workflow

1. Classify update type (one-way vs two-way, frequency, fan-out).
2. Pick transport and define event schema.
3. Implement reconnect and resume strategy.
4. Handle backpressure and throttling.
5. Provide frontend state machine for stream lifecycle.
6. Add observability (dropped connections, reconnect count, lag).

## Reliability Rules

- Add heartbeat/keepalive.
- Support reconnection with exponential backoff.
- Tag events with monotonic sequence numbers.
- Make updates idempotent on client.

## Implementation Assets

- Use `scripts/create_streaming_demo.py` to scaffold FastAPI + SSE/WebSocket demo.
- Use `references/reference.md` for protocol tradeoffs and operations.
- Use `references/examples.md` for frontend integration snippets.
- Use `assets/event-schema.json` as baseline event model.

## Output Format

1. Transport choice with rationale
2. Event contract
3. Backend endpoint/channel design
4. Frontend stream management plan
5. Failure handling and fallback strategy
