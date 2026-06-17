# Design Quality Rubric

Use this rubric during direction, implementation gate, review, and acceptance.

## P0: Product Fit

- Page role is obvious within the first scan.
- The core user task is faster or clearer than before.
- P0 information is visually dominant and not hidden below decorative content.
- The main CTA matches the user's next best action.
- The layout archetype fits the surface and density.

## P1: Interaction And State Quality

- Loading, empty, error, selected, disabled, and success states are covered when relevant.
- Filters, forms, navigation, and overlays show feedback after interaction.
- Responsive behavior preserves task order, not just visual balance.
- Accessibility basics are present: labels, focus, contrast, keyboard path.
- Copy explains user impact and recovery.

## P2: Visual Craft

- Typography establishes hierarchy without relying on oversized type in compact surfaces.
- Spacing rhythm groups related controls and separates unrelated regions.
- Color and accents communicate state and priority.
- Components follow local design system conventions.
- Motion, shadows, and decoration serve orientation or feedback.

## Reject Conditions

- New page with no clear P0/P1/P2 hierarchy.
- Dashboard made of equal-weight cards without action or comparison.
- Operational tool presented like a marketing landing page.
- Form with placeholder-only labels or destructive action ambiguity.
- Missing error/empty/loading state for a data-dependent surface.
- Subjective feedback patched only with color or decoration.

## Acceptance Rating

- Accept: P0 is satisfied, required states exist, and remaining issues are minor.
- Accept with notes: P0 works, but P1/P2 refinements remain.
- Revise: P0 is unclear, state coverage is missing, or the layout contradicts the task.
