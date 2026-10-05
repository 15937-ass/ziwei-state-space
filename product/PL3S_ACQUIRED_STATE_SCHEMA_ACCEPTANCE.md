# PL3-S AcquiredState Schema v0.1

状态：**IMPLEMENTED — REALITY STATE CONTAINER READY**

## 1. 目的

PL3-S 开始承载现实世界中会随时间变化、会影响后续应象的获得性状态：

~~~text
S_t = AcquiredStateProfile
~~~

它与 Natal Prior `N`、Temporal Environment `E_t`、Action `A_t`、External Context `C_t`、Empirical Probability 永久分层。

## 2. v0.1 容器

AcquiredStateProfile 保存：

- 现实状态 assertions；
- actions；
- exposure / external / counterparty context；
- missingness；
- unresolved conflicts；
- source observation IDs；
- snapshot confidence；
- previous_state_id（仅版本链，不是无边界 history bag）。

## 3. Reality domains

v0.1 只定义现实信息容器，不定义紫微语义：

~~~text
RELATIONSHIP
CAREER
RESOURCE
RELOCATION
COMMITMENT
SOCIAL_EXPOSURE
HEALTH_CONTEXT
EDUCATION_CONTEXT
FAMILY_CONTEXT
HOUSING_CONTEXT
OTHER
~~~

这些 domain 只是现实状态 namespace，不是 manifestation ontology，也不是传统宫位映射。

## 4. Assertion contract

每条 assertion 必须具有：fact_id、domain、key、scalar value、status、confidence、observation_refs。

`value=null` 不允许伪装成状态值；未知必须进入 `missingness`。

v0.1 不允许复杂 JSON object 作为单一 value，以减少后续 parser 对结构语义的自由发挥。

## 5. Action 与 Context 分离

actions 继续使用 INTENDED / PLANNED / ACTUAL / ABANDONED / UNKNOWN。

context_items 显式区分：

~~~text
EXPOSURE
EXTERNAL
COUNTERPARTY
~~~

这保持之前冻结的边界：个人选择不是 disturbance；他人行为/现实机会也不等同 observation。

## 6. Missingness / conflict 是一等数据

不知道、没问、没观察到、数据过期、用户不愿提供，都不能自动当成 false。

互相矛盾的现实报告必须保留多个 fact，并由 conflict object 引用；schema 不自动裁决谁真谁假。

## 7. Provenance

每个 assertion/action/context item 必须引用 observation_refs，且引用必须出现在 profile 的 source_observation_ids 中。

因此任何现实状态都不能由 LLM 凭感觉写入。

## 8. Natal / empirical 防污染

AcquiredState payload 明确拒绝 canonical_facts、natal_profile、temporal_rules、manifestation_probability、population_probability、personalized_posterior 等字段。

现实反馈可以改变 S_t，但不能改写 N 或 canonical rule truth。

## 9. Determinism

对相同规范化内容计算：

~~~text
state_id = ASTATE-<content hash>
~~~

输入项目顺序变化后仍应得到同一 state_id；如果外部 supplied state_id 与内容不匹配，fail closed。

## 10. 本工作单元不做

- 不从 observation 自动推断状态变化；
- 不做 Bayesian posterior；
- 不设状态衰减；
- 不定义领域特定 transition；
- 不把 missing 当 negative；
- 不做 manifestation probability。

## 11. 下一步

**PRODUCT_PL3S_DETERMINISTIC_STATE_UPDATER_V0_1**

下一步才定义 confirmed longitudinal observations 如何在严格 transition rules 下更新 AcquiredStateProfile；没有显式 updater rule 的字段保持原值或 UNKNOWN，不让 LLM 自由改状态。
