# PL7 Longitudinal Observation Schema Acceptance v0.1

状态：**IMPLEMENTED — DATA CONTRACT READY, NO TRAINING YET**

## 1. 目的

本工作单元把新的动态推演架构第一次落实为可验证的数据接口。

训练单位从：

~~~text
一个命盘 + 一个命中事件
~~~

改为：

~~~text
Person × Observation Window × Predefined Target
~~~

本 schema 服务于未来：

- PL3-S Personal State Observer；
- PL4-B blind predictive benchmark；
- PL5 empirical calibration；
- population -> cohort -> individual posterior；
- manifestation routing；
- event-history / survival analysis。

它不修改 canonical knowledge，也不在本阶段训练任何概率模型。

## 2. 核心数据分离

每条记录必须区分 Target Window、Target、Action、External Context / Exposure、Outcome、Observation 和 Model Linkage。

Action 明确区分 INTENDED / PLANNED / ACTUAL / ABANDONED / UNKNOWN。意图不等于实际行为。

Outcome 只能是 EVENT_OCCURRED、EVENT_NOT_OCCURRED、UNKNOWN、CENSORED。

Model Linkage 保存 chart / knowledge / state / forecast 版本引用，但原始现实观察不依赖模型才能存在。

## 3. 负样本的严格定义

EVENT_NOT_OCCURRED 不是“用户没提到”。它必须满足：

~~~text
observed_through >= window_end
AND observation_confidence != INSUFFICIENT
~~~

否则只能是 UNKNOWN 或 CENSORED。

这条规则防止把 missing data 错当 negative sample。

## 4. CENSORED 的严格定义

CENSORED 表示在计划观察窗口结束前停止有效观察，并且截止 censor date 尚未确认目标事件。

要求：

~~~text
observed_through < window_end
censor_reason != null
~~~

如果完整观察到了 window_end 且目标事件没有发生，应使用 EVENT_NOT_OCCURRED。

## 5. Blind benchmark 防泄漏

PROSPECTIVE + BLIND 记录若要进入 blind benchmark：forecast_id、model_version、locked_date 都必须存在，且 locked_date <= window_start，outcome 也必须具备可用观察证据。

该 schema 只能证明时间顺序和 linkage 条件满足，真正 benchmark 仍需独立 split / leakage audit。

## 6. Retrospective 与 prospective 永久分开

RETROSPECTIVE 数据可以用于 schema 验证、hypothesis generation、有限 calibration，以及严格 split 下的部分离线实验；但不能冒充 prospective blind validation。

未来报告必须分别展示两类结果。

## 7. Canonical 与 empirical 边界

LongitudinalObservationRecord 不能改写 Natal Prior、修改 source rule truth、把一个用户经历升级成全局规则，或把某次 EVENT_NOT_OCCURRED 当成对 source rule 的直接反证。

现实数据只能进入 Acquired State、Empirical Calibration、Personal Posterior、Knowledge Gap Report。最后一项也只能触发回源复核。

## 8. 隐私边界

person_key 只允许 pseudonymous key。本 contract 不要求真实姓名、联系方式、身份证明等直接身份字段。

原始自由文本如需保留，应由独立受控存储保存，本记录只存 notes_ref。

## 9. v0.1 不做的事情

- 不定义 manifestation ontology 本身；
- 不定义健康/财富/婚恋事件的具体医学或专业标准；
- 不训练概率；
- 不建立 causal effect；
- 不启动 MPC；
- 不使用 LLM 判断 EVENT_NOT_OCCURRED；
- 不把 casebook 作者案例直接转为 longitudinal ground truth。

## 10. 下一步

**PRODUCT_PL7_PROSPECTIVE_CHECKIN_PROTOCOL_V0_1**

要解决：什么时候创建 observation window；用户如何低负担定期反馈；如何记录“什么也没发生”；如何冻结 target before outcome；如何将自然语言反馈解析为候选结构化 observation，再由确定性 validator 审核；如何防止 memorable-event-only selection bias。
