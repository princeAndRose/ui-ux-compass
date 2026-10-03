---
name: ui-ux-compass-router
description: Choose the minimum useful design workflow when a UI task has unresolved intent, design choices, or review needs. Skip backend work and routine edits with clear requirements.
---

# UI/UX Compass

Help the user reach a fitting, usable interface with as little process as the task needs.

## Decide what is missing

Use the request, existing decisions, relevant UI files, and supplied visual evidence. Distinguish impact from uncertainty: a large page with an approved design can proceed; a small interaction with unclear consequences may need clarification.

- Clear local edit: implement using existing conventions, without an interview.
- Clear new surface: capture only useful intent and acceptance checks, then implement.
- Material unknown that changes the solution: ask the highest-value question with a recommendation where useful. Continue independent work.
- Reversible uncertainty or a request to proceed: state a brief assumption and continue within scope.
- Subjective dissatisfaction: inspect the interface and use `ui-ux-review`; do not restart discovery by default.
- Competing directions requested or genuinely unresolved: use `ui-ux-direction`.
- Before handoff: verify agreed outcomes using `ui-ux-acceptance` at a depth proportional to the change.

Risk 0–4 from the detector describes an initial impact hint, not a mandatory sequence or question quota. If useful, run [scripts/detect_ui_surface.py](../../scripts/detect_ui_surface.py) with an absolute installed-plugin path and the actual target repository. See [references/router-execution.md](../../references/router-execution.md) for invocation and evidence handling. Skip it for obvious non-UI work.

## Preserve the project's design language

Honor the user's selected system, platform, brand, and existing components. For a new choice or conflict, consult only the relevant profile in [references/design-systems.md](../../references/design-systems.md). Keep platform conventions, broadly useful principles, and aesthetic preferences distinct. No universal ban on fonts, color, gradients, shadows, or density.

[references/surface-playbooks.md](../../references/surface-playbooks.md) suggests patterns, not requirements. Shared state belongs to `ui-ux-state`; never treat a previous assumption as confirmed.

## Resource paths

Shared resources are relative to this installed skill: `../../scripts/` and `../../references/`. Resolve them from this file's location, not the user's project. Project arguments point to the user's checkout. Missing shell/browser/hooks reduce available evidence; report the limit and continue supported work.
