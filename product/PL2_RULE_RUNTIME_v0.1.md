# PL2 Rule Runtime v0.1

状态：IMPLEMENTED — CORE CONTRACT

## 目标

把已经审核过的 canonical knowledge 转成产品可执行 Rule IR，同时禁止产品层为了“能跑”而偷偷解释传统文本。

运行链：

```text
reviewed rule row
  -> provenance gate
  -> normalization gate
  -> condition compilation
  -> RuleIR
  -> deterministic matcher
  -> ActiveRuleGraph
  -> downstream EvidencePackage
```

## v0.1 的硬门槛

一条规则只有同时满足以下条件才可进入 executable set：

1. `review_status` 为 `SOURCE_SPAN_VERIFIED` 或 `HUMAN_VERIFIED`；
2. `source_span_verified=true`；
3. `normalization_verified=true`；
4. normalization 不是 `HYPOTHESIS` / `UNRESOLVED`；
5. source 不是 `UNRESOLVED_SOURCE`；
6. operator、target type、normalized target 与 source pointer 完整。

因此“有原文”与“可执行”是两个不同状态。

## 条件处理策略

v0.1 **不使用字符串关键词、正则或 LLM 猜测 free-text condition 的含义**。

- `condition=无`：可直接形成 subject-only rule；
- 非空条件：必须由显式 `condition_registry` 提供结构化 atoms；
- 没有 atoms 的规则进入 `NEEDS_CONDITION_NORMALIZATION`，不会偷偷执行。

这一步是为了防止把“文昌文曲会合”“三方四正见禄”等自然语言条件误编译成错误布尔逻辑。

## RuleIR 最小字段

每个节点保留：

- rule_id；
- school；
- source work/location；
- review/source/normalization epistemic；
- subject/context；
- required facts；
- time/palace/topic scopes；
- operator；
- target type/state；
- symbolic state change；
- valence；
- conflict group；
- evidence text。

## ActiveRuleGraph

`RuleRuntime.match(...)` 只对 RuleIR 做确定性集合匹配：

- required facts 必须全部满足；
- time / palace / question scope 必须匹配；
- 结果按 rule_id 固定排序；
- 同 conflict group 的规则同时保留，不自动择一；
- before state 原样读取；
- after state 仅记录 symbolic operator/delta，不伪造连续数值或权重。

## 明确不做

v0.1 不做：

- 自由文本规则解析；
- 自动参数赋值；
- LLM 选规则；
- 冲突静默消解；
- case-support-only 升格；
- 跨流派多数投票；
- 事件预测。

## 下一步

PL2-B：

1. 建立 canonical `condition_atoms` sidecar/schema；
2. 从已 source-verified、normalization-verified 的事业/财帛规则开始编译小批 executable set；
3. 生成编译覆盖率：EXECUTABLE / BLOCKED_PROVENANCE / BLOCKED_NORMALIZATION / NEEDS_CONDITION_NORMALIZATION；
4. 接入 EvidencePackage；
5. 再进入 PL3 事业/财帛 Inference MVP。
