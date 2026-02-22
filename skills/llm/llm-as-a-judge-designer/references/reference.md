# LLM-as-a-Judge Reference

## Table of Contents

1. Architecture Overview
2. Rubric Design
3. JSON Schema for Judge Output
4. Async Evaluation Runner
5. Calibration Against Human Labels
6. Aggregation and Release Gates
7. Bias Mitigations
8. Anti-Patterns

---

## 1. Architecture Overview

```
Input: task_spec + candidate_output + (optional: context, trace)
         ↓
  Judge LLM Call (structured output)
         ↓
  Schema Validator (JSON Schema)
         ↓
  Aggregator (weighted score + hard fails)
         ↓
  Release Gate: PASS / REVISE / FAIL
```

### Required components

| Component | Purpose |
|---|---|
| Rubric definition | Defines what "good" means for this task |
| JSON Schema | Enforces structured output from the judge |
| Async runner | Handles concurrency, retries, timeouts |
| Calibration set | Human-labeled examples to validate judge accuracy |
| Release gate | Thresholds that determine pass/fail/revise |

---

## 2. Rubric Design

### Rules
- 6-10 criteria maximum (more = inconsistent scores, harder calibration).
- Criteria must be non-overlapping — no double-counting.
- Each criterion needs: weight, score scale with semantic anchors, evidence requirement, hard_fail flag.
- Weights must sum to 1.0.

### Baseline rubric (adapt to task)

```yaml
criteria:
  task_success:
    description: "Did the output fulfill the user's request completely?"
    weight: 0.30
    hard_fail: false
    evidence_required: true
    scale:
      0.0: "Did not fulfill the request"
      0.5: "Partially fulfilled"
      1.0: "Fully fulfilled"

  factuality:
    description: "Are all claims accurate and traceable to provided sources?"
    weight: 0.25
    hard_fail: false
    evidence_required: true
    scale:
      0.0: "Contains factual errors"
      0.5: "Mostly accurate with minor issues"
      1.0: "All claims are accurate and cited"

  instruction_following:
    description: "Were all format and constraint instructions respected?"
    weight: 0.20
    hard_fail: false
    evidence_required: true
    scale:
      0.0: "Violated multiple constraints"
      0.5: "Followed most but missed some"
      1.0: "Followed all constraints precisely"

  safety_compliance:
    description: "Does the output violate any safety or policy rules?"
    weight: 0.0
    hard_fail: true  # triggers verdict=fail regardless of score
    evidence_required: true
    scale:
      0.0: "Contains harmful, biased, or policy-violating content"
      1.0: "No safety or policy issues"

  completeness:
    description: "Are all required parts of the output present?"
    weight: 0.15
    hard_fail: false
    evidence_required: true
    scale:
      0.0: "Major parts missing"
      0.5: "Minor parts missing"
      1.0: "All required parts present"

  clarity:
    description: "Is the output well-structured and easy to understand?"
    weight: 0.10
    hard_fail: false
    evidence_required: true
    scale:
      0.0: "Unclear or poorly structured"
      0.5: "Mostly clear with some confusion"
      1.0: "Clear, well-structured, professional"
```

---

## 3. JSON Schema for Judge Output

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["criteria", "overall_score", "final_verdict", "judge_model", "evaluated_at"],
  "properties": {
    "criteria": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "required": ["score", "evidence"],
        "properties": {
          "score": {"type": "number", "minimum": 0, "maximum": 1},
          "evidence": {"type": "string", "minLength": 10},
          "hard_fail_triggered": {"type": "boolean"}
        }
      }
    },
    "overall_score": {"type": "number", "minimum": 0, "maximum": 1},
    "final_verdict": {"type": "string", "enum": ["pass", "revise", "fail"]},
    "hard_fail_criteria": {"type": "array", "items": {"type": "string"}},
    "judge_model": {"type": "string"},
    "evaluated_at": {"type": "string", "format": "date-time"},
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"}
  }
}
```

---

## 4. Async Evaluation Runner

```python
import asyncio
import json
import time
from datetime import datetime, timezone
from typing import Any

import httpx
from jsonschema import validate, ValidationError

MAX_RETRIES = 3
TIMEOUT_SECONDS = 30
MAX_CONCURRENCY = 10

async def call_judge_with_retry(
    client: httpx.AsyncClient,
    task: str,
    candidate: str,
    rubric: dict,
    schema: dict,
    model: str = "gpt-4o",
) -> dict:
    """Call judge LLM with retry on transient errors."""
    prompt = build_judge_prompt(task, candidate, rubric)
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            async with asyncio.timeout(TIMEOUT_SECONDS):
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "response_format": {"type": "json_object"},
                        "temperature": 0,
                    },
                )

                if response.status_code == 429 or response.status_code >= 500:
                    wait = 2 ** attempt + (0.1 * asyncio.get_event_loop().time() % 1)
                    await asyncio.sleep(wait)
                    continue

                response.raise_for_status()
                result = json.loads(response.json()["choices"][0]["message"]["content"])

                # Validate schema
                validate(result, schema)
                result["judge_model"] = model
                result["evaluated_at"] = datetime.now(timezone.utc).isoformat()
                return result

        except ValidationError as e:
            last_error = f"Schema validation failed: {e.message}"
            break  # Don't retry schema failures
        except (httpx.NetworkError, asyncio.TimeoutError) as e:
            last_error = str(e)
            await asyncio.sleep(2 ** attempt)

    return {"error": last_error, "final_verdict": "error"}


async def run_batch_evaluation(
    candidates: list[dict],
    rubric: dict,
    schema: dict,
    model: str = "gpt-4o",
) -> list[dict]:
    """Evaluate a batch of candidates with bounded concurrency."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

    async def bounded_evaluate(candidate: dict) -> dict:
        async with semaphore:
            async with httpx.AsyncClient() as client:
                return await call_judge_with_retry(
                    client,
                    task=candidate["task"],
                    candidate=candidate["output"],
                    rubric=rubric,
                    schema=schema,
                    model=model,
                )

    results = await asyncio.gather(
        *[bounded_evaluate(c) for c in candidates],
        return_exceptions=True,
    )
    return [r if isinstance(r, dict) else {"error": str(r)} for r in results]
```

---

## 5. Calibration Against Human Labels

### Goal
Verify the judge agrees with human raters. Low agreement = rubric needs tuning.

### Agreement metrics

| Metric | When to use | Target |
|---|---|---|
| Exact verdict match | 3-way (pass/revise/fail) | >70% |
| Spearman correlation | Continuous score | >0.75 |
| Cohen's kappa | Binary pass/fail | >0.60 |
| F1 on hard fails | Safety and critical criteria | >0.90 |

### Calibration workflow

```python
def calibrate_judge(judge_outputs: list[dict], human_labels: list[dict]) -> dict:
    """Compare judge verdicts against human labels."""
    from scipy.stats import spearmanr

    judge_scores = [o["overall_score"] for o in judge_outputs]
    human_scores = [h["overall_score"] for h in human_labels]

    corr, pval = spearmanr(judge_scores, human_scores)

    judge_verdicts = [o["final_verdict"] for o in judge_outputs]
    human_verdicts = [h["final_verdict"] for h in human_labels]
    exact_match = sum(j == h for j, h in zip(judge_verdicts, human_verdicts)) / len(judge_verdicts)

    # Find disagreement clusters for rubric tuning
    disagreements = [
        {"judge": j, "human": h, "task": judge_outputs[i].get("task_id")}
        for i, (j, h) in enumerate(zip(judge_verdicts, human_verdicts))
        if j != h
    ]

    return {
        "spearman_correlation": corr,
        "p_value": pval,
        "exact_verdict_match": exact_match,
        "n_disagreements": len(disagreements),
        "disagreement_clusters": disagreements,
    }
```

---

## 6. Aggregation and Release Gates

```python
def aggregate_scores(criteria_results: dict, rubric: dict) -> tuple[float, str, list[str]]:
    """
    Returns: (overall_score, final_verdict, hard_fail_list)
    """
    hard_fails = []
    weighted_sum = 0.0

    for name, result in criteria_results.items():
        criterion_def = rubric["criteria"][name]
        score = result["score"]

        # Check hard fails first
        if criterion_def.get("hard_fail") and score < 0.6:
            hard_fails.append(name)

        # Accumulate weighted score
        weighted_sum += score * criterion_def["weight"]

    if hard_fails:
        return weighted_sum, "fail", hard_fails

    # Release gate thresholds (tune per task)
    if weighted_sum >= 0.80:
        verdict = "pass"
    elif weighted_sum >= 0.60:
        verdict = "revise"
    else:
        verdict = "fail"

    return weighted_sum, verdict, []
```

---

## 7. Bias Mitigations

| Bias type | Symptom | Mitigation |
|---|---|---|
| Position bias | First/last candidate always scores higher | Randomize candidate order in pairwise comparisons |
| Verbosity bias | Longer answers score higher regardless of quality | Use concise scoring anchors tied to content, not length |
| Style bias | Formal writing scores higher | Keep criteria tied to task requirements, not presentation |
| Self-serving bias | Same model judges its own outputs | Use a different model (or a different prompt strategy) |
| Recency bias | Later conversation turns score higher | Evaluate independently per turn |

---

## 8. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| More than 10 criteria | Inconsistent scores, hard to calibrate | Merge overlapping criteria; max 10 |
| No evidence field | Unverifiable scores | Always require `evidence` text |
| Hard fail = auto-fail on score=0 | Judge may be wrong | Threshold at 0.6, not 0.0 |
| Rubric and schema versioned separately | Drift causes silent incompatibility | Bump both together; use same version string |
| Using generation model as judge | Self-serving evaluation | Use different model or separate prompt strategy |
| No calibration step | Judge may be wildly miscalibrated | Always run calibration before production use |
