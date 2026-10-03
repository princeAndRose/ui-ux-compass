# Independent process judge

Inputs: public task, simulator fact sheet, complete execution/question/tool trace, predefined process checks and actual runtime measures. Do not read visual preference grades before submitting your own assessment.

Assess whether the agent asked questions that materially affected a decision, avoided repeating supplied facts, respected changed decisions, separated assumptions from confirmations, used proportionate intervention and performed the promised verification. Count actual interruptions and observed rework from the trace. Do not infer that a missing trace means zero interruptions or that a long specification means thoughtful design. A planning or review document proves its contents only; it cannot substitute for the execution trace when judging process.

For each process check record `check_id`, pass/fail/unverified/not_applicable, null score, a specific reason and trace evidence with saved relative path and exact event locator. Required checks cannot be skipped. A design decision you dislike is not a process failure unless it violates an explicit constraint or confirmed fact. Flag incomplete logs and simulator deviations; do not fill gaps from imagination.

Keep measured tokens, elapsed time, relevant/irrelevant questions and corrections distinct from output quality. The result template supports actual tokens/time; save detailed process counts in an evidence file with definitions. Submit grades independently before adjudication.
