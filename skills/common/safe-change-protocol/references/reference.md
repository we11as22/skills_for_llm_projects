# Safe Change Protocol Reference

## Change Classification Quick-Reference

```
Is this a cosmetic change only (rename, format)?  → Verify syntax, proceed
Does it add new code without touching existing?    → Run existing tests, proceed
Does it change behaviour/logic/return values?      → STOP: describe change, ask user
Does it change a public interface or schema?       → STOP: offer variants, ask user
Does it remove code or endpoints?                  → STOP: grep usages, confirm explicitly
```

## Pre-Edit Checklist (mandatory)

- [ ] Read the file being changed
- [ ] Read files that import it
- [ ] Run current tests (know the baseline)
- [ ] State in plain language: old behaviour → new behaviour

## Post-Edit Checklist (mandatory)

- [ ] Syntax check passes
- [ ] All tests pass (not just new tests)
- [ ] Manual spot-check (run/call/render the changed path)
- [ ] No unintended removals (grep for deleted names)
- [ ] No new `any`, suppressed types, or disabled lint rules

## When to Offer Variants

Offer variants when the decision has genuine trade-offs and the user didn't specify which approach. Format:
- Option A / Option B (max 3 options)
- One sentence pros/cons each
- One sentence recommendation
- End with: "Which would you like?"

Never silently pick an architecture. Never silently pick a data model. Never silently pick an error strategy.

## Non-Negotiable Stops

| Trigger | Required action |
|---------|----------------|
| Changing return type | Ask user |
| Removing public function | Grep + confirm |
| DB schema migration | Show SQL, confirm |
| Touching file with no tests | Flag to user |
| 2+ valid interpretations of request | Ask for clarification |
