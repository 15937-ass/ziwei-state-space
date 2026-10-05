# PL7 Longitudinal Observation Schema v0.2 Acceptance

状态：**IMPLEMENTED — INTERVAL EVENT TIME READY**

## 1. 变化

v0.2 保留 v0.1 的所有 outcome / negative / censored / blind-lock 语义，只把 EVENT_OCCURRED 的 exact-only event_date 升级为 event_time interval。

统一字段：reported precision、lower bound、upper bound。

支持 DAY / MONTH / YEAR / INTERVAL。

## 2. Normal form

DAY 的上下界相同。

MONTH 必须覆盖一个规范化日历月，从该月 1 日到最后一天。

YEAR 必须覆盖同一年 1 月 1 日到 12 月 31 日。

INTERVAL 原样保存可信上下界。

系统不进行 midpoint 或随机日期插补。

## 3. Target assignment

EVENT_OCCURRED 只有在整个 event-time interval 完整落入 target window 时，才成为该 target 的 positive truth。

如果 event-time interval 只与 target window 部分重叠，runtime fail closed：TEMPORAL_ASSIGNMENT_AMBIGUOUS。

如果完全不相交，则判为 outside target window。

## 4. Non-event statuses

EVENT_NOT_OCCURRED、UNKNOWN、CENSORED 的 event_time 必须为 null。

它们继续沿用 v0.1 对完整 observation window、censoring 与 confidence 的约束。

## 5. v0.1 migration

提供 lossless migration helper。

精确 event_date 迁移为 DAY interval，上下界都等于原日期；无 event_date 的记录迁移为 event_time=null。

## 6. 统计意义

该 normal form 允许以后在不制造假精度的情况下进行 interval-censored event-history / survival 分析，但本工作单元不选择具体统计模型。

## 7. 下一步

**PRODUCT_PL7_CHECKIN_BRIDGE_V0_2_INTERVAL_TIME**

让 prospective check-in bridge 接受 exact day、month、year 或 explicit interval，并生成 v0.2 observation；对于时间区间无法完整归属于 target window 的回答继续 fail closed。
