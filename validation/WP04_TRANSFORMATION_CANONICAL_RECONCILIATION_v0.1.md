# WP04 四化 canonical reconciliation 启动记录

Status: **ACTIVE — SOURCE REVIEW 40/40 COMPLETE; CANONICAL RECONCILIATION STARTED**

## 1. 当前边界

四化专章 40 个 source units 已全部回源，形成 174 条 source-span-verified closure rules。
旧 `transformation_rules_v0.1.csv` 仍为 56 条，主要来自此前十四正曜/六十星系等章节，不能把“旧目录 56 条”与“四化专章覆盖完成”混为一谈。

本轮不直接把 174 条机械 append 到旧目录，而先建立：
`knowledge/migrations/wp04_transformation_canonical_reconciliation_v0.1.csv`

## 2. 初步 reconciliation 分层

- PARTIAL_LEGACY_OVERLAP: 32
- NEW_DEDICATED_PROVENANCE: 140
- NEW_SOURCE_VARIANT: 2

对应执行队列：

- SEMANTIC_RECONCILIATION_REQUIRED: 32
- ADD_DEDICATED_PROVENANCE_PENDING_LAYER_CHECK: 140
- PRESERVE_SOURCE_VARIANT: 2

## 3. 禁止的快捷做法

1. 不允许仅因 modifier 名称相同，就把专章规则与 legacy rule 判定为等价。
2. 不允许把 projection / gate / tradition mapping variant 全部塞进 L1 operator catalog。
3. 不允许把中州派专章中的 mapping variant 静默替换成其他传承常用映射。
4. 不允许为了让测试通过而删减已经 source-reviewed 的 174 条 closure rules。

## 4. 当前发现的 legacy modifier 空位

旧 56 条目录中没有 exact modifier 记录、而专章存在的 modifier：

- 巨门化禄
- 巨门化权
- 武曲化科
- 文昌化科
- 文曲化科
- 天府化科_壬干支系
- 文曲化忌
- 文昌化忌

这类项优先做 canonical layer review，因为它们最可能代表旧目录真实 coverage gap。

## 5. CI 修复

此前 PR #54 的失败并非 source mismatch，而是测试仍冻结在化禄/化权/化科的中间累计数量（45/85/127），当四组全部完成后 closure 已达到 174。
测试现已改为 final-stage + group-subset invariant；最新 decontamination-ci 已通过。

## 6. 下一步

按以下顺序执行：
1. 8 个 exact-modifier coverage gaps；
2. 32 条 PARTIAL_LEGACY_OVERLAP 做语义等价/非等价判定；
3. 其余 NEW_DEDICATED_PROVENANCE 按 L1/L2/gate/projection 分层；
4. 2 条 NEW_SOURCE_VARIANT 固化 tradition-scoped representation；
5. 再进入辅助八曜 / 六煞 / 杂曜原章节 coverage closure。

若此过程中需要改变 core operator definition 或新增 primitive qi，才开启 Human Gate。
