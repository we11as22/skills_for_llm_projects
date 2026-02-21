#!/usr/bin/env python3
"""Lint prompt templates for common quality and safety issues."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED_HINTS = [
    ("output", "Missing explicit output instructions"),
    ("json", "Missing machine-readable output constraint (for structured tasks)"),
]

ANTI_PATTERNS = [
    (r"everything", "Vague scope: avoid words like 'everything'"),
    (r"as much as possible", "Unbounded output request"),
    (r"ignore previous", "Potential prompt injection keyword"),
]


def lint_prompt(text: str) -> list[str]:
    issues: list[str] = []
    lowered = text.lower()

    for token, message in REQUIRED_HINTS:
        if token not in lowered:
            issues.append(message)

    for pattern, message in ANTI_PATTERNS:
        if re.search(pattern, lowered):
            issues.append(message)

    if len(text) > 7000:
        issues.append("Prompt is very long; reduce context to improve consistency")

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Prompt file path")
    args = parser.parse_args()

    text = args.file.read_text()
    issues = lint_prompt(text)

    if not issues:
        print("Prompt lint: OK")
        return

    print("Prompt lint issues:")
    for issue in issues:
        print(f"- {issue}")


if __name__ == "__main__":
    main()
