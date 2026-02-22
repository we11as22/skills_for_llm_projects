# Описание скиллов

Полный список скиллов банка и когда их применять. Формат скиллов соответствует [Agent Skills](https://agentskills.io) и документации платформ: [Claude Code](https://code.claude.com/docs/en/skills), [Cursor](https://cursor.com/ru/docs/context/skills), [Codex](https://developers.openai.com/codex/skills/), [Roo Code](https://docs.roocode.com/features/skills), [Kilo Code](https://kilo.ai/docs/customize/skills).

---

## LangGraph (`skills/langgraph/`)

| Скилл | Когда использовать |
|-------|--------------------|
| [langgraph-tutorials-playbook](../skills/langgraph/langgraph-tutorials-playbook/) | Точка входа: выбор подходящей архитектуры LangGraph по задаче. |
| [langgraph-core-agent-builders](../skills/langgraph/langgraph-core-agent-builders/) | Один агент, tool-агент, code assistant, customer support. |
| [langgraph-multi-agent-systems](../skills/langgraph/langgraph-multi-agent-systems/) | Коллаборация, supervisor, иерархические команды агентов. |
| [langgraph-rag-architectures](../skills/langgraph/langgraph-rag-architectures/) | Agentic, Adaptive, CRAG, Self-RAG, градация качества retrieval. |
| [langgraph-planning-reasoning](../skills/langgraph/langgraph-planning-reasoning/) | Plan-and-Execute, ReWOO, LLM Compiler, LATS, Reflection. |
| [langgraph-evaluation-simulation](../skills/langgraph/langgraph-evaluation-simulation/) | Симулированные пользователи, сценарии, judge-петли, бенчмарки. |
| [langgraph-research-web-agents](../skills/langgraph/langgraph-research-web-agents/) | STORM-синтез, WebVoyager, автономный веб-поиск и бенчмарки. |

---

## LLM (`skills/llm/`)

| Скилл | Когда использовать |
|-------|--------------------|
| [llm-as-a-judge-designer](../skills/llm/llm-as-a-judge-designer/) | Оценка по рубрикам, структурированный скор, release gates. |
| [llm-async-structured-output](../skills/llm/llm-async-structured-output/) | Асинхронные вызовы LLM, валидация по JSON Schema, retry/timeout. |
| [prompt-engineering-playbook](../skills/llm/prompt-engineering-playbook/) | Дизайн промптов, отладка, версионирование, evaluation-петли. |

---

## Platform и Backend (`skills/platform/`, `skills/backend/`)

| Скилл | Когда использовать |
|-------|--------------------|
| [kubernetes-platform-engineer](../skills/platform/kubernetes-platform-engineer/) | Деплой, HPA, безопасность, observability, runbooks. |
| [microservice-architecture-designer](../skills/backend/microservice-architecture-designer/) | Границы сервисов, контракты, docker-compose, отказоустойчивость. |
| [async-backend-orchestrator](../skills/backend/async-backend-orchestrator/) | Очереди, воркеры, retry, идемпотентность, saga/outbox. |
| [async-database-engineer](../skills/backend/async-database-engineer/) | Асинхронный PostgreSQL/MongoDB/Redis/vector DB, пулы, миграции. |

---

## Common — всегда активны (`skills/common/`)

Эти скиллы при установке попадают во все цели и рекомендуются как базовые guardrails.

| Скилл | Когда применять |
|-------|-----------------|
| [terminal-power-user](../skills/common/terminal-power-user/) | Работа с терминалом: сервисы, логи, диск, структура каталогов, параллельный запуск. |
| [safe-change-protocol](../skills/common/safe-change-protocol/) | Перед любым изменением кода/конфига: класс изменения, blast-radius, подтверждение. |
| [agent-discipline](../skills/common/agent-discipline/) | Всегда: против галлюцинаций, контроль скоупа, полный код, честность об ограничениях. |
| [doc-keeper](../skills/common/doc-keeper/) | Актуальные README, ARCHITECTURE.md, docs/changes/ после значимых изменений. |

---

## Frontend (`skills/frontend/`)

| Скилл | Когда использовать |
|-------|--------------------|
| [react-js-engineer](../skills/frontend/react-js-engineer/) | React, TypeScript, состояние, производительность, тесты. |
| [vue-js-engineer](../skills/frontend/vue-js-engineer/) | Vue 3 Composition API, Pinia, composables, тесты. |
| [frontend-design-engineer](../skills/frontend/frontend-design-engineer/) | Design tokens, layout, состояния компонентов, a11y. |
| [web-ui-streaming-engineer](../skills/frontend/web-ui-streaming-engineer/) | SSE, WebSocket, Socket.IO, reconnect, backpressure. |
| [plotly-visualization-engineer](../skills/frontend/plotly-visualization-engineer/) | Интерактивные дашборды, выбор типов графиков, экспорт в HTML. |

---

## Структура скилла

Каждый скилл — директория с обязательным `SKILL.md` и по желанию:

- `references/` — паттерны и чеклисты
- `scripts/` — скрипты для генерации заготовок
- `assets/` — JSON-схемы, шаблоны
- `agents/openai.yaml` — метаданные для Codex (UI, policy, dependencies)

В `SKILL.md`: YAML frontmatter с полями `name` и `description` (соответствуют спецификациям платформ), далее инструкции для агента.

---

## Быстрый запуск скриптов (scaffold)

```bash
# LangGraph
python3 skills/langgraph/langgraph-core-agent-builders/scripts/scaffold_core_agent_graph.py ./output
python3 skills/langgraph/langgraph-multi-agent-systems/scripts/scaffold_multi_agent_graph.py ./output
python3 skills/langgraph/langgraph-rag-architectures/scripts/scaffold_rag_graphs.py ./output
python3 skills/langgraph/langgraph-planning-reasoning/scripts/scaffold_planning_graphs.py ./output
python3 skills/langgraph/langgraph-evaluation-simulation/scripts/scaffold_simulation_harness.py ./output
python3 skills/langgraph/langgraph-research-web-agents/scripts/scaffold_research_agent.py ./output

# Platform и backend
python3 skills/platform/kubernetes-platform-engineer/scripts/scaffold_k8s_service.py myservice --output ./k8s
python3 skills/backend/microservice-architecture-designer/scripts/scaffold_microservices.py myservice --output ./services
python3 skills/backend/async-backend-orchestrator/scripts/scaffold_async_backend.py myworker --output ./workers
python3 skills/backend/async-database-engineer/scripts/generate_async_db_starter.py --output ./db

# Frontend
python3 skills/frontend/react-js-engineer/scripts/scaffold_react_feature.py MyFeature --output ./src/features
python3 skills/frontend/vue-js-engineer/scripts/scaffold_vue_feature.py MyFeature --output ./src/features
python3 skills/frontend/frontend-design-engineer/scripts/generate_design_tokens.py --output ./tokens
python3 skills/frontend/plotly-visualization-engineer/scripts/build_plotly_dashboard.py --output ./dashboard
```

Карта туториалов LangGraph: [langgraph-tutorials-playbook/references/tutorial-map.md](../skills/langgraph/langgraph-tutorials-playbook/references/tutorial-map.md).
