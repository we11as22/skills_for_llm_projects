# Doc Keeper Reference

## Document Scope at a Glance

| Question | Document |
|----------|----------|
| "What is this project and how do I start?" | README.md |
| "Why is it built this way?" | ARCHITECTURE.md |
| "What changed and when?" | docs/changes/YYYY-MM-DD_slug.md |
| "What must never be broken?" | ARCHITECTURE.md → Invariants |
| "What are the trade-offs we accepted?" | ARCHITECTURE.md → Key Decisions |

## Anti-Noise Test

Before writing any sentence, ask:
> "If I deleted this, would a developer making changes miss something important?"

No → delete it.

## Change Log Naming Convention

```
docs/changes/
  2025-01-15_initial-architecture.md
  2025-02-03_switch-to-async-db.md
  2025-02-20_add-rate-limiting.md
  2025-03-01_remove-legacy-sync-api.md
```

- Date: `YYYY-MM-DD`
- Slug: lowercase, hyphen-separated, max 5 words, describes the change not the feature
- Never edit existing files — only add new ones

## Decision Status Values

| Status | Meaning |
|--------|---------|
| `active` | In use now |
| `superseded` | Replaced by a newer decision (link it) |
| `under review` | Being discussed, not finalized |
| `rejected` | Considered but not adopted (keep for history) |

## What Belongs Where — Edge Cases

| Situation | Where it goes |
|-----------|---------------|
| "We use Redis for caching" | ARCHITECTURE.md (dependency + reason) |
| "Set REDIS_URL in .env" | README.md (config table) |
| "We switched from in-memory to Redis cache" | docs/changes/ |
| "Cache keys expire in 5 minutes" | ARCHITECTURE.md (invariant or constraint) |
| New CLI flag added | README.md (entry points / quick start) |
| Why we chose this CLI structure | ARCHITECTURE.md (decision) |

## README Sections — Mandatory vs Optional

| Section | Mandatory |
|---------|-----------|
| What It Does (1–3 sentences) | Yes |
| What Problem It Solves | Yes |
| Quick Start | Yes |
| Key Entry Points | Yes |
| Configuration | Yes if config exists |
| Architecture link | Yes |
| Change log link | Yes |
| Contributing | Optional |
| License | Optional |
| Detailed API docs | No — separate file |

## ARCHITECTURE.md — Mandatory vs Optional

| Section | Mandatory |
|---------|-----------|
| System Overview | Yes |
| Key Decisions | Yes (at least one) |
| Invariants | Yes if any exist |
| Patterns | Yes if codebase enforces any |
| Data Flow | Yes |
| External Dependencies | Yes if non-trivial |
| Known Constraints | Optional |
