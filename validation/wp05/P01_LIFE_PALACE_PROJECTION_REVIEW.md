# WP05 P01 — 命宫 Projection Corpus Checkpoint 1

Status: **CHECKPOINT_CLOSED_SOURCE_SPAN_VERIFIED**

## Scope

- source: SRC-ZZ-003《中州派紫微斗数深造讲义（下册）》
- chapter: 命宫
- source span covered in this checkpoint: printed pp3–6
- reviewed projection records: P01-001 … P01-100

## Result

- reviewed: 100
- SOURCE_SPAN_VERIFIED: 100 / 100
- ADD_CANDIDATE-equivalent reusable projection rules: 79
- CASE_SUPPORT_ONLY: 21
- new primitive qi: 0
- new history-memory type: 0
- new Human Gate: 0
- invented numeric palace weights / continuous gains / decay: 0

## Main modeling findings

1. **命宫 corpus contains many timing rules, not only natal character labels.**  
   The source repeatedly defines decade/year “枢纽” and conditions under which an existing natal structure reacts differently. These belong in `TIMING_TRIGGER` or cross-palace response layers, not a flat personality table.

2. **Cross-palace context is indispensable.**  
   财帛、事业、福德、夫妻、父母、疾厄等 palaces repeatedly constrain a 命宫 reading. P01 therefore validates the P00 design choice to keep named cross-palace dependencies explicit.

3. **The same star signal changes meaning by scene.**  
   Example: 贪狼化忌 in a 紫相 chart is translated according to the palace in which it appears; the source itself gives different parent/superior and relationship examples. This supports `SCENE_TRANSLATION`, not one universal event mapping.

4. **Concrete illness, marriage, legal and severe-loss statements stay L3.**  
   They are source-supported but are not promoted into primitive qi.

5. **No scalar shortcut emerged.**  
   紫微、紫破、紫府、紫贪、紫相、紫杀、天机 systems all show conditional compatibility/gating rather than a single palace score.

## History feedback

Three records contain explicit cross-period language and are marked `CHECK_EXISTING_A2_R1`:

- P01-022 — key-period events may affect the life course;
- P01-041 — source uses a persistence expression for 紫贪化禄;
- P01-056 — cooperation in a repeated 紫相 year is said to reverse in the following year.

These are **not** new transitions yet. They must first be deduplicated against existing A2-R1 history rules and operator normalization. No Human Gate is opened.

## Next anchor

Continue 命宫 from:
- 辰戌[天机天梁]后续
- 巳亥天机
- 太阳、武曲、天同、廉贞……
