# PL3-M Manifestation Ontology Adapter v0.1

状态：**IMPLEMENTED — ADAPTER READY, PRODUCTION ONTOLOGY EMPTY**

## 1. 目的

建立知识侧 KB-WP06B 到产品侧 PL3-M 的版本化 adapter。

产品侧只验证并消费知识侧已经冻结的 manifestation ontology，不在这里发明“什么象对应什么事”。

## 2. Production 状态

当前：

~~~text
PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json
registry_status = EMPTY_PENDING_KB_WP06B
nodes = []
~~~

因此当前产品**没有**偷偷构造应象分类表。

## 3. Node contract

adapter 支持知识路线中已经规定的最小字段：

- manifestation_id；
- parent_id；
- domain；
- abstraction_level；
- source_supported_labels；
- source_rule_ids；
- event_specificity；
- ambiguity_notes；
- probability_status；
- source_refs。

`abstraction_level` 暂不冻结产品侧 universal vocabulary；知识路线中的层级只是 schema 方向，正式 vocabulary 必须等 KB-WP06B。

## 4. Probability boundary

canonical ontology 中：

~~~text
probability_status = UNKNOWN
~~~

并显式拒绝 probability / frequency / weight / score / posterior / likelihood / hazard / odds 等字段。

ontology 只回答“传统资料允许存在什么候选应象节点”，不回答“哪个更常发生”。

## 5. Provenance

`CANONICAL_READY` registry 的每个 node 都必须带 source refs，并满足：

~~~text
review_status = SOURCE_SPAN_VERIFIED | HUMAN_VERIFIED
source_span_verified = true
~~~

测试 fixture 只能使用 `TEST_ONLY` provenance，不能冒充 canonical。

## 6. Topology validation

adapter 确定性验证：

- manifestation_id 唯一；
- parent 必须存在；
- 禁止 self-parent；
- 禁止 cycle；
- source labels / source rule IDs / source refs 不得为空。

不额外规定 parent-child 的传统语义，因为这属于知识侧 ontology owner。

## 7. 下一步

**PRODUCT_PL3M_SOURCE_SUPPORTED_POSSIBILITY_ROUTER_V0_1**

下一步只实现 source-supported mapping 接口。生产 mapping registry 必须继续保持空，直到 KB-WP06C Manifestation Hypothesis Registry 冻结可消费 artifact。
