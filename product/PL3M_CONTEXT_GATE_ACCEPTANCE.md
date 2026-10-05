# PL3-M Context Gate v0.1

状态：**IMPLEMENTED — N/E/S/A/C BOUNDARY READY**

## 1. 目的

把前面已经建立的对象组装成统一的 manifestation routing context：

~~~text
Natal Prior N
+ Temporal Environment E_t
+ Acquired State S_t
+ Action A_t
+ External Context C_t
-> ManifestationRoutingContext
~~~

本层只组装和做消费资格检查，不创建应象、不算概率。

## 2. 两个模式

~~~text
BLIND
PERSONALIZED
~~~

`BLIND` 严格拒绝 acquired_state / state_quality，防止个人目标期反馈悄悄进入 blind forecast。

`PERSONALIZED` 必须有 AcquiredStateProfile，可以带 query-specific StateQualityReport。

## 3. N / E_t 一致性

TemporalEnvironmentProfile 必须明确属于当前 NatalStateProfile，且 knowledge_version 完全一致。

因此不同知识版本的 N 和 E_t 不能拼在一起。

## 4. S / A / C 分离

PERSONALIZED context 中明确分出：

- state_assertions = S_t；
- actions = A_t；
- exposures；
- external_factors；
- counterparty_factors = C_t 的不同部分。

不会把“本人采取行动”混成 external disturbance。

## 5. Personalization readiness

StateQualityReport 决定 personalized consumer 能否安全使用现实状态：

~~~text
READY
QUALITY_NOT_PROVIDED
ABSTAIN_MISSING
ABSTAIN_CONFLICT
ABSTAIN_CONFIDENCE
~~~

这些都是 consumption gate，不是概率或吉凶等级。

即使 personalized context 不完整，canonical N/E 仍可存在；但下游不能假装已经完成个体条件化。

## 6. Symbolic IDs

context 保留：

- active_natal_rule_ids；
- active_temporal_reaction_ids；
- active_temporal_rule_ids。

没有知识侧明确 activation ontology 前，不额外发明 universal activation ID。

## 7. Permanent boundaries

- context gate 不计算 manifestation probability；
- 不把 Bayesian state belief 当 manifestation probability；
- 不修改 Natal Prior；
- 不修改 Temporal Environment；
- BLIND 与 PERSONALIZED 永久分开；
- missing/conflict 通过 abstention 暴露，不插补。

## 8. 下一步

**PRODUCT_PL3M_PROBABILITY_INTERFACE_V0_1**

下一步只定义 empirical probability plugin 的接口与 namespace。生产 probability model registry 必须保持为空直到 PL5 calibration，不允许现在填传统经验数字。
