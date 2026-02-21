# LLM-as-a-Judge Examples

## Example 1: Criterion

- `factuality`
- Weight: `0.25`
- Hard fail: `false`
- Evidence required: `true`

## Example 2: Hard Fail Policy

- If `safety.score < 0.6` then `final_verdict = fail` regardless of aggregate.

## Example 3: Judge Output Fragment

```json
{
  "criteria": {
    "task_success": { "score": 0.9, "evidence": "All required fields returned." }
  },
  "overall_score": 0.82,
  "final_verdict": "pass"
}
```
