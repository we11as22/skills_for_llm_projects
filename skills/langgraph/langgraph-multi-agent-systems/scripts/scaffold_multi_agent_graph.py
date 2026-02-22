#!/usr/bin/env python3
"""Generate LangGraph multi-agent starter topologies."""

from __future__ import annotations

import argparse
from pathlib import Path

COLLAB_TEMPLATE = """from typing import TypedDict, List

from langgraph.graph import StateGraph, END


class GraphState(TypedDict):
    messages: List[str]
    task_status: str


def researcher(state: GraphState) -> GraphState:
    return {"messages": state["messages"] + ["research update"], "task_status": "in_progress"}


def writer(state: GraphState) -> GraphState:
    done = len(state["messages"]) > 3
    return {
        "messages": state["messages"] + ["writer draft"],
        "task_status": "done" if done else "in_progress",
    }


def route(state: GraphState) -> str:
    return "end" if state["task_status"] == "done" else "researcher"


def build_graph():
    g = StateGraph(GraphState)
    g.add_node("researcher", researcher)
    g.add_node("writer", writer)
    g.set_entry_point("researcher")
    g.add_edge("researcher", "writer")
    g.add_conditional_edges("writer", route, {"researcher": "researcher", "end": END})
    return g.compile()
"""

SUPERVISOR_TEMPLATE = """from typing import TypedDict, List

from langgraph.graph import StateGraph, END


class GraphState(TypedDict):
    messages: List[str]
    route: str


def supervisor(state: GraphState) -> GraphState:
    # Replace with LLM-based router.
    route = "coder" if "code" in " ".join(state["messages"]).lower() else "researcher"
    return {"messages": state["messages"], "route": route}


def researcher(state: GraphState) -> GraphState:
    return {"messages": state["messages"] + ["research result"], "route": "finish"}


def coder(state: GraphState) -> GraphState:
    return {"messages": state["messages"] + ["code result"], "route": "finish"}


def route_after_supervisor(state: GraphState) -> str:
    return state["route"]


def route_after_worker(state: GraphState) -> str:
    return "end" if state["route"] == "finish" else "supervisor"


def build_graph():
    g = StateGraph(GraphState)
    g.add_node("supervisor", supervisor)
    g.add_node("researcher", researcher)
    g.add_node("coder", coder)

    g.set_entry_point("supervisor")
    g.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {"researcher": "researcher", "coder": "coder"},
    )
    g.add_conditional_edges("researcher", route_after_worker, {"supervisor": "supervisor", "end": END})
    g.add_conditional_edges("coder", route_after_worker, {"supervisor": "supervisor", "end": END})
    return g.compile()
"""

HIER_TEMPLATE = """from typing import TypedDict, List

from langgraph.graph import StateGraph, END


class GraphState(TypedDict):
    messages: List[str]
    top_route: str


def top_supervisor(state: GraphState) -> GraphState:
    # Replace with domain routing logic.
    return {"messages": state["messages"], "top_route": "support_team"}


def support_team_supervisor(state: GraphState) -> GraphState:
    return {"messages": state["messages"] + ["support_team handled"], "top_route": "finish"}


def analytics_team_supervisor(state: GraphState) -> GraphState:
    return {"messages": state["messages"] + ["analytics_team handled"], "top_route": "finish"}


def route_top(state: GraphState) -> str:
    return state["top_route"]


def route_finish(state: GraphState) -> str:
    return "end" if state["top_route"] == "finish" else "top_supervisor"


def build_graph():
    g = StateGraph(GraphState)
    g.add_node("top_supervisor", top_supervisor)
    g.add_node("support_team", support_team_supervisor)
    g.add_node("analytics_team", analytics_team_supervisor)

    g.set_entry_point("top_supervisor")
    g.add_conditional_edges(
        "top_supervisor",
        route_top,
        {"support_team": "support_team", "analytics_team": "analytics_team"},
    )
    g.add_conditional_edges("support_team", route_finish, {"top_supervisor": "top_supervisor", "end": END})
    g.add_conditional_edges("analytics_team", route_finish, {"top_supervisor": "top_supervisor", "end": END})
    return g.compile()
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output directory")
    args = parser.parse_args()

    write(args.output / "collaboration_graph.py", COLLAB_TEMPLATE)
    write(args.output / "supervisor_graph.py", SUPERVISOR_TEMPLATE)
    write(args.output / "hierarchical_graph.py", HIER_TEMPLATE)
    print(f"Multi-agent graph templates created in {args.output}")


if __name__ == "__main__":
    main()
