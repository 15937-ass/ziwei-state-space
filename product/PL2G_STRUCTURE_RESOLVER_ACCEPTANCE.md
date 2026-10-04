# PL2-G Palace Structure Resolver v0.1

状态：IMPLEMENTED — ONTOLOGY-BOUND STRUCTURE FACTS

## 1. 目标

PL2-F 后，W01 已有 22/100 条规则可执行。继续只增加“本宫单星/四化”规则的边际收益开始下降，剩余高价值规则大量依赖跨宫关系。

PL2-G 因此不直接新增传统断语，而是增加一个确定性的 palace structure resolver：

```text
Normalized Chart Snapshot
 + knowledge/wp05/palace_ontology_v0.1.csv
 -> canonical 12-palace binding
 -> opposite / triad relations
 -> all-palace star + transformation facts
 -> RuleRuntime-ready fact set
```

## 2. Canonical source

本 resolver **不自行计算宫位语义关系**。

它直接消费已经审核进入知识层的：

`knowledge/wp05/palace_ontology_v0.1.csv`

该 ontology 已明确给出每个宫位的：

- palace_id；
- canonical_name；
- legacy_alias；
- opposite_palace；
- triad_palace_1；
- triad_palace_2；
- source_basis；
- epistemic/status。

产品层只把这些已审核关系编译成 runtime structure facts。

## 3. Ontology validation

进入 runtime 前必须满足：

- 恰好 12 宫；
- palace_id 唯一；
- canonical / legacy label 无歧义；
- 所有行均为 ACTIVE；
- 对宫关系双向对称；
- 三合关系形成闭合三元组；
- 对宫、两个三合宫互不重复且不指向自身。

任一条件失败即 fail closed。

## 4. Snapshot binding

resolver 支持：

- schema v0.1 风格 `chart.palaces`；
- P1 v0.2 风格 `natal.palaces`；
- canonical name；
- canonical name 去掉“宫”的显示形式；
- ontology 已登记 legacy alias 及其去“宫”形式。

如果某外部引擎使用 ontology 未登记的显示名，必须由 adapter 显式传入 `extra_aliases`。resolver 不猜别名。

## 5. v0.1 输出关系

当前明确输出：

- SELF（查询接口）；
- OPPOSITE；
- TRIAD；
- 三方四正成员集合（查询接口，= 本宫 + 两个 triad + opposite）。

Runtime facts 中使用显式：

`PALACE_RELATION(source, target, relation=OPPOSITE|TRIAD)`

避免把“会照”写成一个模糊布尔量。

## 6. 跨宫事实

PL2-G 首次能够为 12 宫全部输出：

- `PALACE_PRESENT`
- `BRANCH_PRESENT`
- `PALACE_HAS_STAR`
- `TRANSFORMATION_PRESENT`
- `PALACE_RELATION`

因此下一批规则可以安全表达例如：

```text
P05 武曲化忌
AND P11 天府化科
AND relation(P05, P11) = OPPOSITE
```

而不需要从“财帛武杀、福德天府”这类文字临时猜宫位关系。

## 7. 本阶段明确不实现

### 夹宫

现有 `palace_ontology_v0.1.csv` 没有“夹宫”字段。PL2-G 不通过地支顺序自行补写传统夹宫语义。

### 模糊“会照”

v0.1 不把“会照”直接变成一个 atom。后续 normalization 必须明确它实际需要：

- triad；
- opposite；
- 或二者组合。

### 时间层

PL2-G 只解决 natal palace topology。大限、流年仍留给 PL3 temporal state。

## 8. 测试

测试验证：

- P05 财帛宫对宫=P11 福德宫；
- P05 三合=P01 命宫 + P09 事业宫；
- ontology 对宫对称、三合闭合；
- legacy alias 可确定性绑定；
- 跨宫星曜/四化事实可生成；
- snapshot 顺序不影响结果；
- 未登记宫名 fail closed；
- adapter 可显式提供 engine-specific alias；
- ontology 关系损坏时拒绝执行。

## 9. 下一步

建议下一工作单元：

**PL2-H WEALTH CROSS-PALACE EXECUTABLE BATCH**

优先解锁已经具备明确 ontology 支持的 W01：

- 财帛宫 ↔ 福德宫；
- 财帛宫 ↔ 事业宫；
- 财帛宫 ↔ 命宫；

但仍继续避开：

- “前述结构”；
- 夹宫；
- 未解析的会照语义；
- 大限/流年；
- 需要新理论判断的复杂组合。

这样可以第一次把结构 resolver 真正接入 RuleRuntime，同时保持每条结论可追溯。
