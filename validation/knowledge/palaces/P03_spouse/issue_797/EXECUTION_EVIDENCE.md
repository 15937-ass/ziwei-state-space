# Execution evidence — P03 Issue #797

## Identity

- Issue: #797 — SP03-201…300 source-first spouse-palace audit.
- Lane / shard: KNOWLEDGE_ONLY / P03 夫妻宫.
- Base main SHA at activation: `bacc582403efa5ac573d4a63009b032c61e64e65`.
- Branch: `knowledge/p03-797-spouse-sp03-201-300`.
- Source ID: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》, 下篇·宫垣论·夫妻宫.
- Approved source SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.
- Read-only historical candidate index: `validation/wp05/SP03_spouse_projection_review_201_300.csv`, blob SHA `f28a3df5f4006f5a1069896514f565f9af8f86a0`.
- Historical summary report `validation/wp05/SP03_SPOUSE_PROJECTION_REVIEW.md` is not accepted proof; current source inventory marked this span inventory-only/not rule-reviewed.

## Direct source review

- Original scan images directly inspected: PDF physical pp19–20; audited printed pages 37–39.
- Physical p19 contains printed pp37–38; physical p20 contains printed pp39–40. Printed p40 is excluded from this batch.
- Local PDF SHA-256 recomputed and matched the approved source pin.
- Re-adjudicated exactly SP03-201…SP03-300. 87 candidate rows were promoted into source-grounded records; 13 were held for unsupported/over-specific time layers; 0 deduplications.
- 91 source records were produced, including four supplemental records for unindexed claims carried from the prior batch: two direct source claims for SP02-GAP-001 and two sex-specific branches for SP02-GAP-002.
- Source gaps 001 is partially open (the literal `机录像` and transit layer remain unresolved); gaps 002 and 003 are resolved; gaps 004 and 005 remain open outside the primary span.
- Temporal residuals increased by four groups / 13 candidate rows. Cumulative totals: 16 groups / 40 candidate rows.
- Execution boundary remains `conditions_compiled=0`, `execution_unlocked=0`; no Product/runtime or shared Core semantic change.

## Required final exact-head gate

This file records source-review evidence, not CI success. The authoritative exact PR base/head and matching GitHub Actions run must be read from the live PR after all files are committed. Any later file or base change invalidates the previous exact-head acceptance. Do not merge unless all required checks pass on the same final head and current main:

1. `python -m pytest -q`
2. Product JS adapter syntax check
3. `python src/audit_repository.py --fail-on-p0`
4. Repository Governance v1 validation with exact base/head
5. P03 write-set validation
6. Reconfirm main/base/head immediately before merge; if main advances, sync safely and rerun the required gate.

## Known limitations

- The source audit is a textual fidelity and project-internal evidence exercise; it does not validate real-world predictive accuracy.
- “机录像” remains the literal visible in the source scan; no alternative reading is adopted.
- Traditional health-related statements remain source-only/case-only and are not modern medical claims.
