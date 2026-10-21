# Execution Evidence — Knowledge Issue #576 / P07 Migration M02

## Scope
- Lane: KNOWLEDGE_ONLY
- Shard: P07 / 迁移宫
- Work unit: KB-WP05-P07-MIGRATION-M02-CANONICAL-101-200
- Branch: knowledge/p07-576-migration-m02-canonical
- Source: SRC-ZZ-003 / 《中州派紫微斗数深造讲义（下册）》 / printed pp111–113
- Historical candidate: validation/wp05/M02_migration_projection_review_101_200.csv (read-only acceleration input)
- Historical report: validation/wp05/M02_MIGRATION_PROJECTION_REVIEW.md (read-only)

## Source inspection
The source text for printed pp111–113 was extracted from the supplied PDF and cross-checked against the two-page spread scans containing printed pp111–112 and pp113–114. The complete span covers:
- printed p111: Tianji completion and Solar;
- printed p112: Solar continuation and Wuqu;
- printed p113: Tiantong opening and its relation to Taiyin.

Scan review directly resolved M02-150's Wuqu-Tianfu / 廉贞化忌 outcome wording. Two lexical surfaces remain uncertain and are intentionally not silently repaired:
- M02-181: printed connector in “必须何禄存叠冲”;
- M02-185: glyph after “出外多是…”, while “或惹灾厄” remains legible.

## Deterministic census
- candidate rows: 100
- unique IDs: 100, contiguous M02-101..M02-200
- source_id SRC-ZZ-003: 100/100
- palace_id P07: 100/100
- source_span_verified: 100/100
- CASE_SUPPORT_ONLY: 11
- PATH_DEPENDENT_GATE/history-feedback: 4 (M02-172, M02-184, M02-192, M02-195)

## Source-first re-adjudication
- canonical promotion ready: 100/100
- reusable projection rules: 89
- bounded source/normalization repairs: 6
  - M02-127
  - M02-146
  - M02-181
  - M02-185
  - M02-192
  - M02-200
- transparent source synthesis: M02-174
- scan-resolved row: M02-150
- source lexical uncertainty preserved: M02-181, M02-185
- no new qi primitive / memory type / time scale / shared group semantics / probability / weight / decay: 0

## Key semantic checks
1. Ji-Yin gain and busyness remain separate, with adverse reversal retained.
2. Solar study/status/visibility is not collapsed into wealth; Solar Hua Lu alone does not imply external wealth.
3. Wuqu systems stay separate; Fire/Bell direction remains conditional on actual system location.
4. M02-146 retains the loss/setback base outcome, M02-171 is marked as an overlapping restatement rather than independent evidence, and M02-172 alone carries the ordered prolonged-stay relation.
5. Tiantong Hua Lu remains 纳福/stability/help, not automatic wealth; Lu Cun overlay is required for the wealth reading.
6. M02-192 alternatives and M02-200 base-vs-intensifier are preserved.
7. HG-P07-TEMPORAL-01-A remains unchanged; no generic timer or seventh layer is added.

## Validation status
- connector-side source census / record uniqueness / write-set review: completed during artifact preparation
- targeted pytest: pending local execution
- full repository pytest / P0 audit / governance validation: pending; must be recorded with exact runtime and results before merge
- GitHub Actions: not invoked by this execution script
