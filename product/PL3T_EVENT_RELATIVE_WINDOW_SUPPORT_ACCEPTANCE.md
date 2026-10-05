# PL3-T Event-Relative Window Support v0.1

状态：**IMPLEMENTED — SINGLE APPROVED WINDOW ONLY**

## 1. 目的

本工作单元把知识侧已经由 Human Gate 冻结的：

`MIGRATION_FIRST_THREE_YEARS`

接入产品层 `TemporalEnvironmentProfile.event_relative_context`。

它不是新的通用 timer 框架。

## 2. 唯一允许窗口

来源：

- registry: `knowledge/temporal/event_relative_windows_v0.1.csv`
- resolver: `src/wp05_event_relative_time.py`
- Human Gate: `HG-P07-TEMPORAL-01-A`
- source: `SRC-ZZ-003`, 迁移宫 printed p109

产品层会严格校验 frozen registry：

- event = confirmed distant relocation / settlement；
- counter = `years_since_distant_relocation`；
- active = year 1..3；
- travel-only 不激活；
- Migration Palace = PRIMARY；
- annual Life-Palace rotation = PRESERVED；
- other-palace rotation = PRESERVED。

任何 registry 漂移都会 fail closed。

## 3. 不做的事

v0.1 明确禁止：

- 从排盘自动推断“已经远地定居”；
- 从地址、旅行记录或自然语言自动推断 relocation；
- 从日期自动计算 years-since-relocation；
- 把旅行当定居；
- 延伸到第 4 年以后；
- 建 decay curve；
- 建 numeric priority weight；
- 把 event-relative overlay 变成第七个 canonical time layer；
- 泛化成任意事件的 event timer。

相对年份必须由上游已确认的现实事件/历史层提供。

## 4. 产品接口

新增：

`src/product/event_relative_window.py`

核心接口：

- `load_approved_migration_window_spec()`
- `resolve_approved_migration_window()`
- `build_temporal_environment_with_migration_window()`

产品层不复制传统规则，而是复用知识侧 source-bounded resolver。

## 5. 状态语义

输出 context evidence 仅允许表达：

- `ACTIVE`
- `INACTIVE_TRAVEL_ONLY`
- `INACTIVE_EVENT_UNCONFIRMED`
- `INACTIVE_OUTSIDE_APPROVED_WINDOW`

这些只是 routing/context 状态，不是现实 outcome。

## 6. 确定性

同一 NatalStateProfile、同一 target、同一 temporal facts、同一 confirmed relocation context、同一 knowledge version：

`=> same TemporalEnvironmentProfile.profile_id`

Event-relative context 不创建新的 canonical `active_layers`；例如只输入 YEAR facts 时，active layer 仍然只是 YEAR。

## 7. 测试

新增 `tests/test_product_event_relative_window.py`，覆盖：

- frozen single-window registry；
- year 1/2/3 active；
- year 4 inactive；
- unconfirmed event inactive；
- travel-only inactive；
- primary migration routing + preserved annual rotation；
- deterministic profile ID；
- registry drift fail closed；
- multiple-window generalization fail closed。

## 8. 下一步

**PRODUCT_PL3T_TEMPORAL_FIXTURE_BENCHMARK_V0_1**

把 PL3-T core、asset adapter、source-gated reaction compiler 与 approved event-relative context 组合成固定 fixture benchmark，验证：

`same natal + same target time + same knowledge version -> same TemporalEnvironmentProfile`

并继续保持 production temporal reaction registry 为空，直到知识侧 KB-WP07B structured normalization 到位。
