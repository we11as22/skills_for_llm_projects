# UI/UX Pro Max — Full Reference

Run all commands from the **skill root directory** (the folder containing `scripts/` and `data/`).

---

## Quick Reference by Priority

### 1. Accessibility (CRITICAL)
- `color-contrast` — Minimum 4.5:1 ratio for normal text
- `focus-states` — Visible focus rings on interactive elements
- `alt-text` — Descriptive alt text for meaningful images
- `aria-labels` — aria-label for icon-only buttons
- `keyboard-nav` — Tab order matches visual order
- `form-labels` — Use label with for attribute

### 2. Touch & Interaction (CRITICAL)
- `touch-target-size` — Minimum 44x44px touch targets
- `hover-vs-tap` — Use click/tap for primary interactions
- `loading-buttons` — Disable button during async operations
- `error-feedback` — Clear error messages near problem
- `cursor-pointer` — Add cursor-pointer to clickable elements

### 3. Performance (HIGH)
- `image-optimization` — Use WebP, srcset, lazy loading
- `reduced-motion` — Check prefers-reduced-motion
- `content-jumping` — Reserve space for async content

### 4. Layout & Responsive (HIGH)
- `viewport-meta` — width=device-width initial-scale=1
- `readable-font-size` — Minimum 16px body text on mobile
- `horizontal-scroll` — Ensure content fits viewport width
- `z-index-management` — Define z-index scale (10, 20, 30, 50)

### 5. Typography & Color (MEDIUM)
- `line-height` — Use 1.5-1.75 for body text
- `line-length` — Limit to 65-75 characters per line
- `font-pairing` — Match heading/body font personalities

### 6. Animation (MEDIUM)
- `duration-timing` — Use 150-300ms for micro-interactions
- `transform-performance` — Use transform/opacity, not width/height
- `loading-states` — Skeleton screens or spinners

### 7. Style Selection (MEDIUM)
- `style-match` — Match style to product type
- `consistency` — Use same style across all pages
- `no-emoji-icons` — Use SVG icons, not emojis

### 8. Charts & Data (LOW)
- `chart-type` — Match chart type to data type
- `color-guidance` — Use accessible color palettes
- `data-table` — Provide table alternative for accessibility

---

## Prerequisites

Ensure Python 3 is installed:

```bash
python3 --version || python --version
```

---

## Workflow: How to Use This Skill

### Step 1: Analyze User Requirements

Extract from the request:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, or default `html-tailwind`

### Step 2: Generate Design System (recommended first)

From the **skill root**:

```bash
python3 scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
```

- Searches product, style, color, landing, typography.
- Uses `data/ui-reasoning.csv` to pick best matches.
- Returns design system: pattern, style, colors, typography, effects, anti-patterns.

**Example:**
```bash
python3 scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Step 2b: Persist Design System (Master + Overrides)

```bash
python3 scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

Creates:
- `design-system/MASTER.md` — global design rules
- `design-system/pages/` — for page overrides

With a page override:
```bash
python3 scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

Creates `design-system/pages/dashboard.md`. When building a page, check `design-system/pages/<page>.md` first; if it exists, its rules override MASTER.md.

### Step 3: Domain Searches (as needed)

```bash
python3 scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

| Need | Domain | Example |
|------|--------|---------|
| More style options | `style` | `--domain style "glassmorphism dark"` |
| Chart recommendations | `chart` | `--domain chart "real-time dashboard"` |
| UX best practices | `ux` | `--domain ux "animation accessibility"` |
| Alternative fonts | `typography` | `--domain typography "elegant luxury"` |
| Landing structure | `landing` | `--domain landing "hero social-proof"` |

### Step 4: Stack Guidelines

Default stack: `html-tailwind`.

```bash
python3 scripts/search.py "<keyword>" --stack html-tailwind
```

Stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

---

## Domains and Stacks Reference

### Domains
| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `product` | Product type | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | UI styles, effects | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Font pairings | elegant, playful, professional, modern |
| `color` | Palettes by product | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | Page structure, CTA | hero, testimonial, pricing, social-proof |
| `chart` | Chart types, libraries | trend, comparison, timeline, funnel, pie |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index, loading |
| `react` | React/Next.js performance | waterfall, bundle, suspense, memo, rerender, cache |
| `web` | Web interface | aria, focus, keyboard, semantic, virtualize |
| `prompt` | AI prompts, CSS keywords | (style name) |

### Stacks
| Stack | Focus |
|-------|-------|
| `html-tailwind` | Tailwind, responsive, a11y (DEFAULT) |
| `react` | State, hooks, performance, patterns |
| `nextjs` | SSR, routing, images, API routes |
| `vue` | Composition API, Pinia, Vue Router |
| `svelte` | Runes, stores, SvelteKit |
| `swiftui` | Views, State, Navigation, Animation |
| `react-native` | Components, Navigation, Lists |
| `flutter` | Widgets, State, Layout, Theming |
| `shadcn` | shadcn/ui components, theming, forms |
| `jetpack-compose` | Composables, Modifiers, State Hoisting |

---

## Output Formats for Design System

```bash
# ASCII (default, terminal)
python3 scripts/search.py "fintech crypto" --design-system

# Markdown (documentation)
python3 scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## Tips

1. Use specific keywords: e.g. "healthcare SaaS dashboard" instead of "app".
2. Run multiple searches with different keywords.
3. Combine domains: style + typography + color for a full system.
4. Always check UX: search "animation", "z-index", "accessibility".
5. Use `--stack` for implementation-specific rules.
6. Iterate with different keywords if the first result is off.

---

## Common Rules for Professional UI

### Icons & Visual
| Rule | Do | Don't |
|------|----|-------|
| **No emoji icons** | SVG (Heroicons, Lucide, Simple Icons) | Emojis as UI icons |
| **Stable hover** | Color/opacity transitions | Scale that shifts layout |
| **Correct logos** | Official SVG from Simple Icons | Guess or wrong paths |
| **Icon sizing** | Fixed viewBox 24x24, w-6 h-6 | Random sizes |

### Interaction & Cursor
| Rule | Do | Don't |
|------|----|-------|
| **Cursor pointer** | cursor-pointer on clickable cards | Default cursor on interactive |
| **Hover feedback** | Color, shadow, border change | No feedback |
| **Transitions** | transition-colors duration-200 | Instant or >500ms |

### Light/Dark Contrast
| Rule | Do | Don't |
|------|----|-------|
| **Glass light** | bg-white/80 or higher | bg-white/10 |
| **Text light** | #0F172A (slate-900) for text | #94A3B8 for body |
| **Muted light** | #475569 (slate-600) min | gray-400 or lighter |
| **Borders light** | border-gray-200 | border-white/10 |

### Layout & Spacing
| Rule | Do | Don't |
|------|----|-------|
| **Floating navbar** | top-4 left-4 right-4 | top-0 left-0 right-0 |
| **Content padding** | Account for fixed navbar | Content behind navbar |
| **Max-width** | Same max-w-6xl or max-w-7xl | Mixed container widths |

---

## Pre-Delivery Checklist

### Visual
- [ ] No emojis as icons (use SVG)
- [ ] Icons from one set (Heroicons/Lucide)
- [ ] Brand logos verified (Simple Icons)
- [ ] Hover states don’t shift layout
- [ ] Theme colors (e.g. bg-primary), not raw var() where avoidable

### Interaction
- [ ] Clickable elements have cursor-pointer
- [ ] Hover gives clear feedback
- [ ] Transitions 150–300ms
- [ ] Focus visible for keyboard

### Light/Dark
- [ ] Light text contrast ≥ 4.5:1
- [ ] Glass/transparent visible in light mode
- [ ] Borders visible in both modes
- [ ] Test both modes

### Layout
- [ ] Floating elements spaced from edges
- [ ] No content behind fixed navbars
- [ ] Responsive at 375, 768, 1024, 1440px
- [ ] No horizontal scroll on mobile

### Accessibility
- [ ] Images have alt text
- [ ] Form inputs have labels
- [ ] Color not the only indicator
- [ ] prefers-reduced-motion respected
