# LangGraph Multi-Agent Examples

## Example 1: Collaboration Graph (Researcher + Writer)

```python
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

class CollabState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    current_agent: Literal["researcher", "writer"]
    task_status: Literal["in_progress", "done"]
    step_count: int

MAX_STEPS = 10

def researcher(state: CollabState) -> CollabState:
    # Replace with actual LLM call
    return {
        "messages": [AIMessage(content="Research finding: X", name="researcher")],
        "current_agent": "writer",
        "step_count": state["step_count"] + 1,
    }

def writer(state: CollabState) -> CollabState:
    done = state["step_count"] >= 3
    return {
        "messages": [AIMessage(content="Draft: Y", name="writer")],
        "current_agent": "researcher",
        "task_status": "done" if done else "in_progress",
        "step_count": state["step_count"] + 1,
    }

def route(state: CollabState) -> str:
    if state["task_status"] == "done" or state["step_count"] >= MAX_STEPS:
        return "END"
    return state["current_agent"]

builder = StateGraph(CollabState)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.set_entry_point("researcher")
builder.add_conditional_edges("researcher", route, {"writer": "writer", "END": END})
builder.add_conditional_edges("writer", route, {"researcher": "researcher", "END": END})

graph = builder.compile()

result = graph.invoke({
    "messages": [HumanMessage(content="Write a report on AI trends")],
    "current_agent": "researcher",
    "task_status": "in_progress",
    "step_count": 0,
})
```

---

## Example 2: Supervisor Graph (LLM-based routing)

```python
from typing import TypedDict, Annotated, Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

WORKERS = ["researcher", "coder", "math_solver"]

class Route(BaseModel):
    next: str
    reason: str

class SupervisorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next_worker: Optional[str]
    delegation_chain: list[str]
    task_status: str
    step_count: int
    final_answer: Optional[str]

SUPERVISOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", f"""You are a task supervisor. Route to the right worker or respond FINISH.
Workers: {", ".join(WORKERS)}
- researcher: web/doc research
- coder: write and run code
- math_solver: mathematical computations
When task is complete, set next=FINISH."""),
    ("placeholder", "{messages}"),
])

def supervisor(state: SupervisorState) -> SupervisorState:
    chain = SUPERVISOR_PROMPT | llm.with_structured_output(Route)
    result = chain.invoke({"messages": state["messages"]})
    is_done = result.next == "FINISH"
    return {
        "next_worker": None if is_done else result.next,
        "delegation_chain": state["delegation_chain"] + [result.next],
        "task_status": "done" if is_done else "in_progress",
        "step_count": state["step_count"] + 1,
    }

def researcher(state: SupervisorState) -> SupervisorState:
    return {
        "messages": [AIMessage(content="Research result: ...", name="researcher")],
        "step_count": state["step_count"] + 1,
    }

def coder(state: SupervisorState) -> SupervisorState:
    return {
        "messages": [AIMessage(content="Code result: ...", name="coder")],
        "step_count": state["step_count"] + 1,
    }

def math_solver(state: SupervisorState) -> SupervisorState:
    return {
        "messages": [AIMessage(content="Math result: ...", name="math_solver")],
        "step_count": state["step_count"] + 1,
    }

def route_from_supervisor(state: SupervisorState) -> str:
    if state["task_status"] == "done" or state["step_count"] >= 30:
        return "END"
    return state["next_worker"]

builder = StateGraph(SupervisorState)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher)
builder.add_node("coder", coder)
builder.add_node("math_solver", math_solver)

builder.set_entry_point("supervisor")
builder.add_conditional_edges(
    "supervisor",
    route_from_supervisor,
    {"researcher": "researcher", "coder": "coder", "math_solver": "math_solver", "END": END},
)
# Workers always return to supervisor
for worker in WORKERS:
    builder.add_edge(worker, "supervisor")

graph = builder.compile(recursion_limit=50)

result = graph.invoke({
    "messages": [HumanMessage(content="Research AI trends and write a Python summary script")],
    "next_worker": None,
    "delegation_chain": [],
    "task_status": "in_progress",
    "step_count": 0,
    "final_answer": None,
})
print("Delegation chain:", result["delegation_chain"])
```

---

## Example 3: Hierarchical Teams (top supervisor → team supervisors)

```python
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, AIMessage
from typing import TypedDict, Annotated, Optional

# Shared base state fields
class TeamResult(TypedDict):
    team_name: str
    summary: str

class TopState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    top_route: str              # "support_team" | "analytics_team" | "FINISH"
    team_result: Optional[TeamResult]
    step_count: int

def top_supervisor(state: TopState) -> TopState:
    """Route to team based on query content."""
    msg = state["messages"][-1].content.lower()
    if any(w in msg for w in ["billing", "refund", "account", "support"]):
        route = "support_team"
    elif any(w in msg for w in ["data", "analytics", "report", "chart"]):
        route = "analytics_team"
    else:
        route = "FINISH"
    return {"top_route": route, "step_count": state["step_count"] + 1}

def support_team(state: TopState) -> TopState:
    """Simulate support team handling (replace with subgraph)."""
    return {
        "messages": [AIMessage(content="Support team handled the request.", name="support")],
        "team_result": {"team_name": "support_team", "summary": "Issue resolved."},
        "top_route": "FINISH",
    }

def analytics_team(state: TopState) -> TopState:
    """Simulate analytics team handling (replace with subgraph)."""
    return {
        "messages": [AIMessage(content="Analytics report generated.", name="analytics")],
        "team_result": {"team_name": "analytics_team", "summary": "Report ready."},
        "top_route": "FINISH",
    }

def route_top(state: TopState) -> str:
    if state["top_route"] == "FINISH" or state["step_count"] >= 10:
        return "END"
    return state["top_route"]

builder = StateGraph(TopState)
builder.add_node("top_supervisor", top_supervisor)
builder.add_node("support_team", support_team)
builder.add_node("analytics_team", analytics_team)

builder.set_entry_point("top_supervisor")
builder.add_conditional_edges(
    "top_supervisor",
    route_top,
    {"support_team": "support_team", "analytics_team": "analytics_team", "END": END},
)
builder.add_edge("support_team", "top_supervisor")
builder.add_edge("analytics_team", "top_supervisor")

graph = builder.compile()
```

---

## Example 4: Audit Trail Logging

```python
import logging
import json

logger = logging.getLogger("multi_agent")

def log_routing(state: dict, from_node: str, to_node: str, reason: str = "") -> None:
    logger.info(json.dumps({
        "event": "routing_decision",
        "from": from_node,
        "to": to_node,
        "reason": reason,
        "step": state.get("step_count", 0),
        "delegation_chain": state.get("delegation_chain", []),
    }))
```
