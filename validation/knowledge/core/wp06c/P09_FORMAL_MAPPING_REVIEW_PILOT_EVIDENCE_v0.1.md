# Core #864 — P09 formal mapping-review pilot execution evidence

Status: REVIEW_COMPLETED_VALIDATION_PENDING_AFTER_STALE_HISTORICAL_REGRESSION_REPAIR

## Scope
- Issue: #864
- Work unit: `KB-CORE-WP06C-P09-FORMAL-MAPPING-REVIEW-PILOT-01`
- Branch: `knowledge/core-864-p09-wp06c-formal-mapping-review`
- Initial base: `b762ccf23a9155dedb6416475d70d765913d7221`
- Inputs are accepted-main artifacts from #841/#847 and #673.
- No new source extraction is claimed in this work unit; it reuses the source-reviewed P09 candidate cohort and its cited context evidence.

## Review result
- 3 source candidates reviewed.
- 6 target-specific mapping-review records.
- 3 source-supported candidate targets.
- 3 explicit not-supported target controls.
- Existing `MAPPING_REVIEW_SCHEMA_v0.1` is sufficient for this bounded pilot.
- No new shared semantic primitive or metadata axis is required.

## Guardrails
- No canonical ontology IDs.
- No accepted canonical mappings.
- No production shared schema change.
- No Product/KIB/runtime file modification or consumer authorization.
- No probability, frequency, weight, score, posterior or empirical-validity claim.
- Product ontology/mapping registries remain empty fail-closed.

## Next gate
The pilot can merge as non-canonical reviewed candidate material. Any next step that creates stable shared canonical ontology node identity or promotes an individual mapping to canonical status requires PI/Human Gate.

## First exact-head validation observation

- Run: `40816614824`.
- Head: `210696ec02ebf3b92b2fb22882325872892409c6`.
- Result: **FAIL at pytest only** — `2954 passed, 1 failed, 132 subtests passed`.
- Sole failure: historical #757 closure regression still required `last_completed_issue: 757` in the live Core recovery cache.
- This is stale after the accepted #841/#847 completion: #757 remains historically closed, while the latest completed Core unit legitimately advances.
- Repair: keep #757's closure assertions in its immutable research-closure metadata, require that #757/#783 are not reactivated in the live recovery cache, and stop requiring them to remain the latest completed issue/PR.
- No #864 mapping-review record, source boundary, D1–D5 semantic rule, or Product registry assertion failed.
- Because pytest failed first, Product JS, P0, and Governance steps were skipped; no pass is claimed from this run.

## Final validation
A fresh exact current-main base/head full pytest, Product JS check, deterministic P0 and Governance v1 is required after the historical-regression repair.
