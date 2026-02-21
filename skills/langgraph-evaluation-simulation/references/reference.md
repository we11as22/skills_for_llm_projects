# Evaluation and Simulation Reference

## Table of Contents

1. Scenario design
2. Simulation architecture
3. Judge design
4. Metrics
5. Continuous evaluation operations

## 1. Scenario Design

- Include happy-path, ambiguous, adversarial, and policy-sensitive prompts.
- Tag each scenario with domain, intent, risk level.

## 2. Simulation Architecture

- Simulated user node generates next user message from policy.
- Assistant node responds using target graph.
- Stop conditions: success/failure/max_turns.

## 3. Judge Design

- Use structured JSON outputs.
- Score factuality, instruction following, safety, helpfulness, format compliance.
- Include rationale and concrete evidence spans.

## 4. Metrics

- Task success rate
- Safety violation rate
- Average turns to resolution
- Latency/cost per scenario
- Regression deltas vs baseline

## 5. Continuous Operations

- Run nightly evaluation suites.
- Block release on critical metric regressions.
- Keep scenario versioning with change logs.
