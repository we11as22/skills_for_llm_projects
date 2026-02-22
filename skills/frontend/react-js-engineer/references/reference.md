# React Reference

## Table of Contents

1. Feature architecture
2. State strategy
3. Data fetching
4. Accessibility
5. Testing

## 1. Feature Architecture

- Organize by domain feature, not by technical type only.
- Typical structure:

```text
src/features/orders/
  api.ts
  model.ts
  hooks.ts
  components/
  __tests__/
```

## 2. State Strategy

- UI-only state: component or local context.
- Server state: TanStack Query/RTK Query.
- Global app state: minimal, explicit ownership.

## 3. Data Fetching

- Centralize API client with interceptors and error mapping.
- Keep retry policy explicit by endpoint criticality.
- Use optimistic updates for low-risk interactions.

## 4. Accessibility

- Use semantic HTML first.
- Preserve focus on modal open/close.
- Add keyboard equivalents for all pointer interactions.

## 5. Testing

- Unit: pure helpers and reducers.
- Integration: user interactions and API boundaries.
- E2E: critical flows only (auth, checkout, submission).
