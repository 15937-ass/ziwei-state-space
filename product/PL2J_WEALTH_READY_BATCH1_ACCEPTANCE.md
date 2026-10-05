# PL2-J Wealth Ready Rule Batch 1 — B04

状态：IMPLEMENTED — DATA-ONLY EXECUTABLE EXPANSION

## 1. 目标

PL2-I 已把 W01 剩余 72 条分成明确的产品 readiness taxonomy，并确认 21 条当前基础设施已经足够。

PL2-J 不新增 runtime primitive。本批只从其中挑选 **10 条无 secondary blocker 的 READY 规则**做 explicit normalization。

因此这一批验证的是一个重要产品能力：

> 在 runtime 架构稳定后，新增一批规则应主要表现为“受审计的数据增量”，而不是不断修改推理代码。

## 2. 本批 10 条

```text
W01-002  福德宫影响生财难易
W01-003  福德宫反映生财过程的心力/运筹方式
W01-005  财帛宫与福德宫需综合判断
W01-020  财帛宫所主：赚钱能力与机会
W01-021  命宫格局尺度与财帛能力需要区分
W01-036  田宅宫也表征自己经营店号
W01-046  财帛宫见辅弼：独立经营可行性
W01-068  火星 + 天机 + 禄星
W01-069  火星 + 破军 + 禄星
W01-070  火星 + 地空 + 禄星
```

累计 W01：

- EXECUTABLE: 38
- NORMALIZATION_PENDING: 62
- PATH_DEPENDENT_HOLD: 0
- EXCLUDED: 0

## 3. 为什么只消费 10 / 21

PL2-I 的 READY 含义是“当前 primitive 足够”，并不意味着应该一次性吞掉全部 21 条。

本批优先选择：

- 宫位语义边界明确；
- relation 已由 PL2-G 给出；
- 组合可以直接写成有限 all/any atoms；
- 现有 semantic section 已能容纳；
- 不需要增加新的展示 ontology。

剩余 READY 规则继续保留到下一 bounded batch。

## 4. 明确 alias

本批只新增两个显式 alias normalization：

### 辅弼

`辅弼 -> 左辅 OR 右弼`

用于 W01-046。

### 禄星

本批把 W01-068/069/070 中的“禄星”冻结为：

`禄存 OR 任一 P05 化禄`

即：

- P05 有禄存；或
- P05 任一星曜带 `mutagen=禄`。

不把化权/化科算作禄星，也不跨宫寻找禄。

## 5. 数据优先

本 PR 不修改：

- RuleRuntime；
- condition atom schema；
- palace structure resolver；
- EvidencePackage；
- semantic aggregation engine。

只新增：

- B04 executable registry；
- B04 semantic overlay；
- tests；
- sample tool；
- acceptance。

这说明 PL2-A ~ PL2-H 的底层已经开始具备“规则数据化增长”的形态。

## 6. PL2-I readiness guard

测试要求 B04 中每个 rule_id：

1. 必须存在于 PL2-I gap audit；
2. primary class 只能是 `LOCAL_ATOM_READY` 或 `CROSS_PALACE_READY`；
3. secondary blocker 必须为空。

所以不能绕过 PL2-I 直接把 blocked rule 偷渡进 executable set。

## 7. Confidence

38/100 仍有 62 条未 normalization，因此 PL2-D confidence policy 不变：

`LOW_CONFIDENCE`

规则数量增加不会自动提高到 MEDIUM/HIGH。

## 8. PL2-I READY 剩余

本批消费 10 条后，原 21 条 READY 中还剩 11 条：

```text
W01-004
W01-045
W01-056
W01-060
W01-072
W01-075
W01-078
W01-079
W01-080
W01-081
W01-082
```

建议下一工作单元：

**PRODUCT_PL2J2_WEALTH_READY_RULE_BATCH**

其中 W01-004 / W01-045 需要先给产品展示层补 `consumption` / `support` 合法栏目；其余则继续逐条冻结组合条件。
