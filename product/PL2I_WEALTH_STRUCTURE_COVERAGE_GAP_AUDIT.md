# PL2-I 财帛宫 W01 Structure Coverage / Rule-Gap Audit

状态：COMPLETE — PRODUCT EXECUTABILITY AUDIT

## 1. 审计对象

本审计只处理 W01 中尚未 executable 的 72 条记录。

输入：

- canonical source checkpoint：`validation/wp05/W01_wealth_projection_review_001_100.csv`
- 已执行化 B01：13 条
- 已执行化 B02：9 条
- 已执行化 B03：6 条

因此：

```text
W01 total = 100
already executable = 28
pending = 72
```

**重要：** W01 的 condition / target / mode / source location 来自已经 SOURCE_SPAN_VERIFIED 的 source corpus；本文件新增的 `readiness_class`、blocker 和 roadmap 是**产品工程分类**，不是原书新规则，也不改变知识库理论。

## 2. 分类结果

72 条 pending 的 primary readiness：

| readiness_class | 数量 | 含义 |
|---|---:|---|
| LOCAL_ATOM_READY | 14 | 现有 typed atoms 已足够，可进入下一 bounded normalization batch |
| CROSS_PALACE_READY | 7 | PL2-G topology + 现有 atoms 已足够 |
| NEEDS_STRUCTURE_PRIMITIVE | 16 | 仍缺夹宫、会/冲、见煞、百官朝拱、亮度等明确 primitive |
| NEEDS_TEMPORAL_STATE | 14 | 需要大限/流年/重化/跨层状态；其中 13 条本身是非 NATAL，W01-089 是 NATAL 层的 temporal guard |
| NEEDS_PATH_HISTORY | 0 | W01 001–100 没有 history_feedback 标记 |
| NEEDS_VALENCE_MODEL | 5 | 条件使用“吉/不吉、格局大/小”等尚未批准的宫级状态 |
| ANTECEDENT_DEPENDENT | 10 | 条件明确写“前述/上述”或本质上是已有规则的比较/翻译 |
| NORMALIZATION_AMBIGUOUS | 6 | source row 的简称、开放集合或复合语句不足以唯一生成 boolean condition |

合计：72。

## 3. 立即可推进的规则

当前基础设施已经足够、且没有 secondary blocker 的规则共有 **21 条**：

### LOCAL_ATOM_READY — 14

```text
W01-020
W01-045
W01-046
W01-060
W01-068
W01-069
W01-070
W01-072
W01-075
W01-078
W01-079
W01-080
W01-081
W01-082
```

### CROSS_PALACE_READY — 7

```text
W01-002
W01-003
W01-004
W01-005
W01-021
W01-036
W01-056
```

这些记录仍然必须逐条建立 explicit registry + source-drift guard；“READY”只表示**不需要新增 runtime 理论 primitive**，不表示已经自动执行化。

## 4. 为什么不继续盲目批量转换

剩余 51 条不是简单的“再写一些 JSON”：

### 结构 primitive 缺口

当前 PL2-G 只有：

- SELF query
- OPPOSITE
- TRIAD
- 12 宫 local star/transformation facts

尚未定义：

- 夹宫；
- “会 / 冲会 / 会照”的精确定义；
- “见煞”的闭合煞曜集合与关系；
- 百官朝拱；
- 星曜亮度/入庙 executable predicate；
- 若干 named configurations。

如果直接用同宫 presence 代替这些结构，会产生系统性假阳性。

### Temporal state 缺口

14 条以 temporal 为 primary blocker。需要的不是单个 `TIME_LAYER` 标签，而是：

- natal → decade → year 的分层状态；
- 同一星曜跨层重新四化；
- 叠禄；
- 原局 baseline 对 temporal interpretation 的约束；
- 层间冲会/组合。

因此这些应进入 PL3 temporal architecture，而不是塞进 natal runtime。

### Valence 缺口

“宫吉/不吉”“格局大/小”“原局不主富”目前没有批准的可执行变量。

在没有 canonical valence model 前，不允许通过：

- 星数计分；
- 吉星减煞星；
- LLM 主观评级；

来伪造这些条件。

### Antecedent 缺口

10 条依赖“前述/上述结构”或已有规则比较。

后续应给 RuleIR 增加显式 antecedent/reference composition，而不是把前一条自然语言 condition 复制粘贴进后一条。

## 5. Roadmap

建议按风险从低到高推进：

```text
PL2-J  READY RULE BATCH
       14 LOCAL + 7 CROSS-PALACE candidates
       -> bounded sub-batches, explicit normalization

PL2-L  STRUCTURE PRIMITIVES
       clamp / meeting / malefic set / 百官朝拱 / brightness

PL2-M  ANTECEDENT LINKING
       explicit rule dependency and scene-translation inheritance

PL2-N  PALACE VALENCE MODEL
       only after canonical theory/ontology support exists

PL2-O  NORMALIZATION REVIEW
       close shorthand/open-set ambiguity from source-preserving evidence

PL3    TEMPORAL STATE
       decade/year/retransformation/stacked-lu/history
```

PL2-J 应先做，因为它不要求新理论 primitive，可以继续扩大 executable coverage，同时不会阻塞后续 architecture。

## 6. Fail-closed 验证

新增 validator 要求：

- audit 恰好覆盖 W01 − executable；
- 不得重复审计已 executable rule；
- condition / target / mode / source location 必须与 canonical W01 完全一致；
- readiness_class 只能来自固定枚举；
- READY 行不得携带 secondary blocker；
- 所有非 NATAL pending 规则必须归入 NEEDS_TEMPORAL_STATE；
- 若未来 source row 出现 history_feedback，则必须标记 NEEDS_PATH_HISTORY；
- W01 source 一旦变化而 audit 未同步，测试失败。

## 7. 下一工作单元

建议：

**PRODUCT_PL2J_WEALTH_READY_RULE_BATCH**

先消费这 21 条中的低风险子集，而不是同时开启 structure / valence / temporal 三条架构线。
