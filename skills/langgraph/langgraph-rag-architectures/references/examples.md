# LangGraph RAG Architecture Examples

## Example 1: Adaptive RAG (vectorstore or web search routing)

```python
from typing import TypedDict, Annotated, Literal
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class RAGState(TypedDict):
    query: str
    messages: Annotated[list[BaseMessage], add_messages]
    retrieved_docs: list[dict]
    generation: str
    route: str
    citations: list[str]

class QueryRoute(BaseModel):
    destination: Literal["vectorstore", "web_search"]

route_prompt = ChatPromptTemplate.from_messages([
    ("system", "Route to vectorstore (domain knowledge) or web_search (recent/general). Return JSON."),
    ("human", "{query}"),
])

def route_query(state: RAGState) -> RAGState:
    result = (route_prompt | llm.with_structured_output(QueryRoute)).invoke({"query": state["query"]})
    return {"route": result.destination}

def retrieve_from_vectorstore(state: RAGState) -> RAGState:
    # Replace with actual vectorstore retriever
    docs = [{"content": "Domain doc content...", "source": "internal-kb/doc1.md"}]
    return {"retrieved_docs": docs, "citations": [d["source"] for d in docs]}

def web_search(state: RAGState) -> RAGState:
    # Replace with Tavily/SerpAPI call
    results = [{"content": "Web result placeholder", "url": "https://example.com"}]
    return {"retrieved_docs": results, "citations": ["https://example.com"]}

def generate(state: RAGState) -> RAGState:
    context = "\n\n".join(d["content"] for d in state["retrieved_docs"])
    prompt = f"Answer based on context:\n\n{context}\n\nQuestion: {state['query']}"
    response = llm.invoke(prompt)
    return {"generation": response.content, "messages": [AIMessage(content=response.content)]}

def route_edge(state: RAGState) -> str:
    return state["route"]

builder = StateGraph(RAGState)
builder.add_node("route_query", route_query)
builder.add_node("vectorstore", retrieve_from_vectorstore)
builder.add_node("web_search", web_search)
builder.add_node("generate", generate)

builder.set_entry_point("route_query")
builder.add_conditional_edges(
    "route_query", route_edge,
    {"vectorstore": "vectorstore", "web_search": "web_search"}
)
builder.add_edge("vectorstore", "generate")
builder.add_edge("web_search", "generate")
builder.add_edge("generate", END)

adaptive_rag = builder.compile()
```

---

## Example 2: CRAG — Document Grading + Web Fallback

```python
from pydantic import BaseModel
from typing import Literal

class DocGrade(BaseModel):
    score: Literal["yes", "no"]

grade_prompt = ChatPromptTemplate.from_messages([
    ("system", "Grade document relevance to query. 'yes'=relevant, 'no'=not relevant. Return JSON."),
    ("human", "Query: {query}\n\nDoc: {doc}"),
])

def grade_documents(state: RAGState) -> RAGState:
    grader = grade_prompt | llm.with_structured_output(DocGrade)
    relevant = [
        doc for doc in state["retrieved_docs"]
        if grader.invoke({"query": state["query"], "doc": doc["content"]}).score == "yes"
    ]
    quality = "good" if len(relevant) >= 2 else "poor"
    return {
        "retrieved_docs": relevant or state["retrieved_docs"],  # fallback to all if none relevant
        "retrieval_quality": quality,
    }

def crag_edge(state: RAGState) -> str:
    # If retrieval is poor and we haven't exceeded budget, try web search
    if state.get("retrieval_quality") == "poor" and state.get("revision_count", 0) < 2:
        return "web_search"
    return "generate"
```

---

## Example 3: Self-RAG — Answer Grading Loop

```python
class AnswerGrade(BaseModel):
    grounded: bool    # answer supported by docs
    complete: bool    # answer fully addresses the query

answer_grade_prompt = ChatPromptTemplate.from_messages([
    ("system", "Is the answer grounded in the docs and complete? Return JSON."),
    ("human", "Query: {query}\n\nDocs: {docs}\n\nAnswer: {answer}"),
])

def grade_answer(state: dict) -> dict:
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
        "revision_count": state.get("revision_count", 0) + 1,
    }

def self_rag_edge(state: dict) -> str:
    if state["answer_quality"] == "good":
        return "END"
    if state.get("revision_count", 0) >= state.get("max_revisions", 3):
        return "END"   # emit best-effort answer after max retries
    return "generate"  # retry generation with same docs
```

---

## Example 4: Context Compression to Fit Token Budget

```python
def compress_context(docs: list[dict], max_chars: int = 8000) -> str:
    """Keep most relevant passages within token budget."""
    context_parts = []
    total = 0
    for doc in docs:
        text = doc["content"]
        if total + len(text) > max_chars:
            remaining = max_chars - total
            if remaining > 200:  # only add if meaningful chunk remains
                context_parts.append(text[:remaining])
            break
        context_parts.append(text)
        total += len(text)
    return "\n\n---\n\n".join(context_parts)

def generate_with_compression(state: dict) -> dict:
    context = compress_context(state["retrieved_docs"], max_chars=8000)
    prompt = f"Context:\n{context}\n\nQuestion: {state['query']}\n\nAnswer with citations:"
    response = llm.invoke(prompt)
    return {"generation": response.content, "messages": [AIMessage(content=response.content)]}
```
