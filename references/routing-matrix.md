# Routing Matrix

Use this matrix after `ui-ux-compass-router` gathers model judgment, deterministic detector result, repo evidence, and prior conversation. Choose the lowest risk level that handles the real ambiguity.

## Risk 0: Non-UI

Examples:

- Backend API
- Database schema
- Tests
- Infra config
- Dependency upgrade
- Internal refactor without user-facing behavior change

Action:

Do not intervene. Continue normally.

## Risk 1: Trivial UI

Examples:

- Button text
- Icon alignment
- CSS typo
- Existing component variant
- TypeScript error inside a UI component without design implications

Action:

Proceed with existing conventions. Do not ask UX questions.

## Risk 2: Local UI Ambiguity

Examples:

- Add a table filter
- Add an empty state
- Add a selected state
- Add dark mode using existing tokens
- Adjust spacing on an existing page

Action:

Ask one high-leverage question or state assumptions. Do not run a full brief.

## Risk 3: New Page Or Flow

Examples:

- Dashboard
- Settings page
- Admin management page
- Form flow
- Report page

Action:

Run `ui-ux-capture-intent`, then `ui-ux-brief` or an assumptions gate. Produce a UI Intent Spec before implementation.

## Risk 4: Core, Subjective, Or High-Fidelity

Examples:

- Landing page
- Pricing page
- Flagship dashboard
- Onboarding
- Editor layout
- User says "ugly", "too cramped", "generic", "template-like", or "not product-like"

Action:

Use the full flow or review path:

```text
capture-intent -> full-brief -> direction -> wireframe -> implementation-gate -> review -> acceptance
```

For subjective feedback, start with `ui-ux-review`.
