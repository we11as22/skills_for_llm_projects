# Agent Discipline Reference

## The Most Common LLM Failures and Their Counters

| # | Failure | Counter |
|---|---------|---------|
| 1 | Invents file path without checking | `find . -name X` first |
| 2 | Confidently wrong answer | "I believe X — run Y to verify" |
| 3 | Adds unrequested scope | Mention extras, don't implement them |
| 4 | Returns stubs as solutions | Full runnable code or explain what's missing |
| 5 | Changes logic silently | Stop, describe change, ask |
| 6 | Repeats broken approach | After 2 failures: ask for more context |
| 7 | Skips verification | Run syntax check + tests after every edit |
| 8 | Assumes service/port state | Check with `nc`/`ss`/`curl` |
| 9 | Loses context in long session | Checkpoint summary at 10+ turns |
| 10 | Picks one interpretation silently | List interpretations, ask which one |
| 11 | Band-aid fix (`except: pass`, fallback default) | State root cause, fix at origin |
| 12 | Doesn't understand project flow before fixing | Read entry point → data path → broken point |
| 13 | Dumps code into wrong/bloated file | Check structure, split at 300 lines |
| 14 | Feature half-implemented | Full best-practices implementation, first pass |
| 15 | Copies bad patterns from existing code | Implement correctly, offer to harmonise |

## Fix Quality Checklist

Before declaring a fix done:
- [ ] Root cause stated in one sentence
- [ ] Fix touches the origin of the problem, not just the symptom
- [ ] No `except: pass`, no silent fallbacks that hide errors
- [ ] Original failing execution path re-traced — fix interrupts it at the root
- [ ] Failing case re-verified explicitly (not just "error gone")

## File Structure Decision Table

| Situation | Action |
|-----------|--------|
| File > 300 lines | Warning: consider splitting |
| File > 500 lines | Mandatory split |
| File does 2+ unrelated things | Split by responsibility |
| New code has no clear home | Find right place or propose new structure |
| Function only used in one module | Keep it in that module, not utils |
| utils.py > 100 lines | Split by domain |

## Full Implementation Checklist

New code must have (when applicable):
- [ ] Error handling at every failure point (not just the happy path)
- [ ] Input validation at all external boundaries
- [ ] Type annotations (if project uses them)
- [ ] Logging at service boundaries
- [ ] Timeout on every external call
- [ ] Idempotency on any state-mutating operation
- [ ] Explicit error types, not bare `Exception`

## When to Stop and Ask — Decision Tree

```
Is the request ambiguous?         → Yes: list interpretations, ask
Will you touch >5 files?          → Yes: state plan, ask for approval
Is this a destructive operation?  → Yes: show command/SQL, ask
Are you unsure about a dep version? → Yes: ask or check package registry
Have you failed twice at this?    → Yes: stop, ask for more context
Is a risk present (data, perf, security)? → Yes: surface it before proceeding
```

## Scope Boundary Test

For any piece of code you are about to write or change, ask:

1. Did the user ask for this?
2. Is it strictly necessary to make the requested change work?
3. Does the existing codebase consistently do this everywhere?

If all three are NO → don't add it.  
If you think it should be added → mention it, don't add silently.
