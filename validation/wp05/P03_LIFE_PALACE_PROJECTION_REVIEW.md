# WP05 P03 — 命宫 Projection Corpus Checkpoint 3

Status: **CHECKPOINT_CLOSED_SOURCE_SPAN_VERIFIED**

## Scope

- source: SRC-ZZ-003《中州派紫微斗数深造讲义（下册）》
- chapter: 命宫
- source span: rendered lines 317–422
- reviewed projection records: P03-201 … P03-300

## Result

- reviewed: 100
- SOURCE_SPAN_VERIFIED: 100 / 100
- reusable projection rules: 89
- CASE_SUPPORT_ONLY: 11
- history-feedback items: 2
- new primitive qi: 0
- new history-memory type: 0
- new Human Gate: 0
- invented numeric palace weights / continuous gains / decay: 0

## Main findings

1. **天同 confirms non-monotonic modifier semantics.**  
   辅佐可变成依赖，煞忌在部分结构中反可形成激发，说明“吉曜=正、煞曜=负”的标量编码不可用。

2. **天同的时间层作用高度显式。**  
   七杀、杀破狼、天相、机梁等宫垣多次作为大限/流年枢纽，继续支持 `TIMING_TRIGGER` 作为独立层。

3. **心理、资源、职业与关系结果可并存而不互相替代。**  
   同巨化禄可有财禄，同时仍有隐衷；这类记录不能折成单一总体好坏分。

4. **廉贞表现出明显的 scene translation。**  
   同一廉贞状态可在关系、政治/理想、服务策略、职业、健康等场景中出现不同投影，因此必须保持 palace/scene 层。

5. **传统具体断语继续留在 L3 / CASE_SUPPORT_ONLY。**  
   疾病、死亡、自伤、婚配、具体古代职业等不向底层气核回写。

## History feedback

- P03-222：戊年同阴结构存在“历艰危立业后，因疑忌再破”的跨阶段语义。
- P03-287：未宫廉杀有“历艰辛而成积富”的阶段性路径语义。

两条均只标记 `CHECK_EXISTING_A2_R1`，先与既有 PATH_DEPENDENT_GATE 去重，不新增 memory type。

## Next anchor

Continue 命宫 from:
- 寅申廉贞后续
- 卯酉廉破
- 辰戌廉府
- 巳亥廉贪
- then 天府
