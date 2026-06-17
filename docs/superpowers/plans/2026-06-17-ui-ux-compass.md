# UI/UX Compass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `ui-ux-compass` Codex plugin as a routable UI/UX workflow system with skills, references, scripts, hooks, and eval fixtures.

**Architecture:** The plugin root is the current `ui-ux-compass` directory. The manifest exposes a skills directory; `ui-ux-compass-router` is the main entry point and routes to focused skills for phase detection, intent capture, brief, direction, wireframe, implementation gate, review, acceptance, and state. Standard-library Python scripts provide local detection, route extraction, state rendering, state updates, and intent validation.

**Tech Stack:** Codex plugin manifest, Codex skills, Markdown references, Python standard library scripts, `unittest` verification.

---

### Task 1: Plugin Scaffold

**Files:**
- Create: `.codex-plugin/plugin.json`
- Create: `README.md`
- Create: `assets/icon.svg`
- Create: `assets/logo.svg`

- [x] **Step 1: Define validated plugin manifest**

Use a semver version, required author and interface fields, `skills: ./skills/`, no unsupported `hooks` field, and real asset paths.

- [x] **Step 2: Add plugin usage README**

Document the AGENTS.md snippet, the risk model, and the fact that hooks are included as optional resources but not declared in the manifest until supported by the local validator.

### Task 2: Skills

**Files:**
- Create: `skills/ui-ux-compass-router/SKILL.md`
- Create: `skills/ui-ux-phase-detect/SKILL.md`
- Create: `skills/ui-ux-capture-intent/SKILL.md`
- Create: `skills/ui-ux-brief/SKILL.md`
- Create: `skills/ui-ux-direction/SKILL.md`
- Create: `skills/ui-ux-wireframe/SKILL.md`
- Create: `skills/ui-ux-implementation-gate/SKILL.md`
- Create: `skills/ui-ux-review/SKILL.md`
- Create: `skills/ui-ux-acceptance/SKILL.md`
- Create: `skills/ui-ux-state/SKILL.md`

- [x] **Step 1: Implement concise trigger metadata**

Every skill gets `name` and `description` only in frontmatter, with strong routing boundaries.

- [x] **Step 2: Implement workflow contracts**

Each skill describes when to ask, when to proceed with assumptions, and which output contract to produce.

### Task 3: References

**Files:**
- Create: `references/routing-matrix.md`
- Create: `references/ui-intent-spec-template.md`
- Create: `references/question-bank.md`
- Create: `references/visual-vocabulary.md`
- Create: `references/layout-patterns.md`
- Create: `references/review-checklist.md`
- Create: `references/anti-patterns.md`
- Create: `references/state-schema.md`
- Create: `references/examples.md`
- Create: `references/prompt-contracts.md`

- [x] **Step 1: Add reusable UI/UX decision references**

Keep the router skill compact and move detailed matrices, templates, and examples into references.

### Task 4: Script Tests

**Files:**
- Create: `tests/test_ui_ux_scripts.py`

- [x] **Step 1: Write failing tests first**

Cover risk detection, design-system inspection, route extraction, intent validation, state update, and markdown rendering.

- [x] **Step 2: Run tests and confirm they fail before scripts exist**

Run: `python -m unittest discover -s tests -v`

### Task 5: Scripts And Hooks

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/detect_ui_surface.py`
- Create: `scripts/inspect_design_system.py`
- Create: `scripts/extract_routes.py`
- Create: `scripts/summarize_ui_intent.py`
- Create: `scripts/update_ui_state.py`
- Create: `scripts/validate_ui_intent.py`
- Create: `scripts/render_ui_state.py`
- Create: `hooks/hooks.json`
- Create: `hooks/session_start.py`

- [x] **Step 1: Implement standard-library scripts**

Scripts must support JSON output, avoid network access, and return JSON errors instead of stack traces for CLI failures.

- [x] **Step 2: Run tests and fix failures**

Run: `python -m unittest discover -s tests -v`

### Task 6: Evals And Validation

**Files:**
- Create: `evals/trigger-cases.csv`
- Create: `evals/expected-routing.json`
- Create: `evals/README.md`

- [x] **Step 1: Add trigger eval fixtures**

Use the 15 specification cases and success metrics.

- [x] **Step 2: Validate skills and plugin**

Run quick validation for every skill and `validate_plugin.py` for the plugin root.
