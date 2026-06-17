# Before/After Review Examples

Use these examples to make review feedback concrete and patchable.

## Dashboard

Before:
- Twelve equal cards, no clear P0.
- Charts lack units and filters sit below the fold.
- Empty state is a blank table.

After:
- P0 health summary and primary exception list are first.
- P1 trend chart and filters sit in the same scan region.
- Empty and filtered-empty states explain whether there is no data or no matching data.

Review prompt:
Prioritize scan path, metric units, filter feedback, and table state coverage.

## Settings

Before:
- Long flat form with destructive action beside routine save.
- Disabled fields have no explanation.
- Success is only a toast.

After:
- Group settings by user goal and separate dangerous actions.
- Disabled fields name prerequisites.
- Save success updates inline status and preserves context.

Review prompt:
Check grouping, labels, validation, destructive action safety, and confirmation feedback.

## Admin Table

Before:
- Low-density cards for hundreds of users.
- Bulk action scope is unclear.
- Row status is hidden in a hover menu.

After:
- Dense table with persistent filters, status column, and selected row count.
- Bulk actions show scope and confirmation.
- Detail drawer keeps table context.

Review prompt:
Check density, selected state, filter chips, row action hierarchy, and permission states.

## Landing Page

Before:
- Vague headline, decorative abstract art, no proof above the fold.
- CTA competes with secondary links.
- Mobile first viewport hides product evidence.

After:
- Offer and product/category are explicit in H1 and supporting copy.
- Product visual or proof appears in the first viewport with one primary CTA.
- Next section hint is visible on mobile and desktop.

Review prompt:
Check offer clarity, proof, first viewport composition, CTA priority, and responsive crop.

## Modal

Before:
- Modal contains a full multi-step form.
- Primary action is disabled without reason.
- Error appears only after closing.

After:
- Short focused action moves complex work to page/drawer.
- Disabled action explains missing prerequisites.
- Error remains in context and preserves input.

Review prompt:
Check scope, focus trap, escape path, disabled reason, and recovery state.
