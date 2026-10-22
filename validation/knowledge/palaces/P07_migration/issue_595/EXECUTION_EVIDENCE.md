# Execution Evidence — Knowledge Issue #595 / P07 Migration M03

## Scope
- Lane: KNOWLEDGE_ONLY
- Shard: P07 / 迁移宫
- Work unit: KB-WP05-P07-MIGRATION-M03-CANONICAL-201-300
- Branch: knowledge/p07-595-migration-m03-canonical
- Source: SRC-ZZ-003 / 《中州派紫微斗数深造讲义（下册）》 / printed pp. 113–116
- Scan pages: PDF pp. 57–58; each scan page contains two printed book pages
- Historical candidate: validation/wp05/M03_migration_projection_review_201_300.csv (read-only)

## Source inspection
- Printed pp. 113–114 were directly inspected in the supplied scan image for PDF page 57.
- Printed pp. 115–116 were directly inspected in the supplied scan image for PDF page 58.
- Printed p. 113 overlaps the end of M02, but M03 starts at the next unreviewed passage “天同对拱太阴，以卯宫为佳”; no earlier M02 claim is re-promoted.
- The next 贪狼 section begins on printed p. 116 and is outside this batch.

## Deterministic source census
- candidate rows: 100
- unique IDs: 100, contiguous M03-201..M03-300
- source_id SRC-ZZ-003: 100/100
- palace_id P07: 100/100
- source locations: rechecked against printed pp. 113–116
- reusable projection rules: 81
- CASE_SUPPORT_ONLY: 19; all 19 rows have row-level source-bounded reasons
- history-feedback / PATH_DEPENDENT_GATE: 0
- all canonical conditions: no unresolved “前格” pointer
- canonical-condition normalization: 97 rows
- bounded substantive source-resolution changes: 34 rows
- source text uncertainty preserved: M03-233
- explicit source-coverage gaps: 12
- overlap groups: 20

## Required source repairs
- M03-233: preserve the anomalous scan wording “贞归三” without confident reconstruction; keep uncertainty out of the semantic target and record the uncovered favorable 财荫夹 branch as GAP-012.
- M03-265: do not force Tuo Luo and Tian Yue to co-occur; the source's “天月同度则带病回乡” is kept as its own branch.
- M03-266: keep “煞忌刑重” as the source's broad severe modifier, not a forced Tuo Luo + Tian Yue conjunction.
- M03-270/271: preserve the source's listed alternative Tianxiang clamp structures.
- M03-291: correct attribution to 太阴天机组合 + 天机化忌, with career instability / “事业难成”; not standalone 太阴化忌.
- M03-292: preserve the separate 太阴化忌 external-investment warning.
- M03-293: anchor external disputes / being made to bear blame to the 太阴太阳 + 太阴化忌 + 煞曜/虚耗/刑曜 clause.
- M03-295/296: remove unsupported “even with many benefics” and “yielding guarantees improvement” strengthening.

## Temporal boundary
- Existing source layers remain NATAL / DECADE / YEAR / MONTH.
- M03-238 and M03-239 use only the explicit YEAR trigger in the source.
- The separate “太阴化忌受流年大运化忌冲起” passage is recorded as a source-coverage gap with DECADE/YEAR scope; it is not silently mapped to M03-293.
- Existing HG-P07-TEMPORAL-01-A / MIGRATION_FIRST_THREE_YEARS remains unchanged; no generic event timer or seventh calendar layer is introduced.

## Validation plan / exact-head rule
The PR must pass:
1. M03 targeted deterministic tests;
2. full repository pytest on the current PR head;
3. Product JS syntax check where present;
4. deterministic P0 repository audit;
5. Repository Governance v1 / P07 shard write-set validation;
6. exact-main/base/head comparison immediately before merge.

No full-suite pass is claimed in this evidence file until the actual exact-head GitHub Actions result completes successfully.

## Integrity boundaries
- 19 concrete event-specific claims remain CASE_SUPPORT_ONLY.
- Source coverage gaps remain gaps; no new rule IDs are invented.
- No Product, Core, Governance, or other-palace paths are changed.
- No new qi primitive, history-memory type, shared group semantics, time scale, probability, numeric weight, threshold, decay, causal claim, or runtime permission is introduced.
