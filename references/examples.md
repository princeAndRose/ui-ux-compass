# Examples

## Non-UI

User:
Fix the failing unit test in `utils/date.ts`.

Route:
Risk 0, `observe`. Do not ask UI questions.

## Trivial UI

User:
Change the Save button label to Publish.

Route:
Risk 1, `apply-existing-conventions`. Use the existing component and copy style.

## Local Ambiguity

User:
Add an empty state to the existing tasks table.

Route:
Risk 2, `ask-one-question`.

Question:
Should the empty state mainly help the user create the first task or explain why no rows match filters?

Options:
A. Creation-focused.
B. Filter-explanation-focused.
C. Neutral status only.

Recommendation:
Choose A if this table is often empty for new users; choose B if filtering is common.

## New Page

User:
Create a dashboard page for this project.

Route:
Risk 3, `mini-brief`. Produce a UI Intent Spec before implementation.

## Subjective Review

User:
This generated UI looks ugly and too cramped.

Route:
Risk 4, `review`. Diagnose hierarchy, spacing, density, product realism, and template feel before patching.
