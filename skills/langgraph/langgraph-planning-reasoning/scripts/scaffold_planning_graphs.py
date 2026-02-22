#!/usr/bin/env python3
"""Generate starter templates for LangGraph planning/reasoning architectures."""

from __future__ import annotations

import argparse
from pathlib import Path

PLAN_EXECUTE_TEMPLATE = """from typing import TypedDict, List

from langgraph.graph import StateGraph, END


class PlanState(TypedDict):
    objective: str
    plan: List[str]
    completed_steps: List[str]


def planner(state: PlanState) -> PlanState:
    return {**state, "plan": ["step1", "step2", "step3"], "completed_steps": []}


def executor(state: PlanState) -> PlanState:
    remaining = [s for s in state["plan"] if s not in state["completed_steps"]]
    if remaining:
        return {**state, "completed_steps": state["completed_steps"] + [remaining[0]]}
    return state


def should_continue(state: PlanState) -> str:
    return "done" if len(state["completed_steps"]) >= len(state["plan"]) else "execute"


def build_graph():
    g = StateGraph(PlanState)
    g.add_node("planner", planner)
    g.add_node("execute", executor)
    g.set_entry_point("planner")
    g.add_edge("planner", "execute")
    g.add_conditional_edges("execute", should_continue, {"execute": "execute", "done": END})
    return g.compile()
"""

REWOO_TEMPLATE = """from typing import TypedDict, List, Dict

from langgraph.graph import StateGraph, END


class ReWOOState(TypedDict):
    query: str
    plan_steps: List[Dict[str, str]]
    observations: Dict[str, str]
    answer: str


def planner(state: ReWOOState) -> ReWOOState:
    steps = [
        {"id": "S1", "action": "search", "input": state["query"]},
        {"id": "S2", "action": "summarize", "input": "#S1"},
    ]
    return {**state, "plan_steps": steps, "observations": {}}


def executor(state: ReWOOState) -> ReWOOState:
    observations = dict(state["observations"])
    for step in state["plan_steps"]:
        observations[step["id"]] = f"result_of_{step['action']}"
    return {**state, "observations": observations}


def solver(state: ReWOOState) -> ReWOOState:
    return {**state, "answer": "final answer from observations"}


def build_graph():
    g = StateGraph(ReWOOState)
    g.add_node("planner", planner)
    g.add_node("executor", executor)
    g.add_node("solver", solver)
    g.set_entry_point("planner")
    g.add_edge("planner", "executor")
    g.add_edge("executor", "solver")
    g.add_edge("solver", END)
    return g.compile()
"""

REFLEXION_TEMPLATE = """from typing import TypedDict

from langgraph.graph import StateGraph, END


class ReflexionState(TypedDict):
    prompt: str
    draft: str
    critique: str
    iteration: int


def generate(state: ReflexionState) -> ReflexionState:
    return {**state, "draft": "draft answer", "iteration": state["iteration"] + 1}


def critique(state: ReflexionState) -> ReflexionState:
    issue = "missing evidence" if state["iteration"] < 2 else "ok"
    return {**state, "critique": issue}


def route(state: ReflexionState) -> str:
    return "revise" if state["critique"] != "ok" and state["iteration"] < 3 else "finish"


def revise(state: ReflexionState) -> ReflexionState:
    return {**state, "draft": state["draft"] + " + improved details"}


def build_graph():
    g = StateGraph(ReflexionState)
    g.add_node("generate", generate)
    g.add_node("critique", critique)
    g.add_node("revise", revise)
    g.set_entry_point("generate")
    g.add_edge("generate", "critique")
    g.add_conditional_edges("critique", route, {"revise": "revise", "finish": END})
    g.add_edge("revise", "generate")
    return g.compile()
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output directory")
    args = parser.parse_args()

    write(args.output / "plan_execute_graph.py", PLAN_EXECUTE_TEMPLATE)
    write(args.output / "rewoo_graph.py", REWOO_TEMPLATE)
    write(args.output / "reflexion_graph.py", REFLEXION_TEMPLATE)
    print(f"Planning graph templates created in {args.output}")


if __name__ == "__main__":
    main()
