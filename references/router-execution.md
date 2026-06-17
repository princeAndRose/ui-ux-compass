# Router Execution

Use this guide when `ui-ux-compass-router` decides whether UI/UX Compass should intervene.

## Evidence Stack

1. Model judgment: infer the user's intent, ambiguity, and user-facing impact from the current request and conversation.
2. Deterministic detector result: when local shell access is available and the task is not obviously non-UI, run:

```bash
python3 scripts/detect_ui_surface.py --repo-root . --message "<user request>" --json
```

Use `python` instead of `python3` when that is the available local Python command.

3. Repo evidence: inspect nearby routes, components, styling, design tokens, docs, screenshots, and tests before asking the user.
4. Final routing decision: choose the lowest UI/UX risk level that protects the user-facing result.

The deterministic detector is evidence, not the sole source of truth. Override it when repository context or the user's wording clearly proves a different risk level.

## When To Skip The Detector

Skip the detector when the task is obviously outside user-facing UI:

- Backend API behavior
- Database schema or migrations
- Pure unit tests or test harness work
- Infrastructure, dependency, or CI configuration
- Internal refactors with no user-facing behavior change
- Documentation-only edits outside product UX copy

## Conflict Rules

- If the detector sees a UI word inside a backend/test task, prefer repo and user intent evidence. Example: "Refactor dashboard API tests" remains Risk 0.
- If the detector returns non-UI but the changed files are routes, components, CSS, tokens, or UX copy, inspect the files and route as UI work.
- If subjective feedback appears near a UI surface, route to `ui-ux-review`. Example: "This page feels weird" is Risk 4.
- If a new page or flow has thin details, route to `ui-ux-capture-intent` or `ui-ux-brief` before implementation.
- If the user asks to move fast, reduce questions but keep assumptions explicit.

## Decision Record Shape

When useful, write a compact routing note:

```text
Model judgment: existing dashboard UI, local filter behavior.
Detector evidence: ui_related=true, risk_level=2, recommended_mode=ask-one-question.
Repo evidence: app/dashboard/page.tsx and shared table component exist.
Final routing decision: Risk 2, ask one question or proceed with stated assumptions.
```
