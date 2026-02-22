# LangGraph RAG Architectures Reference

## Table of Contents

1. Architecture Selection Guide
2. RAG State Schema
3. Agentic RAG — tool-using retrieval agent
4. Adaptive RAG — query routing
5. CRAG — corrective retrieval
6. Self-RAG — self-critique loops
7. Retrieval Grading
8. Local Model Considerations
9. Evaluation Hooks
10. Anti-Patterns

---

## 1. Architecture Selection Guide

| Architecture | Query type | Retrieval quality | Use when |
|---|---|---|---|
| Agentic RAG | Multi-turn, interactive | Varies | Agent decides when/what to retrieve |
| Adaptive RAG | Single-turn, routable | Unknown | Need to pick best source per query |
| CRAG | Single-turn | Often low | Source quality unpredictable, needs repair |
| Self-RAG | Single-turn | Varies | Model must grade its own output before returning |

Start with **Adaptive RAG** for most production use cases. Add **CRAG** or **Self-RAG** when retrieval quality is consistently problematic.

---

## 2. RAG State Schema

```python
from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class RAGState(TypedDict):
    # Input
    query: str
    messages: Annotated[list[BaseMessage], add_messages]

    # Retrieval
    retrieved_docs: list[dict]          # {"content": str, "source": str, "score": float}
    doc_relevance_scores: list[float]   # per-doc grader output
    web_results: list[dict]             # {"content": str, "url": str}

    # Generation
    generation: str                     # current draft answer
    citations: list[str]                # source URLs/doc IDs used

    # Control
    revision_count: int                 # corrective loop counter
    max_revisions: int                  # hard cap (default: 3)
    retrieval_quality: str              # "good" | "poor" | "needs_web"
    answer_quality: str                 # "good" | "hallucinated" | "incomplete"
    route: str                          # "vectorstore" | "web_search" | "generate"
```

---

## 3. Agentic RAG

### Pattern
The agent has retrieval as a tool and decides autonomously when to call it.

```python
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

@tool
def retrieve_documents(query: str) -> str:
    """Retrieve relevant documents from the knowledge base."""
    docs = vectorstore.similarity_search(query, k=4)
    return "\n\n".join(f"[{d.metadata.get('source','?')}]\n{d.page_content}" for d in docs)

@tool
def web_search(query: str) -> str:
    """Search the web for recent information."""
    # Use Tavily, Bing, or SerpAPI
    ...

# Tool budget guard: limit tool calls to prevent overuse
tools = [retrieve_documents, web_search]
agent = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier="You are a research assistant. Use tools to find information. "
                   "Cite your sources. Do not call tools more than 5 times total.",
)
```

### Key rule: tool budget
```python
# Track tool call count in state
if tool_call_count >= MAX_TOOL_CALLS:
    return {"generation": "Tool budget exceeded. Partial answer: ...", "answer_quality": "incomplete"}
```

---

## 4. Adaptive RAG — Query Routing

### Query classifier
```python
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from typing import Literal

class QueryRoute(BaseModel):
    destination: Literal["vectorstore", "web_search"]
    reason: str

route_prompt = ChatPromptTemplate.from_messages([
    ("system", """Route the user query to the right retrieval source.
- vectorstore: for domain-specific, proprietary, or historical knowledge
- web_search: for recent events, current data, or general world knowledge
Return JSON with destination and reason."""),
    ("human", "{query}"),
])

def route_query(state: RAGState) -> RAGState:
    result = route_prompt | llm.with_structured_output(QueryRoute)
    route = result.invoke({"query": state["query"]})
    return {"route": route.destination}

def routing_edge(state: RAGState) -> str:
    return state["route"]  # "vectorstore" or "web_search"
```

---

## 5. CRAG — Corrective Retrieval

### Retrieval grader node
```python
from pydantic import BaseModel

class RelevanceGrade(BaseModel):
    score: Literal["yes", "no"]
    reason: str

grade_prompt = ChatPromptTemplate.from_messages([
    ("system", """Grade whether this document is relevant to the query.
Score 'yes' only if the document contains information useful for answering the query.
Return JSON."""),
    ("human", "Query: {query}\n\nDocument: {document}"),
])

def grade_documents(state: RAGState) -> RAGState:
    grader = grade_prompt | llm.with_structured_output(RelevanceGrade)
    scores = []
    for doc in state["retrieved_docs"]:
        result = grader.invoke({"query": state["query"], "document": doc["content"]})
        scores.append(1.0 if result.score == "yes" else 0.0)

    avg_score = sum(scores) / max(len(scores), 1)
    quality = "good" if avg_score >= 0.5 else "poor"
    return {
        "doc_relevance_scores": scores,
        "retrieval_quality": quality,
    }

def crag_routing(state: RAGState) -> str:
    if state["retrieval_quality"] == "poor":
        if state["revision_count"] >= state["max_revisions"]:
            return "generate"  # proceed with what we have
        return "web_search"    # repair via web
    return "generate"
```

---

## 6. Self-RAG — Answer Critique Loop

### Answer grader node
```python
class AnswerGrade(BaseModel):
    grounded: bool        # is answer supported by retrieved docs?
    complete: bool        # does it fully answer the query?
    needs_revision: bool  # should we revise?
    critique: str         # what's wrong (if anything)

answer_grade_prompt = ChatPromptTemplate.from_messages([
    ("system", """Evaluate this answer against the source documents and the original query.
- grounded: Is every claim traceable to the provided documents?
- complete: Does the answer fully address the query?
- needs_revision: Should the answer be revised?
Return JSON."""),
    ("human", "Query: {query}\n\nDocuments: {docs}\n\nAnswer: {answer}"),
])

def grade_answer(state: RAGState) -> RAGState:
    grader = answer_grade_prompt | llm.with_structured_output(AnswerGrade)
    docs_text = "\n\n".join(d["content"] for d in state["retrieved_docs"])
    result = grader.invoke({
        "query": state["query"],
        "docs": docs_text,
        "answer": state["generation"],
    })
    quality = "good" if (result.grounded and result.complete) else "hallucinated"
    return {
        "answer_quality": quality,
        "revision_count": state["revision_count"] + 1,
    }

def self_rag_routing(state: RAGState) -> str:
    if state["answer_quality"] == "good":
        return "END"
    if state["revision_count"] >= state["max_revisions"]:
        return "END"  # emit best effort answer
    return "generate"  # retry generation
```

---

## 7. Retrieval Grading — Best Practices

| Practice | Why |
|---|---|
| Score each doc independently | Avoid one bad doc killing the whole batch |
| Use threshold (≥0.5 good docs) not all-or-nothing | More robust to mixed batches |
| Store scores in state | Enable downstream decisions (web search, revision) |
| Separate retrieval confidence from answer confidence | They measure different things |
| Preserve source URLs and doc IDs | Citations must be traceable |

### Context compression before generation
```python
def compress_context(docs: list[dict], query: str, max_tokens: int = 3000) -> str:
    """Keep only the most relevant passages to fit context window."""
    from langchain.retrievers.document_compressors import LLMChainExtractor
    # Or simple truncation:
    combined = "\n\n".join(d["content"] for d in docs)
    return combined[:max_tokens * 4]  # rough char estimate
```

---

## 8. Local Model Considerations

When using Ollama, LMStudio, or vLLM:

- **Chunking**: use smaller chunks (512 tokens max) for local embedding models.
- **Context window**: limit retrieved context to fit local model's context (often 4k-8k tokens).
- **Quantization**: test Q4_K_M vs Q8_0 — grading prompts need more precision.
- **Embedding model mismatch**: always use the same embedding model for indexing and retrieval.
- **Temperature**: set temperature=0 for grader and router nodes; non-zero only for generation.

```python
from langchain_ollama import ChatOllama, OllamaEmbeddings

llm = ChatOllama(model="llama3.1:8b", temperature=0)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
```

---

## 9. Evaluation Hooks

### Core RAG metrics

| Metric | What it measures | Target |
|---|---|---|
| Retrieval recall | % of relevant docs retrieved | >80% |
| Answer faithfulness | Claims grounded in retrieved docs | >90% |
| Answer relevance | Answer addresses the query | >85% |
| Latency (p95) | End-to-end response time | <5s |
| Correction rate | % of queries needing web fallback | <30% |
| Revision rate | % of answers needing self-revision | <20% |

---

## 10. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| No stop condition on corrective loop | Infinite loop in production | Add `max_revisions` hard cap |
| Web search without sanitization | Prompt injection via web content | Sanitize extracted text before injecting |
| Dropping source URLs | Unverifiable citations | Always carry doc IDs in state |
| Same model for generation and grading | Self-validation bias | Use separate model or prompt strategy for graders |
| Retrieving too many docs | Context bloat, worse generation | Retrieve 3-5 docs, compress before generation |
| Retrieval quality = generation quality | They're different dimensions | Separate grader nodes for retrieval and answer |
