---
name: ui-ux-pro-max
description: "UI/UX design intelligence for frontend. 50+ styles, 21 palettes, 50 font pairings, 20 charts, 9 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Use when designing or implementing UI, landing pages, dashboards, choosing palettes/typography, or reviewing UX. Includes BM25 search and design-system generator (scripts + CSV data)."
---

# UI/UX Pro Max

Design intelligence for web and mobile: styles, palettes, font pairings, UX guidelines, chart types, and stack-specific rules. Use the scripts in this skill to search by domain and generate design systems.

## Goal

Give the agent a single, searchable source of UI/UX rules (accessibility, touch, performance, layout, typography, animation, style, charts) and stack-specific guidance so it can propose consistent, accessible frontends and design systems.

## When to use

- User asks to design, build, create, implement, review, fix, or improve UI/UX.
- Choosing color palettes, typography, or styles (glassmorphism, minimalism, dark mode, etc.).
- Building landing pages, dashboards, admin panels, e-commerce, SaaS, portfolio, blog, or mobile UI.
- Need stack-specific guidance (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui).
- Implementing accessibility, animations, layout, or responsive behavior.

## Workflow

1. **Analyze request**: Product type, style keywords, industry, stack (default `html-tailwind`).
2. **Generate design system (recommended first step)**: From the **skill root directory** run:
   ```bash
   python3 scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
   ```
   Use `--persist` to write `design-system/MASTER.md` and optionally `--page "pagename"` for page overrides.
3. **Optional domain searches**: For more detail use `--domain <domain>` (e.g. `style`, `chart`, `ux`, `typography`, `landing`, `color`, `product`, `web`, `react`).
4. **Stack guidelines**: Use `--stack <stack>` for implementation rules (e.g. `--stack html-tailwind` or `react`, `nextjs`, `vue`, `svelte`, `shadcn`, etc.).
5. Apply the rules and checklist from this skill and from `references/reference.md` before delivering UI code.

## Rule priorities (quick reference)

| Priority | Category            | Domain      |
|----------|---------------------|-------------|
| 1        | Accessibility        | `ux`        |
| 2        | Touch & Interaction | `ux`        |
| 3        | Performance         | `ux`        |
| 4        | Layout & Responsive  | `ux`        |
| 5        | Typography & Color   | `typography`, `color` |
| 6        | Animation            | `ux`        |
| 7        | Style Selection      | `style`, `product` |
| 8        | Charts & Data        | `chart`     |

## Implementation assets

- **Scripts**: `scripts/search.py` (search + design-system), `scripts/core.py` (BM25), `scripts/design_system.py` (aggregation).
- **Data**: `data/*.csv` and `data/stacks/*.csv` (styles, colors, typography, ux-guidelines, landing, products, charts, icons, react-performance, web-interface, ui-reasoning, and per-stack CSVs).
- **Reference**: `references/reference.md` — full workflow, quick reference, checklist, and professional UI rules.

Run all commands from the **skill root** (the directory containing `scripts/` and `data/`) so paths resolve correctly.

## Output

- Design system summary (pattern, style, colors, typography, effects, anti-patterns).
- Code that follows accessibility, touch targets, contrast, and layout rules from the skill.
- Pre-delivery checklist (icons, cursor/hover, light/dark contrast, layout, a11y) satisfied.
