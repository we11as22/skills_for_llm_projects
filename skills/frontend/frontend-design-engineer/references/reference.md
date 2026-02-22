# Frontend Design Reference

## Table of Contents

1. Token architecture
2. Typography and spacing
3. Component state model
4. Accessibility checks
5. Responsive strategy

## 1. Token Architecture

- Base tokens: raw values (e.g., `gray-100`, `space-4`).
- Semantic tokens: usage meaning (e.g., `surface-primary`, `text-muted`).
- Component tokens: scoped overrides when needed.

## 2. Typography and Spacing

- Use a modular scale.
- Limit font weights to 3-4 practical levels.
- Define line-height as system tokens.

## 3. Component State Model

Define at minimum:

- default
- hover
- focus-visible
- active
- disabled
- loading
- error

## 4. Accessibility Checks

- WCAG contrast for text and controls.
- Keyboard-only traversal.
- Visible focus ring.
- ARIA for custom controls.

## 5. Responsive Strategy

- Mobile-first breakpoints.
- Fluid container widths.
- Clamp-based typography for smooth scaling.
