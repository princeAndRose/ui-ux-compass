---
name: ui-ux-capture-intent
description: Use before asking UI/UX questions or implementing UI to extract existing product context, user preferences, page role, user task, design constraints, design system conventions, and unresolved UI decisions from conversation and repository context.
---

# UI/UX Capture Intent

Extract existing UI intent silently or semi-silently before asking the user.

Read available context first: conversation, project docs, routes, existing components, styling setup, design tokens, screenshots, and previous UI decisions. Do not generate high-fidelity UI from this skill alone.

## Responsibilities

- Identify product and surface context.
- Identify target users and core tasks already implied by the request.
- Inspect design system conventions when code is available.
- Separate known decisions, project facts, user preferences, assumptions, and gaps.
- Recommend the single best next question only if needed.

## Output Contract

```md
## Captured UI Intent

Known:
- Product:
- Target user:
- Page / surface:
- Core task:
- Existing design system:
- User preferences:
- Anti-goals:

Unknown:
- Primary visual focus:
- P0/P1/P2 hierarchy:
- Main CTA:
- Layout archetype:
- Visual density:
- Interaction states:

Recommended next question:
```

Use `scripts/inspect_design_system.py`, `scripts/extract_routes.py`, and `scripts/render_ui_state.py` when local project context is useful.
