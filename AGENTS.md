# Agent Instructions for skills_for_llm_projects

Use skills from `skills/` as reusable building blocks.

## Skill Selection

1. Read `README.md` skill index.
2. Pick the minimal skill set for the task.
3. Prefer specialized LangGraph/Kubernetes/Judge skills for those domains.

## Work Style

- Validate generated outputs with scripts in each skill's `scripts/` directory.
- Reuse templates from `assets/` instead of rewriting boilerplate.
- Keep structured output contracts aligned with JSON schemas in assets.
