# UI/UX Compass

UI/UX Compass is a design workflow plugin for UI work. It helps an agent identify consequential unknowns, preserve a project's design language, and verify the actual interface with evidence. Version 0.2.0 adds contextual design-system guidance and controlled evaluation infrastructure.

## Working principles

- Ask only when an answer would change the solution; reuse supplied designs and prior decisions.
- Separate task impact from uncertainty. A new page does not automatically require an interview.
- Follow the user's selected platform, system, brand and components. Apple HIG, Material 3, Carbon and GOV.UK supply contextual guidance, not a universal visual style.
- Treat gradients, density, fonts, cards and expressive imagery according to purpose. New state contains no prescribed aesthetic preferences.
- Review screenshots for visual claims, interactions for behavior, source for implementation, and execution traces for process. Missing evidence stays unverified.
- Keep facts, confirmed decisions and assumptions separate, with optional scope, sources and revisit conditions.

Start with `ui-ux-compass-router` for unresolved UI work. The focused skills cover intent, brief, direction, wireframe, implementation readiness, review, acceptance and state. They are optional activities, not a compulsory chain. Existing skill names remain available.

Read [design-system selection](references/design-systems.md) for source links and applicability. [Quality criteria](references/design-quality-rubric.md) separate hard requirements, contextual heuristics and style fit.

## Package and runtime

```text
plugin.json                 # portable Agent Plugins identity + OpenAI extension
.codex-plugin/plugin.json   # matching compatibility manifest
skills/                     # focused workflow entrypoints
references/                 # progressively loaded guidance
scripts/                    # Python helpers and benchmark packager
hooks/                      # optional SessionStart runtime cache initialization
assets/                     # plugin icons
evals/                     # deterministic fixtures, scenarios and independent judges
```

The portable manifest is canonical. Its `extensions.com.openai` contains presentation and hooks; the compatibility manifest mirrors those settings for older hosts. OpenAI uses the inline extension instead of merging both overlays. See [official packaging guidance](https://developers.openai.com/plugins/build/plugins).

Shared resource paths resolve from the **installed plugin**, not the user's checkout. Skills link to `../../scripts/` and `../../references/`; pass the target repository separately to helpers. Browser/shell availability varies by environment. No MCP server is required.

Hooks are supported by the current platform and require runtime trust before execution. The optional SessionStart hook initializes a neutral cache in `PLUGIN_DATA`, preserves existing files, and never injects project preferences or blocks a session on cache failure. Core skills and state commands work without hooks. See [hook behavior](references/state-schema.md#optional-sessionstart-hook). The host needs `python3` available to run it; installing the plugin does not install a Python runtime.

For repository integration, an optional `AGENTS.md` instruction is:

```md
Use UI/UX Compass when UI work has unresolved design decisions or needs review.
Reuse the supplied brief, design system and established project conventions.
Proceed directly on clear local changes; ask only consequential questions.
```

## State

Project state uses `.ui-ux-compass/state.json`; runtime cache is optional. Source-aware schema v2 now supports design-system profile/platform/sources and decision metadata. Existing v2 confirmed preferences are preserved. Unbucketed v1 preferences migrate to assumptions because their original provenance is ambiguous. See [state schema and examples](references/state-schema.md).

The detector's risk levels remain heuristic hints. The full-spec validator checks document completeness, not visual quality or authorization. An existing approved design can be sufficient without filling every legacy field.

## Verification and experiments

Use Python 3.10+ for the benchmark; all project helpers use the standard library.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_trigger_evals.py --cases evals/trigger-cases.csv --repo-root .
python3 scripts/run_workflow_evals.py --fixtures evals/workflows --repo-root .
python3 scripts/benchmark.py validate --scenarios evals/scenarios
```

The original trigger/workflow fixtures test deterministic scripts. The 12 new scenarios cover original adaptations of classic interaction patterns, explicit design contracts, expressive design, targeted edits and review controls. They are not copied branded assets or completed model experiments.

[Evaluation instructions](evals/README.md) explain how to prepare A (no plugin), B (stable) and C (candidate) runs, collect evidence, and audit results. [The protocol](evals/protocol.md) covers isolated runtimes, fixed user facts, independent/blind judges, human calibration and holdout discipline. The benchmark does not launch models, enforce execution budgets, or automatically decide a release winner. Subagent smoke runs are useful forward tests but share host context and do not establish causal improvement.

A [three-task forward-test pilot](evals/pilots/2026-10-03/README.md) preserves original artifacts, independent review and limitations. It identified fixture ambiguity and an evidence-type gap; it is not a completed effectiveness benchmark.
