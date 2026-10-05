# PL3-M Source-Supported Possibility Router v0.1

状态：**IMPLEMENTED — ROUTER READY, PRODUCTION MAPPING EMPTY**

## 1. 目的

实现知识侧停止位置：

~~~text
symbolic activation
-> manifestation candidate
-> evidence tier
-> source trace
[STOP before probability]
~~~

## 2. Production 状态

当前 mapping registry：

~~~text
registry_status = EMPTY_PENDING_KB_WP06C
mappings = []
~~~

因此在知识侧 WP06C 未冻结前，产品不会自行建立“某气核一定/容易应某事”的映射。

## 3. Mapping antecedent

v0.1 只接受显式：

- required_activation_ids；
- required_rule_ids。

至少一个非空。router 只做集合匹配，不解析传统自由文本，不用 LLM 猜 antecedent。

## 4. Evidence tier

完整保存知识路线要求的四级：

~~~text
EXPLICIT
TRANSPARENT_INFERENCE
CASE_SUPPORT_ONLY
HYPOTHESIS
~~~

但只有前两级可以输出：

~~~text
SOURCE_SUPPORTED_POSSIBILITY
~~~

`CASE_SUPPORT_ONLY` 与 `HYPOTHESIS` 即使 antecedent 命中，也只进入 held_mappings，不冒充 canonical possibility。

## 5. Probability boundary

所有 mapping 与 output 强制：

~~~text
probability_status = UNKNOWN
~~~

并拒绝 probability / frequency / weight / score / posterior / likelihood / hazard / odds / rank 等字段。

本 router 没有排序，也没有“最可能应象”。

## 6. Provenance

possibility 同时携带：

- mapping source refs；
- ontology node source refs；
- matched activation IDs；
- matched rule IDs；
- evidence tier。

因此以后即使加 empirical probability，也能清楚区分传统来源和统计来源。

## 7. Fail-closed

- ontology 未冻结 -> ONTOLOGY_NOT_READY；
- mapping 未冻结 -> MAPPING_REGISTRY_NOT_READY；
- 无命中 -> NO_ACTIVE_MAPPING；
- TEST_ONLY / CANONICAL_READY 两端模式不一致 -> 拒绝。

## 8. 下一步

**PRODUCT_PL3M_CONTEXT_GATE_V0_1**

下一步建立 N + E_t + S_t + A_t + C_t 的产品上下文容器，但仍不产生经验概率。它只决定哪些输入可供后续 manifestation routing/calibration 使用，并显式保留 missing/conflict/abstention。
