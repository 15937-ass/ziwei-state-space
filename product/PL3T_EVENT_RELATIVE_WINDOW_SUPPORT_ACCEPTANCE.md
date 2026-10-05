# PL3-T Event-Relative Window Support v0.1

状态：**IMPLEMENTED — HG-P07-TEMPORAL-01-A ONLY**

## 1. 范围

本工作单元只实现知识侧已经批准的：

~~~text
MIGRATION_FIRST_THREE_YEARS
~~~

来源：`SRC-ZZ-003`，迁移宫 printed p109；Human Gate：`HG-P07-TEMPORAL-01-A`。

它不是通用 event timer。

## 2. 输入

resolver 只接受：

~~~text
confirmed_distant_settlement: bool
years_since_distant_relocation: int | null
travel_only: bool
trigger_provenance: str
~~~

`years_since_distant_relocation` 由上游显式提供；本层不根据日期、地址、旅行记录或命盘自动推断。

只要 confirmed_distant_settlement=true，就必须携带 trigger_provenance，以便明确现实触发证据来自哪里。

## 3. 激活条件

严格按 approved schema：

~~~text
confirmed_distant_settlement == true
AND travel_only == false
AND 1 <= years_since_distant_relocation <= 3
~~~

满足时：

~~~text
projection_priority:migration_palace:primary
rotation:annual_life_palace:preserved
rotation:other_palace:preserved
~~~

`PRIMARY` 是 ordinal routing label，不是数值权重。

## 4. Fail-closed 状态

resolver 输出 ACTIVE / INACTIVE / INSUFFICIENT。

- 未确认远地定居：INACTIVE；
- travel_only：INACTIVE；
- 已确认定居但缺 elapsed year：INSUFFICIENT；
- 第 1–3 年：ACTIVE；
- 第 4 年及以后：INACTIVE。

没有 decay、没有第 4 年 residual effect、没有自动外推。

## 5. 与 PL3-S 的边界

该规则使用一个**已确认的外部事件触发事实**，因此 TemporalEnvironmentProfile 增加：

~~~text
external_event_trigger_used = true | false
~~~

这不等于 `feedback_used` 或 `acquired_state_used`。

理由是该 Human Gate 已明确规定：这是有限 event-relative temporal context，而不是持久 acquired disposition / path-dependent memory。

因此：

- 它不改写 NatalStateProfile；
- 不写入 canonical natal truth；
- 不自动形成一般个人状态；
- 不允许从 travel signal 反推 settlement；
- 后续若需要由 observation 自动生成此 trigger，必须经过 PL3-S/bridge 的 provenance 与确认机制。

## 6. Machine-readable routing facts

ACTIVE 时至少保留：

~~~text
event:distant_relocation_settlement:confirmed
event_relative:distant_relocation_year:<1|2|3>
gate:migration_first_three_years:active
projection_priority:migration_palace:primary
rotation:annual_life_palace:preserved
rotation:other_palace:preserved
~~~

这些是 deterministic routing facts，不是 manifestation probability。

## 7. 明确禁止

- 不建立任意事件通用计时器；
- 不推断 relocation 是否发生；
- 不自动计算 elapsed years；
- 不扩展到第 4 年；
- 不设置衰减曲线；
- 不设置 priority coefficient；
- 不暂停其他宫位正常流年轮转；
- 不把这个特例泛化到婚恋、事业、疾病等事件。

## 8. 下一步

**PRODUCT_PL3T_TEMPORAL_FIXTURE_BENCHMARK_V0_1**

验证 PL3-T 从 validated temporal asset + approved event-relative overlay 到 TemporalEnvironmentProfile 的 deterministic stability，并为后续 Temporal EvidencePackage integration 冻结 fixtures。
