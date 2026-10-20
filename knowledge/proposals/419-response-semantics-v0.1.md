# Proposal 419 — Response Semantics v0.1

Status: **IMPLEMENTING — PI APPROVED BOUNDED SCOPE**  
Tracking Issue: #419  
Lane: KNOWLEDGE_ONLY

## Motivation

Career 事业宫 888 条 source review 已完成；其中 GROUP-related blocker 251/251 已完成来源审查。旧 Human Gate `HG-KB-GROUP-QUANTIFIER-01` 把主要问题表达成“未明示 shorthand 应默认 ANY 还是 ALL”。

后续 PI 讨论指出，该二选一模型过粗。像“火铃”“昌曲”等简称至少可能同时涉及：
- 成员 identity；
- 单成员是否有效；
- 成员之间是否有强弱差异；
- 双成员是否出现增强、门控或质变；
- 同度、会照、夹、对拱等 relation；
- 上下文限定。

因此 GROUP 不应同时承担 membership 与 executable response 语义。

## Goals

1. 把 lexical membership 与 activation / interaction / relation 分离。
2. 新增一个最小 Response Semantics schema，允许来源支持的结构化语义进入 KB。
3. 保留 `UNSPECIFIED`，禁止给未明示 shorthand 自动补 ANY/ALL。
4. 允许 source-explicit ordinal constraint，但禁止提前数值化。
5. 用少量已审来源建立 pilot，不批量迁移 888 条规则。
6. 将完整动态/经验建模原则写成 future guidance，但不在本 work unit 实现。

## Non-Goals

- 不修改 Product runtime。
- 不实现 TendencyField / ResponseProfile runtime。
- 不训练连续权重或概率。
- 不引入 JAX / NumPyro / factor graph / neural state-space。
- 不建立人的完整决策模型。
- 不自动解锁 251 blockers。
- 不重写历史 closure artifact。
- 不把“吉/凶”做 primitive latent dimension。

## Current Problem

旧抽象：

```text
火铃 -> GROUP -> choose ANY or ALL
```

不能表达下列不同事实：
- 某局部上下文中火星、铃星可分别讨论；
- 两颗星可有 ordinal 差异；
- 某些命名复合词要求成对；
- relation 可能是触发结构的一部分；
- 同一简称在不同上下文可能使用不同 activation semantics。

## Proposed Design

最小知识对象：

```text
ResponseSemanticsRecord
= membership
+ scope
+ activation
+ relation_constraints
+ interaction
+ ordinal_constraints
+ effect_targets
+ provenance
+ epistemic / execution status
```

核心规则：

1. **GROUP = membership only.**
2. activation 无来源时必须为 `UNSPECIFIED`。
3. interaction 无来源时必须为 `UNSPECIFIED`。
4. relation 独立保存，不由 group 名称隐含推断。
5. ordinal constraint 只保存来源明确的相对关系，不创造数值。
6. effect target 可以为空；在 latent dimension ontology 未冻结时，不为追求可执行率强造 target。
7. Product 是否消费这些记录，由未来单独 Product Issue 决定。

## Alternatives

### A. Global ANY default
拒绝。会把“见一个即可”的假设扩散到来源没有说的上下文。

### B. Global ALL default
拒绝。会把“必须成对”的假设扩散到来源没有说的上下文。

### C. Full factor-graph / hypergraph rewrite now
拒绝。理论上可行，但当前数据与 runtime 不需要，工程复杂度过高。

### D. Keep all GROUP blockers unresolved forever
拒绝。会丢失来源已经明确给出的 pair、relation、ordinal 与 local member-response 信息。

## Compatibility

- canonical source rows 不修改；
- existing review sidecars 不修改；
- historical `CAREER_GROUP_QUANTIFIER_CLOSURE_v0.1` 保持历史事实；
- 新 schema 是附加层；
- old loaders/runtime 不消费新 registry，因此默认行为不变。

## Knowledge Impact

允许把现有 GROUP / RELATION / ORDINAL 证据组合到同一个语义记录中；不再把 quantifier 当作唯一问题。

## Product Impact

本 PR **无 Product 写入**。未来若接入，预期只是增加一个 bounded compiler：

```text
ActiveRuleGraph -> ResponseProfile
```

不要求同时实现 Bayesian state-space、决策模型或 world model。

## Risks / Failure Modes

- 把局部 response 错误推广成全局；
- 把“更甚/次之”偷换成数值；
- 把 named composite 的 pair requirement 错套到 generic shorthand；
- schema 变成新的大而全 ontology；
- Product 在没有单独 gate 时直接消费 provisional semantics。

## Test Plan

- JSON schema 可解析；
- pilot records 唯一、字段合法；
- activation/interaction 均可显式 `UNSPECIFIED`；
- lexical groups 不得因 membership 自动带出 ANY/ALL；
- registry 不允许 numeric weight / probability 字段；
- source provenance 非空；
- full repository quality gate。

## Migration Plan

v0.1 只建 schema + pilot。  
后续若 pilot 稳定：
1. 对 251 blocker 做 compatibility classification；
2. 只把 source-supported semantics 迁入 registry；
3. 仍 unresolved 的保持 blocked；
4. Product adapter 另开 Product Issue。

## Rollback Plan

删除本 work unit 新增的 response artifacts 即可；canonical source、existing rule runtime、Product runtime 不受影响。

## Graduation Criteria

- pilot 能表达至少：lexical-only group、pair-required composite、scoped heterogeneous category、local ordinal response；
- 无任何未授权 global default；
- Product unchanged；
- CI / audit / governance green。

## Human Gate

Gate: `HG-KB-RESPONSE-SEMANTICS-01`

PI 已明确批准：
> 先进行这些比较基础的修改，并把上面的原理写进 GitHub 做未来指导。

批准范围仅限本 Proposal 的 bounded knowledge schema + guidance。

旧 `HG-KB-GROUP-QUANTIFIER-01` 的 A/B/C 决策路径因此**被本设计方向取代**；但旧 artifact 中“generic shorthand cardinality unresolved”的历史结论仍然成立，不被追溯改写。

## Decision

**APPROVED_BOUNDED_SCHEMA_ONLY**

- Group membership 可以冻结到来源支持范围；
- response activation / interaction 需独立来源；
- 未明示语义保持 `UNSPECIFIED`；
- learned magnitude / probability 不属于 canonical KB；
- Product integration 与 empirical training 均需后续独立 gate。

## Implementation History

- 2026-10-20: PI 批准 bounded basic modification + future-guidance recording。
- Issue #419: v0.1 schema / pilot / guidance / tests。
