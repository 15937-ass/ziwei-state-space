# PL2-F 财帛 Executable Normalization Batch 2

状态：IMPLEMENTED — BOUNDED BATCH

## 1. 范围

本批继续只消费：

- `validation/wp05/W01_wealth_projection_review_001_100.csv`
- P05 财帛宫
- NATAL
- SOURCE_SPAN_VERIFIED
- 非 CASE_SUPPORT_ONLY

PL2-C 的 13 条历史 registry 不修改。本批以独立 overlay 形式新增 9 条，运行时显式 compose。

## 2. 新增 9 条

```text
W01-032  天府：管理留存 != 主动生财
W01-037  化禄 / 化权 / 化科正向资源修饰
W01-039  化权：发挥所化星曜本质求财
W01-041  文昌化忌 / 文曲化忌：文书契约损失
W01-047  魁钺：制度/机构变化收入机会
W01-048  昌曲：名誉提升多于直接收入
W01-049  昌曲化科：文艺/学术类收入
W01-061  擎羊 + 廉贞 + 贪狼，且无火铃
W01-066  火铃：求财困难与投入增加
```

累计 W01 coverage：

- EXECUTABLE: 22
- NORMALIZATION_PENDING: 78
- PATH_DEPENDENT_HOLD: 0
- EXCLUDED: 0

## 3. 为什么这批仍然很小

本批继续拒绝自动处理：

- “前述结构”；
- 三方、会照、对拱；
- 大限/流年叠层；
- “见煞”“百官朝拱”等需要更高层 structure resolver 的条件；
- 含糊的组合简称，如果无法只靠星名 alias 明确展开。

因此没有因为要提高 coverage 而把跨宫/时序条件伪装成同宫布尔条件。

## 4. Name alias 边界

本批只做以下显式名称展开：

- 魁钺 -> 天魁 / 天钺；
- 昌曲 -> 文昌 / 文曲；
- 火铃 -> 火星 / 铃星。

这只是星名 alias normalization，不增加三方、夹、会、冲、对拱等传统结构。

## 5. Registry composition

新增 `compose_wealth_registries()`：

- 历史 batch 保持不可变；
- 新 batch 通过 composition 加入；
- rule_id 重复直接 fail closed；
- source_csv 不一致直接拒绝；
- EvidencePackage 的 knowledge_version 随 executable rule 数更新。

语义层同样通过 `compose_wealth_semantic_registries()` 叠加展示 mapping，不覆盖 PL2-E 基础 section ontology。

## 6. 报告改善

第二批使当前 22-rule 本命报告首次稳定覆盖到：

- 投入与心力成本；
- 名誉与地位介导收入；

并补强：

- 获取机会；
- 生财方式；
- 风险；
- 结构约束。

仍没有单一 wealth score 或净吉凶。

## 7. 下一步

建议 **PL2-G STRUCTURE RESOLVER v0.1**，而不是继续盲目加简单规则。

原因是 W01 剩余 78 条中，大量价值更高的规则已经依赖：

- 三方 / 对宫 / 会照；
- named cross-palace constraints；
- 夹宫；
- “百官朝拱”等结构；
- 大限/流年 time layer。

先补 structure resolver，随后同一批知识可以更安全地进入 executable set，避免把复杂命理结构压扁成错误的同宫条件。
