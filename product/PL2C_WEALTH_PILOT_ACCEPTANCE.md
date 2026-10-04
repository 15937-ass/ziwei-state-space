# PL2-C 财帛宫 Executable Pilot v0.1

状态：IMPLEMENTED — BOUNDED PILOT

## 1. 范围

本 checkpoint **只消费**已经进入 GitHub canonical state 的：

- `validation/wp05/W01_wealth_projection_review_001_100.csv`
- 财帛宫 P05
- NATAL
- SOURCE_SPAN_VERIFIED
- 非 CASE_SUPPORT_ONLY

没有重新解释原书，也没有扩大 source review。

## 2. Pilot 选择

W01 共 100 条。本次只选择 13 条条件足够直接、可以在 Normalized Chart Snapshot 中确定性观察的规则：

```text
W01-025  化禄
W01-026  禄存且无天马
W01-028  武曲
W01-029  太阴
W01-031  天府
W01-038  化禄
W01-040  化忌
W01-042  文曲化忌
W01-058  擎羊
W01-090  紫微
W01-091  紫微
W01-092  紫微
W01-097  紫微化科
```

其余 87 条**没有被自动解释**，当前保持 `NORMALIZATION_PENDING`。

因此本阶段 coverage 是：

- EXECUTABLE: 13
- NORMALIZATION_PENDING: 87
- PATH_DEPENDENT_HOLD: 0
- EXCLUDED: 0

这不是“只有 13 条有效”，而是“当前只对 13 条完成了可审计运行时 normalization”。

## 3. 为什么只做 13 条

W01 其余记录大量包含：

- “前述结构”；
- 跨宫条件；
- 多星组合；
- 三方/对拱；
- 时序条件；
- 比较关系；
- 隐含例外。

如果用关键词或 LLM 一次性把这些条件翻成布尔逻辑，会把 source review 与 executable normalization 混在一起，产生不可审计的假精度。

PL2-C 先证明最小链路：

```text
SOURCE_SPAN_VERIFIED projection rule
 -> explicit normalization registry
 -> typed condition atoms
 -> RuleIR
 -> chart-fact extraction
 -> deterministic RuleRuntime
 -> ActiveRuleGraph
```

## 4. Source drift guard

Registry 同时保存：

- expected condition；
- expected projection target；
- expected projection mode。

如果 canonical W01 记录被修改而 registry 未同步，编译直接失败，不允许悄悄继续执行。

## 5. Snapshot fact extraction

当前只抽取 pilot 必需的确定性事实：

- P05 是否存在；
- 财帛宫星曜；
- 星曜四化；
- 财帛宫地支；
- subject=财帛宫。

不计算新的命理结论，不推断“百官朝拱”“三方四正”“禄马交驰”等高级结构。

## 6. 认识论说明

W01 checkpoint 导出表没有单独导出 `source_epistemic` 列，因此产品层**没有擅自补写 EXPLICIT/INFERRED**。

运行 trace 中只保留事实：

`WP05_SOURCE_SPAN_VERIFIED`

本次 `normalization_epistemic=IMPLEMENTATION` 只描述“把已审核条件映射到运行时 atom”这个工程步骤，不改变传统规则本身。

## 7. 下一步

PL2-D：

1. 把 ActiveRuleGraph 结构化转换成 EvidencePackage；
2. 给 13 条 pilot 加 contrastive/conflict 输出；
3. 建立一个无 LLM 的财帛结构化 inference sample；
4. 再扩第二批条件 normalization，而不是直接吞掉 932 条；
5. 接近 PL3 时再引入本命 + 大限 + 流年的联合时序输入。
