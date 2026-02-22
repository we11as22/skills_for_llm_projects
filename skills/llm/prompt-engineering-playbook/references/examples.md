# Prompt Engineering Examples

## Before

"Analyze this and tell me everything important."

## After

"Extract the top 5 risks from the input text. Return strict JSON array with fields: `risk`, `impact`, `evidence_quote`, `confidence` (0-1). Do not output any text outside JSON."

## Structured System Prompt Skeleton

```text
You are a domain analyst.
Follow all constraints strictly.
If required field is missing, return null and add `missing_fields` list.
```

## Evaluation Row Example

- input_id: `doc_14`
- expected: 5 risks
- observed: 4 risks
- issue: missing legal risk
