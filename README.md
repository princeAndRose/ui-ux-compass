# UI/UX Compass

UI/UX Compass is a Codex workflow plugin for frontend and product UI work. It detects when a coding task enters user-facing UI/UX territory, classifies the design risk, and routes the agent through the minimum useful amount of clarification before implementation.

The core stance is simple:

- Default to assist, not interrupt.
- Always route; do not always interview.
- Risk 0-1: no UX questions.
- Risk 2: ask at most one high-leverage question or state assumptions.
- Risk 3: capture UI intent before implementing.
- Risk 4: use brief, direction, wireframe, implementation gate, review, and acceptance.

## Plugin Shape

```text
.codex-plugin/plugin.json
skills/
references/
scripts/
hooks/
evals/
assets/
```

The manifest exposes `./skills/`. The optional `hooks/` files are included as local resources, but the manifest intentionally does not declare a `hooks` field because the current local plugin validator rejects that field.

Skill names remain English for Codex compatibility. The deterministic detector, trigger evaluations, and review vocabulary support English, Chinese, and mixed Chinese-English UI/UX requests. The detector is an evidence tool for the router, not a replacement for model judgment or repository context.

## Suggested AGENTS.md Snippet

```md
## UI/UX Compass

When the UI/UX Compass plugin is installed, invoke or follow `ui-ux-compass-router` before any task that may affect user-facing UI, frontend components, layouts, styling, routes, product flows, prototypes, visual design, UX copy, or UI review.

Do not start a full UX interview by default. First classify UI/UX risk:
- Risk 0-1: proceed silently using existing conventions.
- Risk 2: ask at most one high-leverage question or state assumptions.
- Risk 3-4: capture UI intent before implementing.

Before implementing a new user-facing page or substantial UI flow, produce a UI Intent Spec or an explicit assumptions gate.
```

## Local Checks

```bash
python -m unittest discover -s tests -v
python scripts/run_trigger_evals.py --cases evals/trigger-cases.csv --repo-root .
```

If you have the Codex plugin validation tools installed, also run the official plugin validator from your local Codex tooling against the repository root. Those validators may require PyYAML in the Python environment that runs them.
