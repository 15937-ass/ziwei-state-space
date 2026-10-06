# PL3 Product Maturity Audit v0.1

状态：**GOVERNANCE HARDENING — PL3-M INTERFACE EXIT / PL4-A ENTRY**

## 1. 目的

本审计解决两个风险：

1. 状态治理：禁止旧聊天、旧分支或顶层过期摘要重新成为产品执行指针；
2. 产品空壳化：明确区分“接口已经定义”与“生产知识/概率已经可用”。

本文件不修改中州派 canonical rule，不新增 qi、manifestation family、数值权重、概率或因果语义。

## 2. 唯一产品执行指针

产品工作单元只以：

`product/PRODUCT_STATE.yaml`

为 authoritative pointer。

`PROJECT_STATE.yaml -> productization` 只保留摘要和跨轨依赖，不再拥有产品 `next_work_unit`。

旧聊天、旧 PR、历史 branch 名称不得覆盖这一规则。

## 3. PL3 当前成熟度

| 能力 | 接口/架构 | 生产资产 | 判定 |
|---|---|---|---|
| Deterministic chart | 完成 | Chart Trust v1 | READY |
| Rule runtime | 完成 | 有界规则集 | PARTIAL/USABLE |
| Natal wealth | 完成 | W01 59/100 executable | PARTIAL |
| Natal career | provider contract 已有 | 等待 CA04-CA08 repair + CA09 closure | BLOCKED |
| Temporal environment | 完成 | 基础时序事实可用 | PARTIAL |
| Temporal reactions | compiler 完成 | production registry 空，等 KB-WP07B | BLOCKED_CONTENT |
| Manifestation ontology | adapter 完成 | production registry 空，等 KB-WP06B | BLOCKED_CONTENT |
| Manifestation mapping | router 完成 | production registry 空，等 KB-WP06C | BLOCKED_CONTENT |
| Population probability | plugin contract 完成 | production registry 空，等 PL5 | NOT_CALIBRATED |
| Personalized posterior | plugin contract 完成 | production registry 空，等 PL5-C | NOT_CALIBRATED |

结论：

> **PL3-M 可以宣布“接口设计完成”，但不能宣布“产品推理能力完成”。**

## 4. 立即生效的 anti-scaffolding 规则

从本审计开始：

1. 不再因为路线图上还有一个名词就自动新增 interface / registry / adapter。
2. 下一阶段必须转向 **PL4-A Internal Fidelity**，用真实非空资产验证系统。
3. 任何空 registry：
   - 只能记为 BLOCKED / UNCOVERED；
   - 不能因为 schema、fixture、unit test 通过就记为 fidelity pass。
4. 新增抽象层必须由一个具体的 benchmark failure 或 canonical integration gap 触发。
5. PL4-A 只测“是否忠实实现中州派/已批准知识”，不把教材案例当现实预测真值。
6. PL5 以前不得把 source wording 数值化为 empirical probability。
7. Personalized posterior 在 PL5-C 前保持 fail closed。

## 5. PL4-A 首批应该测什么

优先使用已经非空的真实资产，而不是新增接口：

- P1 Chart Trust / chart reconstruction；
- W01 已 executable 的 59 条财富规则；
- ActiveRuleGraph -> EvidencePackage trace；
- PL3-N wealth provider；
- PL3-T 已验证的 temporal facts / fixtures；
- canonical source provenance / conflict preservation。

Career、manifestation ontology/mapping、production temporal reactions 等在对应知识资产进入 canonical main 后再扩大 coverage。

## 6. PL4-A 报告必须同时给 coverage

禁止只报“通过/失败”。

至少报告：

- eligible assets；
- covered assets；
- blocked-by-empty-registry；
- blocked-by-knowledge-dependency；
- trace completeness；
- deterministic reproducibility；
- contradiction preservation；
- unresolved / insufficient evidence count。

因此一个局部 benchmark 可以 PASS，但必须同时明确：

> PASS on covered subset != production readiness.

## 7. 分支与状态规则

当前 Personalized Posterior 工作通过 PR #274 进入正式审查/CI。

在 PR 合并前：
- main 仍以 main 的 `product/PRODUCT_STATE.yaml` 为准；
- branch 中的 “PL4-A next” 不能反向冒充 main 状态。

合并后：
- PL3-M 接口层正式关闭；
- `product/PRODUCT_STATE.yaml` 指向 PL4-A；
- 本审计作为 PL4-A entry guard 持续有效。

## 8. Human Gate

本审计只做治理和成熟度判定，没有改变理论边界。

**Human Gate：NONE。**
