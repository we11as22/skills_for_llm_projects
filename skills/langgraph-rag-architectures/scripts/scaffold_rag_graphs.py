#!/usr/bin/env python3
"""Generate LangGraph RAG starter templates for adaptive, CRAG, and self-RAG patterns."""

from __future__ import annotations

import argparse
from pathlib import Path

ADAPTIVE_TEMPLATE = """from typing import TypedDict, List

from langgraph.graph import StateGraph, END


class RAGState(TypedDict):
    query: str
    route: str
    docs: List[str]
    answer: str


def route_query(state: RAGState) -> RAGState:
    query = state["query"].lower()
    route = "web_search" if "today" in query or "latest" in query else "vectorstore"
    return {**state, "route": route}


def vectorstore_retrieve(state: RAGState) -> RAGState:
    return {**state, "docs": ["domain doc 1", "domain doc 2"]}


def web_search(state: RAGState) -> RAGState:
    return {**state, "docs": ["web doc 1", "web doc 2"]}


def generate(state: RAGState) -> RAGState:
    return {**state, "answer": "generated answer grounded in docs"}


def route_after_router(state: RAGState) -> str:
    return state["route"]


def build_graph():
    g = StateGraph(RAGState)
    g.add_node("router", route_query)
    g.add_node("vectorstore", vectorstore_retrieve)
    g.add_node("web_search", web_search)
    g.add_node("generate", generate)

    g.set_entry_point("router")
    g.add_conditional_edges("router", route_after_router, {"vectorstore": "vectorstore", "web_search": "web_search"})
    g.add_edge("vectorstore", "generate")
    g.add_edge("web_search", "generate")
    g.add_edge("generate", END)
    return g.compile()
"""

CRAG_TEMPLATE = """from typing import TypedDict, List

from langgraph.graph import StateGraph, END


class RAGState(TypedDict):
    query: str
    docs: List[str]
    retrieval_score: float
    answer: str


def retrieve(state: RAGState) -> RAGState:
    return {**state, "docs": ["candidate doc"], "retrieval_score": 0.55}


def grade_retrieval(state: RAGState) -> str:
    return "correct" if state["retrieval_score"] < 0.7 else "generate"


def corrective_retrieve(state: RAGState) -> RAGState:
    return {**state, "docs": state["docs"] + ["corrective web doc"], "retrieval_score": 0.82}


def generate(state: RAGState) -> RAGState:
    return {**state, "answer": "answer with corrected evidence"}


def build_graph():
    g = StateGraph(RAGState)
    g.add_node("retrieve", retrieve)
    g.add_node("correct", corrective_retrieve)
    g.add_node("generate", generate)

    g.set_entry_point("retrieve")
    g.add_conditional_edges("retrieve", grade_retrieval, {"correct": "correct", "generate": "generate"})
    g.add_edge("correct", "generate")
    g.add_edge("generate", END)
    return g.compile()
"""

SELF_RAG_TEMPLATE = """from typing import TypedDict, List

from langgraph.graph import StateGraph, END


class RAGState(TypedDict):
    query: str
    docs: List[str]
    answer: str
    answer_supported: bool


def retrieve(state: RAGState) -> RAGState:
    return {**state, "docs": ["doc a", "doc b"]}


def generate(state: RAGState) -> RAGState:
    return {**state, "answer": "draft answer"}


def self_grade(state: RAGState) -> str:
    # Replace with LLM grading logic.
    supported = len(state["docs"]) > 0
    return "accept" if supported else "retry"


def retry_retrieve(state: RAGState) -> RAGState:
    return {**state, "docs": state["docs"] + ["extra doc"]}


def build_graph():
    g = StateGraph(RAGState)
    g.add_node("retrieve", retrieve)
    g.add_node("generate", generate)
    g.add_node("retry_retrieve", retry_retrieve)

    g.set_entry_point("retrieve")
    g.add_edge("retrieve", "generate")
    g.add_conditional_edges("generate", self_grade, {"accept": END, "retry": "retry_retrieve"})
    g.add_edge("retry_retrieve", "generate")
    return g.compile()
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output directory")
    args = parser.parse_args()

    write(args.output / "adaptive_rag_graph.py", ADAPTIVE_TEMPLATE)
    write(args.output / "crag_graph.py", CRAG_TEMPLATE)
    write(args.output / "self_rag_graph.py", SELF_RAG_TEMPLATE)
    print(f"RAG graph templates generated at {args.output}")


if __name__ == "__main__":
    main()
