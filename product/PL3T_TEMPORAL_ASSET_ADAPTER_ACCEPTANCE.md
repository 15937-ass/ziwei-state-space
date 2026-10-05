# PL3-T Temporal Asset Adapter v0.1

状态：**IMPLEMENTATION CONTRACT**

## 1. 目的

本工作单元复用 PL1 已通过多引擎验证的 normalized horoscope snapshot，将其直接适配为 PL3-T `TemporalFact`。

不重新排盘，不重新计算大限/流年，不新增传统语义。

## 2. 冻结映射

PL1 scope 到 PL3-T layer：

~~~text
decadal -> DECADE
age     -> SMALL_LIMIT
yearly  -> YEAR
monthly -> MONTH
daily   -> DAY
hourly  -> HOUR
~~~

`age` 是 PL1 normalized exporter 对小限 scope 的工程字段名；PL3-T 使用产品层统一名 `SMALL_LIMIT`。

## 3. 保留的事实

每层直接保留 normalized scope 中已有的：

- index；
- name；
- stem；
- branch；
- nominal_age（存在时）；
- palace_names；
- mutagen；
- flow stars；
- YEAR 层额外保留 suiqian12 / jiangqian12。

这些字段被拆成稳定原子事实字符串，仅用于 deterministic matching / trace，不代表产品层已经赋予吉凶或事件含义。

## 4. Provenance

每条 TemporalFact 保留：

~~~text
PL1:<engine>:<engine_version>:adapter=<adapter_version>:target=<target_id>:scope=<scope>
~~~

因此 PL3-T 可以追溯事实来自哪套已经进入 Chart Trust 的 normalized engine output。

## 5. Fail-closed

六个 scope 任一缺失、scope 关键字段缺失、stars 结构不合法、target_id 不唯一时，adapter 直接拒绝。

不使用“缺了就猜”“用相邻时间层补齐”等降级逻辑。

## 6. 边界

本 adapter 不做：

- 吉凶判断；
- temporal reaction 推理；
- manifestation routing；
- empirical probability；
- feedback/state update；
- source 未定义的 layer priority。

## 7. 下一步

**PRODUCT_PL3T_NATAL_TEMPORAL_REACTION_COMPILER_V0_1**

在 PL1 temporal facts 已接入后，下一步只把知识侧已经 source-reviewed 的 temporal reaction 规则编译为 `TemporalReactionEvidence`，并要求 antecedent 与 Natal/Temporal facts 显式匹配。
