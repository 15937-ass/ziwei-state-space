# WP05 P04 — 命宫 Projection Corpus Checkpoint 4

Status: **CHECKPOINT_CLOSED_SOURCE_SPAN_VERIFIED**

## Scope

- source: SRC-ZZ-003《中州派紫微斗数深造讲义（下册）》
- chapter: 命宫
- source span: rendered lines 421–455 + printed pp13–15
- reviewed projection records: P04-301 … P04-400

## Result

- reviewed: 100
- SOURCE_SPAN_VERIFIED: 100 / 100
- reusable projection rules: 88
- CASE_SUPPORT_ONLY: 12
- history-feedback items: 0
- new primitive qi: 0
- new history-memory type: 0
- new Human Gate: 0
- invented numeric palace weights / continuous gains / decay: 0

## Cumulative WP05 命宫 result after P01–P04

- reviewed: 400
- reusable projection rules: 326
- CASE_SUPPORT_ONLY: 74
- history-feedback items queued for A2-R1 deduplication: 6

## Main modeling findings

1. **天府 validates explicit cross-palace gating.**  
   “逢府看相” is insufficient by itself; the source also requires checking 七杀. The model therefore keeps 天相/七杀 as named dependencies rather than collapsing them into a single palace-strength score.

2. **空库/露库 are discrete structural states, not numeric penalties.**  
   Empty/exposed-store behavior changes again with 七杀、天相、禄 and 夹局 conditions.

3. **Resource, status and decision dimensions stay separate.**  
   紫微化科 can emphasize status without equivalent wealth; 武曲化禄 in 命宫 emphasizes financial decisiveness; 禄存 can instead produce a more conservative/惜财 expression.

4. **太阴 confirms cross-palace psychological projection.**  
   命宫太阴 must explicitly inspect 福德宫巨门, especially for mental enjoyment. This strengthens the P00 decision to model scene dependencies directly.

5. **Diagnostic, criminal, death/self-harm and traditional family claims remain L3.**  
   They are retained as source-supported CASE_SUPPORT_ONLY records and are not treated as medical, legal or personality facts.

## Decontamination

No new gate is required. No source passage in this batch justifies:
- a new primitive qi dimension;
- a new memory class;
- a decay/forgetting parameter;
- continuous palace weights;
- a global good/bad scalar.

## Next anchor

Continue 命宫 from:
- 太阴后续（日月会照、反背、羊陀空劫等）
- 贪狼
- 巨门
