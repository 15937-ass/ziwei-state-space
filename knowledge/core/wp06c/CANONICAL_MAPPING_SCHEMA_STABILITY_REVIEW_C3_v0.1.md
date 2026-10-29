# Core C3 — Manifestation Mapping Schema Stability Review v0.1

Status: **REVIEW_COMPLETE**  
Verdict: **STABLE_WITH_BACKWARD_COMPATIBLE_REFINEMENT**  
Issue: #912  
Accepted corpus: **15 KMN / 15 KMM** on main `cadc98070a63cd4f76eaed1ace0f4ae182e75695`.

## 结论

现有 WP06B canonical manifestation node contract 与 WP06C canonical mapping contract 已经承受了 15 条正式映射、约 10 类语义结构的压力测试。当前证据**不支持重做本体、封闭 output_kind/event_specificity 词表、增加 universal root、或把 Core 改造成可执行 Boolean IR**。

C3 只确认一个真实的、可向后兼容修复：review provenance 的定位目前分散在 pilot / batch1 / batch2 三份文件中。新增 `CANONICAL_MAPPING_REVIEW_PROVENANCE_INDEX_v0.1.json` 作为纯索引层；它不拥有语义权威，不改变任何 review disposition、KMN/KMM 含义或 Product 权限。

## 八个审查问题

1. **source-local 条件是否可保存？— 可以。**  
   `source_condition_text`、`antecedent_rule_ids`、`modality_terms`、`real_world_prerequisites` 与 `unresolved_semantics` 可以保留来源边界；Core 并未声称这些字段已组成 executable Boolean IR。

2. **时间层是否被强行缩窄？— 没有。**  
   当前正式实例同时保存 `NATAL`、`DECADE`、`DECADE_YEAR` 与 `SOURCE_TEMPORAL_LAYER_UNSPECIFIED`。KMM-000011 对未知时间层继续 fail-closed。

3. **跨宫与 antecedent 是否足够？— 对 canonical preservation 足够。**  
   KMM-000002 显式保存 antecedent rule IDs；跨宫/OR 等复杂结构保留在 source-local 条件文本与 negative boundaries 中。Product 若要编译成结构化路由条件，应在 Product adapter 层解决，而不是倒逼 Core 发明可执行语义。

4. **语气、现实前提和禁止推断是否分离？— 是。**  
   `往往`、`唯若`、`若同时`、`除非`、`即使`均保留；“勉强求变”被明确标成 chart 无法自行建立的现实前提；blockers / forbidden inferences 独立保存。

5. **是否需要 universal root？— 不需要。**  
   15/15 KMN 当前 parent 为 null，但 Option C 已规定 null 只表示“当前没有已接受父节点”，不等于存在隐含 universal root。树仍可保持 source-native forest。

6. **Product 反馈是否暴露 GAP_CORE？— 当前没有。**  
   PG-001…PG-007 均属于 Product adapter/runtime 表达能力；HOLD-CORE-001/002 是应继续保留的来源语义未决，不应为了 Product 强解 AND/OR。

7. **review provenance 是否可扩展？— 语义足够，寻址方式需小修。**  
   当前 30 条 review record 在三份文件中均唯一，但此前消费者需手工拼接/目录 glob。C3 新增非语义 provenance index 解决定位问题。

8. **是否能向后兼容？— 可以。**  
   C3 不修改任何既有 KMN/KMM、不升 schema 版本、不改 ID、不改 canonical approval。新索引是 additive auxiliary artifact。

## 开放词表与“碎片化”风险

15 条 KMM 出现 15 个不同的 `output_kind`，14 个不同的 `event_specificity`；15 个 KMN 使用 11 个 domain 字符串。这个现象值得后续持续监控，但**不能仅凭数量就合并标签**。

原因是 #841 已接受 D2：`output_kind` 是非穷举开放词表。C3 只允许在有来源与目标语义证据时认定同义重复。比如 `career` 与 `career_scene` 目前只是 normalization review candidate，不足以触发迁移。

## 尚未由 15 条正式实例覆盖的 contract 分支

以下能力已有 schema / contract test 支持，但尚无当前 canonical 实例，因此不得宣称已被正式语料充分验证：

- KMM 的 `output_kind=UNKNOWN`;
- KMM 的 `event_specificity=NOT_APPLICABLE`;
- KMN 的 non-null `parent_id`;
- KMN/KMM 的 `SUPERSEDED` lifecycle。

这不是当前阻塞项，也不是要求人为制造实例的理由。

## Product feedback disposition

- PG-001…PG-007: **GAP_PRODUCT / NO_CORE_CHANGE**。
- HOLD-CORE-001（火铃量词）: **PRESERVE_HOLD**。
- HOLD-CORE-002（煞曜空劫量词）: **PRESERVE_HOLD**。

因此 Core 可以声明 contract 对**更广泛的 diagnostic crosswalk**稳定，但这不等于 Product production promotion、KIB/runtime authorization 或 predictive validity。

## C3 refinement

唯一实施：

`knowledge/core/wp06c/CANONICAL_MAPPING_REVIEW_PROVENANCE_INDEX_v0.1.json`

性质：
- additive；
- non-semantic；
- no schema bump；
- no KMN/KMM rewrite；
- no Product authority；
- probability remains UNKNOWN。

## 下一步

C3 验收后停止盲目扩充 mapping。按 #901 进入 C4，比较真正的共享阻塞：
1. Product 返回的 genuine GAP_CORE（当前没有）；
2. palace `KNOWLEDGE_CORE_GAP`；
3. 真正阻塞 `N -> E -> tau -> M0` 的 WP07B temporal-response gap。

本 review **未触发 PI Human Gate**。
