# KB-WP02 十四正曜全文规则抽取完成报告

状态：COMPLETE（相对于《深造讲义（上）》十四正曜书内页5–32）

## 1. 覆盖范围

本模块覆盖《中州派紫微斗数深造讲义（上）》十四正曜章节：

- 紫微：书内页 5–6
- 天机：7–8
- 太阳：9–10
- 武曲：11–12
- 天同：13–14
- 廉贞：15–16
- 天府：17–18
- 太阴：19–20
- 贪狼：21–22
- 巨门：23–24
- 天相：25–26
- 天梁：27–28
- 七杀：29–30
- 破军：31–32

## 2. 两轮抽取结果

Canonical rule file：

`knowledge/rules/stars/major_stars_canonical_v0.1.csv`

共 **430 条 reviewed rules**。

各星规则数：

- 紫微 43
- 天机 39
- 太阳 40
- 武曲 41
- 天同 25
- 廉贞 27
- 天府 25
- 太阴 26
- 贪狼 29
- 巨门 26
- 天相 27
- 天梁 26
- 七杀 26
- 破军 30

## 3. Schema / KB 完整性

关键字段检查：

- rule_id：430/430
- source_work：430/430
- source_location：430/430
- condition：430/430
- target_literal：430/430
- target_normalized：430/430
- operator：430/430
- state_change：430/430
- valence：430/430
- epistemic_type_source：430/430
- evidence_text：430/430
- coverage_unit_id：430/430

关键字段完整率：**100%**。

## 4. 规则族分布

当前 canonical 规则族包括：

- definition：36
- structural_rule：62
- projection_rule：78
- comparison：15
- modifier_or_interaction：176
- temporal_response：24
- state_property：39

这说明十四正曜章节本身并非只有“星性描述”，还包含大量：
- 条件修正；
- 结构关系；
- 四化/运限反应；
- 宫位/现实投影；
- 比较与优先序。

这进一步支持 G1–G5 所采用的分层和算子化架构。

## 5. 双遍完整性审计

`validation/major_stars_extraction_ledger.csv` 记录十四个 coverage units 的：

- Pass 1 extraction：complete
- Pass 2 extraction：complete
- Source span recheck：complete
- unresolved_count：0

源文中未进入 rule object 的剩余文字被归入：
- commentary；
- illustrative quotation；
- duplicate support；
- non-executable description。

因此本模块可标记为 COMPLETE。

## 6. 认识论边界

COMPLETE 的含义是：

> 相对于当前固定版本《深造讲义（上）》十四正曜书内页5–32，项目已完成可执行规则的两轮内部抽取、归一化、来源定位和页段复核。

不表示：
- 十四正曜在所有中州派著作中的全部知识都已穷尽；
- 初级讲义相关规则已全部并入；
- 六十星系、宫位、化曜对十四星的后续反馈已经全部回写；
- 这些规则已获现实预测验证。

后续可通过 KB-WP03～05 发现新的交互规则，再以版本化方式补入 v0.2。

## 7. 对推演引擎的意义

现在十四正曜不再依赖 LLM 自由回忆。

推演时可直接通过：

~~~text
star
-> canonical Rule IDs
-> latent/core mapping
-> modifier conditions
-> structural relations
-> provenance
~~~

获得可追溯的基础气核和条件规则。

## 8. 下一步

进入 KB-WP03：

> 六十星系全文规则与反应原则库。

该阶段将从当前“60项索引 + principal mode”扩展到每个星系的：
- 三方四正构成；
- 本质判别；
- 四化条件；
- 辅佐煞曜条件；
- 运限枢纽；
- 原文案例；
- interaction_delta evidence；
- 与单星气核的可约化/涌现关系。
