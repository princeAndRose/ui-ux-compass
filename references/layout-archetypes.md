# Layout Archetypes

Choose an archetype from user task and information hierarchy, not from visual taste.

## Summary Plus Drilldown

- Best for: dashboard, analytics overview, admin health.
- Structure: P0 summary row, P1 chart/table region, P2 activity/detail.
- Watch for: equal-weight KPI cards, chart overload, filters too far from affected data.
- Constraints: stable chart dimensions, explicit units, responsive collapse that keeps P0 first.

## App Shell Workspace

- Best for: workspace, editor, admin tool, repeated operations.
- Structure: persistent nav, primary work area, optional inspector or utility rail.
- Watch for: landing-page hero inside an operational tool, decorative cards, weak active state.
- Constraints: fast scanning, keyboard path, predictable navigation, no layout shift on hover.

## Split Pane / List-detail

- Best for: inbox, CRM, issue tracker, item review.
- Structure: filterable list on one side, selected detail on the other.
- Watch for: losing selection on mobile, hidden primary action, stale detail after filter.
- Constraints: selected state must be visible; mobile can stack list then detail.

## Stepper / Wizard

- Best for: onboarding, setup, multi-step forms, migration flows.
- Structure: progress, current step, next action, optional review.
- Watch for: too many fields per step, no save/resume, unclear validation.
- Constraints: preserve entered data, show progress honestly, keep escape path.

## Dense Table

- Best for: admin, finance, logs, records, permissions.
- Structure: filter bar, table, row actions, pagination or virtualization.
- Watch for: low information density, unlabeled icons, hidden filters.
- Constraints: stable columns, accessible sorting, useful empty and filtered-empty states.

## Focused Form

- Best for: settings, profile, create/edit record.
- Structure: grouped fields, inline validation, primary action near completion.
- Watch for: flat wall of fields, destructive actions in the main flow.
- Constraints: labels persist, validation is recoverable, disabled states explain why.

## Marketing Proof Flow

- Best for: landing, pricing, product page.
- Structure: offer, proof, product evidence, plan/detail, conversion CTA.
- Watch for: vague hero, decorative-only visual, no proof above the fold.
- Constraints: first viewport reveals brand/offer and next section hint; mobile keeps CTA visible.

## Command Surface

- Best for: command palette, quick switcher, search.
- Structure: input, grouped results, keyboard hints only where useful.
- Watch for: poor empty state, no ranking, mouse-only behavior.
- Constraints: keyboard focus, result labels, safe destructive commands.
