# PL7 Event-Time Precision Review v0.1

状态：**DECISION FROZEN — MOVE TO INTERVAL NORMAL FORM**

## 1. 问题

PL7 observation v0.1 对 EVENT_OCCURRED 要求精确 event_date。这个要求对前瞻即时报告还可以，但对真实长期数据过严：用户常常只能记得“某个月”“某一年”或“大概在这两个月之间”。

如果系统为了满足 schema 自行补成某一天，会制造假的时间精度，并污染后续 event-history / survival calibration。

## 2. 裁决

Observation Schema v0.2 采用统一的 event-time interval normal form：

~~~text
reported_precision
lower_bound_date
upper_bound_date
~~~

支持 DAY / MONTH / YEAR / INTERVAL。

DAY：上下界相同。

MONTH：按真实日历扩成该月第一天到最后一天。

YEAR：扩成 1 月 1 日到 12 月 31 日。

INTERVAL：保留用户/记录实际给出的上下界。

## 3. 绝不做 midpoint imputation

如果用户只说“2027 年 5 月”，不能改写成 2027-05-15。

如果只说“2027 年”，不能改写成某个随机日期。

系统保存的是信息边界，而不是制造不存在的信息。

## 4. 与 target window 的关系

一个 EVENT_OCCURRED 只有在其报告时间区间完整落在 target window 内，才能成为该 target 的 occurrence truth。

如果只是部分重叠，例如 target 是 2027Q2，但用户只记得“2027 年发生过”，则不能断定事件发生在 Q2。

这种情况标记为：

~~~text
TEMPORAL_ASSIGNMENT_AMBIGUOUS
~~~

不能强行计入 positive sample。

## 5. 与统计模型的兼容性

这种表示天然兼容未来 interval-censored event-time / survival analysis，同时不会要求我们现在就选择具体 survival model。

## 6. v0.1 迁移

已有精确 event_date 可以无损迁移：

~~~text
reported_precision = DAY
lower_bound_date = event_date
upper_bound_date = event_date
~~~

所以无需丢弃当前 fixture 和测试思想。

## 7. 暂不处理

- 同一 target window 内多次重复事件；
- 小时级/分钟级事件时间；
- 概率化时间插补；
- 具体 survival 模型选择。

这些都不应在数据 schema 阶段提前复杂化。

## 8. 下一步

**PRODUCT_PL7_LONGITUDINAL_OBSERVATION_SCHEMA_V0_2**

把 event_time interval 正式加入 runtime validator、fixtures、check-in bridge，并保留 v0.1 exact-date 迁移 helper。
