# Component Patterns

Use components as task primitives. A component choice should support the user's next action and the surface density.

## Data Table And Filters

- Use when users compare many similar records.
- Must include: useful columns, sort/filter feedback, empty and filtered-empty states, row action hierarchy.
- P0: rows, key status, primary filter/search.
- P1: secondary filters, row actions, saved views.
- P2: export, density controls, metadata.
- Avoid: card grids for dense records, hidden filter chips, unlabeled icon-only actions.

## Modal

- Use when the task is short, interruptive, and must be completed or dismissed.
- Must include: clear title, one primary action, safe cancel, focus trap, error state.
- Avoid: multi-step creation flows, large tables, hidden scroll areas.

## Drawer

- Use when users need detail without losing table/list context.
- Must include: selected item title, status, primary action, close control, responsive fallback.
- Avoid: burying critical fields below a long scroll without anchors.

## Command Palette

- Use when power users need fast navigation or action invocation.
- Must include: input focus, grouped results, empty state, keyboard selection, safe command labeling.
- Avoid: destructive commands without confirmation or indistinguishable result types.

## Form Controls

- Use radios or segmented controls for small exclusive choices, checkboxes/toggles for binary settings, sliders/steppers/inputs for numeric values, menus for long option sets.
- Must include: persistent labels, inline validation, help text only where it reduces errors.
- Avoid: placeholder-only labels and disabled controls with no reason.

## Navigation

- Use tabs for peer views, sidebar for product areas, breadcrumbs for hierarchy, stepper for ordered progress.
- Must include: active state, accessible labels, mobile behavior.
- Avoid: nav items that look like marketing chips in operational tools.

## Cards

- Use for repeated objects or summaries, not as a wrapper for every section.
- Must include: clear object identity, one dominant metric/action, consistent metadata order.
- Avoid: nested cards, equal-weight bento blocks with no P0/P1/P2 distinction.

## Empty, Loading, Error Components

- Use states inside the real layout slot they replace.
- Must include: status, reason when known, recovery or next action.
- Avoid: skeletons that change final dimensions or generic "something went wrong" copy.
