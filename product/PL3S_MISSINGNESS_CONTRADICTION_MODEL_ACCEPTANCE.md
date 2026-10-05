# PL3-S Missingness / Contradiction Model v0.1

状态：**IMPLEMENTED — AUDIT-ONLY QUALITY LAYER**

## 1. 目的

把 AcquiredStateProfile 中的现实状态逐 slot 审计为 OBSERVED / MISSING / CONFLICTED，为后续 StateBelief 准备明确的数据质量接口。

## 2. 关键原则

UNKNOWN / NOT_OBSERVED / NOT_ASKED / OUTDATED / WITHHELD 都不是 false，也不是 0。

UNRESOLVED conflict 不自动裁决，不按 confidence 标签偷偷选赢家。

## 3. Slot disposition

- OBSERVED -> READY_OBSERVED
- MISSING -> HOLD_MISSING
- CONFLICTED -> HOLD_CONFLICT

READY_OBSERVED 只代表结构上有可用现实观测，不代表预测为真，也不代表某个概率。

## 4. Fail-closed integrity

若同一 domain/key 同时既有 assertion 又标 missingness，直接拒绝。

若同一 domain/key 出现不同 value 却没有 StateConflict，直接拒绝。

若 conflict 引用不属于该 slot 的事实，直接拒绝。

## 5. Confidence

原 HIGH / MEDIUM / LOW / INSUFFICIENT 标签原样保留。

本工作单元不把 ordinal confidence 转成 numeric likelihood、Bayesian weight 或 empirical probability。

## 6. 输出

StateQualityReport 包含每个 slot 的 fact_ids、values、confidence labels、missingness reason、conflict ids、observation refs 及三类计数。

## 7. 永久边界

本层不 impute、不 resolve conflict、不修改 state、不读取 Natal/Temporal 来补现实数据、不计算 manifestation probability。

## 8. 下一步

**PRODUCT_PL3S_BAYESIAN_BELIEF_V0_1**

进入下一步前必须继续遵守：没有 source/empirical 支持的 likelihood 或 prior 数字不得拍脑袋设定。若数值 Bayesian update 缺少可审计参数，则应 fail closed 或先定义非数值 belief contract，而不是伪造概率。
