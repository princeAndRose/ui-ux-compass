# Router execution

Use the current request and relevant project evidence to select the next useful action. Impact, unresolved decisions, evidence quality, and reversibility are separate considerations.

## Optional detector

The deterministic detector is a multilingual keyword/repository signal. Its risk and recommended mode are hypotheses, not final policy. It cannot know that an attached design is approved or that a prior answer resolved an uncertainty.

Resolve the installed plugin root from the loaded skill (`../..`). Keep it separate from the target checkout:

```bash
python3 "/absolute/installed-plugin/scripts/detect_ui_surface.py" \
  --repo-root "/absolute/target-project" --message "Add filters to the orders UI" --json
```

Pass user text as a safely quoted argument or through a process API; do not interpolate untrusted text into shell syntax. Skip this command for obvious non-UI work and when the request is already clear.

## Interpretation

- Backend/test context overrides incidental UI words.
- Supplied, complete designs and established conventions can resolve a high-impact task without a new interview.
- Subjective feedback warrants inspecting the current artifact before proposing a change.
- A missing screenshot does not authorize an invented visual diagnosis.
- A small change can require clarification when it changes the meaning or consequences of an action.
- User requests to proceed permit reversible assumptions within scope; they do not confirm those assumptions.

Keep reasoning concise: evidence used, material unknown (if any), next action. Consult [routing-matrix.md](routing-matrix.md) for examples.

## Implementation and verification

Use existing components and the chosen design system unless the task changes them. Use only the references needed for the decision. Verification follows the original user outcome, not just generated documents. [design-quality-rubric.md](design-quality-rubric.md) defines evidence and applicability; [../evals/protocol.md](../evals/protocol.md) defines controlled comparisons.
