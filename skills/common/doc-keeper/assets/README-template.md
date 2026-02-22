# [Project Name]

[One sharp sentence: what it does and for whom.]

## What It Solves

[2–4 sentences: the problem, why it matters, who has it.]

## Quick Start

```bash
git clone <URL>
cd <project>
cp .env.example .env   # Required: set DATABASE_URL, API_KEY
make install
make run
```

## How It Works (Overview)

[3–6 sentences: the mental model. Input → processing → output. No code details.]

## Key Entry Points

| What | Where |
|------|-------|
| Main entrypoint | `src/main.py` |
| API routes | `src/api/routes.py` |
| Configuration | `config/settings.py` |

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL DSN |
| `DEBUG` | No | `false` | Enable debug logging |

## Further Reading

- Architecture and key decisions → [ARCHITECTURE.md](ARCHITECTURE.md)
- What changed and why → [docs/changes/](docs/changes/)
