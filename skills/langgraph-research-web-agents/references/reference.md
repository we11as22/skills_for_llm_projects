# Research and Web Agents Reference

## Table of Contents

1. STORM pattern
2. Web navigation pattern
3. Benchmark-driven loops
4. Safety policy
5. Evaluation

## 1. STORM Pattern

- Planner builds outline.
- Retriever/browser gathers sources per section.
- Writer synthesizes section drafts with citations.
- Refiner enforces structure and consistency.

## 2. Web Navigation Pattern

- Observe page state.
- Choose action (click/type/scroll/open).
- Execute action and collect new observation.
- Repeat until goal or budget reached.

## 3. Benchmark-Driven Loops

- Add deterministic scoring harness.
- Keep traces for failed runs.
- Compare prompt/graph variants via A/B runs.

## 4. Safety Policy

- Restrict external domains and form submission actions.
- Mask sensitive content before logging.
- Add manual approval gate for risky actions.

## 5. Evaluation

- Task completion rate
- Action efficiency (steps to success)
- Citation quality
- Hallucination rate
