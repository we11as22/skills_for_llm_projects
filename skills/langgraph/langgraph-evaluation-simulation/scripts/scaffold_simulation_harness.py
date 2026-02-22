#!/usr/bin/env python3
"""Generate an async simulation harness for agent evaluation."""

from __future__ import annotations

import argparse
from pathlib import Path

HARNESS_TEMPLATE = """from __future__ import annotations

import asyncio
from dataclasses import dataclass


@dataclass
class Scenario:
    scenario_id: str
    prompt: str
    expected_keywords: list[str]


async def simulated_user_turn(scenario: Scenario, turn: int) -> str:
    if turn == 0:
        return scenario.prompt
    return "Please clarify with exact policy details."


async def assistant_turn(user_message: str) -> str:
    # Replace with your LangGraph app invocation.
    await asyncio.sleep(0.05)
    return f"assistant response to: {user_message}"


def judge_response(response: str, expected_keywords: list[str]) -> dict:
    matched = [k for k in expected_keywords if k.lower() in response.lower()]
    score = len(matched) / max(1, len(expected_keywords))
    return {
        "task_success": score > 0.6,
        "keyword_coverage": score,
        "matched_keywords": matched,
    }


async def run_scenario(scenario: Scenario, max_turns: int = 3) -> dict:
    transcript: list[dict] = []
    final_response = ""
    for turn in range(max_turns):
        user_message = await simulated_user_turn(scenario, turn)
        final_response = await assistant_turn(user_message)
        transcript.append({"turn": turn, "user": user_message, "assistant": final_response})
    judge = judge_response(final_response, scenario.expected_keywords)
    return {"scenario_id": scenario.scenario_id, "judge": judge, "transcript": transcript}


async def main() -> None:
    scenarios = [
        Scenario("demo_1", "How can I reset my password?", ["password", "reset"]),
        Scenario("demo_2", "I need invoice export", ["invoice", "export"]),
    ]
    results = await asyncio.gather(*(run_scenario(s) for s in scenarios))
    for r in results:
        print(r)


if __name__ == "__main__":
    asyncio.run(main())
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output file path for harness")
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(HARNESS_TEMPLATE)
    print(f"Simulation harness scaffolded: {args.output}")


if __name__ == "__main__":
    main()
