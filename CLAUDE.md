# Claude Project Memory — skills_for_llm_projects

This repository is a production-quality skill pack for LLM engineering, LangGraph architectures, platform operations, and evaluation pipelines.

## How to Work with Skills

Every task maps to a skill in `skills/`. Before writing code:

1. **Identify the skill** using the table below.
2. **Read the skill's SKILL.md** — it defines the mandatory workflow, critical rules, and output format.
3. **Read `references/reference.md`** — architecture patterns and production checklist.
4. **Read `references/examples.md`** — concrete code patterns.
5. **Scaffold starter code** using scripts in `skills/<category>/<name>/scripts/`.
6. **Copy templates** from `skills/<category>/<name>/assets/` — never rewrite boilerplate from scratch.

## Skill Routing Table

Skills are grouped by category: `langgraph/`, `llm/`, `frontend/`, `backend/`, `platform/`.

| Task | Skill |
|---|---|
| LangGraph: choose architecture | `skills/langgraph/langgraph-tutorials-playbook/` |
| LangGraph: single-agent / tool-agent | `skills/langgraph/langgraph-core-agent-builders/` |
| LangGraph: multi-agent / supervisor / hierarchy | `skills/langgraph/langgraph-multi-agent-systems/` |
| LangGraph: RAG (agentic, adaptive, CRAG, self-RAG) | `skills/langgraph/langgraph-rag-architectures/` |
| LangGraph: planning (plan-execute, ReWOO, LATS, reflection) | `skills/langgraph/langgraph-planning-reasoning/` |
| LangGraph: evaluation / simulation harness | `skills/langgraph/langgraph-evaluation-simulation/` |
| LangGraph: web research / STORM / WebVoyager | `skills/langgraph/langgraph-research-web-agents/` |
| LLM evaluation / judge / scoring | `skills/llm/llm-as-a-judge-designer/` |
| LLM async API / structured output | `skills/llm/llm-async-structured-output/` |
| Prompt design / optimization / debugging | `skills/llm/prompt-engineering-playbook/` |
| Kubernetes / container deployment | `skills/platform/kubernetes-platform-engineer/` |
| Microservice architecture | `skills/backend/microservice-architecture-designer/` |
| Async backend / queues / workers / sagas | `skills/backend/async-backend-orchestrator/` |
| Database / async data layer | `skills/backend/async-database-engineer/` |
| React application development | `skills/frontend/react-js-engineer/` |
| Vue 3 application development | `skills/frontend/vue-js-engineer/` |
| Design system / CSS tokens / layout | `skills/frontend/frontend-design-engineer/` |
| SSE / WebSocket / real-time streaming | `skills/frontend/web-ui-streaming-engineer/` |
| Plotly / interactive dashboards | `skills/frontend/plotly-visualization-engineer/` |

## Claude Code Slash Commands

All skills are available as slash commands in this project:

```
/langgraph-core        — single-agent and tool-agent patterns
/langgraph-multi-agent — collaboration, supervisor, hierarchy
/langgraph-rag         — agentic, adaptive, CRAG, self-RAG
/langgraph-planning    — plan-execute, ReWOO, LATS, reflection
/langgraph-eval        — evaluation and simulation harness
/langgraph-research-agent — web research and STORM patterns
/langgraph-playbook    — choose the right LangGraph architecture
/llm-judge             — judge design, rubrics, calibration
/kubernetes-engineer   — K8s manifests, security, observability
/microservice-design   — service boundaries, contracts, docker
/async-backend         — queues, workers, retries, sagas
/async-database        — async DB layers, pooling, migrations
/llm-async-output      — async LLM with structured output
/prompt-engineering    — prompt design, linting, evaluation
/react-engineer        — React features, state, testing
/vue-engineer          — Vue 3 Composition API, Pinia
/frontend-design       — design tokens, components, a11y
/web-streaming         — SSE, WebSocket, streaming UI
/plotly-viz            — Plotly dashboards, chart selection
```

## Non-Negotiable Engineering Rules

### LangGraph
- `TypedDict` for all state — never plain `dict`.
- `Annotated[list[BaseMessage], add_messages]` for message lists.
- Every conditional edge must have an explicit `END` path.
- Add `step_count` guard to every graph that can loop.
- Return only modified fields from nodes (partial state update).

### Kubernetes
- Always set resource `requests` AND `limits`.
- Always `runAsNonRoot: true` + drop all capabilities.
- Never `latest` image tag in production.
- Always include all three probe types.

### Async Python
- All task handlers must be idempotent.
- Retry only transient failures (429, 5xx, network errors).
- Validate all LLM structured output with Pydantic before downstream use.
- Bound concurrency with `asyncio.Semaphore`.

### Output Quality
- Follow the Output Format section in every SKILL.md exactly.
- Never produce incomplete stubs — provide complete, runnable code.
- Always include the production hardening checklist from the skill.

## Validation

```bash
./scripts/validate_all_skills.sh
```
