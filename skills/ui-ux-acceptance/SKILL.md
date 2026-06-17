---
name: ui-ux-acceptance
description: Use after implementing or revising UI to decide whether it satisfies the UI Intent Spec, acceptance criteria, visual direction, state coverage, accessibility expectations, and frontend maintainability requirements.
---

# UI/UX Acceptance

Decide whether the UI is ready to accept, accept with notes, or revise.

Compare the implemented UI against the UI Intent Spec, implementation gate, visual direction, review checklist, accessibility expectations, responsive strategy, and maintainability constraints.

## Output Contract

```md
## UI Acceptance

Decision: accept / accept-with-notes / revise

Acceptance criteria:
- [ ] ...
- [ ] ...
- [ ] ...

Remaining issues:

Recommended next action:
```

Do not accept a UI that lacks required states, contradicts the primary user task, hides P0 content, or violates stated constraints.

Use `references/design-quality-rubric.md`, `references/state-patterns.md`, and `references/component-patterns.md` before accepting or requesting revisions.
