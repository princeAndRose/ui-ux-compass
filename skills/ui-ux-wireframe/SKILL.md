---
name: ui-ux-wireframe
description: Use before high-fidelity UI implementation when layout, information hierarchy, page regions, visual flow, or responsive structure should be validated without committing to colors and detailed styling.
---

# UI/UX Wireframe

Produce a low-fidelity layout before high-fidelity implementation when structure or hierarchy is still risky.

Do not focus on color, gradients, decoration, or fine styling. Focus on regions, hierarchy, flow, density, state placement, and responsive behavior.

## Required Output

- ASCII wireframe
- Region descriptions
- Visual flow
- P0/P1/P2 mapping
- Desktop layout
- Mobile layout
- Risks and open decisions

## Example Shape

```text
+-------------------------------------------+
| Header: title, context, primary action     |
+-------------------------------------------+
| P0 summary / main work area                |
|                                           |
+----------------------+--------------------+
| P1 list / table      | P1 details/helper  |
|                      |                    |
+----------------------+--------------------+
```

Use `references/layout-patterns.md` and `references/ui-intent-spec-template.md`.
