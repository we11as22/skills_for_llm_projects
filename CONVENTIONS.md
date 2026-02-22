# Aider Conventions — skills_for_llm_projects

This repository contains production coding skills in `skills/`. Read the relevant skill before implementing any feature.

## Skill routing

- LangGraph agent: skills/langgraph-tutorials-playbook/SKILL.md (start here)
- Multi-agent: skills/langgraph-multi-agent-systems/SKILL.md
- RAG: skills/langgraph-rag-architectures/SKILL.md
- Kubernetes: skills/kubernetes-platform-engineer/SKILL.md
- React: skills/react-js-engineer/SKILL.md
- See AGENTS.md for the full skill routing table.

## Non-negotiable rules

- LangGraph state: TypedDict only, step_count guard on every loop.
- Kubernetes: always set resource limits, runAsNonRoot, readinessProbe.
- Async Python: idempotent handlers, retry only transient errors.
- React/Vue: TypeScript strict, handle all async states.
