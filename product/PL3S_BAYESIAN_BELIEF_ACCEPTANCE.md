# PL3-S Bayesian Belief v0.1

状态：**IMPLEMENTED — EXTERNALLY CALIBRATED DISCRETE BAYES ONLY**

## 1. 为什么这一版不内置 prior / likelihood

PL3-S 已经进入概率状态估计，但当前项目还没有足够的现实校准数据去诚实地产生通用 prior 与 likelihood。

因此 v0.1 实现 Bayes 运算接口，但生产模式没有任何默认数字。

## 2. 最小模型

只支持离散 state hypothesis 的单步更新：posterior(h) ∝ prior(h) × likelihood(e|h)。

不启用 particle filter、DBN、neural state-space，也不自动假设多条 evidence 条件独立。

## 3. Parameter provenance gate

生产参数只接受 EMPIRICAL_CALIBRATION provenance，必须带 artifact_id / artifact_version / parameter_set_id。

TEST_ONLY_SYNTHETIC 只用于 regression test；默认 compile 会拒绝，只有显式 allow_test_only=true 才能进入。

这保证测试 Bayes 算法时使用的示例数字不会被误当成产品经验参数。

## 4. Quality gate

Bayesian update 必须绑定 StateQualityReport 中一个 requirement，而且该 requirement 必须为 AVAILABLE。

MISSING、CONFLICTED、INSUFFICIENT_CONFIDENCE 全部 fail closed，不进行概率更新。

## 5. 不数值化旧 confidence

HIGH / MEDIUM / LOW / INSUFFICIENT 仍只是数据质量标签。本模块不会自行把它们映射成 0.9 / 0.6 / 0.3 等 likelihood。

## 6. 数值规则

prior 必须显式给出并精确归一为 1；prior 与 likelihood 的 hypothesis set 必须完全一致；零 marginal likelihood 直接拒绝。

使用 Decimal 保持可复现计算，不冻结任何紫微业务概率。

## 7. 分层边界

State belief 属于现实状态估计 S_t，不写回 Natal Prior，不修改 Temporal Environment，不等于 manifestation probability，也不等于 population predictive calibration。

## 8. 当前产品能力

现在已经可以安全表达“如果我们有一套经过现实数据校准的状态 prior/likelihood，如何更新个人当前状态 belief”，但在校准参数不存在时产品必须 abstain。

## 9. 下一步

**PRODUCT_PL3S_STATE_BELIEF_BENCHMARK_V0_1**

建立固定 observation / directive / quality / calibrated-test-parameter sequence，验证 state snapshot 与 belief 更新可重复，并明确 production 参数缺失时的 abstention contract。
