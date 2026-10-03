---
name: ui-ux-capture-intent
description: Extract existing UI decisions from a brief, conversation, design reference, or repository before clarifying unresolved requirements.
---

# Capture UI Intent

Read relevant evidence: the request, selected design/reference, current components, project conventions, and prior decisions. Summarize enough to continue; do not require a separate document for a small change.

Distinguish user-confirmed choices, sourced project facts, scoped assumptions, and consequential unresolved decisions. Preserve the target platform and product purpose. A component library name alone does not establish visual direction or prove design-system compliance.

When useful, run [scripts/inspect_design_system.py](../../scripts/inspect_design_system.py), [scripts/extract_routes.py](../../scripts/extract_routes.py), or [scripts/render_ui_state.py](../../scripts/render_ui_state.py) using paths resolved from this skill's installed location. Pass the user's checkout separately. Use [references/design-systems.md](../../references/design-systems.md) for relevant guidance and [references/layout-archetypes.md](../../references/layout-archetypes.md) for unresolved structure.

If intent is sufficient, continue the requested work. Otherwise identify the specific missing decision without starting a full interview automatically.
