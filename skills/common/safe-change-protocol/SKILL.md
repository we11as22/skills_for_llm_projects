---
name: safe-change-protocol
description: Mandatory discipline for making any code or config change. Apply before every edit: verify nothing is broken, surface side-effects, ask the user when logic changes, offer multiple implementation variants for non-trivial decisions. Always active — does not matter what stack or task.
disable-model-invocation: false
---

# Safe Change Protocol

## Overview

Every change carries risk. LLMs tend to make changes too confidently, silently alter logic, miss side-effects, and not ask when they should. This skill defines the minimal discipline that must be applied to every edit, regardless of size or context.

---

## Phase 1: Before Touching Anything

1. **Read the full context first.** Never edit a file you haven't read. Read at minimum:
   - The file being changed
   - Any files that import or call the changed code
   - Related tests

2. **Map the blast radius.** Ask yourself:
   - What calls this function/component/config?
   - What does it return/emit/write — and who reads that?
   - Are there tests covering this path? Run them before touching anything.

3. **State your understanding** before coding:
   > "I'm going to change X. This affects Y and Z. The existing behaviour is A. The new behaviour will be B."

---

## Phase 2: Classifying the Change

Classify the change before making it. The class determines how much caution is needed.

| Class | Description | Required action |
|-------|-------------|-----------------|
| **Cosmetic** | Rename, formatting, comment | Verify syntax only |
| **Additive** | New function/file, no existing code modified | Run existing tests |
| **Behavioural** | Logic changes, return values change, side-effects change | **Stop — ask user first** |
| **Interface** | Public API, schema, event contract changes | **Stop — propose variants** |
| **Removal** | Deleting code, config, endpoints | **Stop — confirm explicitly** |

### Rule: behavioural and interface changes always require explicit user confirmation.

When you detect a behavioural or interface change:
1. Stop before writing code.
2. Describe **exactly** what the old behaviour is and what the new behaviour will be.
3. Ask the user to confirm, or offer 2–3 implementation variants (see Phase 4).

---

## Phase 3: Making the Change

### Surgical edits
- Change **only** what is necessary for the stated goal. Do not clean up unrelated code in the same pass.
- One logical change per edit block. If you need to fix two independent things, do them in sequence with a check between.

### Preserve invariants
- If a function had a contract (e.g. "always returns a non-null list"), verify the new code preserves it.
- If a DB schema changes, check all queries that read/write that table.
- If an API response shape changes, check all consumers.

### Leave a clear trail
- Briefly note **what** changed and **why** (in commit message or a comment when non-obvious).
- Do not note **how** it changed — the diff shows that.

---

## Phase 4: Offering Variants (Non-Trivial Decisions)

When a task has multiple valid approaches, **do not silently pick one**. Present variants:

```
Option A — [Name]
  How it works: ...
  Pros: ...
  Cons: ...
  Best when: ...

Option B — [Name]
  How it works: ...
  Pros: ...
  Cons: ...
  Best when: ...

My recommendation: Option A, because ... [one sentence].
Which would you like to proceed with?
```

When to offer variants:
- State management strategy (local vs global vs server-state)
- Database schema design choices
- API design (REST vs RPC vs event-driven)
- Error handling approach (retry vs fail-fast vs circuit breaker)
- Any refactor that has more than one non-equivalent shape

---

## Phase 5: After the Change — Verification Checklist

Run this checklist after **every** non-cosmetic change:

- [ ] **Syntax**: file parses without error (`python -m py_compile`, `tsc --noEmit`, `eslint`, etc.)
- [ ] **Existing tests pass**: run the test suite for the affected module
- [ ] **Manual spot-check**: exercise the changed path at least once (run it, open it, call it)
- [ ] **Side-effects checked**: files/modules that import the changed code still work
- [ ] **No unintended removals**: grep for usages of anything you deleted or renamed
- [ ] **Types consistent**: if typed, no new `any` or suppressed errors introduced
- [ ] **Behaviour preserved** (if not intentionally changed): old inputs still produce old outputs

If any check fails: **stop, revert, diagnose, then retry** — do not layer more changes on top of broken code.

---

## Non-Negotiable Rules

- **Never** modify logic and style in the same edit. Separate them.
- **Never** assume a refactor is "purely mechanical" without checking callers.
- **Never** delete code without grepping for all usages first.
- **Never** change a public API, schema, or contract without asking the user explicitly.
- **Never** run a migration, destructive query, or `DROP` without showing the exact statement first and asking for confirmation.
- **Always** run tests before declaring a change done. "I think it works" is not verification.
- **Always** ask when you are not 100% sure what the user wants. Clarifying questions are cheaper than wrong implementations.

---

## Red Flags — Stop and Ask the User

If any of these are true, stop and surface it before continuing:

- The change would alter a return type, response shape, or emitted event
- The change removes or renames a public function/class/endpoint
- The change would require updating >3 files you haven't read
- The change touches a file with no tests and non-trivial logic
- You are not sure which of two interpretations of the request is correct
- The existing code has a comment like "# DO NOT CHANGE" or "# legacy — keep"
- You found a bug adjacent to the change that wasn't mentioned by the user

---

## Output Format

For every non-trivial change, produce a brief change card:

```
CHANGE CARD
───────────
What:    [one line description of what changes]
Why:     [one line reason]
Class:   [cosmetic / additive / behavioural / interface / removal]
Affects: [list of files/modules with changes]
Checked: syntax ✓  tests ✓  side-effects ✓  types ✓
Risk:    [low / medium / high — one line explanation]
```
