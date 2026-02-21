---
name: vue-js-engineer
description: Build and refactor Vue.js applications using Composition API, Pinia, routing patterns, async data handling, and testable component design. Use when creating Vue features, optimizing Vue performance, structuring Vue codebases, setting state management conventions, or scaffolding Vue modules.
---

# Vue JS Engineer

## Overview

Implement scalable Vue applications with predictable module boundaries, typed composables, and maintainable store design. Deliver Vue features with clear state flows and testability.

## Workflow

1. Define route-level boundaries and data dependencies.
2. Build feature modules around composables and focused components.
3. Keep API access inside service/composable layers.
4. Use Pinia only for shared cross-view state.
5. Add loading/error/empty UX states for every async path.
6. Cover critical flows with component + e2e tests.

## Architecture Rules

- Prefer Composition API with `<script setup>`.
- Keep composables pure where possible.
- Keep Pinia stores slim and explicit.
- Avoid hidden side effects in watchers.

## Implementation Assets

- Use `scripts/scaffold_vue_feature.py` for rapid module generation.
- Use `references/reference.md` for state and performance guidance.
- Use `references/examples.md` for composable and store examples.
- Use `assets/template-vue-app/` for bootstrapping.

## Output Format

1. Feature module design
2. Composable/store contracts
3. Rendering strategy
4. Testing and rollout checklist
