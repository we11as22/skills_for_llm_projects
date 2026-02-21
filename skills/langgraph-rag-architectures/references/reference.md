# LangGraph RAG Reference

## Table of Contents

1. Agentic RAG
2. Adaptive RAG
3. CRAG
4. Self-RAG
5. Local-model considerations

## 1. Agentic RAG

- Agent decides when/what to retrieve.
- Good for interactive multi-turn tasks.
- Risk: tool overuse; add tool budget limits.

## 2. Adaptive RAG

- Add query router node.
- Route to vectorstore for domain-specific queries.
- Route to web search for recency/open-world queries.

## 3. CRAG

- Add retrieval grader.
- If docs are weak, repair via web augmentation/re-retrieval.
- Re-run generation with improved context.

## 4. Self-RAG

- Add model-based critique for evidence and answer quality.
- Reject or revise weak answers.
- Use strict max-iteration controls.

## 5. Local-Model Considerations

- Quantize and benchmark model quality.
- Tune chunking for local embedding constraints.
- Use smaller prompt context with retrieval compression.
