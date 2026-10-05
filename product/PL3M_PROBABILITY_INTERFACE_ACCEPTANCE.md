# PL3-M Empirical Probability Interface v0.1

状态：**IMPLEMENTED — INTERFACE READY, PRODUCTION MODELS EMPTY**

## 1. 目的

把 `SOURCE_SUPPORTED_POSSIBILITY` 与未来 PL5 训练出来的 population/cohort empirical model 接起来。

正式 namespace：

~~~text
EMPIRICALLY_CALIBRATED_PROBABILITY
~~~

这一步不是把传统文字数值化。

## 2. Production registry

当前：

~~~text
registry_status = EMPTY_PENDING_PL5_CALIBRATION
models = []
~~~

因此当前所有 canonical possibility 的 empirical probability 都应为 `null`，状态为 `NOT_CALIBRATED`。

## 3. 参数来源

只允许：

~~~text
EMPIRICAL_POPULATION
EMPIRICAL_COHORT
TEST_FIXTURE
~~~

不允许 CANONICAL / TRADITIONAL / SOURCE_TEXT 作为概率参数层。

## 4. 模型发布条件

`CALIBRATED` model 必须显式保存：

- model_id / model_version；
- target manifestation_id / ontology version；
- predictor family；
- parameter layer；
- calibration dataset version；
- calibration metrics ref；
- allowed context modes；
- 是否要求完整 personal context。

生产 `CALIBRATED_READY` registry 只能包含 CALIBRATED models。

## 5. Plugin boundary

PL3-M 只定义 `PopulationProbabilityPlugin` 协议。

实际 logistic / multinomial / survival / hierarchical model 实现留到 PL5，且必须经过对应 benchmark/calibration gate。

## 6. Abstention

接口支持：

~~~text
NOT_CALIBRATED
MODEL_NOT_AVAILABLE
PLUGIN_NOT_AVAILABLE
PLUGIN_ABSTAIN
ABSTAIN_CONTEXT_MODE
ABSTAIN_CONTEXT_QUALITY
ESTIMATED
~~~

非 ESTIMATED 状态强制 `probability=null`。

## 7. 与 personalized posterior 的隔离

`EmpiricalProbabilityResult` 强制：

~~~text
is_personalized_posterior = false
~~~

population/cohort conditional probability 即使使用了 S_t/C_t 条件，也仍然不是个人参数 posterior。

个人 posterior 要使用独立 namespace 和下一工作单元。

## 8. Test-only 数字

fixture 只验证 plugin 接口，可以返回测试数字；这些数字不得进入 production registry，也不代表紫微经验概率。

## 9. 下一步

**PRODUCT_PL3M_PERSONALIZED_POSTERIOR_INTERFACE_V0_1**

下一步冻结 population probability 与 individual posterior 的最后一道 namespace/parameter 边界；生产 personal manifestation posterior 同样保持不可用，直到个体纵向数据与 PL5 hierarchical calibration 满足门槛。
