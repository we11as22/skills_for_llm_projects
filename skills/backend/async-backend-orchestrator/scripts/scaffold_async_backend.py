#!/usr/bin/env python3
"""Generate an async backend starter with API and worker processes."""

from __future__ import annotations

import argparse
from pathlib import Path

API_TEMPLATE = """from __future__ import annotations

import asyncio
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel

from shared.queue import in_memory_queue

app = FastAPI(title=\"Async Backend Starter\")


class TaskRequest(BaseModel):
    type: str
    payload: dict


@app.post(\"/tasks\")
async def create_task(task: TaskRequest) -> dict:
    task_id = str(uuid4())
    await in_memory_queue.put({"task_id": task_id, "type": task.type, "payload": task.payload, "attempt": 1})
    return {"task_id": task_id, "status": "queued"}


@app.get(\"/health\")
async def health() -> dict:
    return {"status": "ok", "queue_size": in_memory_queue.qsize()}
"""

WORKER_TEMPLATE = """from __future__ import annotations

import asyncio
import random

from shared.queue import in_memory_queue


async def process(task: dict) -> None:
    # Replace this with domain logic.
    await asyncio.sleep(0.2)
    if random.random() < 0.1:
        raise RuntimeError("Transient worker error")


async def worker_loop() -> None:
    while True:
        task = await in_memory_queue.get()
        try:
            await process(task)
            print(f"done: {task['task_id']}")
        except Exception as exc:
            task["attempt"] += 1
            if task["attempt"] > 4:
                print(f"dlq: {task['task_id']} reason={exc}")
            else:
                await asyncio.sleep(2 ** task["attempt"])
                await in_memory_queue.put(task)
                print(f"retry: {task['task_id']} attempt={task['attempt']}")
        finally:
            in_memory_queue.task_done()


if __name__ == "__main__":
    asyncio.run(worker_loop())
"""

QUEUE_TEMPLATE = """from __future__ import annotations

import asyncio

# In-memory queue for local demo. Replace with Redis/RabbitMQ/Kafka in production.
in_memory_queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=10000)
"""

DOCKER_COMPOSE = """version: '3.9'
services:
  api:
    build: .
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000
    ports:
      - \"8000:8000\"
  worker:
    build: .
    command: python worker/runner.py
"""

DOCKERFILE = """FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
"""

REQUIREMENTS = "fastapi==0.115.0\nuvicorn[standard]==0.30.6\npydantic==2.8.2\n"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output project directory")
    args = parser.parse_args()

    root = args.output
    write(root / "api" / "main.py", API_TEMPLATE)
    write(root / "worker" / "runner.py", WORKER_TEMPLATE)
    write(root / "shared" / "queue.py", QUEUE_TEMPLATE)
    write(root / "docker-compose.yml", DOCKER_COMPOSE)
    write(root / "Dockerfile", DOCKERFILE)
    write(root / "requirements.txt", REQUIREMENTS)
    print(f"Async backend starter created at {root}")


if __name__ == "__main__":
    main()
