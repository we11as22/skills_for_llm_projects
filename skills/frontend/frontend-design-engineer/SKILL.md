---
name: frontend-design-engineer
description: Design and implement frontend UI systems in code using design tokens, layout rules, typography systems, interaction states, accessibility, and responsive behavior. Use when translating visual design to production code, creating a design system foundation, generating CSS token layers, or improving visual consistency and UX quality.
---

# Frontend Design Engineer

## Overview

Turn product requirements into a coherent visual system directly in code: tokens, components, layout primitives, and interaction behavior. Focus on consistency, accessibility, and implementation speed.

## Workflow

1. Define design principles and visual direction.
2. Create token layers (color, spacing, typography, motion, radius, elevation).
3. Build layout primitives (stack, grid, shell, section).
4. Define component states (default, hover, focus, disabled, loading, error).
5. Encode responsive breakpoints and container behavior.
6. Validate contrast, keyboard navigation, and focus visibility.

## Quality Rules

- Prefer token-driven styles over hardcoded values.
- Keep spacing and type scales intentional and finite.
- Define motion for hierarchy, not decoration.
- Preserve design consistency across React/Vue/native HTML.

## Implementation Assets

- Use `scripts/generate_design_tokens.py` to convert JSON tokens into CSS variables and JS exports.
- Use `references/reference.md` for system design checklist.
- Use `references/examples.md` for token and component examples.
- Use `assets/layout-starter/` as minimal starter for responsive shell.

## Output Format

1. Visual direction summary
2. Token set and naming
3. Component/state mapping
4. Responsive and accessibility checklist
5. Code snippets and integration plan
