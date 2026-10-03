---
name: ui-ux-implementation-gate
description: Check whether unresolved UI decisions would prevent useful implementation of a substantial interface change.
---

# Implementation Readiness

Check the decisions that determine the change: core task, relevant information/actions, project/platform constraints, and success checks.

- Ready: implement.
- Ready with assumptions: state consequential reversible assumptions and implement.
- Needs a decision: identify the unresolved choice and its impact; continue independent work.

Missing template fields are not automatically blocking. A read-only report may have no CTA. Existing evidence can supply a layout and direction without new questions. Do not demand approval already provided.

For substantial specs, [scripts/validate_ui_intent.py](../../scripts/validate_ui_intent.py) checks document completeness using the legacy full-spec format. Its score is not a UI quality score; its `blocked` status is a diagnostic, not an authorization decision. Resolve the script from this installed skill's location.

Use [references/design-quality-rubric.md](../../references/design-quality-rubric.md) and relevant [references/component-patterns.md](../../references/component-patterns.md).
