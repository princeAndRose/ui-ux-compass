# State Patterns

Every UI Intent Spec should name required states or justify why a state is not applicable.

## Core State Checklist

- Loading: preserve layout dimensions, show what is loading, avoid fake precision.
- Empty: distinguish first-use empty from zero-result filtered empty.
- Error: explain what failed, preserve user input, provide retry or recovery.
- Success: confirm action and show the changed system state.
- Disabled: explain prerequisites when the user can reasonably fix them.
- Selected: make the selected item visible in list, detail, table, and keyboard focus.
- Dirty/unsaved: show save status and prevent accidental loss.
- Permission denied: show safe explanation and next path.
- Stale/revalidating: communicate that data may be out of date without blocking scanning.

## Surface Defaults

- Dashboard: loading, empty, error, stale data.
- Workspace/editor: saving, saved, error, dirty, selected, disabled.
- Settings/admin: loading, error, success, disabled, permission denied.
- List-detail/table: loading, empty, filtered-empty, error, selected.
- Form/wizard/onboarding: validation, loading, error, success, skipped or blocked.
- Landing/pricing: responsive, form loading, form error, selected plan.
- Modal/drawer/command palette: focus, loading, empty, error, disabled.

## Review Questions

- Does the state keep the same container size as the normal UI?
- Does the copy name the user-facing condition rather than the implementation detail?
- Is there a next action or a clear reason no action is available?
- Are keyboard and screen-reader states represented?
