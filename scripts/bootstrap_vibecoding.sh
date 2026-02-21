#!/usr/bin/env bash
set -euo pipefail

MODE="symlink"
if [[ "${1:-}" == "--copy" ]]; then
  MODE="copy"
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"

if [[ ! -d "$SKILLS_DIR" ]]; then
  echo "[ERROR] skills directory not found: $SKILLS_DIR"
  exit 1
fi

link_or_copy() {
  local src="$1"
  local dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [[ "$MODE" == "copy" ]]; then
    rm -rf "$dst"
    cp -R "$src" "$dst"
  else
    ln -sfn "$src" "$dst"
  fi
}

# Codex integration
link_or_copy "$SKILLS_DIR" "$HOME/.codex/skills/skills_for_llm_projects"

# Optional Claude local skills mirror (useful for custom tooling around CLAUDE.md)
link_or_copy "$SKILLS_DIR" "$HOME/.claude/skills/skills_for_llm_projects"

# Project-level instruction files used by many coding agents
if [[ ! -f "$REPO_ROOT/AGENTS.md" ]]; then
  cat > "$REPO_ROOT/AGENTS.md" <<'AGENTS'
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
AGENTS
fi

if [[ ! -f "$REPO_ROOT/CLAUDE.md" ]]; then
  cat > "$REPO_ROOT/CLAUDE.md" <<'CLAUDE'
# Claude Project Memory

This repository contains production-oriented coding skills in `skills/`.

## How to Use

- Start from `README.md` to choose a relevant skill.
- For LangGraph design tasks, prefer the `langgraph-*` skills.
- For infra tasks, use `kubernetes-platform-engineer`.
- For evaluation tasks, use `llm-as-a-judge-designer`.
CLAUDE
fi

echo "[OK] bootstrap complete"
echo "- Codex skills: ~/.codex/skills/skills_for_llm_projects"
echo "- Claude skills mirror: ~/.claude/skills/skills_for_llm_projects"
echo "- Project instruction files: AGENTS.md, CLAUDE.md"
