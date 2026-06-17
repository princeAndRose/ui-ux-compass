---
name: ui-ux-compass-router
description: Use at the start of any Codex conversation to decide whether UI/UX Compass applies, and whenever work may affect user-facing UI, frontend components, layouts, styling, routes, product flows, prototypes, visual design, UX copy, or UI review. This skill routes only; it must not start a full interview unless risk warrants it.
---

# UI/UX Compass Router

Act as the routing layer for UI/UX Compass.

Do not design immediately. Decide whether the task is entering UI/UX territory, how risky the UI decision is, and which UI/UX Compass skill should be used next.

Core principle: default to assist, not interrupt.

Do not ask UX questions for backend-only, infra-only, test-only, dependency-only, or trivial copy changes unless they affect user-facing behavior or interaction meaning.

## Routing Steps

1. Determine whether the task affects a user-facing interface.
2. Inspect likely UI files, routes, components, styling, and design tokens before asking the user.
3. Classify UI/UX risk from 0 to 4.
4. Choose the minimum useful intervention.
5. If implementation is safe, continue with explicit assumptions.
6. If implementation is risky, route to the appropriate UI/UX Compass skill.

## Risk Levels

Risk 0: no user-facing UI impact. Do not intervene.

Risk 1: trivial or local UI change within an existing pattern. Proceed silently using project conventions.

Risk 2: local component or existing page improvement with limited ambiguity. Ask at most one high-leverage question, or proceed with clearly stated assumptions.

Risk 3: new page, new flow, new dashboard, new editor, new form flow, or substantial layout change. Route to `ui-ux-capture-intent` or `ui-ux-brief`; produce a UI Intent Spec before implementation.

Risk 4: core product surface, high-fidelity prototype, landing page, onboarding flow, pricing page, complex dashboard, or subjective UI dissatisfaction. Use the full flow: brief, direction, wireframe, implementation gate, review, acceptance.

## Intervention Modes

- `observe`
- `apply-existing-conventions`
- `ask-one-question`
- `assumptions-gate`
- `mini-brief`
- `full-brief`
- `visual-direction`
- `review`
- `acceptance`

## Hard Rules

- Never start high-fidelity UI implementation when page role, primary user task, information hierarchy, main CTA, and layout archetype are all unknown.
- Never ask vague aesthetic questions such as "what style do you like?"
- Ask one question at a time when interviewing.
- Every question must include options and a recommendation.
- Prefer extracting answers from existing code, screenshots, docs, routes, components, and prior conversation before asking the user.
- If the user asks to move fast, reduce questions but still produce explicit assumptions.
- If the user says not to ask questions, proceed with assumptions and mark them as assumptions.

## Useful References

Read `references/routing-matrix.md` for risk details, `references/prompt-contracts.md` for output contracts, and `references/examples.md` for common routing examples.
