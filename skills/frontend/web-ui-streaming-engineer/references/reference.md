# Web UI Streaming Reference

## Table of Contents

1. SSE vs WebSocket vs Socket.IO
2. Event schema
3. Backend patterns
4. Frontend patterns
5. Operations checklist

## 1. SSE vs WebSocket vs Socket.IO

- SSE: unidirectional, simple, HTTP-native, ideal for progress/log streams.
- WebSocket: full-duplex, low overhead, protocol-level control.
- Socket.IO: higher-level semantics (rooms, auto-reconnect), extra abstraction cost.

## 2. Event Schema

Required fields:

- `event_id`: unique event id
- `sequence`: monotonic sequence
- `task_id`: correlation id
- `type`: progress/log/error/done
- `timestamp`: ISO 8601
- `payload`: event-specific data

## 3. Backend Patterns

- Emit coarse-grained progress every N items/time interval.
- Avoid flooding clients with raw logs.
- Persist checkpoint to allow replay after reconnect.

## 4. Frontend Patterns

- Use finite-state machine: idle -> connecting -> streaming -> completed/error.
- Buffer and batch UI updates to avoid render thrash.
- Keep reconnection attempts bounded.

## 5. Operations Checklist

- Track active connections and disconnect reasons.
- Alert on sustained reconnect spikes.
- Document fallback behavior for environments that block sockets.
