# WP05 Career CA04–CA08 CSV Schema Repair

Status: **REPAIRED / NO SEMANTIC RULE CHANGE**

## Finding
Product readiness audit identified a column-order drift in the canonical Career Palace review CSVs CA04–CA08.

The header remained:

`palace_id,time_layer,condition,projection_domain,...`

but the 500 data rows stored the values after `palace_id` as:

`condition,time_layer,projection_domain,...`

CA01–CA03 were already correct.

## Repair
Files repaired:
- CA04_career_projection_review_301_400.csv
- CA05_career_projection_review_401_500.csv
- CA06_career_projection_review_501_600.csv
- CA07_career_projection_review_601_700.csv
- CA08_career_projection_review_701_800.csv

Exactly 100 rows per file / 500 rows total were repaired by swapping the two misplaced values into their declared header columns.

## Invariants
- projection_rule_id unchanged
- source_id / source_location unchanged
- palace_id unchanged
- semantic condition text unchanged
- time layer unchanged
- projection domain / target / mode unchanged
- review status unchanged
- source-span verification unchanged
- CASE_SUPPORT_ONLY flags unchanged
- history-feedback markers unchanged
- no rule added or removed
- no new primitive, memory type, Human Gate, time scale, numeric weight, probability or decay

This is a schema-position correction only. It does not change the reviewed/reusable/case-support/history counts of P09.

## Prevention
All subsequent WP05 review batches must serialize rows in the exact canonical header order and validate `time_layer` against the approved temporal enum before merge.
