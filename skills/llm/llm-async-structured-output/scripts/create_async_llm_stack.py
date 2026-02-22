#!/usr/bin/env python3
"""Generate a provider-agnostic async LLM stack with retries and JSON Schema validation."""

from __future__ import annotations

import argparse
from pathlib import Path

CLIENT_TEMPLATE = """from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any, Protocol

import jsonschema
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential


class TransientLLMError(Exception):
    pass


class LLMTransport(Protocol):
    async def complete(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        ...


@dataclass
class AsyncStructuredLLMClient:
    transport: LLMTransport
    timeout_seconds: float = 30.0

    @retry(
        retry=retry_if_exception_type(TransientLLMError),
        wait=wait_random_exponential(multiplier=0.5, max=8),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    async def _call_with_retry(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        return await self.transport.complete(prompt, schema)

    async def run(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        result = await asyncio.wait_for(self._call_with_retry(prompt, schema), timeout=self.timeout_seconds)
        jsonschema.validate(instance=result, schema=schema)
        return result
"""

TRANSPORT_TEMPLATE = """from __future__ import annotations

import json
from typing import Any

import httpx

from llm_client import TransientLLMError


class HttpResponsesTransport:
    \"\"\"HTTP transport for providers exposing a responses-like endpoint.

    Adapt endpoint/payload extraction to your provider.
    \"\"\"

    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    async def complete(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "input": prompt,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_response",
                    "schema": schema,
                    "strict": True,
                },
            },
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{self.base_url}/v1/responses", json=payload, headers=headers)

        if response.status_code in {429, 500, 502, 503, 504}:
            raise TransientLLMError(f"Transient status: {response.status_code}")
        response.raise_for_status()

        body = response.json()
        # Provider-specific extraction. Keep this parser centralized.
        if isinstance(body.get("output_json"), dict):
            return body["output_json"]

        text = body.get("output_text")
        if isinstance(text, str):
            return json.loads(text)

        raise ValueError("Cannot extract structured output from provider response")
"""

PIPELINE_TEMPLATE = """from __future__ import annotations

import asyncio
from typing import Any

from llm_client import AsyncStructuredLLMClient


async def run_batch(
    client: AsyncStructuredLLMClient,
    prompts: list[str],
    schema: dict[str, Any],
    concurrency: int = 8,
) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(concurrency)

    async def run_one(prompt: str) -> dict[str, Any]:
        async with semaphore:
            return await client.run(prompt, schema)

    return await asyncio.gather(*(run_one(prompt) for prompt in prompts))
"""

REQUIREMENTS = "httpx==0.27.0\njsonschema==4.23.0\ntenacity==9.0.0\n"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output directory")
    args = parser.parse_args()

    write(args.output / "llm_client.py", CLIENT_TEMPLATE)
    write(args.output / "transport_http.py", TRANSPORT_TEMPLATE)
    write(args.output / "pipeline.py", PIPELINE_TEMPLATE)
    write(args.output / "requirements.txt", REQUIREMENTS)
    print(f"Async LLM stack created at {args.output}")


if __name__ == "__main__":
    main()
