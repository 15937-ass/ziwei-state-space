# PL3-T Temporal Environment Profile v0.1

状态：**IMPLEMENTATION CONTRACT**

## 1. 目的

PL3-T 把已验证的时间层排盘事实与 source-backed temporal reaction 组合成一个确定性的 `TemporalEnvironmentProfile`。

~~~text
NatalStateProfile
+ normalized temporal chart facts
+ source-backed temporal reaction evidence
-> TemporalEnvironmentProfile
~~~

它描述“这一时段有哪些结构条件被激活、加强、削弱、转化或改变解释路由”，不描述现实事件必然发生。

## 2. 核心边界

`TemporalEnvironmentProfile` 禁止使用：

- user feedback；
- acquired personal state；
- target-period outcome；
- empirical manifestation probability；
- personal posterior。

这些都属于 PL3-S / PL3-M / PL5 后续层。

## 3. Temporal layers

v0.1 容器允许：

~~~text
DECADE
SMALL_LIMIT
YEAR
MONTH
DAY
HOUR
~~~

这里只表示产品可承载的时间层，不建立新的传统优先级规则。

## 4. Reaction effect

v0.1 只保存非数值、source-backed effect label：

~~~text
ACTIVATE
STRENGTHEN
WEAKEN
TRANSFORM
ROUTE
PRESERVE
~~~

幅值默认 `UNIDENTIFIED`。若 source 明确给出相对次序，可使用 `SOURCE_ORDINAL_ONLY`，但不得自行转成数值。

## 5. Event-relative context

本 core 只提供 evidence 容器。

具体 event-relative window 只能由已经 source-reviewed / Human-Gate-approved 的规则进入，例如既有 `MIGRATION_FIRST_THREE_YEARS`。core 不提供通用事件计时器。

## 6. Determinism

~~~text
same NatalStateProfile
+ same target_label
+ same temporal facts
+ same reaction evidence
+ same knowledge version
=> same TemporalEnvironmentProfile.profile_id
~~~

输入顺序变化不得改变 profile_id。

## 7. 与 PL3-N 的关系

PL3-T 必须引用 `natal_profile_id`，且 knowledge_version 必须与 NatalStateProfile 完全一致。

时间层不能回写 NatalStateProfile。

## 8. v0.1 不做

- 不直接读取用户现实状态；
- 不训练 probability；
- 不定义 manifestation router；
- 不计算 causal effect；
- 不生成“今年一定发生 X”的输出；
- 不把多个 reaction 做人工加权求和。

## 9. 下一步

**PRODUCT_PL3T_TEMPORAL_ASSET_ADAPTER_V0_1**

把 PL1 已通过双/三引擎验证的 temporal snapshot 输出适配为 `TemporalFact`，复用现有 decade/year/month/day/hour 事实，不重新发明排盘逻辑。
