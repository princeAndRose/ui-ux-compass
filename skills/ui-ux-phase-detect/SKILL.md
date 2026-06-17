---
name: ui-ux-phase-detect
description: Use when a frontend or product task may be transitioning between requirements, UX design, visual design, implementation, review, or polish. Classifies the current phase and recommends the next UI/UX Compass action.
---

# UI/UX Phase Detect

Classify the current product and UI phase before choosing a workflow.

Use evidence from the user request, current files, existing components, routes, screenshots, and prior conversation. Avoid inventing missing context.

## Phase Enum

- `product-idea`
- `requirements`
- `information-architecture`
- `interaction-design`
- `visual-direction`
- `wireframe`
- `frontend-implementation`
- `ui-review`
- `polish`
- `acceptance`
- `non-ui`

## Output Contract

```md
## UI/UX Phase Detection

Current phase:
Confidence:
Evidence:
Missing decisions:
Recommended next skill:
Recommended intervention level:
```

If confidence is low, route to `ui-ux-capture-intent` instead of asking broad questions.
