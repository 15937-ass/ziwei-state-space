# Issue #811 — SP07 exact-head validation evidence

## Immutable inputs
- Approved source SHA-256: 6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c
- Historical candidate inventory blob SHA: 7f2bc6ec32c5b5655d4266ccdb2914d019acc6b2
- Direct visual scan: printed pp45–48 / PDF physical pp23–24.
- Boundary: printed p45 heading “10 巨门” through the SP07-700 sentence on printed p48; exclude the SP08-701 continuation.

## Source audit result
- 100 candidates directly re-adjudicated: 78 promoted, 20 temporal-granularity holds, 2 deduplicated.
- 81 source records: 53 reusable and 28 CASE_SUPPORT_ONLY, including three P03-local supplements.
- 17 source gaps recorded; four pre-existing gaps remain open/partial; temporal residuals total 53 groups / 149 candidate rows.
- conditions_compiled=0; execution_unlocked=0; history_feedback=0.

## Required exact-head gate
- Full python -m pytest -q.
- Product JS adapter/syntax check.
- Deterministic P0 repository gate.
- Repository Governance v1 and P03 shard/write-set validation.
- Recheck latest main, exact PR head, and matching workflow run before merge.

Final exact head, matching workflow run ID/status, current main comparison, and merge SHA will be recorded in Issue #811 / the PR after the last code commit completes the exact-head gate. Do not add an evidence-only commit after the final successful run.

## Execution boundary
- P03-only; no Core/shared semantics, other-palace, Governance, Product/runtime, KIB, probability, numeric-weight, decay, or feedback changes.
- Source audit does not assert empirical predictive validity.
