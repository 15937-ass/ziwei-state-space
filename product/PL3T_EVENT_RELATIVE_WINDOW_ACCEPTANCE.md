# PL3-T Event-relative Window Support v0.1

状态：**IMPLEMENTED — ONLY HG-P07-TEMPORAL-01-A**

## 1. 范围

本工作单元只实现知识侧已经 Human Gate 批准的：

~~~text
MIGRATION_FIRST_THREE_YEARS
~~~

即远地定居后头三年的迁移宫解释优先窗口。

没有建立通用 event timer。

## 2. 输入

严格沿用 approved schema：

~~~text
confirmed_distant_settlement: bool
years_since_distant_relocation: int | null
travel_only: bool
trigger_provenance: required when confirmed=true
~~~

产品层不从日期、地址、旅行记录或命盘自行推算 relocation event 或 elapsed years。

## 3. 激活条件

只有：

~~~text
confirmed_distant_settlement == true
AND travel_only == false
AND 1 <= years_since_distant_relocation <= 3
~~~

才返回 ACTIVE。

## 4. ACTIVE 输出

只输出 source-approved routing facts：

~~~text
event:distant_relocation_settlement:confirmed
event_relative:distant_relocation_year:<1|2|3>
gate:migration_first_three_years:active
projection_priority:migration_palace:primary
rotation:annual_life_palace:preserved
rotation:other_palace:preserved
~~~

`PRIMARY` 是 ordinal routing label，不是数值权重。

## 5. 为什么这里允许 external event trigger

此前 PL3-T 禁止 personal feedback 修改 chart-derived temporal facts，这一边界继续成立。

HG-P07-TEMPORAL-01-A 是一个已经批准的窄例外：source 明确把“已发生的远地定居”作为有限时间窗触发条件。因此 profile 增加：

~~~text
external_event_trigger_used
~~~

它与 `feedback_used` / `acquired_state_used` 分开：

- external event 只开启 source-explicit temporal routing window；
- 不改 Natal Prior；
- 不学习 personal posterior；
- 不成为通用 history memory；
- 不建立 decay。

## 6. Fail-closed

- confirmed=true 但无 trigger provenance -> reject；
- confirmed=true 但 elapsed years unknown -> INSUFFICIENT；
- travel only -> INACTIVE；
- year > 3 -> INACTIVE；
- negative year -> reject。

## 7. 下一步

**PRODUCT_PL3T_TEMPORAL_FIXTURE_BENCHMARK_V0_1**

建立 PL3-T fixture benchmark：固定 NatalStateProfile + PL1 temporal snapshot + reaction registry version + event-relative context，验证 profile determinism、层级边界、冲突保留和 source trace。
