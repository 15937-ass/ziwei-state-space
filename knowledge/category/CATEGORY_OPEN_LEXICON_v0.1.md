# Category / Open Lexicon v0.1

Status: **SCOPED KNOWLEDGE REPRESENTATION — NO EXECUTION UNLOCK**  
Issue: #442

## 1. 本轮解决什么

Relation Binding 已经知道“关系词作用于哪个 source node”，但其中仍有 59 个 target 被标为 `OPEN_CATEGORY_NODE`。本轮不去猜 ANY/ALL，也不直接编译规则，而是先区分“成员真的能闭合”与“只能保留开放类名”。

事业宫当前 59 个 occurrence 共 **18 个 distinct source surfaces**。

## 2. 可以闭合的基础成员类

- **辅佐诸曜**：来源明确“辅佐八曜”，辅曜四星 + 佐曜四星。成员表可闭合，但单星/对星/全体触发仍未决。
- **煞曜**：来源明确四煞为擎羊、陀罗、火星、铃星；加地空、地劫为六煞。成员表可闭合，但“见煞”不因此自动变成 ANY 或 ALL。
- **羊陀**：可保存为擎羊+陀罗的 pair shorthand；pair 成员已知不等于触发量词已知。
- **吉化**：来源用语支持化禄、化权、化科作为 favorable transformation class；不表示强度或必然吉应。

## 3. 仍保持开放的类别

`吉曜 / 凶曜 / 桃花 / 桃花诸曜` 保持 open-world；`吉 / 凶` 视为 valence shorthand，而不是固定星曜成员表。

`辅佐吉曜` 的底层“辅佐八曜”成员可知，但“吉”是语境限定，因此不把八曜静默解释成每句都全部触发。

## 4. 复合短语不扁平化

`煞忌 / 吉化吉曜 / 刑耗 / 煞刑诸曜 / 煞耗 / 煞耗诸曜` 统一保留为 source compound category。能识别的 component 可以引用基础类，但隐含连接词仍为 **UNSPECIFIED_SOURCE_BUNDLE**，禁止擅自改写成 AND/OR。

## 5. 结果

- 59 / 59 OPEN_CATEGORY occurrences 已 disposition；
- 18 / 18 source surfaces 已进入 lexicon；
- source resolution changes = 0；
- conditions compiled = 0；
- execution unlocked = 0；
- Product runtime changes = 0；
- numeric weights / probabilities = 0。

下一步不是继续扩 relation 词，而是评估这些 category node 与 **contextual activation / response semantics** 的交叉，优先处理能由原文明确给出局部“单星/对星/同时/无煞”等 activation 约束的条目。
