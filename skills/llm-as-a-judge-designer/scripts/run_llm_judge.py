#!/usr/bin/env python3
"""Run asynchronous LLM-as-a-Judge evaluation with strict JSON Schema validation.

This script includes a deterministic local fallback judge for environments without
an online LLM provider. Replace `call_external_judge` with your provider client.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any

import jsonschema


DEFAULT_RUBRIC = {
    "task_success": 0.2,
    "factuality": 0.25,
    "instruction_following": 0.15,
    "safety": 0.2,
    "completeness": 0.1,
    "clarity": 0.1,
}


def local_fallback_judge(candidate_output: str, rubric: dict[str, float]) -> dict[str, Any]:
    length_score = 0.9 if len(candidate_output) > 80 else 0.6
    criteria = {}
    for name in rubric:
        criteria[name] = {
            "score": length_score,
            "evidence": f"Heuristic placeholder for {name}.",
            "issues": [],
        }

    overall = sum(criteria[name]["score"] * weight for name, weight in rubric.items())
    hard_fail = criteria["safety"]["score"] < 0.6
    verdict = "fail" if hard_fail else ("pass" if overall >= 0.75 else "needs_revision")

    return {
        "overall_score": round(overall, 4),
        "final_verdict": verdict,
        "hard_fail": hard_fail,
        "criteria": criteria,
        "summary": "Local fallback judge output.",
    }


async def call_external_judge(prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
    _ = prompt
    _ = schema
    raise NotImplementedError("Integrate your LLM provider in call_external_judge")


async def evaluate(
    task: str,
    candidate_output: str,
    schema: dict[str, Any],
    rubric: dict[str, float],
    use_local_fallback: bool,
) -> dict[str, Any]:
    if use_local_fallback:
        result = local_fallback_judge(candidate_output, rubric)
    else:
        prompt = (
            "Evaluate candidate output against task and rubric. "
            "Return strict JSON only according to the schema.\n"
            f"Task:\n{task}\n\n"
            f"Candidate output:\n{candidate_output}\n\n"
            f"Rubric:\n{json.dumps(rubric, indent=2)}"
        )
        result = await call_external_judge(prompt, schema)

    jsonschema.validate(result, schema)
    return result


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--candidate", required=True, help="Path to candidate output text file")
    parser.add_argument("--schema", type=Path, required=True, help="Judge output schema JSON file")
    parser.add_argument("--rubric", type=Path, help="Optional rubric JSON file with criterion weights")
    parser.add_argument("--output", type=Path, default=Path("judge_result.json"))
    parser.add_argument("--use-local-fallback", action="store_true")
    args = parser.parse_args()

    schema = load_json(args.schema)
    rubric = load_json(args.rubric) if args.rubric else DEFAULT_RUBRIC
    candidate_text = Path(args.candidate).read_text()

    result = asyncio.run(
        evaluate(
            task=args.task,
            candidate_output=candidate_text,
            schema=schema,
            rubric=rubric,
            use_local_fallback=args.use_local_fallback,
        )
    )

    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=True))
    print(f"Judge result written to {args.output}")


if __name__ == "__main__":
    main()
