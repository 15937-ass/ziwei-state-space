# PL3-S StateBelief Benchmark v0.1

状态：**IMPLEMENTED — DETERMINISTIC CONTRACT BENCHMARK**

## 1. 目的

本工作单元验证 PL3-S 的状态 belief 接口是否稳定、可重复、会在缺失/冲突/低质量证据下正确 abstain。

它**不是现实预测准确率 benchmark**，也不是 Bayesian 参数校准结果。

## 2. 固定输入

Benchmark 复用：

- `PL3S_ACQUIRED_STATE_FIXTURE_v0.1.json`
- `PL3S_BELIEF_MODEL_FIXTURE_v0.1.json`
- `PL3S_BELIEF_MODEL_REGISTRY_v0.1.json`

其中 belief model 明确是：

`TEST_FIXTURE / TEST_ONLY`

测试里的 0.5、0.8、0.2 只检验数学接口和边界，不属于紫微经验概率。

## 3. 五个冻结场景

1. AVAILABLE_EMPLOYED  
   -> UPDATED / USED

2. MISSING_EMPLOYMENT  
   -> NO_USABLE_EVIDENCE / SKIPPED_MISSING

3. CONFLICTING_EMPLOYMENT  
   -> NO_USABLE_EVIDENCE / SKIPPED_CONFLICT

4. LOW_CONFIDENCE_EMPLOYMENT  
   -> NO_USABLE_EVIDENCE / SKIPPED_CONFIDENCE

5. UNMODELLED_EMPLOYMENT_VALUE  
   -> NO_USABLE_EVIDENCE / SKIPPED_UNMODELLED_VALUE

## 4. Determinism

同一 state fixture + 同一 model fixture + 同一代码版本：

- `benchmark_id` 必须一致；
- 每个 case 的 result digest 必须一致；
- posterior 必须一致。

## 5. Abstention

四个不可安全消费的场景均保持 posterior=prior。

Benchmark 因此验证的是：

> 没有可用现实证据时，系统不会为了“给答案”而编造更新。

## 6. Production registry guard

Benchmark 强制要求生产 registry：

`status = EMPTY_PENDING_EMPIRICAL_CALIBRATION`

并且：

`models = []`

若 production registry 已出现模型，本 benchmark 会 fail closed，防止 TEST_FIXTURE 与真实 calibration 混在一起。

## 7. 不做的事

本工作单元不测：

- 命盘预测准确率；
- manifestation accuracy；
- calibration curve；
- Brier / log loss；
- population prior；
- personalized posterior accuracy；
- 紫微规则增量价值。

这些必须留给 PL4-B / PL5 的真实盲测和经验校准。

## 8. PL3-S 阶段结论

至此 PL3-S v0.1 主干已经具备：

- AcquiredState schema；
- deterministic updater；
- missingness / contradiction quality gate；
- minimal discrete Bayesian belief interface；
- deterministic StateBelief benchmark。

但生产 Bayesian model registry 仍为空，因此我们只完成了**状态观察器骨架**，没有声称已经拥有可靠的个人概率模型。

## 9. 下一步

**PRODUCT_PL3M_MANIFESTATION_ONTOLOGY_ADAPTER_V0_1**

进入 PL3-M 前先检查知识侧 WP06B / WP06C manifestation ontology 是否已经达到可消费状态。若知识侧尚未 ready，则只建立 fail-closed adapter contract，不在产品侧发明 manifestation ontology。
