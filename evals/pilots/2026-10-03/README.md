# Candidate forward-test pilot — 2026-10-03

Three fresh subagents (`fork_turns="none"`) completed development tasks with the candidate's relevant Compass entrypoint. A fourth fresh agent independently reviewed anonymous task/artifact pairs. The producer tasks contained no evaluator checks. The judge received the frozen task plus checks and output, but not plugin instructions, producer notes or version labels.

This is a small behavioral smoke test, **not an A/B/C experiment or release verdict**. Agents shared the host/filesystem and platform instructions. The candidate was not frozen into a separate runtime, loaded skills were not independently audited, and complete tool-event traces, actual token/time measures, calibrated human labels, screenshots and interaction runs were not collected. No causal improvement, interruption rate, visual win rate or accessibility claim follows from this pilot.

| Packet | Task | Directly inspectable result | Limits |
| --- | --- | --- | --- |
| 1 | Apple-inspired journal settings specification | Current-note sort/export remain local; appearance follows the system; uncertain choices are labeled | Reminder/permission wording in the original fixture was ambiguous; process beyond the artifact is unverified |
| 2 | Source review of a session-only preference component | No fabricated defect or replacement UI; source observations separated from untested behavior | No browser, screen-reader or keyboard evidence |
| 3 | Literal toolbar spacing edit | Only the requested gap changes from 8px to 12px in the returned snippet | Earlier questions and actual project writes are not established by the snippet |

`review.json` contains the independent judge's original, uncalibrated assessment. It found no confirmed artifact defects, while flagging process evidence gaps and fixture ambiguity. Pass judgments about review wording or absence of replacement code establish only what appears in the final artifact, not the complete run. `producer-notes.json` files are self-reports, not authoritative execution traces; local machine paths were replaced with `<plugin>` / `<run>`.

The numbered `task.json` files preserve the exact judge packets used in this pilot. They include hidden checks; never expose these packets to future producers. Corresponding `artifact.md` files preserve the original outputs.

## Changes supported by the pilot

- Added `document` evidence to the benchmark so a specification/review can establish its own textual contents without pretending to be a complete execution trace. Process and interaction checks still require their own evidence.
- Clarified the development Apple settings fixture: reminder enabled state, stored time and unknown OS permission are separate. The current scenario differs from this frozen pilot packet; the original ratings do not certify the revised case.
- Kept independent judging and missing-evidence reporting. No plugin rule was added merely to force a higher score on these three tasks.

Next credible effectiveness measurement requires frozen A/B/C environments, complete traces, runnable initial artifacts for implementation tasks, human judge calibration and matched repeats under the [experiment protocol](../../protocol.md). The four holdout scenarios were not executed in this pilot.
