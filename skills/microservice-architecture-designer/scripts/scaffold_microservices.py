#!/usr/bin/env python3
"""Scaffold a production-oriented local microservice workspace with Docker and Compose."""

from __future__ import annotations

import argparse
from pathlib import Path

SERVICE_TEMPLATE = """from fastapi import FastAPI

app = FastAPI(title=\"{service_name}\")


@app.get(\"/health\")
async def health() -> dict[str, str]:
    return {{\"status\": \"ok\", \"service\": \"{service_name}\"}}
"""

DOCKERFILE_TEMPLATE = """FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -m appuser

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
USER appuser

EXPOSE 8000
CMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]
"""

REQUIREMENTS = "fastapi==0.115.0\nuvicorn[standard]==0.30.6\n"

COMPOSE_TEMPLATE = """version: '3.9'

services:
  gateway:
    build: ./services/gateway
    ports:
      - \"8080:8000\"
    environment:
      - SERVICE_NAME=gateway
      - USERS_URL=http://users:8000
      - CATALOG_URL=http://catalog:8000
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started

  users:
    build: ./services/users
    environment:
      - DATABASE_URL=postgresql://app:app@postgres:5432/users
      - REDIS_URL=redis://redis:6379/0

  catalog:
    build: ./services/catalog
    environment:
      - DATABASE_URL=postgresql://app:app@postgres:5432/catalog

  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: app
    healthcheck:
      test: [\"CMD-SHELL\", \"pg_isready -U app\"]
      interval: 5s
      timeout: 3s
      retries: 10

  redis:
    image: redis:7

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - \"15672:15672\"
"""

MAKEFILE = """up:
\tdocker compose up --build

down:
\tdocker compose down -v

logs:
\tdocker compose logs -f
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def scaffold(target: Path, services: list[str]) -> None:
    write(target / "docker-compose.yml", COMPOSE_TEMPLATE)
    write(target / "Makefile", MAKEFILE)
    write(
        target / ".env.example",
        "POSTGRES_USER=app\nPOSTGRES_PASSWORD=app\nPOSTGRES_DB=app\n",
    )

    for service in services:
        service_dir = target / "services" / service
        write(service_dir / "app" / "main.py", SERVICE_TEMPLATE.format(service_name=service))
        write(service_dir / "requirements.txt", REQUIREMENTS)
        write(service_dir / "Dockerfile", DOCKERFILE_TEMPLATE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output project directory")
    parser.add_argument(
        "--services",
        nargs="+",
        default=["gateway", "users", "catalog"],
        help="Service names to scaffold",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scaffold(args.output, args.services)
    print(f"Scaffold created at {args.output}")


if __name__ == "__main__":
    main()
