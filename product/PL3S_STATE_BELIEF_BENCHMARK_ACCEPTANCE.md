# PL3-S State Belief Benchmark v0.1

状态：**IMPLEMENTED — CONTRACT BENCHMARK PASS REQUIRED**

## 1. 目的

冻结 PL3-S belief 层的工程行为：

~~~text
same AcquiredState
+ same belief model version
-> same posterior
~~~

以及 missing / conflict / low-confidence / unmodelled-value 的 abstention 行为。

## 2. 当前五类 fixture

~~~text
BASE_UPDATED
MISSING
CONFLICT
LOW_CONFIDENCE
UNMODELLED_VALUE
~~~

BASE 只验证 fixture 数学；其余四类验证系统不会为了得到答案而补数据。

## 3. Benchmark 内容

每个 case 比较：

- update status；
- posterior；
- evidence-use status；
- repeated-run deterministic equality。

posterior 使用严格 tolerance 比较。

## 4. 不是预测准确率

本 benchmark 不包含真实世界 holdout outcomes，因此不能回答：

> 紫微预测准不准？

也不能回答：

> 这些 0.8/0.2 是否是现实概率？

它只是 PL3-S internal contract benchmark。

## 5. PL3-S 阶段结论

完成本工作单元后，PL3-S v0.1 产品骨架已经具备：

~~~text
AcquiredState container
-> deterministic updater
-> missing/conflict quality gate
-> minimal Bayesian belief
-> deterministic belief benchmark
~~~

真正的 production Bayesian parameters 仍然为空，必须等待 PL5 empirical calibration。

## 6. 下一步

主线进入：

**PRODUCT_PL3M_MANIFESTATION_ONTOLOGY_ADAPTER_V0_1**

如果知识侧 KB-WP06B / WP06C 尚未冻结可消费 artifact，产品侧必须 fail closed，并转去推进并行 PL7 data-quality work，而不是自造 manifestation taxonomy。
