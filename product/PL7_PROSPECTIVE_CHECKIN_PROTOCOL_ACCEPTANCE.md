# PL7 Prospective Check-in Protocol Acceptance v0.1

状态：**IMPLEMENTED — PROSPECTIVE COLLECTION CONTRACT READY**

## 1. 目的

本工作单元规定纵向数据应该如何被前瞻性地采集，重点解决 memorable-event-only bias、目标事后重定义、预测泄漏和“没发生”无法进入样本的问题。

它建立的是 collection protocol，不训练模型。

## 2. 核心流程

~~~text
plan created
  -> targets locked
  -> forecast locked if any
  -> observation window starts
  -> optional neutral mid-window check
  -> event-triggered self report allowed
  -> mandatory window-close check
  -> confirmed response enters LongitudinalObservationRecord
~~~

目标必须在 observation window 开始前冻结。

## 3. 为什么必须有 WINDOW_CLOSE

用户平时只会主动报告显著事件，这会天然造成 memorable-event bias。

因此每个 prospective plan 必须恰好有一个 WINDOW_CLOSE checkpoint，并且安排在 window_end。

只有这个 close-out check 上的 NO，经过 observation confidence 与完整窗口校验后，才有资格成为 EVENT_NOT_OCCURRED。

mid-window 的 NO 只能表示 NO_EVENT_YET，绝不能提前成为负样本。

## 4. Prediction Exposure

protocol 显式保存三种状态：

- HIDDEN
- VISIBLE
- NO_FORECAST

BLIND_BENCHMARK 必须使用 HIDDEN。

PERSONALIZED_FOLLOWUP 可以使用 VISIBLE，但这种数据后续分析必须承认预测本身可能改变行为或报告方式，不能与 blind benchmark 混为一谈。

## 5. Forecast lock

只要 prediction_exposure 不是 NO_FORECAST，就必须有 forecast_id、model_version、locked_date。

并满足：

~~~text
forecast.locked_date <= target_lock_date <= window.start_date
~~~

这保证不能看到结果后再调整 prediction target。

## 6. Outcome leakage 防线

ProspectiveCheckinPlan 禁止包含 outcome、event_status、event_date、observed_through、severity、duration_days、censor_reason 等结果字段。

plan 只定义未来要观察什么，不保存已经知道的答案。

## 7. Neutral collection

check-in prompt 不展示预测概率，不使用“命盘说你会……”之类引导性语言。

标准问题只询问：在预定义窗口内，目标事件是否发生。

v0.1 标准回答：YES / NO / UNSURE / NO_RESPONSE。

## 8. LLM 边界

未来 LLM 可以把用户自由文本解析成结构化 candidate，但：

- candidate_only = true；
- user_confirmation_required = true；
- LLM 不能直接生成最终 EVENT_NOT_OCCURRED；
- deterministic validator 决定记录是否满足 schema。

## 9. 低负担策略

v0.1 不强制高频打卡。

最小有效方案是：

- 目标事前冻结；
- 用户可随时主动报告已发生事件；
- 一个 window-close check-in；
- mid-window check 可选。

这样可以在用户负担和 negative-sample 质量之间取得平衡。

## 10. 与 LongitudinalObservationRecord 的关系

ProspectiveCheckinPlan 不是现实 observation。

它只负责冻结 target 与 collection procedure。

之后经过实际回答、用户确认和 observation validator，才能形成 PL7_LONGITUDINAL_OBSERVATION_SCHEMA_v0.1 记录。

## 11. 下一步

**PRODUCT_PL7_CHECKIN_TO_OBSERVATION_BRIDGE_V0_1**

下一工作单元建立从 check-in response 到 LongitudinalObservationRecord candidate 的确定性桥接：保留 plan/target/checkpoint provenance；区分 EVENT_OCCURRED_CANDIDATE、NO_EVENT_YET、EVENT_NOT_OCCURRED_CANDIDATE、UNKNOWN_CANDIDATE、NO_OBSERVATION；且不允许 parser 绕过用户确认。
