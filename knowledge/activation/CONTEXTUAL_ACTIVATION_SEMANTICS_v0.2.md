# Contextual Activation Semantics v0.2

Status: **SOURCE-PRESERVING STRUCTURAL LAYER — NO EXECUTION UNLOCK**  
Issue: #451

v0.2 保留 v0.1 的全部边界，只增加本批原文明确出现的两种结构。

## 1. “必须”

`必须` 记录为 `EXPLICIT_NECESSITY`，只约束出现该词的 source-local clause。

它不意味着：
- 所有“见禄”都必须；
- 所有 group shorthand 都变成 ALL；
- 可以绕过成员/关系未决状态直接执行。

## 2. “轻 / 重 / 重重”

`煞轻 / 煞重 / 重重` 等保存为 `SOURCE_ORDINAL_NON_NUMERIC`。

它允许知识库保留“程度有序”的传统信息，但禁止自行写成 0.3/0.7、星数阈值或概率。若未来进入 KB-WP08 Ordinal Registry，可复用这些 source labels。

## 3. 其余边界继续不变

- OR/AND/additive/simultaneous/negation 只按原文局部生效；
- negation 执行前要求 closed-world evidence；
- 前格必须有 dependency edge；
- membership closure != activation quantifier；
- relation binding != member realization；
- no Product runtime compilation。
