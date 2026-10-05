# PL7 Check-in Bridge v0.2 — Interval Event Time

状态：**IMPLEMENTED — V0.2 PROSPECTIVE DATA ENTRY CLOSED LOOP READY**

## 1. 目的

把 prospective check-in bridge 从 exact-day only 升级为与 LongitudinalObservation v0.2 一致的事件时间区间。

## 2. 支持的用户时间表达

工程输入支持：

- DAY：YYYY-MM-DD；
- MONTH：YYYY-MM；
- YEAR：YYYY；
- INTERVAL：lower_bound_date + upper_bound_date。

所有输入只做确定性 normalization，不做 midpoint/random-date imputation。

## 3. 归属规则

如果归一后的 event-time interval 完整落入 locked target window，则可生成 EVENT_OCCURRED observation。

如果只部分重叠 target window，则返回：

~~~text
TEMPORAL_ASSIGNMENT_AMBIGUOUS
~~~

不写入 target-specific positive truth。

如果完全在 target window 外，则直接拒绝。

## 4. 其他 v0.1 边界继续生效

- user_confirmed=false 不进入 ground truth；
- MID_WINDOW + NO 只是 NO_EVENT_YET；
- WINDOW_CLOSE + NO 才可能形成 EVENT_NOT_OCCURRED；
- UNSURE -> UNKNOWN；
- NO_RESPONSE -> NO_OBSERVATION；
- target 与 forecast provenance 只能来自 locked plan。

## 5. 产品阶段裁决

至此 PL7 的最低数据入口闭环已经具备：

~~~text
Target Lock
-> Prospective Check-in
-> User Confirmation
-> Bounded Event Time
-> Positive / Negative / Unknown / Censored Observation
~~~

PL7 后续仍会继续建设数据质量、样本治理和 calibration corpus，但不再阻塞主推演链。

## 6. 下一主工作单元

按 Product Roadmap v0.3 回到主链：

**PRODUCT_PL3T_TEMPORAL_ENVIRONMENT_CORE_V0_1**

原因：既有路线明确是 PL3-N -> PL3-T -> PL3-S -> PL3-M；PL7 是提前并行建设的数据基础设施，不应取代主链顺序。
