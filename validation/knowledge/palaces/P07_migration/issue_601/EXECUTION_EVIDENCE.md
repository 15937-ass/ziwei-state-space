# Execution Evidence — Knowledge Issue #601 / P07 Migration M04

## Scope
- Lane: KNOWLEDGE_ONLY; shard P07 / 迁移宫
- Work unit: KB-WP05-P07-MIGRATION-M04-CANONICAL-301-400
- Branch: knowledge/p07-601-migration-m04-canonical
- Source: SRC-ZZ-003 / 《中州派紫微斗数深造讲义（下册）》 / printed pp. 115–117
- Scan pages: PDF p58 contains printed pp115–116; PDF p59 contains printed pp117–118
- Historical candidate: validation/wp05/M04_migration_projection_review_301_400.csv (read-only)

## Source inspection and span audit
- PDF scan p58 and p59 were visually inspected, including printed-page numbers and section headings.
- Printed p115 contains M04-301..M04-324; the compound Taiyin flowing-Hua-Ji sentence spans pp115–116 for M04-325/326; M04-327..368 are on p116; M04-369..400 are on p117.
- The historical CSV incorrectly labels M04-301..M04-326 as printed p116. Canonical records preserve the archived location and correct it.
- Printed p118 begins the next 天相 section and is outside this batch.

## Deterministic census
- Candidate rows: 100, unique contiguous M04-301..M04-400
- Canonical records: 100
- Reusable projection rules: 91
- CASE_SUPPORT_ONLY: 9, each with an individual source-bounded reason
- Historical PATH_DEPENDENT_GATE flags: M04-328 and M04-349; canonical gates: 0
- Canonical-condition normalization: 60 rows
- Substantive source-resolution changes: 40 rows
- Source-location corrections: 26 rows
- Time-layer corrections: 0 rows
- New source-coverage gaps: 3
- M03 gaps resolved by this batch: 10; carried forward: 2

## Key source corrections
- M04-327/328 correct the source subject from candidate “太阴” to source “太阳”.
- M04-328 and M04-349 are source-internal sequences, not personal-history gates.
- M04-319 is re-anchored to the separate Taiyin-Hua-Ji financial-loss sentence.
- M04-368's existing YEAR layer is confirmed and its full annual antecedent expanded; M04-388/389's existing DECADE/YEAR layers are confirmed with the inherited base condition made explicit.
- M04-301..326 source locations are corrected to printed p115 / pp115–116; M04-347..349 are corrected from pp116–117 to p116.
- M04-325/326 preserve the full compound trigger and alternative Yang/Tuo branches.
- M04-377's favorable Lu/support branch does not close the missing adverse “no auspicious support” clause.

## Temporal / governance boundaries
- Preserve NATAL / DECADE / YEAR / MONTH only.
- Preserve MIGRATION_FIRST_THREE_YEARS / HG-P07-TEMPORAL-01-A unchanged.
- No generic event timer, seventh calendar layer, new qi primitive, history-memory type, shared group semantics, probability, numeric weight, decay, causal claim, or Product runtime permission.
- No Product, Core, Governance, or other-palace paths changed.

## Validation plan
The exact final PR head must pass targeted tests, full repository pytest, Product JS adapter checks, deterministic P0 repository audit, Repository Governance v1 and exact-main/base/head comparison before merge. No full-suite pass is claimed until the actual exact-head run completes successfully.
