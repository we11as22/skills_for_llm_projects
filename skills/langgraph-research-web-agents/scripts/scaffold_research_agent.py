#!/usr/bin/env python3
"""Generate a research/web-agent LangGraph scaffold with planner, navigator, and synthesizer nodes."""

from __future__ import annotations

import argparse
from pathlib import Path

TEMPLATE = """from typing import TypedDict, List, Dict

from langgraph.graph import StateGraph, END


class ResearchState(TypedDict):
    objective: str
    plan: List[str]
    observations: List[str]
    evidence: List[Dict[str, str]]
    draft: str
    done: bool


def planner(state: ResearchState) -> ResearchState:
    plan = ["search", "collect", "synthesize"]
    return {**state, "plan": plan}


def navigator(state: ResearchState) -> ResearchState:
    observations = state["observations"] + ["visited page and extracted snippet"]
    evidence = state["evidence"] + [{"url": "https://example.com", "snippet": "key fact"}]
    return {**state, "observations": observations, "evidence": evidence}


def synthesizer(state: ResearchState) -> ResearchState:
    draft = "Synthesis with citations"
    return {**state, "draft": draft, "done": True}


def route_after_planner(state: ResearchState) -> str:
    return "navigate"


def route_after_navigation(state: ResearchState) -> str:
    return "synthesize" if len(state["evidence"]) >= 1 else "navigate"


def build_graph():
    g = StateGraph(ResearchState)
    g.add_node("planner", planner)
    g.add_node("navigate", navigator)
    g.add_node("synthesize", synthesizer)
    g.set_entry_point("planner")
    g.add_conditional_edges("planner", route_after_planner, {"navigate": "navigate"})
    g.add_conditional_edges("navigate", route_after_navigation, {"navigate": "navigate", "synthesize": "synthesize"})
    g.add_edge("synthesize", END)
    return g.compile()
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(TEMPLATE)
    print(f"Research agent scaffold written to {args.output}")


if __name__ == "__main__":
    main()
