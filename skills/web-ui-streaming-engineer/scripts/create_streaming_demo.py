#!/usr/bin/env python3
"""Generate a FastAPI streaming demo with SSE and WebSocket endpoints."""

from __future__ import annotations

import argparse
from pathlib import Path

APP_TEMPLATE = """from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone

from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse

app = FastAPI(title=\"Streaming Demo\")


def make_event(sequence: int) -> dict:
    return {
        \"event_id\": f\"evt_{sequence:04d}\",
        \"sequence\": sequence,
        \"task_id\": \"task_demo\",
        \"type\": \"progress\",
        \"timestamp\": datetime.now(timezone.utc).isoformat(),
        \"payload\": {\"percent\": sequence * 5},
    }


@app.get(\"/stream/sse\")
async def stream_sse() -> StreamingResponse:
    async def generator():
        for i in range(1, 21):
            payload = json.dumps(make_event(i))
            yield f\"data: {payload}\\n\\n\"
            await asyncio.sleep(0.4)

    return StreamingResponse(generator(), media_type=\"text/event-stream\")


@app.websocket(\"/stream/ws\")
async def stream_ws(websocket: WebSocket) -> None:
    await websocket.accept()
    for i in range(1, 21):
        await websocket.send_json(make_event(i))
        await asyncio.sleep(0.4)
    await websocket.close()
"""

HTML_TEMPLATE = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
    <title>Streaming Demo</title>
  </head>
  <body>
    <h1>Streaming Demo</h1>
    <button id=\"sse\">Start SSE</button>
    <button id=\"ws\">Start WebSocket</button>
    <pre id=\"output\"></pre>
    <script>
      const out = document.getElementById("output");

      document.getElementById("sse").onclick = () => {
        const es = new EventSource("/stream/sse");
        es.onmessage = (event) => {
          out.textContent += "SSE: " + event.data + "\\n";
        };
      };

      document.getElementById("ws").onclick = () => {
        const ws = new WebSocket(`ws://${location.host}/stream/ws`);
        ws.onmessage = (event) => {
          out.textContent += "WS: " + event.data + "\\n";
        };
      };
    </script>
  </body>
</html>
"""

REQS = "fastapi==0.115.0\nuvicorn[standard]==0.30.6\n"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output demo directory")
    args = parser.parse_args()

    write(args.output / "app.py", APP_TEMPLATE)
    write(args.output / "static" / "index.html", HTML_TEMPLATE)
    write(args.output / "requirements.txt", REQS)
    print(f"Streaming demo created at {args.output}")


if __name__ == "__main__":
    main()
