# PL2-H 财帛跨宫 Executable Batch

状态：IMPLEMENTED — STRUCTURE-BOUND CROSS-PALACE PILOT

## 1. 目标

PL2-G 已把审核后的十二宫 ontology 编译成确定性结构事实。PL2-H 第一次把这些事实真正接入财帛 Rule Runtime。

执行链现在变为：

```text
Normalized Chart Snapshot
 + palace_ontology_v0.1
 -> PL2-G structure facts
 + W01 executable registries
 -> RuleRuntime
 -> EvidencePackage
 -> semantic wealth report
```

## 2. 新增 6 条

本批新增：

```text
W01-001  财帛宫 ↔ 福德宫：必须联读
W01-006  财帛武曲七杀、武曲化忌 + 福德天府化科
W01-013  财帛宫 ↔ 事业宫：三合联读收入性质
W01-014  财帛太阳在巳 + 事业天梁在丑
W01-083  财帛天姚阴煞：须结合命宫与福德宫辨别
W01-100  紫微 + 禄存/化禄同度或对拱
```

累计 W01：

- EXECUTABLE: 28
- NORMALIZATION_PENDING: 72
- PATH_DEPENDENT_HOLD: 0
- EXCLUDED: 0

## 3. Structure dependency

本批 registry 标记：

`requires_palace_structure=true`

只要 B03 被 compose 进 executable registry，而调用方没有提供 PL2-G ontology，runtime 直接 fail closed。

这避免跨宫规则在缺少结构事实时静默“不触发”，造成假阴性。

## 4. W01-001 / W01-013 为什么会常驻

这两条不是具体吉凶预测，而是 source-span verified 的宫位语义边界：

- 财帛与福德必须联读；
- 财帛与事业三合，共同定义收入性质。

因此只要 canonical ontology 验证通过，它们会作为结构性解释规则常驻 EvidencePackage。

它们不会提高 confidence，也不会被当作“好/坏”评分。

## 5. W01-006

条件被拆为完全显式的 atoms：

- P05 ↔ P11 = OPPOSITE；
- P05 武曲；
- P05 七杀；
- P05 武曲化忌；
- P11 天府；
- P11 天府化科。

少任一条件都不触发。

## 6. W01-014

条件同时要求：

- P05 ↔ P09 = TRIAD；
- P05 branch = 巳；
- P05 太阳；
- P09 branch = 丑；
- P09 天梁。

因此不会只凭“太阳 + 天梁”就错误命中。

## 7. W01-083

只在财帛宫同时见：

- 天姚；
- 阴煞；

并确认：

- P01 命宫为 P05 三合宫；
- P11 福德宫为 P05 对宫；

时触发“必须结合命、福语境辨别”的结构规则。

本层不进一步自动判断它最终是损失还是收益。

## 8. W01-100

把“同度或对拱”明确展开为：

- P05 紫微；
- 并且禄存/化禄出现在 P05 同宫，或 P11 对宫；
- P05 ↔ P11 的 OPPOSITE 关系由 PL2-G ontology 提供。

没有把“对拱”泛化成任意会照。

## 9. Semantic section 扩充

PL2-H 增加：

`career_income_relation / 事业与收入联动`

其依据不是产品层新造概念，而是 canonical P05 ontology 已明确：

`secondary_semantic_scope = career_income_relation`

因此 W01-014 的 career-domain 结论可以有合法的产品展示位置。

## 10. 仍然不处理

本批继续冻结：

- “前述结构”；
- 吉/不吉这类尚未有可执行 palace valence 的条件；
- 夹宫；
- 百官朝拱；
- 模糊“会照”；
- 大限/流年；
- 需要 OR-of-conjunctions 但 source normalization 不足以无歧义展开的结构。

## 11. 下一步

建议进入：

**PL2-I WEALTH STRUCTURE COVERAGE + RULE-GAP AUDIT**

目的不是马上再加一批，而是对 W01 剩余 72 条做产品侧可执行性分类：

- LOCAL_ATOM_READY；
- CROSS_PALACE_READY；
- NEEDS_STRUCTURE_PRIMITIVE；
- NEEDS_TEMPORAL_STATE；
- NEEDS_PATH_HISTORY；
- NEEDS_VALENCE_MODEL；
- ANTECEDENT_DEPENDENT；
- NORMALIZATION_AMBIGUOUS。

这样下一轮扩展会从“挑规则”升级为一张明确的 executable roadmap。
