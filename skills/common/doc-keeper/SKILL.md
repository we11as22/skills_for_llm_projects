---
name: doc-keeper
description: Keeps project documentation alive, accurate, and noise-free. Maintains three living documents: README.md (project identity and quick orientation), ARCHITECTURE.md (key logic, decisions, invariants), and docs/changes/ (semantic change log — only what matters conceptually). Apply after every meaningful change to any of these. Always active on any project task.
---

# Doc Keeper

## Overview

Documentation rots silently. LLMs make changes and never update the docs. Users open a project weeks later and the README is stale, the architecture decisions are scattered across commit messages, and nobody knows why a key choice was made. This skill defines exactly which documents to maintain, what goes in each, and when to update them.

Three living documents. Each has a strict scope and format. Nothing outside scope goes in.

---

## The Three Documents

### Document 1 — `README.md` (Project Identity)

**Purpose:** Someone opens the repo for the first time. In 2 minutes they must understand what this project is, what problem it solves, and how to start using it. Nothing else.

**Update trigger:** Any change to the project's purpose, main interfaces, setup steps, or key usage patterns.

**What goes in:**
- What this project is (1–3 sentences, sharp and concrete)
- What problem it solves and for whom
- Quick start (exact commands from zero to running)
- Main entry points (key files, URLs, commands)
- Configuration overview (env vars, config file)
- Links to ARCHITECTURE.md and docs/changes/

**What does NOT go in:**
- Internal implementation details
- History of how it was built
- Lists of every function or class
- Opinions about technology choices (that goes in ARCHITECTURE.md)
- Debug notes, workarounds, "TODO: fix later"
- Version history (that goes in docs/changes/)

**README.md format:**
```markdown
# [Project Name]

[One sharp sentence: what it does and for whom.]

## What It Solves

[2–4 sentences: the problem, why it matters, who has it.]

## Quick Start

```bash
# Exact commands from zero to running
git clone ...
cd ...
cp .env.example .env   # edit X, Y, Z
make install
make run
```

## How It Works (Overview)

[3–6 sentences: the mental model. Input → process → output. No code.]

## Key Entry Points

| What | Where |
|------|-------|
| Main config | `config/settings.py` |
| API routes | `src/api/routes.py` |
| Worker entrypoint | `src/worker/main.py` |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | — | Postgres DSN |
| `REDIS_URL` | — | Redis DSN |

## Further Reading

- Architecture and key decisions → [ARCHITECTURE.md](ARCHITECTURE.md)
- What changed and why → [docs/changes/](docs/changes/)
```

---

### Document 2 — `ARCHITECTURE.md` (Logic and Decisions)

**Purpose:** Explains the non-obvious. Why was this approach chosen over the alternative? What are the invariants that must not be broken? What patterns does this codebase enforce?

A developer about to change core logic must read this first. An LLM working on this project must read this first.

**Update trigger:**
- A design decision is made (even informally — "we decided to use X instead of Y")
- A core invariant is added or changed
- A new pattern is introduced
- A trade-off is accepted that future maintainers need to know about
- A "why" question was asked and answered in chat — that answer goes here

**What goes in:**
- Architecture decisions with explicit rationale (ADR-lite format)
- Key invariants: things that MUST stay true
- Pattern library: recurring patterns enforced in this codebase
- Data flow: how information moves through the system (high level)
- External dependencies and why each was chosen
- Known constraints and their reasons

**What does NOT go in:**
- How-to instructions (those go in README)
- Full API documentation
- Code comments repeated in prose
- Things that are obvious from reading the code

**ARCHITECTURE.md format:**
```markdown
# Architecture

## System Overview

[Data flow diagram or description: what comes in, how it's processed, what goes out.]

## Key Decisions

### [Decision Title]
**Status:** active / superseded / under review
**Context:** [Why this decision needed to be made]
**Decision:** [What was decided]
**Rationale:** [Why this option over alternatives]
**Trade-offs:** [What we accept as a consequence]
**Alternatives considered:** [What was rejected and why]

---

## Invariants

Rules that MUST NOT be broken. If you are about to violate one, stop and discuss.

- **[Invariant name]:** [Statement of the rule] — *reason: [why this matters]*
- ...

## Patterns

Recurring patterns enforced across this codebase.

### [Pattern Name]
**When to use:** ...
**How to apply:** ...
**Example:** `path/to/example.py`

---

## Data Flow

[Diagram or step-by-step description of how data moves through the system.]

## External Dependencies

| Dependency | Why this one | Why not alternative |
|-----------|-------------|---------------------|
| PostgreSQL | ACID, jsonb | MySQL: weaker jsonb |

## Known Constraints

- [Constraint]: [Reason it exists]
```

---

### Document 3 — `docs/changes/<YYYY-MM-DD>_<slug>.md` (Semantic Change Log)

**Purpose:** A searchable archive of *what changed conceptually and why*. Not a commit log. Not a diff. The answer to: "Why does this work the way it does now, and when did it change?"

**Structure:** One file per meaningful change, named by date and slug. Files are never edited — only new files are added.

**Update trigger:**
- A design decision changes
- A key invariant is added, relaxed, or removed
- The architecture changes (new layer, removed service, new data flow)
- A significant refactor that changes how something works
- A bug was fixed in a way that revealed a design assumption — that assumption should be recorded
- A feature was added that requires new mental model

**What goes in each file:**
- What changed (concrete, one paragraph)
- Why it changed (reason, not just "user requested")
- What it replaces or supersedes
- What to watch out for going forward

**What does NOT go in:**
- Lists of files changed (that's in git)
- Formatting/style changes
- Dependency version bumps (unless they change behaviour)
- Bug fixes that don't reveal anything about the design
- "Refactored for clarity"

**`docs/changes/YYYY-MM-DD_slug.md` format:**
```markdown
# [Short title of what changed]

**Date:** YYYY-MM-DD
**Type:** decision / invariant / architecture / feature / constraint / removal

## What Changed

[1–3 paragraphs. Concrete. What is different now vs before.]

## Why

[The actual reason. Not "user asked for it" — what drove the need.]

## What This Replaces

[What was the previous approach, if any. "None" if new.]

## Watch Out For

[What can go wrong if you don't know this change happened. Skip if nothing.]

## Related

- ARCHITECTURE.md: [section name]
- Decision that triggered this: [link or description]
```

---

## When to Update — Decision Table

| Event | README | ARCHITECTURE | docs/changes/ |
|-------|--------|--------------|---------------|
| New feature added | If entry points change | If new pattern/decision | If it changes the mental model |
| Bug fix | No | Only if it revealed a design flaw | Only if design assumption changed |
| Refactor (same behaviour) | No | If pattern changes | No |
| Architecture decision made | No | Yes | Yes |
| New config/env variable | Yes (config table) | If non-obvious | No |
| External dependency added | If changes quick start | Yes (dependencies table) | Only if significant trade-off |
| Invariant added or changed | No | Yes | Yes |
| Project purpose shifts | Yes | Possibly | Yes |
| Breaking change to API/CLI | Yes | Yes | Yes |

---

## The Anti-Noise Principle

Every sentence in every document must pass this test:

> "If I deleted this sentence, would someone making changes to this project be missing something important?"

If the answer is no — delete it.

**Noise patterns to reject:**
- "This was implemented using standard Python best practices" → says nothing
- "As mentioned above…" → just say it again or don't
- "In the future we might want to…" → if it's not decided, it's a todo, not documentation
- Lists that repeat what the code already says clearly
- Section headers with no content
- Dates in the main body of README or ARCHITECTURE (dates go in docs/changes/)

---

## Initialisation Workflow

When starting documentation on a new or undocumented project:

1. **Read the codebase first.** At minimum: entry points, config, main data flows.
2. **Create README.md** — fill only what you can state confidently. Leave gaps rather than guess.
3. **Create ARCHITECTURE.md** — list only decisions and invariants you can infer from the code. Mark uncertainties as `[NEEDS CONFIRMATION]`.
4. **Create `docs/changes/` folder** — add one file for the initial documentation event.
5. **Ask the user to review** and fill gaps before publishing.

---

## Update Workflow (After Any Change)

1. Identify what changed (feature, decision, invariant, etc.)
2. Check the decision table above: which documents need updating?
3. For ARCHITECTURE.md: add or update the relevant section. If a decision is superseded, mark it `Status: superseded` and link to the new decision.
4. For docs/changes/: create a new file. Never edit existing change files.
5. For README.md: update only the sections affected. Do not rewrite sections that didn't change.
6. Re-read the updated section and apply the anti-noise test.

---

## Rules

- **Never** write documentation about what you are about to do. Write it after the change is done and verified.
- **Never** delete existing ARCHITECTURE.md decisions — mark them `Status: superseded`.
- **Never** put rationale in README. Rationale goes in ARCHITECTURE.md.
- **Never** put instructions in ARCHITECTURE.md. Instructions go in README.
- **Always** write change log entries in past tense ("was changed", "was replaced", "was removed").
- **Always** ask the user before marking an invariant as removed — invariants usually exist for a reason.

---

## Output Format

When updating documentation, produce:

```
DOC UPDATE
──────────
Files updated: [list]
README:        [section(s) changed, or "no change"]
ARCHITECTURE:  [section(s) changed or added, or "no change"]
docs/changes/: [new file name, or "no change"]
Anti-noise:    [confirm each added sentence passes the test]
```
