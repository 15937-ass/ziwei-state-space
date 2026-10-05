# PL3-S Bayesian Belief v0.1

状态：**IMPLEMENTED — INTERFACE READY, PRODUCTION PARAMETER REGISTRY EMPTY**

## 1. 目的

为现实获得性状态 `S_t` 提供最小离散 Bayesian belief interface。

它估计的是：

~~~text
P(acquired latent state | observed personal-state evidence)
~~~

不是：

~~~text
P(real-world manifestation | chart)
~~~

后者属于 PL3-M / PL5。

## 2. 为什么现在只做离散 Bayes

当前数据稀疏、异步、分类变量较多，因此按既定架构先做最简单可审计模型。

v0.1 不使用 particle filter、neural state-space、GNN。

## 3. 参数边界

Bayesian 数值参数只允许来自：

~~~text
EMPIRICAL
PERSONAL
TEST_FIXTURE
~~~

没有 CANONICAL/TRADITIONAL 参数层。

这意味着传统资料中的“多主、往往、易”不能直接转换成 prior 或 likelihood。

## 4. Production registry

当前：

~~~text
PL3S_BELIEF_MODEL_REGISTRY_v0.1.json
status = EMPTY_PENDING_EMPIRICAL_CALIBRATION
~~~

也就是说 engine 已经实现，但没有任何拍脑袋生产概率。

测试 fixture 中的 0.8/0.2 只验证数学与边界，不是紫微经验参数。

## 5. Observation model

每个 evidence channel 显式声明：

- reality domain/key；
- accepted confidence；
- observed value；
- P(value | hypothesis) likelihood table。

每个 hypothesis 下，所有 modelled observation values 的 likelihood 必须归一为 1。

prior 同样必须严格归一。

## 6. Missing / conflict

Bayesian updater 不进行 imputation：

- missing -> SKIPPED_MISSING；
- unresolved conflict -> SKIPPED_CONFLICT；
- confidence 不满足 model contract -> SKIPPED_CONFIDENCE；
- 新出现但模型没见过的值 -> SKIPPED_UNMODELLED_VALUE。

如果没有任何可用 evidence，posterior=prior，同时 status=NO_USABLE_EVIDENCE。

## 7. 与 canonical 的隔离

Belief model：

- 不读取/修改 Natal Prior；
- 不读取 traditional rule valence 作为概率；
- 不修改 Temporal Environment；
- 不修改 source rule truth。

它只消费 `AcquiredStateProfile`。

## 8. 数字的语义

posterior 数字是给定明确统计参数后的 personal-state belief。

不是 source membership、不是吉凶分、不是命盘准确率，也不是现实事件概率。

## 9. 下一步

**PRODUCT_PL3S_STATE_BELIEF_BENCHMARK_V0_1**

用固定 AcquiredState fixtures + fixed test-only belief specs 验证 same state + same model -> same posterior，并冻结 missing/conflict/unsupported-value 的 abstention 行为。
