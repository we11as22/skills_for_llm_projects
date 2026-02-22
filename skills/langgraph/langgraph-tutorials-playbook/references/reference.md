# LangGraph Playbook Reference

## Table of Contents

1. Pattern selection matrix
2. Reliability controls
3. Safety controls
4. Evaluation readiness
5. Production rollout

## 1. Pattern Selection Matrix

- Single graph, low branching: introduction/core builders.
- Tool-specialist collaboration: multi-agent collaboration.
- Team routing and ownership: supervisor/hierarchical teams.
- Retrieval uncertainty: adaptive/corrective/self-RAG.
- Multi-step dependencies: plan-and-execute, ReWOO, LLM compiler.
- Search over candidate reasoning traces: LATS.

## 2. Reliability Controls

- Add typed graph state with strict schemas.
- Add retries on transient tool failures.
- Add persistence/checkpointing for resumability.
- Add explicit time budget per run.

## 3. Safety Controls

- Restrict tool permissions by node role.
- Add prompt injection defenses for retrieval nodes.
- Add structured policy checks before irreversible actions.

## 4. Evaluation Readiness

- Build synthetic and real golden datasets.
- Track task success, factuality, tool error rates, latency, cost.
- Add judge model and human spot checks for critical domains.

## 5. Production Rollout

- Start with shadow mode.
- Add canary traffic percentages.
- Compare baseline vs new graph metrics before full cutover.
