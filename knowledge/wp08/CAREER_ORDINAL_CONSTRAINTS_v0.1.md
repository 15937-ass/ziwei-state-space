# Career Ordinal / Constraint Registry v0.1

Status: **Career source scan complete — no numericization**  
Issue: #461

## 覆盖
- source: SRC-ZZ-003 事业宫 printed pp132–155
- source spans scanned: **24**
- broad candidate sentences: **131**
- accepted candidate sentences: **118**
- excluded after critic filter: **13**
- normalized ordinal/constraint records: **130**

## 类型
- SOURCE_LOCAL_EMPHASIS: 27
- MORE_IMPORTANT_THAN: 1
- DEGREE_LABEL_ONLY: 27
- ESPECIALLY_AVOID: 12
- STRONGER_THAN: 10
- WEAKER_THAN: 7
- ESPECIALLY_PREFERRED: 24
- LESS_PREFERRED_THAN: 1
- PREFERRED_OVER: 11
- LESS_STABLE_THAN: 1
- MORE_PRONOUNCED_THAN: 4
- RANKED_AHEAD_OF: 5

## 这批具体冻结了什么
包括“本宫星曜远比对宫星曜重要”、多处“名大于利/名重于利”、宫位配置优劣、武曲化禄优先于禄存、戌宫上格未宫次之、夜生人优先于日生人、人和第一技能次之、破军与七杀在开创力/风险/毅力上的明确比较，以及大量“最喜/最忌/煞轻/煞重/尤其”等来源定性信息。

## Critic
对 target 或 condition 本身带关键 OCR 不确定性的句子不做静默修复。本轮额外排除了：
- printed p145 “廉贞化安者尤为吉利”；
- printed p146 “空劫又同瞍耆，最宜艺术……”。
它们保留在 candidate audit 中，待未来视觉源页校订，不进入 canonical ordinal constraint。

所有 degree / emphasis 都保持非数值。
