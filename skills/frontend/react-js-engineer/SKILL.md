---
name: react-js-engineer
description: Build and refactor React.js applications with scalable feature architecture, data fetching strategy, performance optimization, testing, and production delivery practices. Use when implementing React UI, designing state management, structuring components, improving render performance, setting up testing, or scaffolding React project modules.
---

# React JS Engineer

## Overview

Implement production-grade React projects using feature-first architecture, strict typing, predictable state, and test coverage. Generate consistent modules fast and enforce stable patterns.

## Workflow

1. Define user flows and screen states (idle, loading, success, error, empty).
2. Split code into feature modules (`src/features/<name>`).
3. Keep API contracts separate from presentational components.
4. Use memoization only for measured hotspots.
5. Add accessibility and keyboard navigation from the start.
6. Add test pyramid: unit, integration, and critical e2e flows.

## Architecture Rules

- Prefer TypeScript.
- Keep components small and composable.
- Place side effects in hooks/services, not UI components.
- Keep server state and client UI state separated.
- Prevent prop drilling with context only where stable.

## Performance Rules

- Use code-splitting for route bundles.
- Preload critical data on navigation where possible.
- Track Core Web Vitals and fix regressions before release.
- Avoid global state for local concerns.

## Implementation Assets

- Use `scripts/scaffold_react_feature.py` to generate a full feature module.
- Use `references/reference.md` for architecture and testing standards.
- Use `references/examples.md` for patterns (forms, tables, optimistic UI).
- Use `assets/template-vite-react/` as starter project baseline.

## Output Format

1. Feature architecture proposal
2. Data/state strategy
3. Component tree and contracts
4. Testing plan
5. Delivery checklist
