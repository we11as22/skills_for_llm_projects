# RAG Architecture Examples

## Example 1: Adaptive Route

- Router decides: `vectorstore` vs `web_search`.
- Unified evidence schema after both branches.

## Example 2: CRAG Loop

1. Retrieve docs.
2. Grade relevance.
3. If low score, run corrective retrieval.
4. Generate answer.

## Example 3: Self-RAG Validation

- Generate answer draft.
- Run self-grader node for factual support.
- If unsupported, re-retrieve and regenerate.
