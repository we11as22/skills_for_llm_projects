# Agent Instructions — skills_for_llm_projects

This repository contains production-quality coding skills in `skills/`. Each skill covers a specific engineering domain and provides: a workflow, mandatory rules, reference patterns, code examples, and scaffolding scripts.

## How to Use Skills

For every implementation task:

1. **Find the skill** using the routing table below (skills are under `skills/<category>/<name>/`).
2. **Read `skills/<category>/<name>/SKILL.md`** — workflow and mandatory rules.
3. **Read `skills/<category>/<name>/references/reference.md`** — architecture patterns.
4. **Read `skills/<category>/<name>/references/examples.md`** — code examples.
5. **Scaffold with** `python3 skills/<category>/<name>/scripts/<scaffold_script>.py <output_dir>`.
6. **Copy from** `skills/<category>/<name>/assets/` — templates, schemas, starters.

## Skill Routing Table

### LangGraph Skills

| Signal in task | Skill |
|---|---|
| "build a LangGraph agent" (unclear type) | Read `skills/langgraph/langgraph-tutorials-playbook/SKILL.md` first |
| Single agent, tool calling, customer support | `skills/langgraph/langgraph-core-agent-builders/` |
| Multiple agents, supervisor, hierarchy, delegation | `skills/langgraph/langgraph-multi-agent-systems/` |
| RAG, retrieval, vectorstore, CRAG, self-RAG | `skills/langgraph/langgraph-rag-architectures/` |
| Multi-step planning, ReWOO, LATS, reflection | `skills/langgraph/langgraph-planning-reasoning/` |
| Evaluation, simulation, quality benchmarking | `skills/langgraph/langgraph-evaluation-simulation/` |
| Web research, STORM, browser automation agent | `skills/langgraph/langgraph-research-web-agents/` |

### Platform and Backend Skills

| Signal in task | Skill |
|---|---|
| Kubernetes, containers, Helm, Kustomize | `skills/platform/kubernetes-platform-engineer/` |
| Microservices, service boundaries, docker-compose | `skills/backend/microservice-architecture-designer/` |
| Queues, workers, async jobs, saga, outbox | `skills/backend/async-backend-orchestrator/` |
| PostgreSQL, MongoDB, Redis, vector DB, async ORM | `skills/backend/async-database-engineer/` |

### LLM and Frontend Skills

| Signal in task | Skill |
|---|---|
| LLM quality evaluation, rubric, judge pipeline | `skills/llm/llm-as-a-judge-designer/` |
| LLM API calls, structured output, retries | `skills/llm/llm-async-structured-output/` |
| Prompt writing, optimization, linting | `skills/llm/prompt-engineering-playbook/` |
| React, TypeScript, hooks, state management | `skills/frontend/react-js-engineer/` |
| Vue 3, Composition API, Pinia | `skills/frontend/vue-js-engineer/` |
| Design tokens, CSS variables, design system | `skills/frontend/frontend-design-engineer/` |
| SSE, WebSocket, token streaming, real-time UI | `skills/frontend/web-ui-streaming-engineer/` |
| Plotly, dashboards, data visualization | `skills/frontend/plotly-visualization-engineer/` |

## Mandatory Rules per Domain

### LangGraph (ALL graphs)
- State: `TypedDict` only. Message lists: `Annotated[list[BaseMessage], add_messages]`.
- Every conditional edge must have an `END` path — no dangling branches.
- Every looping graph needs a `step_count` field and a `max_steps` guard.
- Nodes return only modified fields (partial state update, not full state copy).
- Validate tool arguments with Pydantic before execution.

### Kubernetes
- Every container: `resources.requests` + `resources.limits` (REQUIRED, no exceptions).
- Security: `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `capabilities.drop: [ALL]`.
- Never `latest` tag in production.
- Rolling update: `maxUnavailable: 0`.

### Async Python
- All task handlers: idempotent (safe to retry with same input).
- Retries: only on 429/5xx/network. Never on 4xx client errors.
- Concurrency: `asyncio.Semaphore` on all external calls.
- Timeouts: `asyncio.timeout()` on every external call.
- LLM output: validate with Pydantic before downstream use.

### LLM Judge
- Rubric: 6-10 criteria, non-overlapping, weights sum to 1.0.
- Every score requires `evidence` field.
- Hard-fail criteria bypass aggregate score.

### React / Vue
- TypeScript strict mode. No `any`.
- Async paths: always handle loading, error, empty, success.
- Components: ≤150 lines. Extract logic to hooks/composables.
- A11y: keyboard navigation, ARIA labels, focus management.

## Scaffolding Quick Reference

```bash
# LangGraph
python3 skills/langgraph/langgraph-core-agent-builders/scripts/scaffold_core_agent_graph.py ./output
python3 skills/langgraph/langgraph-multi-agent-systems/scripts/scaffold_multi_agent_graph.py ./output
python3 skills/langgraph/langgraph-rag-architectures/scripts/scaffold_rag_graphs.py ./output
python3 skills/langgraph/langgraph-planning-reasoning/scripts/scaffold_planning_graphs.py ./output

# Platform & backend
python3 skills/platform/kubernetes-platform-engineer/scripts/scaffold_k8s_service.py myservice --output ./k8s
python3 skills/backend/microservice-architecture-designer/scripts/scaffold_microservices.py myservice --output ./services

# Frontend
python3 skills/frontend/react-js-engineer/scripts/scaffold_react_feature.py MyFeature --output ./src/features
python3 skills/frontend/vue-js-engineer/scripts/scaffold_vue_feature.py MyFeature --output ./src/features
```

## Validation

Always run after any skill scaffold:
```bash
./scripts/validate_all_skills.sh
```
