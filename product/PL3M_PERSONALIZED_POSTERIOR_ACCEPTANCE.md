# PL3-M Personalized Manifestation Posterior Interface v0.1

状态：**IMPLEMENTED — INTERFACE READY, PRODUCTION PERSONAL MODELS EMPTY**

## 1. 目的

本工作单元冻结应象概率的第三级接口：

~~~text
SOURCE_SUPPORTED_POSSIBILITY
        ↓
EMPIRICALLY_CALIBRATED_PROBABILITY
        ↓
PERSONALIZED_POSTERIOR
~~~

对应：

~~~text
P(M | Q, context, individual history)
~~~

本接口不训练模型，不给传统断语赋概率，也不把当前用户的一次经历写回 canonical rule。

## 2. 独立 namespace

个人应象后验固定使用：

~~~text
PERSONALIZED_POSTERIOR
~~~

并与：

~~~text
SOURCE_SUPPORTED_POSSIBILITY
EMPIRICALLY_CALIBRATED_PROBABILITY
~~~

永久分离。

结果同时保留 population baseline 与 personalized posterior，避免把“群体概率”和“个人后验”混成同一个数字。

## 3. Production registry

当前生产 registry：

~~~text
registry_status = EMPTY_PENDING_PL5C_CALIBRATION
models = []
~~~

因此当前系统不能生成生产级 personal manifestation probability。

这不是缺失默认值，而是主动 fail closed：在 PL5-C hierarchical/personal calibration 完成以前，个人 posterior 必须保持不可用。

## 4. Personal context gate

个人后验只允许在：

~~~text
context.mode = PERSONALIZED
personalization_readiness = READY
person_key != null
acquired_state_id != null
~~~

时继续。

BLIND mode 永远不能调用个人 posterior。

Missing / conflict / insufficient-confidence 仍由 PL3-S / PL3-M context gate 的 abstention 语义控制，不得在本层自动补值或猜测。

## 5. Population baseline dependency

v0.1 要求 personal posterior 必须建立在已存在的独立 population/cohort empirical baseline 上。

必须满足：

- baseline namespace = `EMPIRICALLY_CALIBRATED_PROBABILITY`；
- manifestation_id 一致；
- source possibility mapping 一致；
- context_id 一致；
- baseline status = `ESTIMATED`；
- baseline probability 非空；
- population model identity 与 personal model descriptor 声明的 `population_model_id` 一致。

因此不允许：

~~~text
traditional source wording
-> directly produce personal probability
~~~

也不允许：

~~~text
uncalibrated population layer
-> pretend to be a personal posterior
~~~

## 6. Plugin boundary

PL3-M 只定义：

~~~text
PersonalizedPosteriorPlugin
~~~

真实 hierarchical Bayesian / individual random-effect / shrinkage 实现留给 PL5-C。

本层不冻结：

- shrinkage strength；
- minimum personal sample count；
- personal random-effect prior；
- likelihood family；
- update threshold；
- posterior concentration threshold。

这些必须由未来经验建模与验证决定，不能在 PL3-M 预先拍数值。

## 7. 与 PL3-S Bayesian belief 的区别

`BeliefUpdateResult` 是：

> 对 acquired state (S_t) 的状态 belief。

`PersonalizedPosteriorResult` 是：

> 对 manifestation (M) 的个人后验。

两者不是同一个对象，也不能互相冒充。

未来 personal manifestation model 可以消费经过批准的 state belief / longitudinal features，但必须经过独立 PL5-C 模型契约。

## 8. Abstention

接口支持：

~~~text
NOT_CALIBRATED
MODEL_NOT_AVAILABLE
POPULATION_BASELINE_NOT_AVAILABLE
POPULATION_MODEL_MISMATCH
PLUGIN_NOT_AVAILABLE
PLUGIN_ABSTAIN
ABSTAIN_CONTEXT_MODE
ABSTAIN_CONTEXT_QUALITY
ESTIMATED
~~~

除 `ESTIMATED` 外：

~~~text
posterior_probability = null
~~~

## 9. Test-only fixture

测试 registry 使用：

~~~text
parameter_layer = TEST_FIXTURE
model_status = TEST_ONLY
~~~

测试 plugin 可返回人工常数，只用于验证接口和 namespace 边界。

任何 TEST_FIXTURE 数字均不得进入 production registry，也不代表紫微经验概率。

## 10. Human Gate

本工作单元没有新增：

- primitive qi；
- natal/temporal 边界；
- canonical rule；
- manifestation family；
- persistence / decay；
- source 外数值权重；
- causal claim。

因此 **不触发新的 Human Gate**。

## 11. 交付

新增：

- `src/product/personalized_posterior.py`
- `product/PL3M_PERSONALIZED_POSTERIOR_REGISTRY_v0.1.json`
- `product/PL3M_PERSONALIZED_POSTERIOR_FIXTURE_v0.1.json`
- `tests/test_product_personalized_posterior.py`

## 12. 下一步

PL3-M 五个接口工作单元至此齐备。

下一正式主线：

**PRODUCT_PL4A_INTERNAL_FIDELITY_BENCHMARK_CONTRACT_V0_1**

PL4-A 先验证系统是否忠实重建 canonical reasoning；不把教材案例误当现实预测 ground truth，也不提前进入 PL5 概率训练。
