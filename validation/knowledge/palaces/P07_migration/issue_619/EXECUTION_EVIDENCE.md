# Execution Evidence — Knowledge Issue #619 / P07 Migration M05

## Scope
- Replacement PR: #622
- Lane: KNOWLEDGE_ONLY; shard P07 / 迁移宫
- Work unit: KB-WP05-P07-MIGRATION-M05-CANONICAL-401-500
- Branch: knowledge/p07-619-migration-m05-canonical
- Source: SRC-ZZ-003 / 《中州派紫微斗数深造讲义（下册）》/ printed pp.117–120
- Scan pages: PDF p59 contains printed pp117–118; PDF p60 contains printed pp119–120
- Historical candidate input: validation/wp05/M05_migration_projection_review_401_500.csv (read-only)

## Source inspection
- Printed-page numbers and page transitions were visually inspected on PDF scan pages 59–60.
- M05-401..409 overlap printed p117 with the prior M04 span and close the three exact M04 source gaps; no duplicate evidence is promoted.
- M05-401..418 map to p117; M05-419..423 span pp117–118; M05-424..461 map to p118; M05-462 spans pp118–119; M05-463..500 map to p119.
- Image inspection corrects OCR “怨罔刑耗诸星同会” to “煞曜刑耗诸星同会” for M05-423.
- The historical source-location field is corrected on 41 rows.

## Deterministic census
- Historical candidates: 100 unique contiguous IDs M05-401..M05-500
- Canonical records: 100
- Canonical-condition normalization: 100
- Source-resolution changes: 56
- Reusable projection rules: 90
- CASE_SUPPORT_ONLY: 10, each with an individual source-bounded reason
- Historical PATH_DEPENDENT_GATE: M05-455, M05-487; canonical history gates: 0
- M04 source gaps closed: 3
- New p118 Tianxiang source gaps: 4
- Time-layer changes: 0

## Validation
- Branch synchronized to current main `11cbd21a38f593fbc75bf0d0c49eb1f02fba4191`; exact-main comparison and quality gate are being rerun on the current PR head.
- Focused regression tests are encoded in tests/test_knowledge_p07_migration_m05_canonical.py.
- Full repository pytest, Product JS adapter checks, deterministic P0 audit, Repository Governance v1 and exact-main/base/head comparison must pass on the final PR head before merge.
- This evidence file does not claim the GitHub Actions quality gate has passed until the actual final-head run completes.
- Do not change source/test artifacts after the final exact-head quality run; if any file changes, rerun the gate.

## Boundaries
- Preserve only NATAL / DECADE / YEAR / MONTH.
- Preserve MIGRATION_FIRST_THREE_YEARS / HG-P07-TEMPORAL-01-A unchanged.
- No new qi primitive, history-memory type, shared group semantics, independent time scale, probability, numeric weight, decay, causal claim, or Product runtime permission.
- No Product, Core, Governance, or other-palace paths changed.

## Next source anchor
Re-adjudicate M06-501..590 against printed pp119–122: Qisha completion, the complete Pojun section and the chapter boundary. Carry the four p118 Tianxiang gaps forward explicitly; do not claim complete source coverage until they are resolved or explicitly accepted as residual gaps.
