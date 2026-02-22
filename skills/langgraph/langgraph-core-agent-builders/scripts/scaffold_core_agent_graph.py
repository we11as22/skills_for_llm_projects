#!/usr/bin/env python3
"""Generate a core LangGraph app scaffold (single-agent + tools + validation node)."""

from __future__ import annotations

import argparse
from pathlib import Path

STATE_TEMPLATE = """from typing import TypedDict, Dict, List


class CoreState(TypedDict):
    user_input: str
    collected: Dict[str, str]
    messages: List[str]
    answer: str
    done: bool
"""

GRAPH_TEMPLATE = """from __future__ import annotations

from langgraph.graph import StateGraph, END

from state import CoreState


def gather(state: CoreState) -> CoreState:
    collected = dict(state["collected"])
    if "goal" not in collected:
        collected["goal"] = "filled"
    return {**state, "collected": collected}


def answer(state: CoreState) -> CoreState:
    text = f"Answer based on goal={state['collected'].get('goal', 'unknown')}"
    return {**state, "answer": text, "done": True}


def route(state: CoreState) -> str:
    return "answer" if "goal" in state["collected"] else "gather"


def build_graph():
    g = StateGraph(CoreState)
    g.add_node("gather", gather)
    g.add_node("answer", answer)
    g.set_entry_point("gather")
    g.add_conditional_edges("gather", route, {"gather": "gather", "answer": "answer"})
    g.add_edge("answer", END)
    return g.compile()
"""

README_TEMPLATE = """# Core LangGraph App

Files:
- `state.py`: typed state definition
- `graph.py`: graph nodes and transitions

Integrate your LLM and tools inside `gather`/`answer` nodes.
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    write(args.output / "state.py", STATE_TEMPLATE)
    write(args.output / "graph.py", GRAPH_TEMPLATE)
    write(args.output / "README.md", README_TEMPLATE)
    print(f"Core LangGraph scaffold generated in {args.output}")


if __name__ == "__main__":
    main()
