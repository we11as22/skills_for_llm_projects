# Vue Examples

## Example 1: Composable

```ts
export function useOrders() {
  const orders = ref([]);
  const isLoading = ref(false);
  return { orders, isLoading };
}
```

## Example 2: Pinia Store

```ts
export const useSessionStore = defineStore("session", {
  state: () => ({ token: null as string | null }),
});
```

## Example 3: Async Component

```ts
const HeavyChart = defineAsyncComponent(() => import("./HeavyChart.vue"));
```
