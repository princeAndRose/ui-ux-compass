---
name: ui-ux-review
description: Use when reviewing an existing UI, screenshot, prototype, generated frontend, or when the user says the UI feels ugly, cramped, generic, template-like, off, too busy, too empty, not premium, not product-like, or hard to use.
---

# UI/UX Review

Diagnose existing UI and convert subjective feedback into executable changes.

Use this when the user is dissatisfied with a UI, after implementation self-review, or when a screenshot/prototype needs critique.

## Diagnostic Dimensions

- Information hierarchy
- Visual focus
- Layout structure
- Spacing rhythm
- Typography hierarchy
- Color strategy
- Component consistency
- State completeness
- Product realism
- Template feel
- Responsive behavior
- Accessibility
- Interaction path
- Over-decoration

## Translation Rules

- "Ugly" may mean unclear focus, flat hierarchy, mixed visual variables, or weak rhythm.
- "Too cramped" may mean insufficient section spacing, overloaded first viewport, or weak grouping.
- "Not premium" may mean uncontrolled shadows, cheap decoration, inconsistent type, or color imbalance.
- "Template-like" may mean equal-weight card layout, generic SaaS structure, or content not shaped around the core task.
- "Not product-like" may mean missing loading, empty, error, selected, disabled, or real data states.

## Output Contract

```md
# UI Review

## Diagnosis
1. Problem:
   Evidence:
   Impact:
   Fix:

2. Problem:
   Evidence:
   Impact:
   Fix:

## Priority patch list
P0:
P1:
P2:

## Revised implementation prompt

## Acceptance checklist
```

Use `references/review-checklist.md`, `references/anti-patterns.md`, `references/visual-vocabulary.md`, `references/design-quality-rubric.md`, `references/feedback-translation-table.md`, `references/state-patterns.md`, and `references/before-after-review-examples.md`.
