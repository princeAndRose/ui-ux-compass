---
name: ui-ux-acceptance
description: Verify a completed UI change against the agreed task, design constraints, and acceptance checks.
---

# UI/UX Acceptance

Verify the agreed change at the appropriate depth. Use the original request and confirmed decisions alongside implementation; a generated spec cannot silently redefine success.

For each relevant check record `pass`, `fail`, `unverified`, or justified `not-applicable`, with evidence. Use actual interaction for functional claims, rendered screenshots for visual claims, and source inspection for implementation constraints. Accessibility automation is partial evidence, not proof of full accessibility.

Report:
- Accept: required checks are verified and pass.
- Accept with notes: required checks pass; noncritical refinements remain explicit.
- Revise: a required outcome fails.
- Unverified: evidence needed for acceptance is missing.

Compare expression with the selected system/brand, not a default preference for minimalism. A high visual score cannot compensate for a broken primary task.

Use [references/design-quality-rubric.md](../../references/design-quality-rubric.md) and relevant [references/state-patterns.md](../../references/state-patterns.md). Persist sourced decisions and actual verification through `ui-ux-state`; report exactly what was tested.
