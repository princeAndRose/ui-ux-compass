---
name: ui-ux-implementation-gate
description: Use immediately before implementing or modifying a user-facing UI to verify that design intent, information hierarchy, layout strategy, component constraints, states, and acceptance criteria are sufficient.
---

# UI/UX Implementation Gate

Check whether implementation can begin.

Use this gate before creating a new user-facing page, substantial component, flow, dashboard, editor, landing page, onboarding sequence, or high-fidelity prototype.

## Checklist

- Page role is clear.
- Target user is clear.
- Core task is clear.
- First visual focus is clear.
- P0/P1/P2 hierarchy is clear.
- Main CTA is clear.
- Layout model is clear.
- Information density is clear.
- Visual direction is clear.
- Component system constraints are clear.
- Required states are covered.
- Responsive strategy is clear.
- Acceptance criteria are clear.

## Output Contract

```md
## Implementation Gate

Status: pass / pass-with-assumptions / blocked

Known decisions:

Assumptions:

Blocking gaps:

Implementation instructions:
```

If status is `blocked`, do not write high-fidelity UI. If the user explicitly asks to continue, switch to `pass-with-assumptions` and list the assumptions plainly.
