# WP05 P00 — Twelve-Palace Projection Schema Audit

Status: **P00 CLOSED — READY FOR CORPUS EXTRACTION**

## Source basis

Primary source for P00:
- SRC-ZZ-003: 《中州派紫微斗数深造讲义（下册）》, 下篇《宫垣论》
- source scope used for schema design:
  - 前言
  - 十二宫 chapter introductions and explicit palace-boundary statements

P00 is a schema/ontology checkpoint, not a 100-item source-review batch.

## Source-derived architecture

The lower-volume preface establishes three constraints that are now hard-coded into WP05:

1. The twelve palaces must be read through the stars in the palace together with triad and opposite relations.
2. Natal palace nature is established first.
3. Moved decade/year palace configurations are interpreted as reactions to that established nature; mechanically reading each moved `三方四正` in isolation is rejected.

These constraints are represented in `PALACE_PROJECTION_SCHEMA_v0.1.md`.

## Palace semantic boundaries

P00 creates:
- 12 canonical palace records
- 24 scene records
- explicit opposite/triad topology
- scene boundaries for overlapping modern semantics

High-risk overlaps are explicitly separated:

- 兄弟 vs 交友: peer friends remain primarily 兄弟; lower-generation/subordinate relations use 交友.
- 子女 vs 交友: personally cultivated protégés/trusted junior assistants may use 子女; ordinary employees/subordinates use 交友.
- 父母: parents and superiors/supervising institutions are separate scenes.
- 事业 vs 财帛: career prominence and money acquisition/retention are separate projection targets.
- 命 vs 福德: outer/material life expression and mental/subjective experience remain distinct.
- 迁移: movement and outcome after movement are separate.
- 田宅: property/home and service-institution/work-environment scenes are separate.

## Decontamination result

P00 introduces:
- new primitive qi: 0
- new history-memory type: 0
- new continuous weight: 0
- new decay parameter: 0
- new Human Gate: 0

No palace is assigned an arbitrary numeric importance weight.

## Artifacts

- `knowledge/wp05/PALACE_PROJECTION_SCHEMA_v0.1.md`
- `knowledge/wp05/palace_ontology_v0.1.csv`
- `knowledge/wp05/palace_scene_ontology_v0.1.csv`
- `knowledge/wp05/projection_rule_template_v0.1.csv`

## Acceptance checks

- canonical palaces: 12 / 12
- opposite relation present: 12 / 12
- triad relation present: 12 / 12
- canonical scenes: 24
- source/normalization epistemic fields present: YES
- event-specificity routing defined: YES
- temporal layer separation defined: YES
- A2-R1 history routing preserved: YES

## Next work unit

**WP05 P01 — 命宫 projection corpus**

P01 begins source-span extraction from the `命宫` chapter. Use the existing 100-item recoverable checkpoint policy; user-facing reporting remains every 200 reviewed items unless a chapter boundary occurs first.
