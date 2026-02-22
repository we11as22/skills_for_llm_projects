# Web UI Streaming Examples

## SSE Client

```ts
const source = new EventSource("/stream/tasks/123");
source.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateProgress(data);
};
```

## WebSocket Client

```ts
const ws = new WebSocket("ws://localhost:8000/ws/tasks/123");
ws.onmessage = (event) => applyEvent(JSON.parse(event.data));
ws.send(JSON.stringify({ type: "pause" }));
```

## Event Payload

```json
{
  "event_id": "evt_001",
  "sequence": 10,
  "task_id": "task_123",
  "type": "progress",
  "payload": { "percent": 42 }
}
```
