#!/usr/bin/env python3
"""Generate an architecture decision record scaffold for LangGraph projects."""

from __future__ import annotations

import argparse
from pathlib import Path

TEMPLATE = """# ADR: {title}

## Context

- Problem:
- Users:
- Constraints (latency/cost/safety/compliance):

## Selected Tutorial Family

- Family: {family}
- Pattern: {pattern}
- Source tutorial URL:

## Decision

- Graph topology:
- Node responsibilities:
- State schema:
- Tool boundaries:

## Reliability and Safety

- Retry policy:
- Timeouts:
- Checkpointing:
- Guardrails:

## Evaluation Plan

- Offline dataset:
- Metrics:
- Judge/human review:

## Rollout Plan

- Phase 1 (shadow):
- Phase 2 (canary):
- Phase 3 (full):

## Risks and Mitigations

- Risk 1:
- Risk 2:
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output ADR markdown file")
    parser.add_argument("--title", default="LangGraph Architecture")
    parser.add_argument("--family", default="multi-agent")
    parser.add_argument("--pattern", default="agent-supervisor")
    args = parser.parse_args()

    content = TEMPLATE.format(title=args.title, family=args.family, pattern=args.pattern)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content)
    print(f"ADR template written: {args.output}")


if __name__ == "__main__":
    main()
