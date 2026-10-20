# 事业宫 blocker ontology backlog v0.1

Issue #406。事业宫 canonical Career 已完成 888/888 structured-ID closure。本工作单元不再逐条补规则，而是把严格复核阶段留下的 **513 条 BLOCKED_OUTCOME_MAPPING** 转换为下一阶段可执行的 ontology backlog。

## 1. 当前闭合状态

- canonical Career rules：888
- strict-review rules：836
- COMPLETE_CONDITION_MAPPING：216
- METHODOLOGY_OR_CONTEXT_ONLY：107
- BLOCKED_OUTCOME_MAPPING：513
- pre-hundred specialized structured IDs：52
- unique structured IDs：888 / 888

这里的 888/888 表示**每个 canonical ID 都有可追溯 disposition**，不表示 888 条都已经可执行。

## 2. 513 条 blocker 全量分布

- GROUP: 171
- COMPOSITE: 92
- RELATION: 74
- RELATION_AND_GROUP: 59
- CONTEXT_STATE: 43
- TEMPORAL: 17
- ABSENCE_AND_GROUP: 16
- DIGNITY: 13
- ACTION: 6
- ABSENCE: 6
- VALENCE: 5
- DIGNITY_AND_GROUP: 5
- EXAMPLE: 3
- UNMODELED_STATE: 2
- DIGNITY_AND_RELATION: 1

最大的单一类别是 GROUP=171；如果把 GROUP 与 relation/absence/dignity 的交叉 blocker 一并计算，**251 条 blocked records 直接触及 group/quantifier 语义**。这使群组语义成为下一阶段的第一优先级。

## 3. 词汇层观察：只做 census，不做解释

以下数字是对 `source_condition_text` 的字面子串统计，只用于定位术语密度；它们不是 ontology 定义，也不能用来推导 ANY/ALL 等量词。

### 群组词

- 空劫: 37
- 吉曜: 32
- 火铃: 24
- 昌曲: 22
- 煞曜: 17
- 辅弼: 11
- 刑耗: 11
- 魁钺: 10
- 桃花: 10
- 禄马: 8
- 羊陀: 7
- 四煞: 6
- 三台八座: 4

其中“空劫”“吉曜”“火铃”“昌曲”最常反复出现。问题不只是“有哪些成员”，更重要的是原文往往没有明确说：
- 是任一成员即可；
- 两颗同时出现；
- 至少 N 颗；
- 还是一个传统命名结构整体。

因此**不能通过建立星曜集合就自动解锁 GROUP blocker**。

### 空间关系词

- 会: 83
- 夹: 18
- 同会: 16
- 借会: 6
- 相会: 6
- 三方: 6
- 同拱: 4
- 相对: 4
- 对拱: 2
- 会照: 1

单字“会”在 blocked conditions 中出现 83 次，是最危险的高频模糊词之一。“同会”“同拱”“借会”“相会”也都有独立出现。

当前已经支持明确 OPPOSITE 的地方，只来自原文明确“对宫/相对”等可定位几何；本 backlog 不把“会”自动扩张成固定宫位集合。

### 庙陷 / 缺席 / 现实输入 / 时间

- 入庙：12
- 落陷：11
- 无煞：16
- 不见：8
- 无禄：8
- 从商：9
- 从政：6
- 大运：6
- 流年：6
- “前格”：139

“前格”高频出现再次说明来源规则存在大量继承链；后续 ontology 改造不能破坏已经显式保存的 inherited_source_rule_ids。

## 4. 推荐工作流顺序

### P1 — GROUP / QUANTIFIER

影响面：251 条（非互斥工作流统计，包含 GROUP 与其交叉 blocker）。

安全前置工作可以直接做：建立**群组词典、来源成员证据、显式量词词汇表**。但“没有量词时默认 ANY 还是 ALL”属于 canonical semantics，必须进入 Human Gate：

**HG-KB-GROUP-QUANTIFIER-01**

### P2 — SPATIAL RELATION

影响面：134 条。

先建立“会 / 同会 / 会照 / 同拱 / 借会 / 相会”等来源例句矩阵，和已经可确定的“相对/对宫”分开。真正把这些词映射到 palace graph 前，需要：

**HG-KB-SPATIAL-RELATION-01**

### P3 — COMPOSITE PATTERN

影响面：92 条。

包括夹宫、三方四正、命名格局、多段联合前件。核心架构问题是：财荫夹、刑忌夹、府相朝垣、阳梁昌禄等究竟是 primitive facts，还是由基础事实推导的可审计 macros。

候选 gate：

**HG-KB-COMPOSITE-PATTERN-01**

### P4 — REAL-WORLD CONTEXT INPUT

影响面：51 条（CONTEXT_STATE + ACTION + UNMODELED_STATE）。

包括从商、从政、从医、任职、自行经营、学历、资历，以及最后尾批暴露出的显式性别条件等。这一层不应进入 Natal facts，而应成为独立 external/context inputs。

候选 gate：

**HG-KB-CONTEXT-INPUT-01**

### P5 — ABSENCE

影响面：22 条。

核心不是语法，而是逻辑世界观：未观察到某星，是否可以视为不存在？当前项目坚持 **silence ≠ negative**。若未来要执行“无煞/不见禄”等规则，需要先定义完整命盘快照中的 explicit-negative 生成方式。

候选 gate：

**HG-KB-ABSENCE-01**

### P6 — DIGNITY

影响面：19 条。

需要解决 canonical 庙旺利陷数据源、枚举以及不同传统表格冲突问题。

候选 gate：

**HG-KB-DIGNITY-01**

### P7 — TEMPORAL / PATH

影响面：17 条。

包括大运、流年、克应期、连续三四年、先挫折后转业等。这里需要区分：
- point trigger；
- interval/window；
- path dependency；
- temporal environment 与 manifestation。

候选 gate：

**HG-KB-TEMPORAL-WINDOW-01**

### P8 — VALENCE / EXAMPLE

共 8 条。主要是比较性质或例示边界，可以继续作为 methodology/context annotation，不急于建立执行 semantics。

## 5. 为什么先做 GROUP，而不是直接做 relation

GROUP 的直接/交叉影响面最大，而且“空劫、昌曲、火铃、辅弼、魁钺”等词贯穿多个主星系。

但下一工作单元也只能先做**来源词典与显式量词证据**。不能在没有 PI gate 的情况下写：
- 空劫 = 地空 OR 地劫；
- 空劫 = 地空 AND 地劫；
- 吉曜 = 任一吉曜；
- 煞曜 = 任一煞曜。

这些默认值都会改变传统规则的触发范围。

## 6. 与状态空间架构的关系

513 条 blocker 已经自然分出三种不同层：

1. **Natal observation language 缺口**：group、relation、composite、absence、dignity；
2. **External/control input 缺口**：context-state、action、学历资历等；
3. **Dynamic evolution 缺口**：temporal window、path dependency。

这与既定推演链条是相容的：

`PL3-N Natal Prior → PL3-T Temporal Environment → PL3-S Personal State → PL3-M Manifestation`

因此下一阶段不是把所有 blocker 都塞进 Natal，而是决定每类语义属于哪个状态层。

## 7. 本工作单元没有做什么

- 没有新增 condition atom；
- 没有新增群组默认量词；
- 没有定义“会照”的宫位集合；
- 没有引入 closed-world assumption；
- 没有新增庙陷表；
- 没有解锁任何 blocked rule；
- 没有修改 Product/runtime。

下一工作单元建议进入 **WS-GROUP-QUANTIFIER 的 source-grounded lexicon inventory**。它仍可在不触发 Human Gate 的情况下先做证据整理；真正给群组设执行语义时再请 PI 决策。
