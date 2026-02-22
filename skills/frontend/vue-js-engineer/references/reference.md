# Vue Reference

## Table of Contents

1. Project structure
2. State and composables
3. Async data and UX
4. Performance
5. Testing

## 1. Project Structure

```text
src/features/payments/
  api.ts
  composables/
  components/
  stores/
```

## 2. State and Composables

- Use composables for reusable async flows.
- Use Pinia for shared state across screens.
- Keep store actions deterministic and testable.

## 3. Async Data and UX

- Track `isLoading`, `error`, `data` explicitly.
- Cancel stale requests on route change.
- Centralize API error mapping.

## 4. Performance

- Split bundles by route.
- Use `defineAsyncComponent` for heavy UI.
- Avoid deep watchers over large objects.

## 5. Testing

- Unit test composables.
- Component tests for interaction.
- Playwright/Cypress for critical journeys.
