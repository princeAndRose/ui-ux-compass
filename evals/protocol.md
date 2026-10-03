# Controlled plugin evaluation protocol

## Purpose and limits

Estimate whether Compass improves task outcomes and collaboration under the same model, tools and budget. Test contextual design quality, not resemblance to one favored aesthetic. Apple HIG, Material Design and other systems supply documented principles and illustrative patterns; adaptations of their examples are experimental tasks, not official certifications or endorsements. Verify the scenario's source and record source versions or retrieval dates. Do not copy protected assets into fixtures without suitable rights.

The checked-in scenarios are development infrastructure, not completed experiments. Public holdout scenarios support a disciplined workflow but are not secret test data. A stronger generalization claim needs fresh families held outside the candidate author's accessible workspace, plus disclosure of possible prior model exposure to famous examples.

## Roles and separation

1. A coordinator freezes scenarios, initial project snapshots, dependencies, assets, runtime settings, source captures, budgets and release criteria. Record content hashes for uncommitted plugin versions. Keep all hidden checks and simulator facts outside execution workspaces.
2. Execution agents receive identical public tasks and starting projects. A loads no Compass; B loads the frozen baseline; C loads the candidate. Do not give any arm supplemental design skills unless that is a separate predeclared experiment. Remove unrelated personal instructions, other design plugins, hooks and persistent project memories consistently. Platform rules and model pretraining remain present and should be acknowledged.
3. A user simulator answers from a fixed fact sheet. It may paraphrase but must not invent preferences, recommend solutions or volunteer hidden facts. Unanswerable questions receive the same neutral response. Log each question, answer, elapsed time and interruption. Human corrections follow a predetermined policy shared by all arms.
4. Artifact judges inspect the original brief and anonymous artifacts independently using `judges/artifact.md`. They do not see plugin version, execution agent rationale, design claims, condition, or process grades. The coordinator creates neutral artifact names and removes condition markers from paths and metadata without altering UI content. The generated judge packet is raw coordinator input; do not expose its containing run name.
5. A process judge uses `judges/process.md` on the complete execution trace after product scores are locked. Review questions and decision handling independently from visual taste.
6. A human reviews calibrated samples, regressions, critical failures and judge disagreements. Multiple model judges share potential biases; agreement alone is not human validation.

For a pilot, fresh subagents created with `fork_turns="none"` reduce inherited conversation contamination. They still share filesystem and host configuration and therefore are not a clean-room experiment. For credible A/B/C comparisons use separate runtime configurations and isolated project copies, with logs of loaded plugins, skills, hooks, memory, tools and model settings. Never give an execution agent the repository containing these hidden checks. Do not run agents with identical writable workspaces concurrently.

## Fixed execution and repeated measures

Hold model version, reasoning effort, tool access, browser version, fonts, viewport, assets, dependencies, initial data, source access, network policy and starting project constant. `--model` can include the fixed reasoning configuration; `--snapshot` should identify a record containing all other controls. Budget applies to the full attempt, including questions, retries and fixes. Record measured tokens/time rather than assuming the configured maximum was consumed. The offline packager does not enforce these controls or budgets.

Run separate strata for explicit plugin invocation and natural triggering. A natural-trigger prompt must not name Compass or force a skill. Separate from-scratch generation, targeted edits, review-only tasks and recovery tasks. For tasks requiring initial code, create and hash that code once before launching arms. A textual scenario alone is not a runnable project fixture.

Start with a small pilot to detect broken fixtures. Then run the same repeat IDs across all conditions; randomize scheduling to reduce time-of-day/runtime effects. Freeze stopping rules; do not retry only losing arms or discard tool failures. If a run is unusable due to infrastructure, keep its record, state the exclusion rule and repeat all matched arms when necessary.

A repeated run is nested within a task, and tasks from one family may also be dependent. First summarize each task's paired differences, then examine category/system and family coverage. Never multiply the independent sample size by judges or repeat count. Small pilots describe observed outcomes; they do not establish broad statistical superiority. If reporting uncertainty later, use a method matched to the family/task clustering and disclose it before looking at results.

## Rubric and evidence

- **Hard:** observable requirements such as completing the critical task, retaining input on failure, keyboard operability or an explicit contract. Test with interaction/code evidence as the check specifies. No visual attractiveness can compensate for a failed critical task.
- **Heuristic:** task-dependent hierarchy, grouping, feedback, density, navigation and consistency. Score 0–3 with concrete anchors: 0 obstructs the task; 1 significant ambiguity or friction; 2 meets the task in ordinary states; 3 remains clear in the specified demanding states. A scenario may refine these anchors before runs.
- **Style:** fit to the brief, brand and explicitly chosen system. Score 0–3 against the stated direction: 0 contradicts it; 1 partial/inconsistent; 2 coherent and suitable; 3 coherent across all tested conditions with clear intentional detail. Extra decoration does not earn 3. A different valid aesthetic is not a failure.
- **Process:** relevant questions, appropriate intervention, honoring decisions, factual memory, avoiding redundant questions, and verification. Use complete traces. Lack of a visible trace is unverified, not zero interruptions.

The coordinator must define pass thresholds or acceptance descriptions per check before judging. Scores and binary statuses serve different purposes; record both for heuristic/style checks. Missing evidence is `unverified`. `not_applicable` requires justification and evidence, and is forbidden for required checks. Judge unknowns honestly. Plans and claims are not proof of functioning UI; a screenshot alone cannot establish keyboard or error recovery behavior. `document` evidence can establish the contents of requested specifications, plans and reviews, with section/line locators. It cannot establish runtime behavior or process: use interaction evidence for observed UI behavior and execution traces for process checks. A review claiming it tested a control is document content, not proof that the interaction happened.

Collect original renders at fixed viewports and states, interaction logs/videos with exact steps, execution traces, source changes, actual budgets and artifact paths. `benchmark.py` validates file availability and result structure; a reviewer must validate semantic support and evidence authenticity.

## Judge calibration and pairwise comparisons

Before using model grades, label a calibration set with human reviewers. Include attractive but broken UIs, sound high-density UIs, divergent equally valid styles, excellent writeups with weak implementation, and injected known defects. Check missed defects, false positives, severity and human/model disagreement by category. Record the calibration set identity and observed limitations with each judge. Changes to judge prompts require recalibration.

For relative visual quality, use `judges/pairwise.md` with anonymous outputs from the same brief and state. Allow ties and insufficient evidence. Randomize left/right order, then repeat with swapped order. Flag inconsistent preferences; do not count both views as two independent comparisons. Separate product preference from process/cost, and keep pairwise records alongside the evidence. The current harness audits single-run rubrics; pairwise and human adjudication remain separately recorded evidence, not an automatically computed win rate.

## Holdout discipline and failure learning

Tune prompts/rules on development families only. Keep all variants from the same family in one split. Lock the candidate before holdout evaluation. Do not silently move a failed holdout case into development and continue reporting the old holdout result as independent; version the split and reserve fresh families for the next release.

Classify failures by trigger, missing evidence, intent interpretation, rule selection, implementation drift, verification omission, simulator ambiguity or infrastructure. First check whether the task or judge is wrong. Fix the narrow demonstrated cause and preserve the failing example as a regression where appropriate. A high-density enterprise page should not be repaired into a sparse marketing page just because a judge prefers whitespace.

## Predeclared release decision

Before full runs, write a release decision record including:

- The frozen candidate and baseline, target task families, case/repeat counts and exclusion rules.
- Required behavior and acceptable regression limits per important category, including no newly introduced critical hard failures.
- Minimum practically useful paired improvement and how ties/unverified cases count; values must be selected before results are visible.
- Acceptable question/interruption, latency and token changes under an explicitly stated budget.
- Required evidence coverage, human review sampling, judge agreement expectations and unresolved-disagreement policy.

Do not compensate a critical regression with an average visual score. Publish case-level gains and losses, unmatched/unfinished runs, cost and interruption changes, human review coverage and known limitations. A packaging test passing is not a product release verdict; record an actual evaluation only after agents have run and evidence has been independently judged.
