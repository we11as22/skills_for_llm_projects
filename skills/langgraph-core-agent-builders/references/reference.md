# Core Agent Builders Reference

## Table of Contents

1. Intro graph baseline
2. Information-gather prompting
3. Code assistant flow
4. Customer support flow
5. Production hardening

## 1. Intro Graph Baseline

- Start with typed state object.
- Keep transition conditions explicit and testable.

## 2. Information-Gather Prompting

- Ask follow-up questions until required fields are complete.
- Generate final prompt template only after constraints are clear.

## 3. Code Assistant Flow

- Retrieve docs/context.
- Generate draft code.
- Run checks/tests.
- Revise and finalize.

## 4. Customer Support Flow

- Intent classification.
- Policy/tool retrieval.
- Resolution or escalation.
- Structured case summary output.

## 5. Production Hardening

- Add timeout and retry controls.
- Add PII/safety checks.
- Add response schema validation.
