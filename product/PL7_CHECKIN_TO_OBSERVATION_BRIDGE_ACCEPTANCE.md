# PL7 Check-in → Observation Bridge Acceptance v0.1

状态：**IMPLEMENTED — DETERMINISTIC RESPONSE BRIDGE READY**

## 1. 目的

本工作单元把 ProspectiveCheckinPlan 的实际回答转换成 LongitudinalObservationRecord candidate。

桥接层不做概率判断，不改 target，不改 forecast，不补猜用户没说的信息。

## 2. 关键映射

~~~text
MID_WINDOW + NO
  -> NO_EVENT_YET
  -> 不生成负样本

WINDOW_CLOSE + NO
  -> EVENT_NOT_OCCURRED_CANDIDATE
  -> 只有窗口结束后才能形成 observation

YES
  -> EVENT_OCCURRED_CANDIDATE
  -> 需要 event_date 才能形成 v0.1 observation

UNSURE
  -> UNKNOWN_CANDIDATE

NO_RESPONSE
  -> NO_OBSERVATION
~~~

## 3. 用户确认是硬门槛

response.user_confirmed=false 时，不论 parser 或规则得到什么 candidate，都不能形成 observation。

因此未来 LLM/NLP 只能负责 candidate extraction，不能直接写入 empirical ground truth。

## 4. Target provenance 不可改

target_id、domain、manifestation_family、event_type、ontology_version 全部从 locked plan 复制。response 不能重新定义 target。

## 5. Forecast provenance 不可改

forecast_id、model_version、locked_date 来自 plan。

BLIND_BENCHMARK 自动进入 BLIND linkage；NO_FORECAST 自动进入 NONE；其他有预测的 prospective follow-up 进入 PERSONALIZED。

## 6. v0.1 已知限制

当前 LongitudinalObservationRecord v0.1 对 EVENT_OCCURRED 要求精确 event_date。

如果用户确认事件发生但只能给出月份或区间，bridge 返回 NEEDS_EVENT_DATE_DETAIL，不伪造日期。

后续是否支持 interval-censored event time，单独做 schema extension，不在本桥接层偷补。

## 7. 下一步

**PRODUCT_PL7_EVENT_TIME_PRECISION_REVIEW_V0_1**

评估是否需要 YEAR / MONTH / DAY / INTERVAL 四级事件时间表示，以支持真实世界中不精确回忆和 interval-censored survival data。
