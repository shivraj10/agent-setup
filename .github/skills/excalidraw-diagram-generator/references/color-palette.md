# Color Palette

All colors used in diagrams. This is the single source of truth.

## Semantic Shape Colors

| Purpose | Fill | Stroke | When to Use |
|---------|------|--------|-------------|
| Primary / Neutral | `#a5d8ff` | `#4a9eed` | Default nodes, inputs, sources |
| Secondary | `#d0bfff` | `#8b5cf6` | Processing, middleware, agents |
| Success / Output | `#b2f2bb` | `#22c55e` | Completed steps, outputs, pass states |
| Warning / Pending | `#ffd8a8` | `#f59e0b` | External systems, pending items |
| Decision / Planning | `#fff3bf` | `#f59e0b` | Decision diamonds, notes, planning |
| Error / Critical | `#ffc9c9` | `#ef4444` | Failure paths, error states, alerts |
| Storage / Data | `#c3fae8` | `#22c55e` | Databases, context files, data stores |
| Documentation / Analytics | `#eebefa` | `#ec4899` | Docs agents, metrics, analytics |

## Zone Backgrounds

Use with `opacity: 25-35` for grouping related elements.

| Purpose | Background | Stroke | Label Color |
|---------|-----------|--------|-------------|
| Planning / UI layer | `#dbe4ff` | `#4a9eed` | `#2563eb` |
| Logic / Agent layer | `#e5dbff` | `#8b5cf6` | `#6d28d9` |
| Quality / Testing layer | `#d3f9d8` | `#22c55e` | `#15803d` |
| Delivery / Output layer | `#dbe4ff` | `#4a9eed` | `#2563eb` |

## Text Hierarchy Colors

| Level | Color | Font Size | Use For |
|-------|-------|-----------|---------|
| Title | `#1e1e1e` | 28 | Main diagram title |
| Subtitle | `#757575` | 16-18 | Secondary descriptions |
| Body / Labels | `#1e1e1e` | 18-22 | Node labels, primary text |
| Annotations | `#757575` | 14-16 | Arrow labels, side notes |
| Semantic: Success | `#22c55e` | 16 | "Yes" labels, pass indicators |
| Semantic: Error | `#ef4444` | 16 | "No" labels, fail indicators |

## Arrow Colors

| Purpose | Color | Style |
|---------|-------|-------|
| Normal flow | `#1e1e1e` | solid, strokeWidth 2 |
| Success / forward | `#22c55e` | solid, strokeWidth 2 |
| Failure / retry | `#ef4444` | dashed, strokeWidth 2 |
| Optional / secondary | `#757575` | dashed, strokeWidth 2 |

## Evidence Artifact Colors (for Technical Diagrams)

| Element | Background | Text Color |
|---------|-----------|------------|
| Code snippet bg | `#1e1e2e` | `#e5e5e5` |
| JSON key | — | `#4a9eed` |
| JSON string value | — | `#22c55e` |
| JSON number | — | `#f59e0b` |
| Comment text | — | `#757575` |

## Dark Mode Override

When user requests dark mode, replace the above with:

| Element | Color |
|---------|-------|
| Canvas background | `#1e1e2e` |
| Primary text | `#e5e5e5` |
| Secondary text | `#a0a0a0` |
| Shape fills | Darker variants: `#1e3a5f`, `#1a4d2e`, `#2d1b69`, `#5c3d1a`, `#5c1a1a` |
| Shape strokes | Use bright primary colors from Arrow Colors |
