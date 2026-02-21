# Multi-Agent Examples

## Example 1: Collaboration

- `researcher` and `writer` exchange until done.
- Stop when writer emits `task_status=done`.

## Example 2: Supervisor

- Supervisor routes requests to `math`, `web`, `code` agents.
- Supervisor validates and merges responses.

## Example 3: Hierarchical

- Top supervisor routes to `support_team` and `analytics_team`.
- Each team has local supervisor + specialists.
