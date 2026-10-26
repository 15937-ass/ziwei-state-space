# Execution evidence — P03 Issue #794

## Identity

- Issue: #794 — SP02-101…200 source-first spouse-palace audit.
- Lane / shard: KNOWLEDGE_ONLY / P03 夫妻宫.
- Base main SHA at activation: `0b372a188f2edf1bef3544c30c94388b6a88a131`.
- Branch: `knowledge/p03-794-spouse-sp02-101-200`.
- Source ID: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》, 下篇·宫垣论·夫妻宫.
- Approved source SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.
- Historical candidate index blob SHA: `0bc7a6f9c03790cf8b7c610a19ca55d78b3cf007`.

The original PDF's SHA-256 was recomputed locally and matched the approved pin. Original scan images for PDF physical pp18–19 were inspected directly; the audited printed-page span is pp35–37. Text extraction was used only to locate spans.

## Work performed

- Re-adjudicated exactly 100 candidate rows, SP02-101…SP02-200.
- 77 source-grounded candidate rows promoted into 77 source-audit records.
- 65 reusable projection/method records; 12 CASE_SUPPORT_ONLY records.
- 23 rows held because their historical YEAR/TIMING_TRIGGER mapping was not supported at that time-layer specificity.
- 0 deduplications; 0 history-feedback items; 0 new primitives, shared semantics, weights, probabilities or decay.
- Reconciled prior source gaps P03-SP01-GAP-002/003/004 using SP02-101, SP02-102/103, and corrected SP02-104 respectively. P03-SP01-GAP-001 remains open.
- Added three source-coverage gaps for printed p37 clauses not represented independently by SP02-196…200.
- Carried forward the two prior temporal-scope residuals and added ten grouped residuals for this batch.

## Required final exact-head gate

This evidence is source-review evidence, not a claim that repository CI has passed. The final PR head SHA and the workflow run tied to that exact head must be taken from the live PR/Actions records after the final evidence commit. Do not merge unless all of the following pass on the same final head and current main:

1. `python -m pytest -q`
2. Product JS adapter syntax check
3. `python src/audit_repository.py --fail-on-p0`
4. Repository Governance v1 validation with exact base/head
5. P03 write-set validation
6. Recheck main/base/head immediately before merge; if main advances, sync and rerun the exact-head gate.

The audit artifact does not authorize conditions_compiled, execution_unlocked, Product/runtime use, or any shared Core semantic change.
