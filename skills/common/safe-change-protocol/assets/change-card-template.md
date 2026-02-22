# Change Card Template

Use this for every non-cosmetic change.

```
CHANGE CARD
───────────
What:    
Why:     
Class:   cosmetic / additive / behavioural / interface / removal
Affects: 
Checked: syntax [ ]  tests [ ]  side-effects [ ]  types [ ]
Risk:    low / medium / high — 
```

## Class Definitions

| Class | Trigger |
|-------|---------|
| cosmetic | Format, rename (no callers affected), comment only |
| additive | New function/file/route, zero existing code changed |
| behavioural | Logic changes, different output for same input |
| interface | API shape, DB schema, event contract, config key names |
| removal | Deleted function, endpoint, field, file |
