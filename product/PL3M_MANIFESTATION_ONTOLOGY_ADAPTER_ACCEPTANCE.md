# PL3-M Manifestation Ontology Adapter v0.1

状态：**IMPLEMENTED — ADAPTER READY / KNOWLEDGE DEPENDENCY EMPTY**

## 1. 结论

产品侧已经建立 WP06B / WP06C 的 manifestation ontology adapter contract。

但当前仓库中尚未发现可消费的正式：

- KB-WP06B Manifestation Ontology artifact；
- KB-WP06C Manifestation Hypothesis Registry artifact。

因此 production registry 明确保持：

`EMPTY_KNOWLEDGE_DEPENDENCY`

产品侧**不会为了推进 PL3-M 自己造一套应象 ontology**。

## 2. 适配的知识结构

WP06B node 至少承载：

- manifestation_id；
- parent_id；
- domain；
- abstraction_level；
- source-supported labels；
- source rule IDs；
- event specificity；
- ambiguity notes；
- probability_status。

WP06C mapping 承载：

- symbolic activation；
- allowed candidate manifestation IDs；
- evidence tier；
- source rule IDs；
- source trace；
- unresolved alternatives。

## 3. Evidence tier

只允许：

- EXPLICIT
- TRANSPARENT_INFERENCE
- CASE_SUPPORT_ONLY
- HYPOTHESIS

这四层保持分开，不会因为产品运行方便而全部升级成 canonical mapping。

## 4. Probability boundary

WP06B 默认 `probability_status=UNKNOWN`。

产品 adapter 不允许把 ontology node 自带成 calibrated probability truth。未来 population calibration 属于 EMPIRICAL layer，不属于知识 ontology。

## 5. Fail-closed

以下情况全部拒绝：

- ontology / mapping version 不一致；
- parent_id 不存在；
- mapping 指向不存在的 manifestation ID；
- source-backed mapping 没有 source rule trace；
- 请求一个尚未进入 ontology 的 domain。

当知识 artifacts 根本不存在时，bundle 返回 EMPTY_KNOWLEDGE_DEPENDENCY，任何 domain routing 都 fail closed。

## 6. Test fixture 说明

测试中使用的小型 career ontology 只验证 schema / adapter 行为，不是中州派正式 ontology，也不会进入 production registry。

## 7. 当前阻塞

PL3M-02 Source-supported Possibility Router 的**接口骨架可以继续开发**，但 production routing candidates 必须保持为空，直到知识侧 WP06B/WP06C 进入 ready 状态。

## 8. 下一步

**PRODUCT_PL3M_SOURCE_SUPPORTED_POSSIBILITY_ROUTER_V0_1**

只实现 source-tier-preserving、probability-free router contract；知识 registry 为空时必须返回 abstention / knowledge dependency missing，而不是生成候选事件。
