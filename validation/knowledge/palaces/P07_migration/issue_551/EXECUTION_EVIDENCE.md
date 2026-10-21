# Execution Evidence — Knowledge Issue #551 / P07 Migration M01

## Scope
- Lane: KNOWLEDGE_ONLY
- Shard: P07 / 迁移宫
- Work unit: KB-WP05-P07-MIGRATION-M01-CANONICAL-001-100
- Branch: `knowledge/p07-551-migration-m01-canonical`
- Source: SRC-ZZ-003 / 《中州派紫微斗数深造讲义（下册）》 / printed pp109–111
- Pre-G12 candidate input: `validation/wp05/M01_migration_projection_review_001_100.csv` (read-only under the P07 shard contract)

## Source inspection
Printed pp109–112 were rendered from the project PDF and visually inspected. The M01 scope ends in the printed p111 天机/天梁 support sequence.

Visual inspection resolved two extraction issues relevant to M01:
- the printed p109 text itself has the typographical surface “紫迁移宫有百官朝拱”; the governing section heading is “1 紫微”, so the archived subject normalization is transparent and bounded;
- printed p110 reads “驿夫、水客”; the parsed-text “水窖” surface is OCR noise.

One printed p109 surface remains nonstandard/damaged:
- “若羊陀裔冲” in the 紫微+禄存 paragraph. This is preserved as uncertainty rather than silently normalized to “羊陀夹冲”.

## Deterministic candidate census
- rows: 100
- unique IDs: 100
- range: M01-001..M01-100
- source_id SRC-ZZ-003: 100/100
- palace_id P07: 100/100
- source_span_verified: 100/100
- CASE_SUPPORT_ONLY: 8
- PATH_DEPENDENT_GATE/history-feedback: 4
  - M01-044
  - M01-054
  - M01-088
  - M01-100

## Re-adjudication result
- canonical promoted: 100
- reusable: 92
- case-only: 8
- bounded source/normalization repairs: 6
  - M01-030
  - M01-047
  - M01-051
  - M01-052
  - M01-060
  - M01-068
- new primitive qi: 0
- new memory type: 0
- new independent time scale: 0
- new shared group semantics: 0
- probability / weight / decay: 0 / 0 / 0

## Key critic outcomes
1. Movement signal remains separate from post-move outcome.
2. 禄马交驰 remains a movement signal and is not promoted to an automatic wealth outcome.
3. Related-palace involuntary movement and Migration-palace post-move outcome remain distinct.
4. M01-060 OR logic and M01-068 alternative flank structures are restored.
5. Concrete severe outcomes remain CASE_SUPPORT_ONLY.
6. HG-P07-TEMPORAL-01-A remains the only event-relative extension and is not generalized.

## Validation status
A deterministic P07 test module is added for the 100-row census, case/history counts, six bounded repairs, temporal overlay boundary, and zero-new-quantitative-semantics checks.

Full repository exact-head quality-gate execution is required before canonical merge; GitHub Actions are not used.

## Exact-head gate
OpenAI-side deterministic exact-head validation completed after rebasing to current main:
- validation base: `9114300e306abc908ab1fe1724faa7957ad728b9`
- PR: #564
- branch behind main: 0
- changed paths: 6
- all changed paths inside P07 shard write-set: PASS
- re-adjudication records: 100 unique / 100 promoted: PASS
- CASE_SUPPORT_ONLY count: 8: PASS
- PATH_DEPENDENT_GATE set: M01-044, M01-054, M01-088, M01-100: PASS
- bounded repair set: M01-030, M01-047, M01-051, M01-052, M01-060, M01-068: PASS
- HG-P07-TEMPORAL-01-A overlay remains non-generic / no seventh layer: PASS
- new probability / weight / decay / shared primitive: 0: PASS
- GitHub PR mergeability at validated head: clean

If main changes after this evidence commit, this gate must be repeated before merge.
