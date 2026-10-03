# WP05 P02 — 命宫 Projection Corpus Checkpoint 2

Status: **CHECKPOINT_CLOSED_SOURCE_SPAN_VERIFIED**

## Scope

- source: SRC-ZZ-003《中州派紫微斗数深造讲义（下册）》
- chapter: 命宫
- source span covered in this checkpoint: printed pp6–9
- reviewed projection records: P02-101 … P02-200
- continuation of P01, no gap or overlap in checkpoint IDs

## Result

- reviewed: 100
- SOURCE_SPAN_VERIFIED: 100 / 100
- reusable projection rules: 70
- CASE_SUPPORT_ONLY: 30
- history-feedback items: 1
- new primitive qi: 0
- new history-memory type: 0
- new Human Gate: 0
- invented numeric palace weights / continuous gains / decay: 0

## Cumulative WP05 命宫 result after P01 + P02

- reviewed: 200
- reusable projection rules: 149
- CASE_SUPPORT_ONLY: 51
- history-feedback items queued for A2-R1 deduplication: 4

## Main modeling findings

1. **Palace projection is strongly cross-palace.**  
   命宫 interpretations repeatedly require 父母、夫妻、迁移、事业、财帛 and 福德 constraints. This confirms that palace projection cannot be implemented as an isolated per-palace lookup.

2. **Time-layer hinges are first-class rules.**  
   The source repeatedly identifies particular system palaces as 大限/流年“枢纽”. These are encoded as `TIMING_TRIGGER` rather than as unconditional natal attributes.

3. **Event wording and reusable mechanism remain separated.**  
   Specific eye disease, diabetes, marriage, bereavement, legal and accident claims are source-supported but retained as `CASE_SUPPORT_ONLY` where appropriate.

4. **Resource dimensions remain decomposed.**  
   武曲 is explicitly treated as resource-generating action, while 太阴 is resource planning. This is consistent with the earlier WP04 separation of acquisition, realization and retention.

5. **Malefics remain context dependent.**  
   火铃 can activate 武贪 yet become adverse in other conditions. The palace corpus therefore does not collapse them into a negative scalar.

6. **Modern occupational translations are auditable scenes, not ontology facts.**  
   技术推销、交通通讯、工程工艺、医药/外科等 examples are retained as `SCENE_TRANSLATION` or case-level examples rather than as deterministic job predictions.

## History feedback

P02-170 contains explicit cross-period wording:

- 武曲贪狼：少年运程之优劣“可以影响一生”
- status: `CHECK_EXISTING_A2_R1`

This is queued for deduplication/normalization against the existing A2-R1 history layer. No new memory type or Human Gate is introduced.

## Next anchor

Continue 命宫 from:
- 天同总论 / 子午同阴
- 丑未同巨
- 寅申同梁
- 卯酉、辰戌、巳亥天同
- then 廉贞
