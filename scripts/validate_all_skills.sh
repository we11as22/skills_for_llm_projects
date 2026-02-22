#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
VALIDATOR="$REPO_ROOT/scripts/quick_validate_skill.py"

echo "[1/3] quick_validate for all skills"
for cat_dir in "$SKILLS_DIR"/*/; do
  [[ -d "$cat_dir" ]] || continue
  for d in "$cat_dir"*/; do
    [[ -f "${d}SKILL.md" ]] || continue
    python3 "$VALIDATOR" "$d"
  done
done

echo "[2/3] py_compile all python scripts"
mapfile -t py_files < <(find "$SKILLS_DIR" -type f -name '*.py' | sort)
if ((${#py_files[@]} > 0)); then
  python3 -m py_compile "${py_files[@]}"
fi

echo "[3/3] basic smoke generation"
TMP_DIR="$(mktemp -d /tmp/skills_for_llm_projects_validate.XXXXXX)"
python3 "$SKILLS_DIR"/langgraph/langgraph-multi-agent-systems/scripts/scaffold_multi_agent_graph.py "$TMP_DIR/multi"
python3 "$SKILLS_DIR"/langgraph/langgraph-rag-architectures/scripts/scaffold_rag_graphs.py "$TMP_DIR/rag"
python3 "$SKILLS_DIR"/platform/kubernetes-platform-engineer/scripts/scaffold_k8s_service.py demo --output "$TMP_DIR/k8s"
echo "Demo candidate output." > "$TMP_DIR/candidate.txt"
if python3 - <<'PY'
import importlib.util
raise SystemExit(0 if importlib.util.find_spec("jsonschema") else 1)
PY
then
  python3 "$SKILLS_DIR"/llm/llm-as-a-judge-designer/scripts/run_llm_judge.py \
    --task "Demo task" \
    --candidate "$TMP_DIR/candidate.txt" \
    --schema "$SKILLS_DIR/llm/llm-as-a-judge-designer/assets/judge-output-schema.json" \
    --use-local-fallback \
    --output "$TMP_DIR/judge_result.json"
else
  echo "[WARN] jsonschema not installed; skipped llm-as-a-judge smoke test"
fi

echo "[OK] validation completed"
echo "Smoke artifacts in: $TMP_DIR"
