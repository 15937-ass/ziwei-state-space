# Option C 最小语义契约收束审查 v0.1

**状态：`PROPOSAL_ONLY_NOT_CANONICAL`；供 PI 审议，不是生产 schema 或冻结词表。**  
**工作单元：** #841 / `KB-CORE-WP06B-OPTION-C-MINIMAL-CONTRACT-CLOSURE-01`  
**架构前提：** PI 已选择 Option C（来源本位根森林 + 正交元数据轴）；本工作不重开 A/B/C 选择。

## 1. 本轮结论

1. Option C 的三轴区分仍然成立：`output_kind` 描述规范化主张的语义形态；`event_specificity` 描述主张与事件的具体关系；`source_epistemic` 描述来源对 literal claim 的支持程度。
2. **现有候选值域不宜直接冻结为穷尽性生产枚举。** 已有边界案例能支持过程、行动条件结果、场景、方向轴、领域边界、跨宫约束、结构约束、时间条件和事件候选；但十四主星矩阵的交叉审计指出，内在状态／性质主张、一般关系主张和评价性主张在候选 crosswalk 中没有直接且稳定的 `output_kind` 对应。不能把它们强塞进最相近的值。
3. 本轮不建议增加全局 `metadata_axis_status` 共享原语。先在非 canonical 审核材料中记录各轴的状态和值；现有 `mapping_review` 只用于其既定的逐目标审核语义，不应被误称为已经提供了通用的三轴状态 schema。
4. 对 `event_specificity`，非事件对象可在审核材料中标记 `NOT_APPLICABLE`；这是一种轴状态，不是新的事件类别。不要把 `UNKNOWN`、`MISSING`、`CONFLICT`、`NOT_APPLICABLE` 塞进事件值域。
5. `source_epistemic` 继续只复用 REVIEW_SCHEMA v0.3 的 `EXPLICIT`、`INFERRED_FROM_SOURCE`、`UNRESOLVED_SOURCE`。跨度核验、归一化状态、审核状态、映射处置、canonical 批准和消费者就绪仍是不同问题。
6. 不创建通用应象根、不分配正式 ontology ID、不接受正式映射、不改共享生产 schema、不开放 Product/KIB/runtime。

## 2. 依据与边界

本审查复用当前 main 已接受的材料，不把提案摘要冒充新的原文核验，也不重复十四主星来源审计：

- `knowledge/core/wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.1.md`：三轴与候选值域、状态提案。
- `knowledge/core/wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.2.md`：QI/QR 映射边界与不新增全局轴的约束。
- `knowledge/core/wp06b/OPTION_C_CONTRACT_VALIDATION_PROBE_v0.1.md`：现有字段与审核材料的能力探针。
- `knowledge/core/wp06b/MAPPING_REVIEW_SCHEMA_v0.1.json`：已接受的逐目标、非 canonical 审核 envelope。
- `knowledge/core/wp06b/MANIFESTATION_ROOT_DECISION_PACKET_v0.1.md`：Option C 方向性决定与来源边界。
- `knowledge/core/14star-property-matrix/14STAR_PROPERTY_MATRIX_QIQR_AUDIT_v0.1.md`：QI/QR 层级、证据角色和输出形态 crosswalk。
- `knowledge/palaces/P09_career/wp06c/P09_WP06C_SOURCE_CANDIDATE_INDEX_v0.1.json`：三个 P09 候选的来源锚点与限制；状态仍为 `CANDIDATE_ONLY_NOT_CANONICAL`。

来源附件 `SRC-ZZ-003` 的 SHA-256：`6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`。CA01-035、CA01-045 在 PDF p.67／印刷 p.133–134，CA05-469 在 PDF p.72／印刷 p.144 已有直接扫描复核记录。W01-002、CA01-005、CA01-007、CA09-809 等其余案例只沿用现有已接受记录；本工作没有声称重新逐字复核这些来源。

## 3. 两条轴的语义边界与测试判定

### 3.1 `output_kind`

建议继续把它定义为“规范化主张的语义形态”，而不是本体深度、规则投影方式、证据等级、语义角色或事件是否真实发生。

现有候选值可以作为**已观察到的候选类别**保留，但暂不能作为穷尽性生产枚举冻结：

- `PROCESS_PATTERN`：过程或发展序列。
- `ACTION_CONDITIONED_OUTCOME`：依赖现实行动前提的结果。
- `SCENE_OR_CONTEXT`：职业／情境场景。
- `DIRECTIONAL_AXIS`：方向或发展轴。
- `DOMAIN_SEMANTIC_BOUNDARY`：领域／宫位语义边界。
- `CROSS_PALACE_CONSTRAINT`：跨宫解释约束。
- `STRUCTURAL_CONSTRAINT`：推断前提或结构条件。
- `TEMPORAL_CONDITION`：时间范围或触发条件。
- `EVENT_CANDIDATE`：仍需证据等级与 case-only 门控的事件候选。

**未覆盖的类别不是被否定的类别。** 现有矩阵 crosswalk 对内在状态／性质、一般关系状态、评价性成分都未找到稳定的一对一候选值。建议在审核层记录轴状态 `UNKNOWN` 和理由（它不等于 `source_epistemic=UNRESOLVED_SOURCE`，也不等于 `normalization_epistemic=UNRESOLVED`），等 WP06C 出现实际目标、并完成来源与概念边界审查后，再决定是否补充候选值。不要仅为“把枚举补齐”而臆造共享原语。

### 3.2 `event_specificity`

候选值只描述候选主张与事件的关系，不是观测事实字段：

- `PROCESS_SEQUENCE_NOT_SINGLE_EVENT`：过程，不是单一事件。
- `CONDITIONAL_OUTCOME_NOT_OBSERVED`：条件性结果，未证明发生。
- `SCENE_NOT_OBSERVED_EVENT`：场景，不是个人事件。
- `EVENT_CLASS_CANDIDATE`：广义事件类别候选，非观测事实。
- `SPECIFIC_EVENT_CANDIDATE`：具体事件候选，仍不表示事件发生。

对方向轴、领域边界、跨宫约束和一般结构约束，建议审核层的轴状态为 `NOT_APPLICABLE`，而不是强行选择事件类别。不得在本体候选上增加 `OBSERVED_EVENT` 来表示现实发生；现实是否发生必须来自独立观察层。

### 3.3 来源与认识论字段

以下字段保持正交，禁止互相推导：

| 字段／门槛 | 只回答什么 | 不能推出什么 |
|---|---|---|
| `source_epistemic` | 来源对 literal claim 的支持程度 | 归一化正确、映射已接受 |
| `normalization_epistemic` | 从来源主张到表示的转换性质 | 来源本身已被核验 |
| `review_status` | 做过哪种来源／审核步骤 | 本体目标已批准 |
| `mapping_disposition` | 当前逐目标研究处置 | canonical 批准或 Product 可消费 |
| canonical approval | 是否通过适用的正式接受门 | 运行时自动获权 |
| consumer readiness | 下游消费者是否另获授权 | 传统主张具有经验预测效度 |

缺失字段不能根据相邻字段自动补齐。历史记录没有独立填写 `source_epistemic` 时，必须保留为缺失／未记录，不得因 `SOURCE_SPAN_VERIFIED` 而补写 `EXPLICIT`。

## 4. 必须通过的边界案例

| 案例 | 建议分类／处置 | 必须保留 | 禁止推导 |
|---|---|---|---|
| CA01-035 | `PROCESS_PATTERN`；`PROCESS_SEQUENCE_NOT_SINGLE_EVENT` | “往往”；火铃简写的 AND/OR 未决 | 必然发生、具体事件或确定时点 |
| CA01-045 | `ACTION_CONDITIONED_OUTCOME`；`CONDITIONAL_OUTCOME_NOT_OBSERVED` | CA01-042／CA01-044 前文关系；“勉强求变”现实行动前提 | 仅凭星曜条件断言现实行为或困境已发生 |
| CA05-469 | `SCENE_OR_CONTEXT`；`SCENE_NOT_OBSERVED_EVENT` | 职业／行业场景语义 | 命主已经受伤、患病或发生事故 |
| M01-006 | `DIRECTIONAL_AXIS`；事件轴 `NOT_APPLICABLE` | 内外／迁移动向 | 已完成迁移 |
| W01-002 | `DOMAIN_SEMANTIC_BOUNDARY`；事件轴 `NOT_APPLICABLE` | 宫位／领域解释边界 | 独立应象节点 |
| CA01-005、CA01-007 | `CROSS_PALACE_CONSTRAINT`；事件轴 `NOT_APPLICABLE` | 跨宫约束及前提关系 | 已观察到的婚姻／事业事件 |
| CA09-809 | `EVENT_CANDIDATE`；`SPECIFIC_EVENT_CANDIDATE`，仅作负控制 | `case_support_only=true` | 通用事件根、普遍映射或发生概率 |
| QI-02／QI-15 | 目标特定的状态／修正／交互审核，不凭标签直接选值 | bearer、target、condition 与证据角色（来源未给出则未知） | 调和结果证明主体自身具备调和能力 |
| QR-01／QR-04 | 区分关系网络、资源存在、资源可用、实际支持 | 证据层级；同一来源不重复计为独立证据 | 资源数量等于关系整合或已获得支持 |
| QI-04／QI-16：ZZ-PJ-X06 | 保留未决 | 原文“或”的替代关系 | 擅自改成 AND／合取条件 |
| QI-17-CAND／QI-18-CAND | candidate-only | 候选 ID 与未决身份 | 分配正式 ID 或接受 canonical mapping |
| 旧记录缺少 review envelope | 记为“尚未按该 envelope 审核” | legacy absence 与已审的 `MISSING` 分开 | 把无 envelope 自动解释为某个字段值 |

本表是审核预期，不是正式映射接受清单。

## 5. 状态建模建议

不建议现在新增全局 `metadata_axis_status` 共享字段。理由：

1. 现有 `mapping_review` 是已接受的逐目标非 canonical 审核结构，但不是三条元数据轴的通用状态对象。
2. Option C v0.1 的按轴状态表仍是提案；将它变成生产共享原语属于新的语义契约变更。
3. 目前可以在本次 review JSON／审核材料里表达每轴状态和值，并通过测试检查不确定性没有被静默消除。
4. 若 WP06C 的真实映射批次证明非 canonical 审核材料不足以保持一致性，再提交最小 schema diff、兼容／迁移／回滚计划，另过 PI/Human Gate；不能在本单顺手实现。

状态语义建议沿用提案定义：`UNKNOWN` = 已审但当前无法判断；`MISSING` = 必要信息或审查记录尚不存在；`CONFLICT` = 不相容解释并存；`NOT_APPLICABLE` = 该轴对该对象确实不适用。四者不可合并为通用 null。旧记录没有 envelope 也不等于 envelope 中的字段状态为 `MISSING`。

## 6. PI 决议记录

**Human Gate 状态：`PI_DECISIONS_RECORDED`。**  
**PI 原始答复（2026-10-29）：** “D1–D5 全部接受，按建议继续。”

已接受的最小契约治理决定：

- **D1 — 已接受。** `output_kind`、`event_specificity`、`source_epistemic` 继续保持正交语义，不把 projection mode、ontology depth、evidence role、review status、mapping disposition、canonical approval 或 consumer readiness 混入三轴。
- **D2 — 已接受。** 当前 `output_kind` 候选值域不冻结为穷尽性 production enum；未被来源充分覆盖的状态／性质、一般关系和评价性主张保持轴状态 `UNKNOWN`，待真实 WP06C 映射案例提供依据后再审查是否扩展。
- **D3 — 已接受。** 本工作单元不新增全局 `metadata_axis_status` 共享原语；只有当实际 WP06C 映射证明现有非 canonical review artifact 无法表达必要状态时，才另提最小 schema diff 并重新过 Human Gate。
- **D4 — 已接受。** 沿用 REVIEW_SCHEMA v0.3 的 `source_epistemic` 枚举；不得从 review status、source-span verification 或其他相邻状态自动推导。
- **D5 — 已接受。** canonical mapping acceptance 与 Product/KIB/runtime consumer readiness 保持独立 Gate。

### 本次 PI 批准实际授权

- 允许以以上 D1–D5 作为后续 WP06C 正式映射审查的治理契约。
- 允许创建新的有界 WP06C Core 工单，对真实来源候选逐目标进行正式映射审查。
- 允许继续使用现有 `mapping_review` v0.1 作为逐目标非 canonical 审核结构。

### 本次 PI 批准明确不授权

- 不创建或接受任何具体 canonical ontology ID。
- 不自动接受任何 individual canonical mapping。
- 不冻结当前 `output_kind` 候选为穷尽性生产枚举。
- 不修改 production shared schema。
- 不授权 Product/KIB/runtime 消费。
- 不分配概率、数值强度或经验预测效度。

因此，本文件的“最小语义契约治理决定”已由 PI 接受，但具体映射仍必须逐项经过来源、目标、mapping disposition 与 canonical acceptance 的后续 Gate。

## 7. 验收限制

- 本轮是来源与契约边界的研究审查，不是经验预测验证。
- 不将来源摘要冒充完整逐字引文。
- 不把重复引用计为独立证据。
- 不以 case-only 记录支持普遍性结论。
- 不修改 `knowledge/qi_ontology.yaml`、`star_cores.yaml`、`star_systems.yaml`、canonical source rows、Product 文件或运行时。
- 所有正式 ID 为空／不创建；映射仍是候选；概率状态仍为 `UNKNOWN`。
