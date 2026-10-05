# PL3-S Missingness / Contradiction Model v0.1

状态：**IMPLEMENTED — NON-PROBABILISTIC QUALITY GATE**

## 1. 目的

在进入 Bayesian belief 之前，先回答一个更基础的问题：

> 当前 AcquiredState 对某个下游任务而言，哪些变量可用、哪些未知、哪些互相矛盾、哪些证据质量不足？

因此本层是 deterministic quality gate，不是概率模型。

## 2. Requirement-driven audit

状态“完整不完整”不能脱离问题定义。

下游模块必须显式声明 `StateRequirement`：

~~~text
domain
key
accepted_confidences
~~~

系统只针对这些字段判断 readiness，不建立一个虚假的全局“个人信息完整度分数”。

## 3. 四类 requirement status

~~~text
AVAILABLE
MISSING
CONFLICTED
INSUFFICIENT_CONFIDENCE
~~~

没有任何加权打分。

## 4. Readiness

确定性优先级：

~~~text
CONFLICTED
> PARTIAL_MISSING
> INSUFFICIENT_CONFIDENCE
> READY
~~~

这个顺序只用于是否允许下游消费，不表示吉凶、概率或严重程度。

## 5. Missingness audit

v0.1 把既有 missingness reason 映射为审计类别：

~~~text
NOT_ASKED     -> DESIGN_MISSING
NOT_OBSERVED  -> OBSERVATION_GAP
OUTDATED      -> STALE
WITHHELD      -> WITHHELD_MNAR_RISK
UNKNOWN       -> UNCLASSIFIED
~~~

`WITHHELD_MNAR_RISK` 只表示存在 missing-not-at-random 风险，不声称已经证明 MNAR。

## 6. Conflict

任何同 key 的 unresolved conflict 都直接让该 requirement = CONFLICTED。

系统不做 majority vote、不按 confidence 私自裁决、不让 LLM 选一个更顺眼的版本。

## 7. Confidence

requirement 自己声明允许哪些 confidence level。

因此不是系统假定 HIGH=1.0 / MEDIUM=0.7 / LOW=0.3，也没有把 ordinal label 偷偷数值化。

## 8. 为 Bayesian Observer 准备什么

本层给后续 belief model 提供：

- 可观测字段；
- 缺失字段及缺失机制线索；
- unresolved conflict；
- low/insufficient confidence evidence；
- query-specific readiness。

这些信息先保持离散可审计，再决定是否需要 posterior。

## 9. 下一步

**PRODUCT_PL3S_BAYESIAN_BELIEF_V0_1**

下一步只在明确的离散 state hypothesis 上实现最小 Bayesian belief interface；不会一上来使用 particle filter，也不会把 Bayesian posterior 写回 canonical Natal Prior。
