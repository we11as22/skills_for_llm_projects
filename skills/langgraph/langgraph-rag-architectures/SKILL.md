---
name: langgraph-rag-architectures
description: Design and implement LangGraph RAG systems across agentic, adaptive, corrective (CRAG), and self-RAG architectures including local model variants. Use when retrieval quality is variable, when routing between vectorstore and web search is needed, or when answer quality must be self-graded before final response.
---

# LangGraph RAG Architectures

## Overview

Build robust RAG graphs using tutorial-derived patterns: Agentic RAG, Adaptive RAG, CRAG, and Self-RAG (cloud and local variants). Optimize routing, retrieval quality control, and generation confidence.

## Architecture Selection

- Agentic RAG: tool-using retrieval agent for interactive tasks.
- Adaptive RAG: route query to best source (index vs web).
- CRAG: detect low-quality retrieval and repair context.
- Self-RAG: model grades evidence and answer before returning output.

## Workflow

1. Define domain corpus and freshness requirements.
2. Implement retrieval + grading nodes.
3. Implement generator with context grounding checks.
4. Add corrective loop for weak evidence.
5. Add local-model branch if offline/on-prem needed.
6. Add evaluation harness (faithfulness, recall, latency, cost).

## Core Rules

- Separate retrieval confidence from final answer confidence.
- Keep web search behind policy and sanitization checks.
- Preserve citations/doc IDs in graph state.
- Add stop conditions for corrective loops.

## Included Resources

- `references/reference.md`: architecture-specific guidance.
- `references/examples.md`: pattern snippets for adaptive/CRAG/self-RAG.
- `scripts/scaffold_rag_graphs.py`: generates starter graph code for key RAG variants.
- `assets/rag-state-schema.json`: strict state contract.

## Output Format

1. Chosen RAG architecture and rationale
2. Graph nodes and transitions
3. Retrieval and grading strategy
4. Safety and failure handling
5. Evaluation plan and thresholds
