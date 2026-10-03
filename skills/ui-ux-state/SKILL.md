---
name: ui-ux-state
description: Read or persist project-specific UI decisions, design-system choices, assumptions, and verification evidence.
---

# UI/UX State

Keep facts, user-confirmed decisions, and assumptions separate. Reuse scoped decisions; revisit them when the user changes direction or evidence becomes stale.

- Project: `.ui-ux-compass/state.json` in the user's repository.
- Optional runtime cache: `PLUGIN_DATA/ui-ux-compass-state.json`.
- Optional page notes: `.ui-ux-compass/pages/<page-id>.md`.

Persist when requested or within the authorized workflow. Otherwise return a proposed patch. Do not ask again for authorization already supplied. `--create` is a filesystem control, not a mandatory extra user approval.

Record the selected system, platform, source, and scope. Do not infer universal taste from one page, promote assumptions to confirmed, or overwrite explicit choices with defaults. Record evidence/revisit conditions; do not claim automatic stale detection.

Read [references/state-schema.md](../../references/state-schema.md) when changing state. Resolve [scripts/update_ui_state.py](../../scripts/update_ui_state.py), [scripts/render_ui_state.py](../../scripts/render_ui_state.py), and [scripts/summarize_ui_intent.py](../../scripts/summarize_ui_intent.py) from this skill's installed location; pass the target repository independently. Core workflows must work without hooks.
