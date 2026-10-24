# 十四主星性质矩阵与 QI/QR 覆盖审计 v0.1

**状态：`PROPOSAL_ONLY_NOT_CANONICAL`。** 本报告是 Issue #712 的研究草案与首轮机器辅助盘点，不是正式本体变更，不是预测有效性证据，也不证明十四主星构成完备性质空间。

- Issue：#712
- 工作单元：`KB-CORE-14STAR-PROPERTY-MATRIX-QIQR-AUDIT-01`
- 本轮起始 main：`bdcbf24ef85959d7a7b35014e82708bbedb329bf`
- 来源规则文件：`knowledge/rules/stars/major_stars_canonical_v0.1.csv`（blob `df9645ab1a8c08411821b8701af85d86bfdaa277`）
- 当前 QI/QR 本体：`knowledge/qi_ontology.yaml`（blob `e92f0e9492406c4d758b9bd1574bf446b1fa81fd`）
- 当前十四主星气核：`knowledge/star_cores.yaml`（blob `0081d4492b070d1785b0dae233d0dc12d6134bff`）
- 当前星系交互模型：`knowledge/star_systems.yaml`（blob `571e67987b6139a7fac05b44c1f10c9e2370ff30`）

## 1. 研究问题与范围

研究假设是：十四主星可能构成一组有来源依据、能够组合的候选语义基元；宫位、星系关系、四化及其他条件、时间窗口与下游投影共同决定这些性质怎样被表达。这个假设必须允许反例：某颗星可以没有已被充分支持的内在维度，某条规则可以同时承担多个语义角色，某些性质可能只在星系或场景层出现。

本轮严格限定在当前 canonical corpus 已接纳的中州派材料，不把古典斗数、河洛、钦天等其他学派的材料混入 canonical 证据。跨学派比较应另列，不能静默拼接。

## 2. 数据盘点

### 2.1 来源规则语料

首轮矩阵逐条保留了 **430 条规则记录**，覆盖 14 颗主星，唯一 rule ID 数为 430。

| 来源 ID | 作品 | 记录数 | 来源 SHA-256 |
|---|---|---:|---|
| SRC-ZZ-002 | 《中州派紫微斗数深造讲义（上）》 | 413 | 1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a |
| SRC-ZZ-001 | 王亭之《中州派紫微斗数初级讲义》 | 17 | 7ebafc8e3477430e2f8e69c6925ecc373d3c28966955f7035078c4949b7475a2 |

规则语料现有记录中，`source_epistemic` 的值为 EXPLICIT 的数量为 430，`normalization_epistemic` 为 UNRESOLVED 的数量为 430，`review_status` 为 MODEL_SELF_REVIEWED 的数量为 430。

这三项必须分开理解：原文主张可有明确来源支持，而将它转换成 QI/QR 维度的归一化仍然可以保持 UNRESOLVED。不能因为来源清楚，就认定映射已经正确或已经过人工确认。

### 2.2 现有 QI/QR 层级

当前 `qi_ontology.yaml` 明确采用 L0–L4 分层，并写明“不使用单一扁平向量强行容纳所有性质”。因此，我们把“性质向量”作为候选表示，而不预先假设它必须是一个同质、数值化、可直接相加的向量。现有结构包括 QI-01 至 QI-16、QR-01 至 QR-04，以及 QI-17-CAND / QI-18-CAND 等候选维度。

| ID | 现有维度 | 直接/主证据引用数 | 星系上下文证据引用数 | 投影证据引用数 |
|---|---|---:|---:|---:|
| QI-01 | 发射—收敛 | 9 | 0 | 0 |
| QI-02 | 刚—柔 | 9 | 0 | 0 |
| QI-03 | 稳定—变动 | 8 | 4 | 0 |
| QI-04 | 守成—开创/冲刺 | 6 | 0 | 0 |
| QI-05 | 现实化—空泛 | 8 | 0 | 0 |
| QI-06 | 决策激活度 | 5 | 0 | 1 |
| QI-07 | 认知机变 | 7 | 0 | 0 |
| QI-08 | 行动驱动 | 6 | 0 | 1 |
| QI-09 | 欲望驱动 | 10 | 0 | 0 |
| QI-10 | 原则/规范约束 | 7 | 0 | 0 |
| QI-11 | 感性—理性张力 | 3 | 5 | 0 |
| QI-12 | 资源保存/管理能力 | 7 | 0 | 0 |
| QI-13 | 表达/传播能力 | 7 | 0 | 1 |
| QI-14 | 信息/状态遮蔽—显露 | 5 | 5 | 0 |
| QI-15 | 缓冲/调和能力 | 8 | 2 | 0 |
| QI-16 | 目标导向性 | 1 | 10 | 0 |
| QR-01 | 关系整合—孤离 | 6 | 16 | 2 |
| QR-02 | 主导—协同 | 6 | 12 | 0 |
| QR-03 | 竞争激活 | 2 | 25 | 1 |
| QR-04 | 支持资源 | 5 | 25 | 4 |
| QI-17-CAND | 意志控制强度 | 0 | 7 | 0 |
| QI-18-CAND | 毅力/持续性 | 2 | 4 | 0 |

这些数字是当前 YAML 中的 evidence-rule 引用数，不是独立样本数、准确率或统计置信度。重复引用同一规则不能自动证明维度独立。

### 2.3 每颗主星的现有气核与语料覆盖

| 主星 | 语料规则数 | 当前内在维度 | 当前关系维度 | 当前条件目标 | 语料中有星核角色引用的规则 | 有 QI/QR 证据引用的规则 |
|---|---:|---|---|---|---:|---:|
| 紫微 | 43 | 无（现有气核留空） | QR-02 | QI-07, QR-01 | 6 | 8 |
| 天机 | 39 | QI-07 | — | QI-03, QI-05, QI-06, QI-10, QR-03 | 10 | 15 |
| 太阳 | 40 | QI-01 | — | QI-01, QI-05, QI-15 | 7 | 7 |
| 武曲 | 41 | QI-02, QI-05, QI-08 | QR-01 | QI-02, QI-06 | 10 | 14 |
| 天同 | 25 | QI-02, QI-15, QI-09 | — | QI-15, QR-04 | 9 | 6 |
| 廉贞 | 27 | QI-11 | — | QI-11, QI-09 | 5 | 8 |
| 天府 | 25 | QI-12, QI-04 | QR-02 | QI-12 | 8 | 8 |
| 太阴 | 26 | QI-01 | — | QI-01, QI-05, QR-04 | 7 | 7 |
| 贪狼 | 29 | QI-09, QI-08 | — | QI-09, QI-10 | 11 | 12 |
| 巨门 | 26 | QI-14, QI-13 | — | QI-14, QI-13 | 9 | 14 |
| 天相 | 27 | QI-02 | — | QI-02, QI-15 | 6 | 4 |
| 天梁 | 26 | QI-10, QI-15 | QR-01 | QI-10, QI-03 | 8 | 9 |
| 七杀 | 26 | QI-02, QI-04, QI-08 | QR-02 | QI-02, QR-04 | 8 | 9 |
| 破军 | 30 | QI-03, QI-04, QI-08 | QR-02 | QI-06, QI-16, QR-04 | 11 | 8 |

关键观察：现有 `star_cores.yaml` 对紫微保留了空的 `intrinsic_signature`，但有关系性和条件性内容。这是当前模型明确允许的情况，不能把“十四主星都必须填满同长度向量”当成验收条件。空值需要区分“当前来源未支持/模型未纳入”与“真实性质不存在”。

## 3. 首轮方法：保留证据，不强行定型

CSV 中每一行对应一条已有 canonical rule，而不是我新造的一条古籍原文。矩阵保留来源作品、原有 source_location、rule ID、target_literal、evidence_text、condition、time_scope、palace_scope、prerequisite/exclusion/conflict 字段，以及既有认识论和审查字段。

注意：
- `evidence_text` 是仓库现有的简述/近源说明，不应误称为完整逐字引文。
- `source_location` 是现有规则提供的定位；本轮没有重新 OCR 或重新核对所有 PDF 页面。
- `claim_roles_candidate` 是从现有结构字段产生的研究候选角色，不是已经人工逐条确认的语义分类。
- `candidate_mapping_targets` 来自当前 QI/QR 的证据引用和 `star_cores.yaml` 角色引用；它们是“现有证据关联”，不是被自动批准的新映射。
- 所有规范化判断仍保留现有 `normalization_epistemic`。本轮不把 UNRESOLVED 自动升格。
- canonical star CSV 没有专用的 `case_support_only` 布尔字段，因此矩阵不会把未出现 case ID 解释成已证明“不是个案支持”。

## 4. 首轮结构发现

### 4.1 星曜性质不等于单一结果

现有 corpus 的 target_type 分布：

- `qi_state`：237 条
- `outcome_descriptor`：90 条
- `structural_relation`：80 条
- `relational_state`：23 条

这表明语料已经同时包含内在状态候选、关系/结构、以及结果描述。它们不能简单地作为同一种性质向量分量处理。

### 4.2 内在性质、关系性质、条件反应与投影必须分层

现有 `star_cores.yaml` 明确采用 DIRECT_STAR、SAME_STAR_MODIFIER、SYSTEM_CONTEXT、PROJECTION 的证据优先级。它还明确禁止把修正曜、四化、夹宫、六十星系与结果描述自动提升为单星内在气核。

因此，对你的“形容词/性质向量”想法，较稳妥的初步形式不是“一颗星 = 一个扁平向量”，而是：

- 基础性质候选；
- 关系性质；
- 条件性修正；
- 星系交互/模态；
- 时间条件与反应；
- 宫位/领域投影；
- 现实观察与评价。

这些层可以通过关系和规则连接，但不应把所有项都塞进同一个向量。

### 4.3 星系不是单星向量的简单相加

当前 `star_systems.yaml` 将星系表示为基础组合、交互项、模态与上下文门控，并明确指出 interaction delta 是模型残差，不是新的神秘实体。

| 星系编号 | 星系 | 主要模态 | 现有交互分类 | 候选交互项 |
|---:|---|---|---|---|
| 7 | 武曲天相寅申 | 刚柔配合与调和 | COMPOSITION, INTERACTION, CONTEXT_GATE | balance_penalty(QI-02, context) |
| 11 | 紫微破军丑未 | 动荡/安定 | INTERACTION, MODE_SWITCH, CONTEXT_GATE | stability_switch |
| 21 | 紫微天府寅申 | 主动/被动；平衡则攻守咸宜 | INTERACTION, MODE_SWITCH | initiative_conservation_balance |
| 49 | 武曲天府子午 | 仅擅生财/擅理财（生财+储存） | COMPOSITION, INTERACTION | resource_coordination |
| 53 | 紫微七杀巳亥 | 权威/横霸 | INTERACTION, MODE_SWITCH, CONTEXT_GATE | authority_regulation |
| 60 | 天机天梁辰戌 | 明断/尖刻 | INTERACTION, MODE_SWITCH, CONTEXT_GATE | sensitivity_discipline_balance |

这些例子支持把“组合产生的新性质”当成待建模的交互项，而不是直接把每颗星的性质数值相加。它们是传统解释结构的形式化例子，不构成现实预测有效性的证明。

### 4.4 QI/QR 的重叠必须审计，不能只靠标签分开

首轮矩阵中，15 条规则在合并 QI/QR 维度引用与星核角色引用后具有多个候选目标；其中 12 条涉及多个不同的 QI/QR 维度，另有 3 条由星核角色引用形成多目标情况。另有 147 条规则带有候选关联目标，但其归一化仍为 UNRESOLVED。这些记录应进入重叠与层级审查，不应因为 YAML 中列出了某个 evidence_rule，就视为映射已经得到确认。

当前本体已明确要求进行的冗余审查包括 QI-01/QI-14、QI-03/QI-04、QI-02/QI-15、QI-08/QI-06、QI-04/QI-16、QI-08/QI-16、QI-17-CAND/QI-18-CAND、QR-01/QR-04。首轮矩阵不会提前宣布这些维度已独立。

### 4.5 代表性案例：结构对齐、歧义、重叠、表面冲突与反例

以下案例只展示当前结构化语料及现有本体引用之间的关系。当前 430 条规则的 `normalization_epistemic` 均为 `UNRESOLVED`，因此“结构上吻合”不等于已经通过人工来源复核的规范化映射。这里的 `evidence_text` 是语料中的摘要字段，不应当作完整逐字引文。

| 审查类型 | 规则与来源定位 | 观察 | 审计结论 |
|---|---|---|---|
| 结构上吻合的候选对齐（不是已接受映射） | `ZZ-TF-002`；《中州派紫微斗数深造讲义（上）》“十四正曜·天府·书页17” | “财库”被归一化为“储藏/管理资源”；现有 QI/QR 引用为 QI-12，`STAR-TF` 的 `intrinsic_signature` 也引用 QI-12，证据层级均指向直接星性/主证据。 | 这是一个内部结构相容的候选对齐；但 `normalization_epistemic` 仍为 `UNRESOLVED`，不得记为已接受映射。 |
| 歧义映射 | `ZZ-ZW-013`；同书“十四正曜·紫微·书页5” | “外部助力”以“左辅右弼三方会合”为条件，同时引用 QR-01 与 QR-04，且两条均为投影证据。 | 现有引用无法单独决定该结果应归入哪一个 QR 维度、是否应保留双重角色；标记为待审，不强行择一。 |
| 重叠/冗余候选 | `ZZ-WQ-020`；同书“十四正曜·武曲·书页11” | “刚烈性”在“天府同度或会合”条件下被减弱，现有引用同时指向 QI-02 与 QI-15；当前本体已把 QI-02/QI-15 列为冗余审查对。 | 这是需要检查维度边界的重叠候选，不足以单凭一次共同引用就断言两个维度等价或删除其中一个。 |
| 表面冲突/条件化反例 | `ZZ-ZW-003` 与 `ZZ-ZW-004`；同书“十四正曜·紫微·书页5” | 两条都指向“整体适配性”，但前者在“形成孤君”条件下为 weaken/decrease，后者在“百官朝拱”条件下为 enhance/increase。 | 若只按目标标签匹配，会误报冲突；条件不同，现有记录更像条件化的相反反应。全体 430 条记录的 `conflicts_with_rule_ids` 均为空，因此语料没有显式登记的规则冲突边；这不证明不存在潜在冲突。 |
| 对固定完整星性向量的反例 | `ZZ-ZW-002`；同书“十四正曜·紫微·书页5” | 现有摘要称紫微性质需依据同度或会合星曜而定；当前 `star_cores.yaml` 又将紫微的 `intrinsic_signature` 保留为空，并把相关内容放在关系/条件层处理。 | 这反驳“十四颗星都必须先填满同长度固定内在向量”的建模假设；它不证明紫微没有任何内在性质，只说明当前已审语料与模型选择不足以支持强行填满。 |

## 5. 对 PR #710 候选分类的交叉检查

PR #710 已作为 proposal-only 基线合并，但其中的值域仍不是 canonical schema。以下 crosswalk 用来发现不匹配，而不是自动给每条规则赋值。

| 研究角色 | PR #710 最接近的 output_kind | 初步判断 | 风险 |
|---|---|---|---|
| intrinsic_property_candidate | 无直接对应 | GAP_OR_OUTSIDE_CURRENT_OUTPUT_KIND | The candidate values describe process, scene, constraints, and event candidates, but do not provide a general intrinsic-property/state descriptor. |
| relational_property | CROSS_PALACE_CONSTRAINT | PARTIAL_ONLY | A general relation is broader than a cross-palace interpretive constraint. |
| structural_relation_or_constraint | STRUCTURAL_CONSTRAINT, CROSS_PALACE_CONSTRAINT | OVERLAPPING_CANDIDATES | Rule function/relationship is mixed with semantic form; boundaries require examples. |
| conditional_tendency_candidate | ACTION_CONDITIONED_OUTCOME, STRUCTURAL_CONSTRAINT, TEMPORAL_CONDITION | MANY_TO_MANY | The list mixes precondition, conditional result, and time scope; a claim may have more than one role. |
| temporal_reaction_or_scope_candidate | TEMPORAL_CONDITION | PARTIAL_ONLY | A temporal condition is not necessarily the reaction/state change that occurs within a time window. |
| domain_context_projection | SCENE_OR_CONTEXT | PARTIAL_ONLY | Projection is a mapping/operation; a scene is a semantic output/context. They should not be assumed equivalent. |
| outcome_or_contextual_manifestation | ACTION_CONDITIONED_OUTCOME, EVENT_CANDIDATE | PARTIAL_ONLY | There is no general outcome value; action-conditioned outcomes are a narrower subclass. |
| evaluation_component | 无直接对应 | KEEP_SEPARATE_OR_GAP | Valence/evaluation should not be smuggled into event type or intrinsic property. |
| process_pattern | PROCESS_PATTERN | CLOSE_MATCH | Must still preserve modality, conditions, and non-event status. |
| scene_or_context | SCENE_OR_CONTEXT | CLOSE_MATCH | Scene must not be promoted to an observed personal event. |
| directional_axis | DIRECTIONAL_AXIS | CLOSE_MATCH | Direction/development axis does not establish completed movement. |
| event_candidate | EVENT_CANDIDATE | CLOSE_MATCH | Candidate classification does not prove the event occurred. |

### 5.1 `output_kind` 逐值检查

| 候选值 | 最接近的研究角色 | 首轮判断 | 主要风险 |
|---|---|---|---|
| `PROCESS_PATTERN` | process_pattern | CLOSE_MATCH_WITH_BOUNDARIES | A process sequence is not a single observed event; retain modal words and prerequisites. |
| `ACTION_CONDITIONED_OUTCOME` | conditional_tendency_candidate, outcome_or_contextual_manifestation, explicit_prerequisite_dependency | MIXED_CONDITION_AND_OUTCOME | Combines a condition/action prerequisite with a result; may conflate rule condition and semantic output. |
| `SCENE_OR_CONTEXT` | scene_or_context, domain_context_projection | SCENE_VS_PROJECTION_AMBIGUITY | A scene/context is semantic content; projection is an operation/relationship that maps a claim into a domain. |
| `DIRECTIONAL_AXIS` | directional_axis | CLOSE_MATCH_WITH_BOUNDARIES | Direction/development axis is not proof that movement or migration occurred. |
| `DOMAIN_SEMANTIC_BOUNDARY` | domain_semantic_boundary | CLOSE_MATCH_WITH_BOUNDARIES | Boundary constrains interpretation; it should not be treated as an event or manifestation. |
| `CROSS_PALACE_CONSTRAINT` | relational_property, structural_relation_or_constraint | TOO_NARROW_FOR_GENERAL_RELATIONS | A cross-palace constraint is one kind of relation, not a general relation/property category. |
| `STRUCTURAL_CONSTRAINT` | structural_relation_or_constraint, conditional_tendency_candidate | OVERLAP_REQUIRES_EXAMPLES | Overlaps prerequisite, condition, and relational constraint roles; define boundary against CROSS_PALACE_CONSTRAINT and ACTION_CONDITIONED_OUTCOME. |
| `TEMPORAL_CONDITION` | temporal_reaction_or_scope_candidate, conditional_tendency_candidate | CONDITION_VS_REACTION | A temporal condition is not the state change/reaction occurring during a time window. |
| `EVENT_CANDIDATE` | event_candidate | CLOSE_MATCH_WITH_BOUNDARIES | Candidate event classification does not establish real-world occurrence or allow case-only promotion. |

### 5.2 `event_specificity` 逐值检查

| 候选值 | 最接近的研究角色 | 首轮判断 | 主要风险 |
|---|---|---|---|
| `PROCESS_SEQUENCE_NOT_SINGLE_EVENT` | process_pattern | SEMANTIC_FORM_NOT_GRANULARITY | Describes process/sequence and non-single-event status, not simply how specific an event is. |
| `CONDITIONAL_OUTCOME_NOT_OBSERVED` | conditional_tendency_candidate, outcome_or_contextual_manifestation | CONDITION_PLUS_OCCURRENCE_STATUS | Combines conditional outcome type with whether occurrence is observed/established. |
| `SCENE_NOT_OBSERVED_EVENT` | scene_or_context, domain_context_projection | SCENE_PLUS_OCCURRENCE_STATUS | Combines scene semantics with an empirical observation-status boundary. |
| `EVENT_CLASS_CANDIDATE` | event_candidate | GRANULARITY_CANDIDATE | Broad event-class granularity; still a candidate, not evidence of occurrence. |
| `SPECIFIC_EVENT_CANDIDATE` | event_candidate | GRANULARITY_CANDIDATE | More specific candidate level, but not proof that a real-world event occurred. |

这里的 `NOT_APPLICABLE` 是提案规定的轴状态，不是一个 `event_specificity` 值。它可能适用于非事件语义，但不能解决候选值域本身混合“语义类型、条件状态与观测状态”的问题。

另一个必须保持的边界是：**条件不等于原因**。前置条件、适用条件、统计相关、因果解释是不同的关系；除非来源明确支持，不得从 `condition` 或 `ACTION_CONDITIONED_OUTCOME` 自动推导因果关系。

初步判断：
1. `output_kind` 同时包含过程/场景等语义形态，以及跨宫/结构/时间约束等推断角色。它们可能都需要，但未必构成互斥、同层级的单一枚举。
2. `event_specificity` 当前候选值包含“过程序列”“条件结果”“场景”“事件类别”“具体事件候选”。这更像事件关系/表现类型与具体程度的混合，而不是自然的单调“具体性”尺度。
3. `NOT_APPLICABLE` 适合表达某轴对非事件对象不适用的状态，但它不能修复字段值域本身混合不同维度的问题。
4. 内在性质、状态描述、关系性质和评价目前没有清楚的直接 output_kind 对应项。这可能是合理的范围边界，也可能是值域遗漏，需通过来源案例判断。
5. `source_epistemic` 的 v0.3 三值复用、与 `normalization_epistemic` 分离、以及 fail-closed 原则是值得保留的治理约束。

因此，不建议在本轮把 output_kind 或 event_specificity 写入任何 canonical 词表。Issue #712 的后续工作应继续检查它们是需要拆分、改名、扩展，还是仅在审查层保留为候选标签。

### 5.3 明确建议：先拆分候选轴，再讨论是否规范化

| 候选轴 | 建议动作 | 理由 | 当前权限边界 |
|---|---|---|---|
| `output_kind` | **建议拆分，不保留为一个同层级平面枚举。** 研究上先区分“语义表现形态”与“推理关系/约束角色”；`PROCESS_PATTERN`、`SCENE_OR_CONTEXT`、`DIRECTIONAL_AXIS`、`EVENT_CANDIDATE` 可继续作为前一类候选，`CROSS_PALACE_CONSTRAINT`、`STRUCTURAL_CONSTRAINT`、`TEMPORAL_CONDITION`、`DOMAIN_SEMANTIC_BOUNDARY` 更接近后一类；`ACTION_CONDITIONED_OUTCOME` 还需拆开条件关系与结果形态。 | 这是研究建议，不新增正式字段或枚举。 |
| `event_specificity` | **建议拆分并改名。** 将过程/条件结果/场景等值域先作为候选的 `event_relation_or_manifestation_kind`；将 `EVENT_CLASS_CANDIDATE` 与 `SPECIFIC_EVENT_CANDIDATE` 作为独立的 `event_granularity` 候选；“是否已观察/发生”另设独立证据状态，不塞入具体程度轴。 | 现有值域混合语义类型、粒度和观测状态，不构成自然的单调具体性尺度。 |
| `source_epistemic` 与 `normalization_epistemic` | **建议保持分离。** 原文主张有来源支持，不代表归一化映射已被接受。 | 不把任何 `UNRESOLVED` 自动升格；`NOT_APPLICABLE` 是轴适用性状态，不是 event-specificity 的候选值。 |

以上为本 Issue 的明确研究建议：对 `output_kind` 采取“拆分”，对 `event_specificity` 采取“拆分并改名”。是否采纳及最终字段名仍需 PI 审阅；本 PR 不实施任何 canonical schema 改动。

## 6. 时间尺度与性质/状态的区分

现有 430 条主星规则中，绝大多数记录的 time_scope 是 generic，另有明确标记 natal、decade/year 的子集。它们是来源规则的时间适用范围，不等同于“原局只代表性质、大限代表状态、流年代表事件”的固定映射。

本轮保留来源中原有 time_scope 与条件字段。任何将时间尺度转换成状态变化或应象的规则，都必须由原文和显式推理规则支持；不能仅凭“大限/流年”标签推定输出类型。

## 7. 负控制、冲突与证据边界

- 未解决的 source/normalization 状态保持原样。
- 多个 QI/QR 目标只标记为重叠审查候选，不自动合并或强行选择一个。
- 规则没有专用 `case_support_only` 字段时，不推断它一定不是个案支持。
- 当前 corpus 是传统文本规则，不能证明某个现实事件已发生，也不能给出概率或预测准确率。
- 本轮没有建立真正的 held-out reconstruction。原因是当前本体和星核已经引用这批规则；如果从同一批数据随意留出一部分，会有信息泄漏风险。未来若要做盲测，需要先冻结候选映射，再由独立审查者对保留规则重新 adjudicate。

## 8. 本轮结论与下一步

这轮矩阵支持一个有限结论：现有紫微斗数项目已经在实践中区分基础性质、关系状态、条件修正、系统模态与场景投影。它与“连续人生经不同标尺离散观测”的理论可以形成接口，但不能简化成一颗星对应一个固定事件或一个完备、同质的数值向量。

本轮尚不能证明十四主星构成完备性质集。要检验这个假设，下一步应：
1. 先对每颗星的 DIRECT_STAR 证据逐条做人工 source-first 复核；
2. 分开基础性质、关系性质、条件性修正与下游投影；
3. 针对 QI/QR 的已知重叠对做独立证据与反例审查；
4. 用六十星系中的 interaction/mode-switch 案例检验是否存在单星维度无法解释的交互残差；
5. 对 PR #710 的 output_kind / event_specificity 进行逐案例 crosswalk，并保留 split/rename/replace 的可能；
6. 不新增 QI/QR primitive，不改正式气核或 Product，除非后续另行经过 PI/Human Gate。

## 9. 机器产物说明

- `14STAR_PROPERTY_MATRIX_QIQR_AUDIT_v0.1.csv`：430 条行级记录，所有候选分类均标注为研究用途。
- `14STAR_PROPERTY_MATRIX_QIQR_AUDIT_v0.1.json`：同一矩阵的机器可读版本，包含现有证据引用、星核角色、重叠标记、交叉分类风险与守门字段。
- `tests/test_knowledge_core_14star_property_matrix.py`：对覆盖率、来源字段、认识论分离、未解决状态保留和非 canonical 守门进行确定性测试。
- 最终 exact-head 验证结果将记录在 `14STAR_PROPERTY_MATRIX_QIQR_AUDIT_EVIDENCE.md`。
