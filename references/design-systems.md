# Design systems: choose by context

Reviewed against official sources on **2026-10-03**. This is an applicability guide, not a claim of certification or exhaustive conformance. Source pages may change; evaluation runs should pin the source revision or save a dated extract, its URL and content hash.

## Three layers of rules

1. **Cross-context principles:** support the stated task; make status and consequences understandable; preserve recoverable input; provide usable navigation and accessible controls. Translate each principle into an observable check for the actual task. A screenshot cannot prove keyboard operation or persistence.
2. **Platform or system conventions:** apply only when the product adopts that platform/system, and identify the relevant version. Native macOS menu behavior, Material adaptive panes, Carbon batch selection, and GOV.UK error summaries are contextual choices, not universal requirements.
3. **Brand and expression:** density, shape, type, color, imagery and motion serve the intended audience. Expressive, restrained and dense designs can each be excellent. Do not penalize a design simply for gradients, cards, asymmetry or generous/tight spacing.

Explicit user requirements and established project constraints take priority over Compass defaults and optional inspirations. If requirements conflict, explain the concrete tradeoff; do not silently replace the project's system. Do not combine several systems' incompatible control or navigation conventions merely to appear comprehensive.

## Official reference families

| Family | Useful when | Transferable ideas | Boundary |
| --- | --- | --- | --- |
| Apple Human Interface Guidelines | Native Apple apps; web work explicitly inspired by an Apple interaction pattern | Keep global preferences separate from task controls; maintain selection context across panes | A web prototype cannot demonstrate native platform compliance; do not prescribe translucency or an Apple visual skin for unrelated products |
| Material 3 | Android and products adopting Material; adaptive interfaces | Rearrange list/detail content for available space; communicate input state; permit expressive typography and shape when appropriate | Choose breakpoints for the task and implementation; an Android implementation example is not a universal validation-timing rule |
| Carbon | Enterprise comparison, monitoring and repeated record operations | Give comparable data space; make sorting and selection scope visible; use density suited to work | Its table conventions are not a reason to turn every product into a data table |
| GOV.UK Design System | Public-service transactions and deliberate question/review flows | Explain how to correct invalid input; retain answers; allow review and correction before submission | Government identity, logos and service-specific conventions do not transfer automatically to commercial products |

Official links, accessed 2026-10-03:

- Apple: [Settings](https://developer.apple.com/design/human-interface-guidelines/settings), [Split views](https://developer.apple.com/design/human-interface-guidelines/split-views). Settings separates general preferences from controls needed in the current task; split views preserve the relationship between selection and content at different widths.
- Material: [Canonical layout examples](https://m3.material.io/foundations/layout/canonical-examples/overview), [Material 3 overview](https://m3.material.io/), [Android input-validation example](https://developer.android.com/develop/ui/compose/quick-guides/content/validate-input?hl=en). The first describes feed, list/detail and supporting-pane layouts; the overview explicitly accommodates expressive design. The Android example pairs an error state with corrective text. The M3 text-field guidelines page required JavaScript in this research session; do not infer unverified requirements from it.
- Carbon: [Data-table guidelines](https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines). The source supports several densities and documents sorting, selection, expansion and batch actions. The legacy `/components/data-table/usage/` URL redirects here.
- GOV.UK: [Validation](https://design-system.service.gov.uk/patterns/validation/), [Check answers](https://design-system.service.gov.uk/patterns/check-answers/). These describe linked field errors, preserving entries, and returning to review after correcting an answer. GOV.UK's default validation timing differs from the Android example; preserve that context rather than inventing one universal rule.

`frontend-design` and `ui-ux-pro-max` are workflow resources, not platform standards. The [UI UX Pro Max primary repository](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (accessed 2026-10-03) provides searchable design guidance and a design-system generation workflow; these can inform exploration, but are not independent evidence of quality. Inspect the installed resource and record its version before attributing a specific recommendation to it. Their presence is neither evidence of compliance nor permission to override a project's design contract. Do not import categorical font or gradient bans as universal quality rules.

## Using classic patterns in evaluations

The scenarios in `evals/scenarios/` use original domains, content and task conditions inspired by these patterns. They contain no copied branded screenshots, proprietary assets or reference implementations. A classic pattern is a source of testable interaction principles, not a pixel template or a single correct answer.

- Give producers the task, project context, applicable system and fixed constraints. Keep evaluator checks and split labels outside the producer workspace. The fixed `user_facts` belong to the responder; answer only questions actually asked.
- Compare baseline, stable and candidate with identical artifacts, source access, tools, budget and starting state. Supplying system inspiration to all arms measures how well Compass applies it, rather than how well it remembers a source.
- Keep related pattern families in the same split. The initial holdout is held out from tuning, not secret from people with repository access; replace exposed cases before using them as fresh evidence.
- Separate hard task requirements, contextual heuristics, requested style and process behavior. Require relevant evidence and allow ties or unverified results. Do not score unrelated loading states on a static article or demand a build for a planning-only task.
- Use both generation and restraint cases: small edits, supplied specifications, already-good code, backend false positives and superseded decisions. A correct review can report no defect.
- Include stylistically different successful outputs when calibrating judges. Test known failures as well as good controls, and ask humans to review disagreements. Agent votes are not independent user observations.
