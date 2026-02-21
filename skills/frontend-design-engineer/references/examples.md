# Frontend Design Examples

## Example 1: CSS Variables

```css
:root {
  --color-surface: #0b1324;
  --color-text: #f7f9ff;
  --space-4: 1rem;
}
```

## Example 2: Tokenized Button

```css
.button {
  background: var(--color-brand);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
}
```

## Example 3: Responsive Type

```css
h1 {
  font-size: clamp(1.8rem, 2vw + 1rem, 3rem);
}
```
