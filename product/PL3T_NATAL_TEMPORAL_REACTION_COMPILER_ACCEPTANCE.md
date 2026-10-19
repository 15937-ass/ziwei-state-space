# PL3-T Natal × Temporal Reaction Compiler v0.1

状态：**IMPLEMENTED — COMPILER READY, PRODUCTION REGISTRY EMPTY**

## 1. 目的

建立：

~~~text
NatalStateProfile
+ TemporalAssetBundle
+ explicitly normalized temporal reaction registry
-> matched TemporalReactionEvidence
~~~

这是 PL3-T 第一个真正把原局与时间层连接起来的执行接口。

## 2. 最重要的 fail-closed 原则

WP05 中大量 DECADE/YEAR/MONTH 等记录虽然已经 source-span reviewed，但 `condition` 仍是自由文本。

本 compiler **禁止**：

- 自动 NLP/LLM 解析自由文本 condition；
- 看到 `TIMING_TRIGGER` 就直接执行；
- 从 EVENT_CANDIDATE 推导现实事件；
- 根据关键词自行拆 natal antecedent / temporal antecedent。

因此 production registry v0.1 当前保持空表，等待知识侧 KB-WP07B 或等价的 structured temporal normalization。

## 3. 一个 reaction 能进入 runtime 的必要条件

必须同时满足：

1. source span verified；
2. review_status 为 SOURCE_SPAN_VERIFIED / HUMAN_VERIFIED；
3. normalization_verified=true；
4. normalization_epistemic 非 hypothesis；
5. case_support_only=false；
6. 明确 natal antecedent facts 或 required_natal_rule_ids；
7. 明确 positive temporal condition；
8. 每个 temporal atom 都显式绑定到 rule.layer。

## 4. Temporal condition facts

PL3T asset adapter 在保留原始 normalized facts 的同时，现在额外输出纯结构化 condition facts：

- TIME_LAYER；
- BRANCH_PRESENT；
- PALACE_PRESENT；
- STAR_PRESENT；
- PALACE_HAS_STAR；
- TRANSFORMATION_PRESENT；
- TAG_PRESENT。

当且仅当 PL1 的 temporal star object 显式携带 `mutagen` 字段时，adapter 还会输出带有 `layer + palace_name + star + mutagen` 的 star-bound `TRANSFORMATION_PRESENT`。scope 级 `mutagen` 数组仍单独保留，不会与同层星曜进行位置猜测或自动关联。

这些只是 PL1 排盘字段的结构化镜像，不包含吉凶、事件或概率解释。

## 5. Reaction evidence

匹配后保存：

- rule/source/review provenance；
- effect；
- magnitude_status；
- matched natal facts；
- matched temporal facts；
- matched natal rule IDs。

所以后续每个“加强/削弱/转化/激活”都必须能回指为什么被触发。

## 6. 数值边界

v0.1 仍只允许：

~~~text
magnitude_status = UNIDENTIFIED | SOURCE_ORDINAL_ONLY
~~~

不得把“加强”擅自变成 +0.7，也不得把多个 reaction 相加成吉凶总分。

## 7. 当前知识依赖

知识侧 roadmap 已将 `KB-WP07B Temporal Reaction Specification` 定为正式 owner。

在其 structured antecedent artifact 冻结前：

~~~text
compiler = READY
production temporal reaction registry = EMPTY
~~~

这不是产品阻塞：我们可以继续实现已经 Human-Gate 批准的 event-relative window、fixtures 与 EvidencePackage；待 KB-WP07B artifact 到位后直接装载。

## 8. 下一步

**PRODUCT_PL3T_EVENT_RELATIVE_WINDOW_SUPPORT_V0_1**

实现已获 HG-P07-TEMPORAL-01-A 批准的 `MIGRATION_FIRST_THREE_YEARS`，只做这个明示窗口，不建立通用事件计时器。


## 9. Product-only fact-contract gap audit

The detailed status is recorded in `product/PL3T_TEMPORAL_FACT_CONTRACT_GAPS_v0.1.md`.

The adapter change does not make any existing free-text temporal rule executable by itself. Activation/convergence semantics, favorable/unfavorable-period predicates, and multi-year sequence gates remain blocked; the canonical production reaction registry stays empty until source-faithful normalization is approved.
