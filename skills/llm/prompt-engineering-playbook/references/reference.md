# Prompt Engineering Reference

## Table of Contents

1. Prompt Anatomy and Section Order
2. Pattern Catalog (with examples)
3. Failure Modes and Fixes
4. Versioning and Experimentation
5. Evaluation Strategy

---

## 1. Prompt Anatomy and Section Order

Optimal section order for most tasks:

```
[Role]
[Non-negotiable constraints]  ← PUT THESE EARLY, not at the end
[Context]                     ← concise, high-signal only
[Task]
[Output format contract]
[Examples]                    ← only if they improve consistency
[Refusal boundaries]
```

### Section guide

| Section | Purpose | Common mistake |
|---|---|---|
| Role | Tell the model who it is | Vague: "You are helpful." Better: "You are a Python security engineer." |
| Constraints | Non-negotiable rules | Burying them at the end — model forgets them |
| Context | Background facts | Adding irrelevant context — dilutes signal |
| Task | Clear instruction | Ambiguous verbs ("analyze", "improve") without success criteria |
| Output format | Machine-parseable contract | Missing it — output format varies per run |
| Examples | Demonstration | Contradicting the rules — examples override rules |
| Refusal | What not to do | Missing — model attempts everything |

---

## 2. Pattern Catalog

### Extractor Pattern
For structured information extraction from unstructured text.

```python
SYSTEM = """You are a data extraction specialist.
Extract the following fields from the user's text. Return ONLY valid JSON.

Required fields:
- company_name: string
- founding_year: integer or null
- funding_amount_usd: number or null
- investors: array of strings

Rules:
- Extract only what is explicitly stated. Never infer.
- If a field is not present in the text, set it to null.
- Do not include explanations. Return only the JSON object."""

# Use structured output for reliability
from pydantic import BaseModel
from typing import Optional

class CompanyInfo(BaseModel):
    company_name: str
    founding_year: Optional[int]
    funding_amount_usd: Optional[float]
    investors: list[str]

response = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}],
    response_format=CompanyInfo,
)
```

### Planner Pattern
For decomposing complex tasks into ordered steps.

```python
SYSTEM = """You are a task planner.
Break the user's goal into a concrete, ordered list of steps.

Output format (strict JSON):
{
  "goal": "one-sentence description of the objective",
  "steps": [
    {"id": 1, "action": "...", "tool": "...", "depends_on": []},
    {"id": 2, "action": "...", "tool": "...", "depends_on": [1]}
  ],
  "success_criteria": "what done looks like"
}

Rules:
- Steps must be atomic and executable.
- List dependencies explicitly.
- Never include steps that can't be verified."""
```

### Critic-Revise Pattern
For self-improvement loops.

```python
CRITIC_PROMPT = """You are a strict code reviewer.

Review the following code and return:
1. A list of specific issues (not suggestions — actual problems).
2. A revised version that fixes ONLY the issues you listed.
3. A brief diff summary.

Be ruthless: if the code is correct, say "No issues found." Do not invent problems."""
```

### Router Pattern
For task classification and dispatch.

```python
ROUTER_PROMPT = """Classify the user request into exactly one category.

Categories:
- "billing": payment, invoice, subscription, charge questions
- "technical": bug reports, feature requests, API questions
- "general": everything else

Return JSON: {"category": "<category>", "confidence": <0.0-1.0>, "reason": "<why>"}

Rules:
- When ambiguous, prefer the more specific category.
- If confidence < 0.7, set category to "general"."""
```

---

## 3. Failure Modes and Fixes

| Failure mode | Symptom | Fix |
|---|---|---|
| Ambiguous instruction | Model interprets differently per run | Add concrete success criteria, not just direction |
| Constraint at end | Model ignores constraint under long context | Move all constraints to the top of the prompt |
| Conflicting instructions | Model picks one inconsistently | Audit for contradictions; remove or prioritize explicitly |
| Missing refusal boundary | Model attempts harmful/out-of-scope tasks | Add explicit "Do not..." for each boundary case |
| Prompt injection risk | User input overrides system instructions | Never interpolate raw user input into system prompt |
| Stale examples | Examples contradict new rules | Keep examples in sync with constraint changes |
| Open-ended output scope | 500-word answers when 50 are needed | State "max X sentences/words/items" explicitly |

### Prompt injection defense
```python
# BAD: directly interpolating user input
system = f"You are an assistant. Context: {user_provided_text}"

# GOOD: separate user content from system instructions
messages = [
    {"role": "system", "content": "You are an assistant. Answer based on the provided context only."},
    {"role": "user", "content": f"Context:\n<context>{user_provided_text}</context>\n\nQuestion: {user_question}"},
]
```

---

## 4. Versioning and Experimentation

### Version scheme
```python
# Prompt version: MAJOR.MINOR.PATCH
# MAJOR: breaking schema change
# MINOR: new criteria or significant rewrite
# PATCH: wording fix, anchor clarification

PROMPT_VERSION = "2.1.0"

EXTRACTION_PROMPT = f"""...(prompt content)...
# Prompt version: {PROMPT_VERSION}
"""
```

### Experiment tracking
```python
import json
from datetime import datetime

def log_prompt_result(prompt_version: str, input_hash: str, result: dict, latency_ms: int) -> None:
    record = {
        "prompt_version": prompt_version,
        "input_hash": input_hash,
        "result": result,
        "latency_ms": latency_ms,
        "timestamp": datetime.utcnow().isoformat(),
    }
    # Write to evaluation store (BigQuery, S3, Postgres, etc.)
    print(json.dumps(record))
```

---

## 5. Evaluation Strategy

### Golden dataset structure
```json
[
  {
    "id": "test-001",
    "input": "...",
    "expected_output": {...},
    "test_type": "happy_path"
  },
  {
    "id": "test-002",
    "input": "...",
    "expected_output": null,
    "expected_refusal": true,
    "test_type": "adversarial"
  }
]
```

### Evaluation metrics

| Metric | What it measures | Target |
|---|---|---|
| Schema compliance | % outputs matching JSON Schema | 100% |
| Field accuracy | % of fields with correct value | >95% |
| Refusal rate | % of refusals on adversarial inputs | >90% |
| Hallucination rate | % of invented facts | <2% |
| Latency p95 | 95th percentile response time | Task-dependent |
| Token cost | Avg tokens per request | Track vs budget |

### Running evaluations
```python
from jsonschema import validate

def evaluate_batch(
    prompts: list[str],
    expected: list[dict],
    schema: dict,
) -> dict:
    results = []
    for prompt, exp in zip(prompts, expected):
        output = call_llm(prompt)
        try:
            validate(output, schema)
            schema_ok = True
        except Exception:
            schema_ok = False
        results.append({"schema_ok": schema_ok, "match": output == exp})

    return {
        "schema_compliance": sum(r["schema_ok"] for r in results) / len(results),
        "exact_match": sum(r["match"] for r in results) / len(results),
        "n": len(results),
    }
```
