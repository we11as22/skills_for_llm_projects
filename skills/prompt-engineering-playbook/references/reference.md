# Prompt Engineering Reference

## Table of Contents

1. Prompt anatomy
2. Pattern catalog
3. Failure modes
4. Evaluation strategy

## 1. Prompt Anatomy

- Goal: what to solve.
- Constraints: mandatory rules.
- Context: relevant facts only.
- Output contract: JSON/table/schema requirements.
- Quality bar: completeness, confidence, citation style.

## 2. Pattern Catalog

- Extractor pattern: strict schema extraction.
- Planner pattern: phased decomposition.
- Critic-revise pattern: self-review with fixed rubric.
- Router pattern: task classification and dispatch.

## 3. Failure Modes

- Ambiguous instruction order.
- Unbounded output scope.
- Missing edge-case constraints.
- Injection-prone context inclusion.

## 4. Evaluation Strategy

- Golden dataset with expected outputs.
- Field-level accuracy and format compliance.
- Hallucination rate and refusal quality.
- Latency and token budget tracking.
