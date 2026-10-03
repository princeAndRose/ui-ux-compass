# Blinded paired product comparison

Inputs: one original brief, constraints, fixed design direction, and two anonymously labeled artifacts captured in identical states and viewports. Never receive model/plugin identity, author rationale, execution cost, previous votes or condition-specific paths.

Choose `left`, `right`, `tie` or `insufficient_evidence` for each requested product dimension. State the decisive observable difference, relevant user consequence, and evidence path/locator for both artifacts. A beautiful artifact that breaks a required task must not win overall because of appearance. Different but equally suitable styles may tie. Judge only the dimensions visible or independently verified in supplied evidence.

Return a record containing anonymous artifact IDs, task ID, dimension, preference, rationale and evidence. The coordinator randomizes order and repeats with swapped positions, then maps anonymous IDs back privately. Mark order-sensitive disagreement for adjudication. Both presentations constitute one paired comparison, not independent samples. Save original judge outputs and the final adjudication separately. The benchmark CLI does not currently aggregate these records; report pairwise findings explicitly as a separate analysis with coverage and uncertainty.
