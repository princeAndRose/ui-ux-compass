---
name: ui-ux-state
description: Use to read, update, summarize, or persist UI/UX Compass state including user UI preferences, project product context, design system conventions, page-level UI Intent Specs, decisions, assumptions, and acceptance status.
---

# UI/UX State

Maintain UI/UX Compass state without confusing assumptions with confirmed decisions.

Use runtime state for plugin-level cache and project state for repository-specific UI intent.

## Storage

- Runtime state: `PLUGIN_DATA/ui-ux-compass-state.json`
- Project state: `.ui-ux-compass/state.json`
- Page notes: `.ui-ux-compass/pages/<page-id>.md`

Do not create project state silently. If `.ui-ux-compass/` does not exist, ask before writing or output a state patch in the response.

## Source Rules

- `user-confirmed`: user explicitly chose or confirmed it.
- `project-fact`: verified from project files or design system.
- `agent-assumption`: inferred by the agent and not confirmed.

Never write an agent assumption as a confirmed decision.

State schema v2 is source-aware:

- Project and design-system context is split into `facts`, `confirmed`, and `assumptions`.
- User preferences are split into `defaults`, `confirmed`, and `assumptions`.
- `project-fact` patches may update facts; `user-confirmed` patches may update confirmed preferences/decisions; `agent-assumption` patches may update only assumptions.
- Existing v1 state is migrated on load by `scripts/update_ui_state.py`.

## Supported Actions

- Read current state.
- Generate a state patch.
- Merge confirmed decisions after user approval.
- Render a Markdown summary.
- Generate a page-level UI Intent Spec.

Use `scripts/update_ui_state.py`, `scripts/render_ui_state.py`, `scripts/summarize_ui_intent.py`, and `references/state-schema.md`.
