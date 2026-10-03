# UI/UX Compass evaluation

There are two distinct evaluation layers:

- `run_trigger_evals.py` and `run_workflow_evals.py` are deterministic routing/schema regressions. They do not measure a model's UI output.
- `benchmark.py` validates real-task scenarios, prepares controlled agent runs, and audits evidence-backed result files. Preparation and unit tests do **not** execute a model, establish visual quality, or demonstrate plugin improvement.

Use Python 3.10+; the benchmark has no third-party dependencies.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_trigger_evals.py --cases evals/trigger-cases.csv --repo-root .
python3 scripts/run_workflow_evals.py --fixtures evals/workflows --repo-root .
python3 scripts/benchmark.py validate --scenarios evals/scenarios
```

## Prepare an experiment

The three conditions are A (no Compass), B (frozen stable Compass), and C (candidate Compass). Select an actual fixed model configuration and immutable snapshot/revision identifiers before running these commands. B must be a preserved baseline; do not label the candidate as both B and C.

```bash
python3 scripts/benchmark.py prepare --scenarios evals/scenarios --out /tmp/compass-benchmark --condition A --model 'fixed-model-and-reasoning-config' --revision none --snapshot 'input-snapshot-digest' --budget-tokens 16000 --repeat 1
python3 scripts/benchmark.py prepare --scenarios evals/scenarios --out /tmp/compass-benchmark --condition B --model 'fixed-model-and-reasoning-config' --revision 'stable-plugin-content-digest' --snapshot 'input-snapshot-digest' --budget-tokens 16000 --repeat 1
python3 scripts/benchmark.py prepare --scenarios evals/scenarios --out /tmp/compass-benchmark --condition C --model 'fixed-model-and-reasoning-config' --revision 'candidate-plugin-content-digest' --snapshot 'input-snapshot-digest' --budget-tokens 16000 --repeat 1
```

`--case ID` selects one scenario. `--repeat 2` creates the second repeat, not two runs. Existing run directories are never overwritten. The strings above are placeholders; preparation records supplied identities but cannot verify their accuracy or enforce token limits.

Each run contains:

```text
manifest.json                 # coordinator: condition, revision, model, budget, repeat, input identity
producer/task.json            # execution agent: public task only
private/scenario.json         # frozen complete case and digest source
private/simulator.json        # user simulator facts; never give to executor
private/judge-input.json       # coordinator's judge packet
private/result-template.json  # blank ratings: all unverified
private/result.json           # filled after execution and independent judging
evidence/                    # captured artifacts, screenshots, traces and interactions
```

Pass only `producer/task.json`, the starting project, allowed resources and the assigned plugin environment to the execution agent. Its task excludes checks, split, hidden facts, condition and plugin revision. A `private/` directory is an organizational boundary, **not** a filesystem sandbox: never give executors access to the experiment root. Copy the public task into a separate environment. Use isolated runtime configurations to control installed skills, hooks and memories; same-workspace subagents cannot prove isolation.

The harness intentionally does not invoke a model or execute generated shell commands. Independent agents or an external CLI runner can consume the public task. Follow [the experiment protocol](protocol.md) for fixed inputs, user simulation, isolation and release decisions.

## Record and audit results

After execution, copy `result-template.json` to `private/result.json`, fill actual execution status and judge identity/calibration, and have independent judges populate ratings. Every rating uses:

```json
{
  "check_id": "scenario-check-id",
  "status": "pass",
  "score": 2,
  "reason": "Observed result and why it meets this criterion",
  "evidence": [
    {
      "type": "screenshot",
      "path": "evidence/settings-desktop.png",
      "locator": "Account section, top-left region"
    }
  ]
}
```

Statuses: `pass`, `fail`, `unverified`, `not_applicable`. A numeric `score` is required only for verified heuristic/style checks (integer 0–3); other checks use `null`. Do not use scores as a substitute for a criterion-specific pass/fail decision. Optional checks may be inapplicable with evidence and a reason; required checks cannot be skipped. Required artifacts map each exact requirement string to one saved evidence path.

Evidence types are `interaction`, `screenshot`, `trace`, `code`, and `document`. Document evidence establishes what a requested specification, plan or review actually contains; cite its section or line. It cannot establish runtime behavior or replace an execution trace for process checks. Match the evidence type declared by each criterion.

All evidence paths must be relative to the run, beneath `evidence/`, and refer to existing nonempty files. Escaping symlinks, traversal, absolute paths, missing files, mismatched evidence types and missing locators invalidate the associated rating. These checks establish evidence availability; they cannot verify screenshot authenticity, whether a trace supports a claim, or judge correctness. Use independent review for that.

```bash
python3 scripts/benchmark.py report --runs /tmp/compass-benchmark > /tmp/compass-report.json
```

The report separates product/process coverage and retains per-check scores, rationales, submitted evidence references, judge provenance, actual execution token/time measurements, evidence problems, invalid artifacts, unmatched controls and case/condition repeat counts. Measurements remain attached to their repeat; no cost-based winner is computed. Run-level validation failures downgrade audited ratings to unverified while preserving submitted statuses and scores for inspection. `available_evidence` means the referenced files exist, not that their claims are trusted; `provenance_valid` means structural provenance checks passed, not independent certification. No scores are fabricated for missing evidence. Required check failures fail the run; incomplete required checks, missing artifacts, unfinished execution or missing judge provenance prevent a pass. Optional gaps remain visible. The report is diagnostic JSON; exit status 0 means the report was generated, not that the candidate passed a release gate.

The harness does not compute a single quality score, independent-sample confidence interval or ungrounded winner. Analyze matched task pairs, nested repeats and related scenario families according to the protocol. Preserve failures and unmatched runs in the published readout.
