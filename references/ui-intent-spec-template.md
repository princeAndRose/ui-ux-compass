# UI intent record

Use a compact record for decisions that matter to implementation. Existing approved designs can supply these decisions. Small edits do not require a full document.

- **Task and audience:** What should the user accomplish or understand?
- **Surface and platform:** Which page/flow, devices, and inputs are in scope?
- **Design system and brand:** Chosen profile/version, project components, reference sources, intentional departures.
- **Content and actions:** Priorities, peer content, navigation, and primary action if applicable.
- **Structure and expression:** Layout, density, typography, color, motion, tone as needed.
- **Relevant states:** Loading, empty, failure/recovery, selection, validation, or explicit inapplicability.
- **Constraints:** Existing implementation and user choices to preserve.
- **Acceptance:** Observable checks and evidence required.
- **Decision provenance:** Confirmed / project fact / assumption; scope, source, and revisit condition.

Omit inapplicable sections. Missing optional fields do not block implementation. Mark unknowns and assumptions honestly.

The existing JSON validator accepts the legacy full-spec field names (page_role, target_user, core_task, information_hierarchy, etc.). It measures document readiness only; it does not evaluate rendered UI quality or user authorization.
