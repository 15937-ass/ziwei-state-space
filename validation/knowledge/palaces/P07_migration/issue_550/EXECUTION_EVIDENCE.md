# P07 Migration M01 execution evidence

Issue: #550  
Branch: `knowledge/p07-550-migration-m01-canonical`  
Lane: KNOWLEDGE_ONLY / P07

## Source verification
- Canonical source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》
- Chapter: 迁移宫
- Printed span: pp109–111
- 100/100 historical candidate rows re-adjudicated against the source span.
- M01-076 received direct page-image inspection: the printed text is “驿夫、水客”, so the parsed-text OCR surface “水窖” is not used.

## Deterministic census
- total: 100
- reusable: 92
- CASE_SUPPORT_ONLY: 8
- PATH_DEPENDENT_GATE/history: 4
- new shared primitive: 0
- new probability/weight/decay: 0

## Validation
Status: **CI_PENDING**

Required exact-head validation before merge:
- repository quality gate
- full pytest
- P0 audit
- Knowledge/G12 shard governance
- no Product file changes

The live Issue/PR remains execution truth while CI is pending.
