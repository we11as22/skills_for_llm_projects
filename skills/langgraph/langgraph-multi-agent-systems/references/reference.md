# LangGraph Multi-Agent Systems Reference

## Table of Contents

1. Architecture Decision Guide
2. Collaboration Pattern (peer agents)
3. Supervisor Pattern (centralized routing)
4. Hierarchical Teams Pattern
5. Shared State Protocol
6. Recursion and Loop Guards
7. Tool Access Control
8. Observability and Audit
9. Reliability and Security Anti-Patterns

---

## 1. Architecture Decision Guide

| Criterion | Collaboration | Supervisor | Hierarchical |
|---|---|---|---|
| Control style | Decentralized | Centralized | Multi-level |
| Best for | Ideation, iteration | SLAs, determinism | Large domain decomposition |
| Failure surface | Peer loops | Single point of control | Sub-team isolation |
| Latency | Higher (multi-hop) | Lower (direct route) | Highest |
| When NOT to use | When you need auditable routing | When peers need peer communication | When team count < 3 |

---

## 2. Collaboration Pattern

### When to use
Agents are peers. One starts, the other critiques or extends. Repeat until done criteria met.

### State schema
```python
from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class CollabState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    current_agent: Literal["researcher", "writer"]
    task_status: Literal["in_progress", "done"]
    step_count: int
```

### Routing function
```python
MAX_STEPS = 20

def route(state: CollabState) -> str:
    if state["step_count"] >= MAX_STEPS:
        return "END"
    if state["task_status"] == "done":
        return "END"
    # alternate between agents
    return "writer" if state["current_agent"] == "researcher" else "researcher"
```

### Key rules
- Set `MAX_STEPS` to prevent infinite loops.
- The last agent to write owns the final answer.
- Each node must increment `step_count`.
- Never let both agents run in the same graph turn.

---

## 3. Supervisor Pattern

### When to use
Central orchestrator classifies the subtask and routes to a specialist. Specialist returns to supervisor.

### State schema
```python
from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

WORKERS = ["researcher", "coder", "math"]

class SupervisorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next_worker: Optional[str]   # which worker to call next
    delegation_reason: str       # why this worker was chosen
    task_status: str             # "in_progress" | "done" | "failed"
    step_count: int
    final_answer: Optional[str]
```

### Supervisor node (LLM-based routing)
```python
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

class Route(BaseModel):
    next: str  # one of WORKERS + ["FINISH"]
    reason: str

SYSTEM = """You are a supervisor. Route the user request to the right worker.
Workers: {workers}
When done, respond with next=FINISH."""

supervisor_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM.format(workers=", ".join(WORKERS))),
    ("placeholder", "{messages}"),
])

def supervisor(state: SupervisorState) -> SupervisorState:
    result = supervisor_prompt | llm.with_structured_output(Route)
    route = result.invoke({"messages": state["messages"]})
    return {
        "next_worker": route.next if route.next != "FINISH" else None,
        "delegation_reason": route.reason,
        "task_status": "done" if route.next == "FINISH" else "in_progress",
        "step_count": state["step_count"] + 1,
    }
```

### Routing edge function
```python
def route_supervisor(state: SupervisorState) -> str:
    if state["task_status"] == "done" or state["step_count"] >= 30:
        return "END"
    return state["next_worker"]
```

---

## 4. Hierarchical Teams Pattern

### When to use
Domains are large. Each domain has a team with its own supervisor and specialists. Top supervisor routes to team supervisors.

### Pattern
```
top_supervisor
├── support_team_supervisor
│   ├── billing_agent
│   └── technical_agent
└── analytics_team_supervisor
    ├── data_agent
    └── report_agent
```

### State design rule
Each level of hierarchy has its own subgraph with its own state. Top-level state has:
```python
class TopState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    top_route: str          # which team to route to
    team_summary: str       # bubbled-up result from team
    step_count: int
```

Each subgraph returns a summary to the top level. Never pass raw internal state upward.

---

## 5. Shared State Protocol

### Required fields (ALL multi-agent graphs)

| Field | Type | Purpose |
|---|---|---|
| `messages` | `Annotated[list[BaseMessage], add_messages]` | Conversation history with safe accumulation |
| `current_agent` | `str` | Which agent is currently active |
| `delegation_chain` | `list[str]` | Audit trail of routing decisions |
| `task_status` | `str` | `"in_progress"` / `"done"` / `"failed"` |
| `step_count` | `int` | Loop guard counter |
| `final_answer` | `Optional[str]` | The terminal output for the user |

### State update discipline
- Every node returns ONLY the fields it modifies.
- Never copy the entire state and mutate — use partial dicts.
- Accumulate delegation: `{"delegation_chain": state["delegation_chain"] + [current_agent]}`.

---

## 6. Recursion and Loop Guards

### Why this matters
Without guards, LangGraph will raise `GraphRecursionError` or spin indefinitely.

### Implementation pattern
```python
from langgraph.graph import StateGraph, END

MAX_STEPS = 25

def any_node(state: MyState) -> MyState:
    if state["step_count"] >= MAX_STEPS:
        return {
            "task_status": "failed",
            "final_answer": "Step budget exceeded.",
            "step_count": state["step_count"] + 1,
        }
    # ... normal logic
    return {"step_count": state["step_count"] + 1, ...}

# Also set LangGraph's built-in recursion limit
graph = builder.compile(recursion_limit=50)
```

### Graph-level guard
```python
config = {"recursion_limit": 50, "configurable": {"thread_id": "session-123"}}
result = graph.invoke(initial_state, config=config)
```

---

## 7. Tool Access Control

### Per-agent tool allowlists
```python
from langchain_core.tools import BaseTool

def make_agent(tools: list[BaseTool], system_prompt: str):
    """Create an agent with access to only specified tools."""
    llm_with_tools = llm.bind_tools(tools)
    # ...

# Researcher can search, not write
researcher = make_agent(tools=[web_search, doc_retrieval], ...)
# Coder can run code, not search
coder = make_agent(tools=[code_executor, file_writer], ...)
```

### Content policy check before final answer
```python
def content_policy_check(state: MyState) -> MyState:
    answer = state.get("final_answer", "")
    if contains_pii(answer) or contains_harmful_content(answer):
        return {
            "final_answer": "[BLOCKED: policy violation]",
            "task_status": "failed",
        }
    return {}
```

---

## 8. Observability and Audit

### What to log per routing decision
```python
import logging
logger = logging.getLogger(__name__)

def supervisor(state: SupervisorState) -> SupervisorState:
    route = ...  # LLM call
    logger.info("routing_decision", extra={
        "from": "supervisor",
        "to": route.next,
        "reason": route.reason,
        "step": state["step_count"],
        "thread_id": config.get("configurable", {}).get("thread_id"),
    })
    return {"delegation_chain": state["delegation_chain"] + [route.next], ...}
```

### LangSmith integration
```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "multi-agent-prod"
```

---

## 9. Anti-Patterns to Avoid

| Anti-pattern | Problem | Fix |
|---|---|---|
| Unconstrained recursion | `GraphRecursionError` in production | Add `step_count` guard + `recursion_limit` |
| Multiple "final answer" owners | Race condition on output | Exactly one node writes `final_answer` |
| Sharing full state across hierarchy levels | Tight coupling, breaks isolation | Define per-level state, bubble summaries up |
| No audit trail | Undebuggable failures | Always append to `delegation_chain` |
| LLM router with free-text output | Routing breaks on unexpected outputs | Use structured output (`with_structured_output`) |
| No content policy on final output | PII or harmful content reaches user | Add policy check node before END |
