# LangGraph Playbook Examples

## Example 1: Architecture Choice

Requirement:

- Need support chatbot with billing + tech specialists and escalation control.

Choice:

- Supervisor topology with specialist agents and escalation node.

## Example 2: RAG Upgrade Path

Requirement:

- Existing RAG fails on ambiguous queries.

Choice:

1. Add adaptive route (vectorstore vs web search).
2. Add corrective loop for low-confidence retrieval.
3. Add self-reflection grade before final answer.

## Example 3: Planning Agent

Requirement:

- Complex tasks with dependent steps and tool calls.

Choice:

- ReWOO/LLM compiler style planner -> executor workers -> solver/joiner.
