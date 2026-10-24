# Option C 元数据契约提案 v0.2：吸收 QI/QR 重叠审计的映射边界

状态：PROPOSAL_ONLY_NOT_CANONICAL  
本文件是 v0.1 的后续提案版本，不覆盖 v0.1，不是冻结 schema。  
关联：[Issue #735](https://github.com/15937-ass/ziwei-state-space/issues/735) · [PI 决策包 v0.1](../qi-qr-overlap-audit/QI_QR_OVERLAP_PI_DECISION_PACKAGE_v0.1.md) · [八组来源/层级审计 v0.1](../qi-qr-overlap-audit/QI_QR_OVERLAP_PAIR_AUDIT_v0.1.md)

## 1. 本版本的目的和边界

v0.1 主要提出 Option C 的三条元数据轴：output_kind、event_specificity、source_epistemic，以及缺失状态处理。v0.2 仅增加一个必要的审查约束：**在来源断言映射到 QI/QR 候选概念时，必须明确语义边界、证据角色和映射理由。**

QI/QR 的概念身份与 output_kind/event_specificity/source_epistemic 不是同一维度：
- output_kind 回答规范化主张是什么语义形态；
- event_specificity 回答该主张与事件的具体关系；
- source_epistemic 回答原始来源对 literal claim 的支持程度；
- QI/QR 是知识本体中的候选/正式语义目标；
- semantic role/evidence tier 说明某条来源在映射论证中扮演什么角色。

不得将 QI/QR 的层级或角色问题塞入 output_kind、event_specificity 或 source_epistemic 的值域；也不得把这次审计解释为需要增加新的全局元数据轴。

## 2. 继续复用的已批准契约

沿用 knowledge/REVIEW_SCHEMA_v0.3.md 与 knowledge/KB_SCHEMA.md：
- source_epistemic：EXPLICIT、INFERRED_FROM_SOURCE、UNRESOLVED_SOURCE；
- normalization_epistemic：SOURCE_PRESERVING、INFERRED、IMPLEMENTATION、HYPOTHESIS、UNRESOLVED；
- review_status：MODEL_EXTRACTED、MODEL_SELF_REVIEWED、SOURCE_SPAN_VERIFIED、HUMAN_VERIFIED；
- target_type、operator、condition、provenance、normalization_rationale、Conflict object 等既有机制。

不得用 review_status 推导 source_epistemic；不得把 source_epistemic=EXPLICIT 当作映射或归一化已经正确；不得因 source span verified 自动批准 QI/QR mapping。

## 3. 映射审查要求（本版本提案）

每个 MappingProposal / inference edge 的审查记录应能回答：

1. **来源主张是什么？** 引用具体 rule ID、source ID/page/span、条件、比较对象和模态。
2. **目标概念是什么？** 使用当前仓库实际存在的 QI/QR ID；候选概念必须保持候选标记。
3. **为什么映射到这个目标？** 给出目标特定的 rationale，不能仅以“同一条规则已用于另一个维度”为理由。
4. **证据角色是什么？** 至少区分 direct-state/relational evidence 与 projection/outcome evidence；必要时说明 source assertion、modifier、interaction/coupling 或 derived outcome。
5. **作用主体和对象是什么？** 对功能、调和、支持等描述，明确 bearer/agent、target、condition；若来源未说明，标记 unknown/unresolved，不自行补齐。
6. **归一化增加了什么？** 明确哪些是 source-preserving，哪些是 inferred/hypothesis/implementation。
7. **哪些推断被禁止？** 记录不能由该规则推出的相邻维度或现实结论。
8. **当前状态是什么？** 区分研究处置、候选映射、经人工批准的 canonical mapping 和 Product 可消费状态。

本提案不要求立即新增数据库字段。先用当前 review artifact、mapping rationale、condition、provenance、target_type/operator、review_status 与现有 Conflict object 表达。只有在实现试验表明现有结构无法满足能力问题时，才提出最小字段差异，并另行走 schema/Human Gate。

## 4. 八组边界的提案约束

下表是研究层映射指导，不修改 knowledge/qi_ontology.yaml 的当前正式定义。

| Pair | 提案边界 | 禁止的自动推导 |
|---|---|---|
| QI-01 / QI-14 | 动力学外放/收敛 vs 信息/状态可见性 | 潜藏 ≠ 必然遮蔽；外放 ≠ 必然显露 |
| QI-03 / QI-04 | 结构是否变化 vs 是否维护/突破既有结构 | 变化 ≠ 开创；共享规则 ≠ 等价/独立证明 |
| QI-02 / QI-15 | 刚柔状态 vs 缓冲/调和功能 | 被调和后的状态 ≠ 被调和主体自身具备缓冲能力 |
| QI-08 / QI-06 | 行动启动/推进驱动 vs 决策启动/迟疑/决断方式 | 决得快 ≠ 执行强；行动多 ≠ 决策审慎 |
| QI-04 / QI-16 | 维护/突破结构 vs 目标明确/目标组织 | 开创 ≠ 目标明确；建设性结果 ≠ 目标明确 |
| QI-08 / QI-16 | 行动驱动 vs 目标组织程度 | 承担任务 ≠ 目标明确；目标明确 ≠ 行动驱动强 |
| QI-17-CAND / QI-18-CAND | 意志控制候选 vs 毅力/持续性候选 | 候选来源区分 ≠ 正式原语批准 |
| QR-01 / QR-04 | 关系整合/孤离 vs 支持资源 | 资源数量 ≠ 关系整合；资源存在 ≠ 资源可用/支持已发生 |

### 4.1 层级/角色问题

- QI-02/QI-15：用现有 operator/condition/provenance 说明调和是状态变化、外部 modifier 还是交互结果；不能把三者默认压成单星 intrinsic capacity。
- QR-01/QR-04：将关系网络状态与资源存在、资源可用、实际支持结果分开；projection-tier 证据不能与 L1/L2 direct-state evidence 等权。
- QI-04/QI-16：ZZ-PJ-X06 的源文条件差异保持 unresolved；不得把原文“或”改成更强的合取条件。
- QI-17-CAND/QI-18-CAND：仅允许 candidate-only review；不分配正式 ID、不接受 canonical mapping。

## 5. 证据和映射状态必须分离

本提案要求审查材料至少区分以下概念状态，但不主张为它们新建一套全局枚举：
- source epistemic：来源对 literal claim 的支持程度；
- normalization epistemic：从 literal claim 到机器/概念表示的转换性质；
- review status：来源跨度/归一化经过什么审查；
- mapping disposition：当前证据是否支持某个候选映射；
- canonical approval：该映射/概念是否通过适用 Human Gate；
- consumer readiness：下游 Product/runtime 是否已被单独授权消费。

一个字段不能替代另一个字段。比如 SOURCE_SPAN_VERIFIED 不等于 mapping accepted；mapping proposal 不等于 canonical mapping；canonical mapping 也不自动等于 Product consumption authorization。

## 6. 未知、缺失、冲突与不适用

继续沿用 v0.1 的保守处理原则：
- UNKNOWN：已经审查，但当前无法判定；
- MISSING：必要字段或审查记录尚不存在；
- CONFLICT：存在互不兼容的解释，保留双方与来源；
- NOT_APPLICABLE：该语义轴对当前对象确实不适用。

优先复用现有 Conflict object 和审查记录；不能把这四种状态改成一个通用 null，也不能把“没有找到共享规则”改成“已证明独立”。若需要正式增加共享状态原语或改动受控词表，先说明为什么现有机制不够用，并取得额外 PI/Human Gate。

## 7. 与 Option C 三轴的兼容关系

- 不改变 output_kind 的语义：它仍描述规范化主张的形态。
- 不改变 event_specificity 的语义：它仍描述与事件的具体关系；不用于表示 QI/QR 层级。
- 不改变 source_epistemic 的受控值：沿用 REVIEW_SCHEMA_v0.3。
- 不改变 projection_mode：它描述规则投影/约束方式，不是 ontology hierarchy。
- 不把 QI/QR mapping disposition 伪装成 source_epistemic 或 event_specificity 值。
- 不覆盖 v0.1；本文件是待审的 v0.2 后续提案，不冻结生产 schema。

## 8. 迁移、兼容和回滚

当前没有生产迁移：
1. 不回写现有源 CSV/JSON，不改 canonical QI/QR 定义或映射。
2. 先在非 canonical review artifact 中试用本提案的映射理由与角色记录。
3. 若未来需要新字段，提交独立 schema diff、旧数据兼容方案、缺失值迁移、验证用例和回滚方案。
4. 若新字段成为共享语义原语，先通过相应 Human Gate，再实现。
5. 任何失败或 PI 拒绝均可通过将本 v0.2 标记为 superseded/不采纳来回滚；不需要回滚生产数据，因为本提案不修改生产数据。

## 9. 非目标

本提案不：
- 更改或冻结 output_kind/event_specificity 的生产词表；
- 修改 REVIEW_SCHEMA_v0.3 或 KB_SCHEMA；
- 修改 knowledge/qi_ontology.yaml、star_cores.yaml、star_systems.yaml 或来源行；
- 分配正式 ontology IDs、接受 mapping 或创建 universal root；
- 修改 Product adapter、registry、KIB lock、runtime 或消费权限；
- 声称概念正交、紫微斗数现实预测有效，或推导数值权重/概率。

## 10. PI 审议结果（2026-10-24）

**PI 决定：六项全部接受，作为下一独立、有限范围的契约实现工作单的设计输入。**

1. **语义边界：** QI/QR 的概念边界属于 mapping review；不将概念层级或语义角色塞入 `output_kind`、`event_specificity` 或 `source_epistemic`。
2. **映射证据：** 每个目标映射必须有独立、目标特定的 rationale，并记录证据角色；同一来源行不能被重复计作独立证据。
3. **定义收窄：** QI-04、QI-06、QI-16 的收窄只作为后续 canonical review 的候选，不在本工作单修改正式定义。
4. **功能与关系角色：** QI-15 的审查应记录 bearer/agent、target、condition，以及证据描述的是状态变化、外部 modifier 还是 interaction；QR-04 区分资源存在、资源可用与支持实际发生。
5. **优先复用 schema：** 先使用现有 review artifact、mapping rationale、condition、provenance、`target_type`/`operator`、`review_status` 与 Conflict object。只有有限实现试验证明存在具体能力缺口时，才提出最小字段差异，并在任何共享 schema 变更前经过额外 Human Gate。
6. **候选保护：** QI-17-CAND / QI-18-CAND 继续保持候选身份；没有独立证据与单独审批，不分配正式 ID、不接受 canonical mapping。

### 批准范围与下一步

本次批准**仅代表接受上述设计输入**，不代表冻结生产 schema，不构成 canonical ontology 修改、正式 mapping 接受、受控词表扩展或 Product/runtime 消费授权。

下一工作单应在非 canonical review artifact/fixture 中做有边界的实现验证，并以测试回答：现有字段是否足以表达目标特定理由、证据角色、主体/对象/条件、来源条件保真、四种未知状态与候选/正式状态边界。若现有结构足够，不新增字段；若不足，先提交最小 schema 差异、兼容/迁移/回滚方案，并等待额外 Human Gate。

本文件仍为 `PROPOSAL_ONLY_NOT_CANONICAL`。任何 canonical 定义修改、正式 ID 分配、accepted mapping 或 Product 消费授权均须另开工作单并通过适用审批。