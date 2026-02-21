# LLM-as-a-Judge Reference

## Table of Contents

1. Judge architecture
2. Rubric design
3. Calibration
4. Aggregation and gates
5. Risks and mitigations

## 1. Judge Architecture

- Input: task spec, prompt/context, candidate output, optional trace.
- Judge model returns strict JSON according to schema.
- Validator enforces schema and score bounds.
- Aggregator computes weighted score and verdict.

## 2. Rubric Design

- Define 6-10 criteria max for operational clarity.
- Add score scale with semantic anchors (0, 0.5, 1.0).
- Add required evidence text per criterion.

## 3. Calibration

- Build human-labeled benchmark set.
- Measure agreement (e.g., correlation, exact verdict match).
- Tune rubric wording and thresholds from disagreement clusters.

## 4. Aggregation and Gates

- Compute weighted total score.
- Apply hard fails (e.g., safety critical failure) before total score.
- Define release gate tiers: pass, revise, fail.

## 5. Risks and Mitigations

- Position bias: randomize candidate order in pairwise settings.
- Verbosity bias: normalize with concise scoring anchors.
- Style bias: keep criteria tied to objective task requirements.
