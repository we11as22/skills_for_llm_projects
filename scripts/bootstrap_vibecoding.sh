#!/usr/bin/env bash
set -euo pipefail

# Skill bank bootstrap: one run installs only selected skills to selected vibecodes.
# No extra junk — only skill directories. Config in bootstrap.config (and optional bootstrap.config.local).
#
# Usage:
#   ./scripts/bootstrap_vibecoding.sh
#     → use bootstrap.config (categories, targets, paths)
#   ./scripts/bootstrap_vibecoding.sh --categories langgraph,llm --targets cursor,claude
#   ./scripts/bootstrap_vibecoding.sh --copy
#
# Paths: default = ~ (e.g. ~/.cursor/skills). Set CLAUDE_PATH, CURSOR_PATH, etc. in config
# to install into a project folder (e.g. /path/to/proj/.cursor/skills).

MODE="symlink"
CATEGORIES=""
TARGETS=""
SKILLS_EXTRA=""

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
BOOTSTRAP_CONFIG="$REPO_ROOT/bootstrap.config"
BOOTSTRAP_LOCAL="$REPO_ROOT/bootstrap.config.local"

ALL_CATEGORIES="langgraph llm frontend backend platform"
ALL_TARGETS="claude codex cursor windsurf cline aider roo kilocode opencode"
# common is always installed — it contains always-on guardrail skills
MANDATORY_CATEGORIES="common"

# Per-target: relative subpath under base (base = $HOME or custom *_PATH).
# So base + subpath = full install dir for skills.
declare -A TARGET_SUBPATH
TARGET_SUBPATH[claude]=".claude/skills"
TARGET_SUBPATH[codex]=".agents/skills"
TARGET_SUBPATH[cursor]=".cursor/skills"
TARGET_SUBPATH[windsurf]=".codeium/windsurf/memories"
TARGET_SUBPATH[roo]=".roo/skills"
TARGET_SUBPATH[kilocode]=".kilocode/skills"
TARGET_SUBPATH[opencode]=".config/opencode/skills"

# Path overrides (base dir for each target; empty = use HOME)
CLAUDE_PATH=""
CODEX_PATH=""
CURSOR_PATH=""
WINDSURF_PATH=""
ROO_PATH=""
KILO_PATH=""
OPENCODE_PATH=""

read_config() {
  local f="$1"
  [[ ! -f "$f" ]] && return
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ "$line" =~ ^#.*$ || -z "${line// }" ]] && continue
    if [[ "$line" =~ ^CATEGORIES=(.*)$ ]]; then
      CATEGORIES="${BASH_REMATCH[1]//\"/}"
    elif [[ "$line" =~ ^TARGETS=(.*)$ ]]; then
      TARGETS="${BASH_REMATCH[1]//\"/}"
    elif [[ "$line" =~ ^SKILLS_EXTRA=(.*)$ ]]; then
      SKILLS_EXTRA="${BASH_REMATCH[1]//\"/}"
    elif [[ "$line" =~ ^CLAUDE_PATH=(.*)$ ]]; then
      CLAUDE_PATH="${BASH_REMATCH[1]//\"/}"
    elif [[ "$line" =~ ^CODEX_PATH=(.*)$ ]]; then
      CODEX_PATH="${BASH_REMATCH[1]//\"/}"
    elif [[ "$line" =~ ^CURSOR_PATH=(.*)$ ]]; then
      CURSOR_PATH="${BASH_REMATCH[1]//\"/}"
    elif [[ "$line" =~ ^WINDSURF_PATH=(.*)$ ]]; then
      WINDSURF_PATH="${BASH_REMATCH[1]//\"/}"
    elif [[ "$line" =~ ^ROO_PATH=(.*)$ ]]; then
      ROO_PATH="${BASH_REMATCH[1]//\"/}"
    elif [[ "$line" =~ ^KILO_PATH=(.*)$ ]]; then
      KILO_PATH="${BASH_REMATCH[1]//\"/}"
    elif [[ "$line" =~ ^OPENCODE_PATH=(.*)$ ]]; then
      OPENCODE_PATH="${BASH_REMATCH[1]//\"/}"
    fi
  done < "$f"
}

# Load config: default then local overrides
read_config "$BOOTSTRAP_CONFIG"
read_config "$BOOTSTRAP_LOCAL"

[[ -z "${CATEGORIES// }" ]] && CATEGORIES="$ALL_CATEGORIES"
[[ -z "${TARGETS// }" ]] && TARGETS="$ALL_TARGETS"
[[ "$CATEGORIES" == "all" ]] && CATEGORIES="$ALL_CATEGORIES"
[[ "$TARGETS" == "all" ]] && TARGETS="$ALL_TARGETS"

# Always include mandatory categories (common) — cannot be excluded
for _mc in $MANDATORY_CATEGORIES; do
  if [[ " $CATEGORIES " != *" $_mc "* ]]; then
    CATEGORIES="$CATEGORIES $_mc"
  fi
done

# Parse CLI (override config)
while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)       MODE="copy"; shift ;;
    --categories) [[ -n "${2:-}" ]] && { CATEGORIES="${2//,/ }"; shift; }; shift ;;
    --targets)    [[ -n "${2:-}" ]] && { TARGETS="${2//,/ }"; shift; }; shift ;;
    --claude)     TARGETS="${TARGETS} claude"; shift ;;
    --codex)      TARGETS="${TARGETS} codex"; shift ;;
    --cursor)     TARGETS="${TARGETS} cursor"; shift ;;
    --windsurf)   TARGETS="${TARGETS} windsurf"; shift ;;
    --cline)      TARGETS="${TARGETS} cline"; shift ;;
    --aider)      TARGETS="${TARGETS} aider"; shift ;;
    --roo)        TARGETS="${TARGETS} roo"; shift ;;
    --kilocode)   TARGETS="${TARGETS} kilocode"; shift ;;
    --opencode)   TARGETS="${TARGETS} opencode"; shift ;;
    --help|-h)
      echo "Usage: $0 [--copy] [--categories A,B] [--targets X,Y] [--cursor] [--claude] ..."
      echo "Config: $BOOTSTRAP_CONFIG (optional: $BOOTSTRAP_LOCAL)"
      echo "  CATEGORIES, TARGETS, SKILLS_EXTRA; CLAUDE_PATH, CURSOR_PATH, ... (empty = use ~)"
      exit 0
      ;;
    *) echo "[ERROR] Unknown option: $1"; exit 1 ;;
  esac
done

# Always re-inject mandatory categories after CLI may have overridden them
for _mc in $MANDATORY_CATEGORIES; do
  if [[ " $CATEGORIES " != *" $_mc "* ]]; then
    CATEGORIES="$CATEGORIES $_mc"
  fi
done

# Resolve target flags
TARGET_CLAUDE=0;   for t in $TARGETS; do [[ "$t" == "claude" ]]   && TARGET_CLAUDE=1; done
TARGET_CODEX=0;    for t in $TARGETS; do [[ "$t" == "codex" ]]    && TARGET_CODEX=1; done
TARGET_CURSOR=0;   for t in $TARGETS; do [[ "$t" == "cursor" ]]   && TARGET_CURSOR=1; done
TARGET_WINDSURF=0; for t in $TARGETS; do [[ "$t" == "windsurf" ]] && TARGET_WINDSURF=1; done
TARGET_CLINE=0;    for t in $TARGETS; do [[ "$t" == "cline" ]]    && TARGET_CLINE=1; done
TARGET_AIDER=0;    for t in $TARGETS; do [[ "$t" == "aider" ]]    && TARGET_AIDER=1; done
TARGET_ROO=0;      for t in $TARGETS; do [[ "$t" == "roo" ]]      && TARGET_ROO=1; done
TARGET_KILO=0;     for t in $TARGETS; do [[ "$t" == "kilocode" ]] && TARGET_KILO=1; done
TARGET_OPENCODE=0; for t in $TARGETS; do [[ "$t" == "opencode" ]] && TARGET_OPENCODE=1; done

if [[ ! -d "$SKILLS_DIR" ]]; then
  echo "[ERROR] skills directory not found: $SKILLS_DIR"
  exit 1
fi

# Collect skill dirs: from categories + SKILLS_EXTRA (find by name in any category)
SKILL_DIRS=()
for cat in $CATEGORIES; do
  cat_dir="$SKILLS_DIR/$cat"
  [[ ! -d "$cat_dir" ]] && continue
  for skill_dir in "$cat_dir"/*/; do
    [[ -d "$skill_dir" ]] || continue
    [[ -f "${skill_dir}SKILL.md" ]] || continue
    SKILL_DIRS+=( "$skill_dir" )
  done
done

# Add extra skills by name (search in all categories)
for name in $SKILLS_EXTRA; do
  found=0
  for cat_dir in "$SKILLS_DIR"/*/; do
    [[ -d "$cat_dir" ]] || continue
    skill_dir="${cat_dir}$name/"
    if [[ -d "$skill_dir" && -f "${skill_dir}SKILL.md" ]]; then
      SKILL_DIRS+=( "$skill_dir" )
      found=1
      break
    fi
  done
  [[ $found -eq 0 ]] && echo "[WARN] SKILLS_EXTRA skill not found: $name"
done

# Dedupe by skill name (same name might appear from category + extra)
declare -A SEEN
DEDUPED=()
for skill_dir in "${SKILL_DIRS[@]}"; do
  skill_name="$(basename "$skill_dir")"
  [[ -n "${SEEN[$skill_name]:-}" ]] && continue
  SEEN[$skill_name]=1
  DEDUPED+=( "$skill_dir" )
done
SKILL_DIRS=( "${DEDUPED[@]}" )

if [[ ${#SKILL_DIRS[@]} -eq 0 ]]; then
  echo "[ERROR] No skills found (categories: $CATEGORIES; SKILLS_EXTRA: $SKILLS_EXTRA)"
  exit 1
fi

link_or_copy() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [[ "$MODE" == "copy" ]]; then
    rm -rf "$dst"
    cp -R "$src" "$dst"
    echo "  [copy] $dst"
  else
    ln -sfn "$src" "$dst"
    echo "  [link] $dst"
  fi
}

copy_file() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
  echo "  [file] $dst"
}

# Resolve base dir for target: use *_PATH or HOME
base_for() {
  case "$1" in
    claude)   echo "${CLAUDE_PATH:-$HOME}" ;;
    codex)    echo "${CODEX_PATH:-$HOME}" ;;
    cursor)   echo "${CURSOR_PATH:-$HOME}" ;;
    windsurf) echo "${WINDSURF_PATH:-$HOME}" ;;
    roo)      echo "${ROO_PATH:-$HOME}" ;;
    kilocode) echo "${KILO_PATH:-$HOME}" ;;
    opencode) echo "${OPENCODE_PATH:-$HOME}" ;;
    *)        echo "$HOME" ;;
  esac
}

STEP=0
step_msg() { STEP=$((STEP+1)); echo ""; echo "[$STEP] $1"; }

echo ""
echo "=== Skill bank bootstrap (mode: $MODE) ==="
echo "  Categories: $CATEGORIES  (common always included)"
echo "  Targets: $TARGETS"
echo "  Skills: ${#SKILL_DIRS[@]}"
echo ""

# ─── Claude Code ─────────────────────────────────────────────────────────────
if [[ $TARGET_CLAUDE -eq 1 ]]; then
  step_msg "Claude Code"
  BASE="$(base_for claude)"
  CLAUDE_SKILLS_DEST="$BASE/.claude/skills"
  mkdir -p "$CLAUDE_SKILLS_DEST"
  if [[ -L "$CLAUDE_SKILLS_DEST/skills_for_llm_projects" ]]; then
    rm -f "$CLAUDE_SKILLS_DEST/skills_for_llm_projects"
    echo "  [rm]   legacy symlink"
  fi
  for skill_dir in "${SKILL_DIRS[@]}"; do
    skill_name="$(basename "$skill_dir")"
    link_or_copy "$skill_dir" "$CLAUDE_SKILLS_DEST/$skill_name"
  done
  # Commands only when global (default path)
  if [[ -z "${CLAUDE_PATH:-}" ]]; then
    CLAUDE_CMDS_DIR="$HOME/.claude/commands"
    mkdir -p "$CLAUDE_CMDS_DIR"
    for cmd_file in "$REPO_ROOT/.claude/commands/"*.md; do
      [[ -f "$cmd_file" ]] || continue
      cmd_name="$(basename "$cmd_file")"
      if [[ "$MODE" == "copy" ]]; then
        cp "$cmd_file" "$CLAUDE_CMDS_DIR/$cmd_name"
      else
        ln -sfn "$cmd_file" "$CLAUDE_CMDS_DIR/$cmd_name"
      fi
      echo "  [cmd]  $CLAUDE_CMDS_DIR/$cmd_name"
    done
  fi
  echo "  → $CLAUDE_SKILLS_DEST"
fi

# ─── OpenAI Codex ────────────────────────────────────────────────────────────
if [[ $TARGET_CODEX -eq 1 ]]; then
  step_msg "OpenAI Codex"
  BASE="$(base_for codex)"
  CODEX_SKILLS_DEST="$BASE/.agents/skills"
  mkdir -p "$CODEX_SKILLS_DEST"
  for skill_dir in "${SKILL_DIRS[@]}"; do
    skill_name="$(basename "$skill_dir")"
    link_or_copy "$skill_dir" "$CODEX_SKILLS_DEST/$skill_name"
  done
  if [[ -z "${CODEX_PATH:-}" ]]; then
    CODEX_INSTRUCTIONS="$HOME/.codex/instructions.md"
    mkdir -p "$HOME/.codex"
    if [[ ! -f "$CODEX_INSTRUCTIONS" ]]; then
      printf '%s\n' "# Codex — skills from skill bank" "Skills: ~/.agents/skills/<name>/" "See project AGENTS.md for routing." > "$CODEX_INSTRUCTIONS"
      echo "  [new]  $CODEX_INSTRUCTIONS"
    fi
  fi
  echo "  → $CODEX_SKILLS_DEST"
fi

# ─── Cursor ──────────────────────────────────────────────────────────────────
if [[ $TARGET_CURSOR -eq 1 ]]; then
  step_msg "Cursor"
  BASE="$(base_for cursor)"
  CURSOR_SKILLS_DEST="$BASE/.cursor/skills"
  mkdir -p "$CURSOR_SKILLS_DEST"
  for skill_dir in "${SKILL_DIRS[@]}"; do
    skill_name="$(basename "$skill_dir")"
    link_or_copy "$skill_dir" "$CURSOR_SKILLS_DEST/$skill_name"
  done
  echo "  → $CURSOR_SKILLS_DEST"
fi

# ─── Roo Code ────────────────────────────────────────────────────────────────
if [[ $TARGET_ROO -eq 1 ]]; then
  step_msg "Roo Code"
  BASE="$(base_for roo)"
  ROO_SKILLS_DEST="$BASE/.roo/skills"
  mkdir -p "$ROO_SKILLS_DEST"
  for skill_dir in "${SKILL_DIRS[@]}"; do
    skill_name="$(basename "$skill_dir")"
    link_or_copy "$skill_dir" "$ROO_SKILLS_DEST/$skill_name"
  done
  echo "  → $ROO_SKILLS_DEST"
fi

# ─── Kilo Code ────────────────────────────────────────────────────────────────
if [[ $TARGET_KILO -eq 1 ]]; then
  step_msg "Kilo Code"
  BASE="$(base_for kilocode)"
  KILO_SKILLS_DEST="$BASE/.kilocode/skills"
  mkdir -p "$KILO_SKILLS_DEST"
  for skill_dir in "${SKILL_DIRS[@]}"; do
    skill_name="$(basename "$skill_dir")"
    link_or_copy "$skill_dir" "$KILO_SKILLS_DEST/$skill_name"
  done
  echo "  → $KILO_SKILLS_DEST"
fi

# ─── Open Code ────────────────────────────────────────────────────────────────
if [[ $TARGET_OPENCODE -eq 1 ]]; then
  step_msg "Open Code"
  BASE="$(base_for opencode)"
  OPENCODE_SKILLS_DEST="$BASE/.config/opencode/skills"
  mkdir -p "$OPENCODE_SKILLS_DEST"
  for skill_dir in "${SKILL_DIRS[@]}"; do
    skill_name="$(basename "$skill_dir")"
    link_or_copy "$skill_dir" "$OPENCODE_SKILLS_DEST/$skill_name"
  done
  echo "  → $OPENCODE_SKILLS_DEST"
fi

# ─── Windsurf ────────────────────────────────────────────────────────────────
if [[ $TARGET_WINDSURF -eq 1 ]]; then
  step_msg "Windsurf"
  BASE="$(base_for windsurf)"
  WINDSURF_DEST="$BASE/.codeium/windsurf/memories"
  if [[ -d "$BASE/.codeium" ]] || [[ "$BASE" == "$HOME" ]]; then
    mkdir -p "$WINDSURF_DEST"
    copy_file "$REPO_ROOT/.windsurfrules" "$WINDSURF_DEST/skills_for_llm_projects.md"
    echo "  → $WINDSURF_DEST/skills_for_llm_projects.md"
  else
    echo "  [skip] .codeium not found under $BASE"
  fi
fi

# ─── Cline / Aider ────────────────────────────────────────────────────────────
if [[ $TARGET_CLINE -eq 1 ]]; then
  step_msg "Cline"
  echo "  [ok]   Use this repo in Cline; .clinerules/ is in repo."
fi
if [[ $TARGET_AIDER -eq 1 ]]; then
  step_msg "Aider"
  AIDER_CONVENTIONS="$REPO_ROOT/CONVENTIONS.md"
  if [[ ! -f "$AIDER_CONVENTIONS" ]]; then
    cat > "$AIDER_CONVENTIONS" <<'AIDER_EOF'
# Aider Conventions — skill bank

Skills in this repo: skills/<category>/<name>/. Read the relevant SKILL.md before implementing.

## Routing
- LangGraph: skills/langgraph/langgraph-tutorials-playbook/ (start)
- Multi-agent: skills/langgraph/langgraph-multi-agent-systems/
- RAG: skills/langgraph/langgraph-rag-architectures/
- K8s: skills/platform/kubernetes-platform-engineer/
- React: skills/frontend/react-js-engineer/
See AGENTS.md for full table.
AIDER_EOF
    echo "  [new]  CONVENTIONS.md"
  fi
  echo "  [ok]   aider --read CONVENTIONS.md"
fi

# ─── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo "=== Done. Only skills installed (no extra files). ==="
echo ""
for t in claude codex cursor roo kilocode opencode; do
  case "$t" in
    claude)  [[ $TARGET_CLAUDE -eq 1 ]] && echo "  Claude:   $(base_for claude)/.claude/skills/" ;;
    codex)   [[ $TARGET_CODEX -eq 1 ]]  && echo "  Codex:    $(base_for codex)/.agents/skills/" ;;
    cursor)  [[ $TARGET_CURSOR -eq 1 ]] && echo "  Cursor:   $(base_for cursor)/.cursor/skills/" ;;
    roo)     [[ $TARGET_ROO -eq 1 ]]    && echo "  Roo:      $(base_for roo)/.roo/skills/" ;;
    kilocode)[[ $TARGET_KILO -eq 1 ]]   && echo "  Kilo:     $(base_for kilocode)/.kilocode/skills/" ;;
    opencode)[[ $TARGET_OPENCODE -eq 1 ]] && echo "  OpenCode: $(base_for opencode)/.config/opencode/skills/" ;;
  esac
done
[[ $TARGET_WINDSURF -eq 1 ]] && echo "  Windsurf: $(base_for windsurf)/.codeium/windsurf/memories/"
echo ""
