# skills_for_llm_projects

Production-oriented skill pack for LLM software engineering, LangGraph architectures, platform operations, and evaluation pipelines.

## 1. Quick Start (3 clicks)

1. Clone repo and enter it:

```bash
git clone <YOUR_REPO_URL> skills_for_llm_projects
cd skills_for_llm_projects
```

2. Run bootstrap:

```bash
./scripts/bootstrap_vibecoding.sh
```

3. Open this folder in your coding agent (Codex/Claude Code/Cursor/Cline).

After bootstrap, skills are available at:

- `./skills/` (project-local source of truth)
- `~/.codex/skills/skills_for_llm_projects` (Codex symlink/copy)
- `~/.claude/skills/skills_for_llm_projects` (Claude mirror)

Use `./scripts/bootstrap_vibecoding.sh --copy` if symlinks are not desired.

## 2. Full Validation

Run all checks:

```bash
./scripts/validate_all_skills.sh
```

This runs:

- frontmatter validation for every skill
- Python syntax validation for all scripts
- smoke generation for key scaffolding scripts

## 3. Skills Index

### General Software Skills

- `skills/microservice-architecture-designer`
- `skills/react-js-engineer`
- `skills/vue-js-engineer`
- `skills/frontend-design-engineer`
- `skills/async-database-engineer`
- `skills/web-ui-streaming-engineer`
- `skills/async-backend-orchestrator`
- `skills/llm-async-structured-output`
- `skills/prompt-engineering-playbook`
- `skills/plotly-visualization-engineer`

### LangGraph Tutorial Skills

- `skills/langgraph-tutorials-playbook`
  Maps the whole tutorial catalog to concrete architecture choices.
- `skills/langgraph-core-agent-builders`
  Intro/info-gather/code-assistant/customer-support style app patterns.
- `skills/langgraph-multi-agent-systems`
  Collaboration, supervisor, and hierarchical teams.
- `skills/langgraph-rag-architectures`
  Agentic/Adaptive/CRAG/Self-RAG, including local variants.
- `skills/langgraph-planning-reasoning`
  Plan-and-execute, ReWOO, LLM compiler, LATS, reflection/reflexion.
- `skills/langgraph-evaluation-simulation`
  Simulation-driven evaluation and benchmark loops.
- `skills/langgraph-research-web-agents`
  STORM, web-voyager style action loops, benchmark research flows.

### Infrastructure and Evaluation Skills

- `skills/kubernetes-platform-engineer`
- `skills/llm-as-a-judge-designer`

## 4. Vibe-Coding Tool Compatibility

This repository is pre-adapted for multi-agent coding tools via project instruction files and portable skill folders.

### Codex

- Uses skills from `~/.codex/skills/skills_for_llm_projects` after bootstrap.

### Claude Code

- Uses project memory in `CLAUDE.md`.
- Skills mirrored into `~/.claude/skills/skills_for_llm_projects` by bootstrap for local reuse workflows.

### Cursor

- Uses `AGENTS.md` in repo root (supported by Cursor agent docs).

### Cline

- Uses `AGENTS.md` in repo root (supported by Cline docs).

## 5. Sources Used for LangGraph Skill Coverage

Tutorial mirror index:

- `https://www.baihezi.com/mirrors/langgraph/tutorials/`

Multi-agent tutorials:

- `https://www.baihezi.com/mirrors/langgraph/tutorials/multi_agent/multi-agent-collaboration/index.html`
- `https://www.baihezi.com/mirrors/langgraph/tutorials/multi_agent/agent_supervisor/index.html`
- `https://www.baihezi.com/mirrors/langgraph/tutorials/multi_agent/hierarchical_agent_teams/index.html`

Full mapping of tutorial URLs is in:

- `skills/langgraph-tutorials-playbook/references/tutorial-map.md`
