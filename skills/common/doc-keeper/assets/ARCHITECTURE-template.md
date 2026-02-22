# Architecture

## System Overview

[Describe data flow: what comes in, how it's processed, what goes out. 4–8 sentences or a simple diagram.]

```
[Input] → [Component A] → [Component B] → [Output]
                              ↓
                         [Storage]
```

---

## Key Decisions

### [Decision Title]

**Status:** active
**Context:** [Why this decision needed to be made — what problem or trade-off prompted it]
**Decision:** [What was decided, in one clear sentence]
**Rationale:** [Why this option over the alternatives]
**Trade-offs:** [What is accepted as a consequence — costs, limitations]
**Alternatives considered:** [What was rejected and the one-line reason why]

---

## Invariants

Rules that MUST NOT be broken. If a change would violate one, stop and discuss first.

- **[Invariant name]:** [Statement] — *reason: [why this matters]*
- **[Invariant name]:** [Statement] — *reason: [why this matters]*

---

## Patterns

### [Pattern Name]

**When to use:** [Situations where this pattern applies]
**How to apply:** [Concrete steps or structure]
**Canonical example:** [`path/to/example.py`](path/to/example.py)

---

## Data Flow

[Step-by-step or diagram showing how data moves through the system end-to-end.]

1. Request arrives at [entry point]
2. Validated by [validator]
3. Processed by [core logic]
4. Persisted to [storage]
5. Response returned as [format]

---

## External Dependencies

| Dependency | Version | Why this one | Why not [alternative] |
|-----------|---------|-------------|----------------------|
| PostgreSQL | 15+ | ACID + jsonb | MySQL: weaker jsonb support |
| Redis | 7+ | Fast pub/sub | RabbitMQ: heavier for this use case |

---

## Known Constraints

- **[Constraint]:** [What it is and why it exists]
- **[Constraint]:** [What it is and why it exists]
