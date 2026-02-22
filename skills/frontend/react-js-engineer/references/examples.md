# React Examples

## Example 1: Feature Hook

```tsx
export function useOrders() {
  return useQuery({ queryKey: ["orders"], queryFn: fetchOrders });
}
```

## Example 2: Error Boundary Usage

```tsx
<ErrorBoundary fallback={<OrdersFallback />}>
  <OrdersPage />
</ErrorBoundary>
```

## Example 3: Container + Presentational Split

- `OrdersPageContainer.tsx`: data fetching and mutation orchestration.
- `OrdersPageView.tsx`: stateless rendering from props.
