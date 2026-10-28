# Option C 最小语义契约收束审议包 v0.1

**状态：`PROPOSAL_ONLY_NOT_CANONICAL`。** 本文件用于 PI 审议，不冻结正式值域、不分配本体 ID、不接受正式映射，也不授权 Product/runtime 消费。

- 工作单：[#841](https://github.com/15937-ass/ziwei-state-space/issues/841)
- 架构方向：Option C — 来源本位根森林 + 有依据的正交语义轴（方向已获 PI 接受）
- 本轮基线 main：`a65e8c3c58e30fda0a04d6123c23141de346a5f2`
- 主要依据：Option C v0.1/v0.2 提案、WP06B 根决策包、#747 契约探针、#755 已接受的逐目标 `mapping_review` Schema、十四主星性质矩阵与 QI/QR 覆盖审计。
- 证据边界：本轮复用 main 上已接受的来源审核记录和研究报告；除非下文明确标注，不声称重新逐字校勘原始扫描页。

## 1. 结论先行

现有研究材料已足以支持一个明确的**研究设计结论**：不应将目前的 `output_kind` 与 `event_specificity` 候选值原样冻结为生产契约。它们内部混合了不同语义职责，需要先在概念层拆分。

推荐 PI 审议以下原则：

1. **把“主张是什么”与“主张在推理中起什么作用”分开。** 过程、场景、方向、状态/性质、事件候选是不同的语义形态；前提、结构约束、时间条件、跨宫约束和宫位语义边界则是条件/关系/约束职责，不应仅因为都影响输出就与语义形态并列成一个扁平枚举。
2. **把事件关系、事件粒度与现实事件是否发生分开。** 当前 `event_specificity` 的候选值并非同一条“具体程度”刻度：过程、条件性结果、场景、事件类别和具体事件混在一起；“未证明发生”又是发生状态边界，不是粒度。
3. **继续严格分离证据与批准状态。** `source_epistemic`、`normalization_epistemic`、`review_status`、逐目标 `mapping_disposition`、canonical approval 和 Product consumer readiness 不能互相推导。
4. 以上是契约设计建议，不是当前正式本体变更。精确字段名、受控值、迁移与消费授权仍须单独审议。

## 2. 当前设计问题与已有证据

### 2.1 `output_kind` 的混合职责

十四主星矩阵的 `pr710_output_kind_value_audit` 与 `pr710_taxonomy_recommendation` 已识别以下问题：

| 现有候选值 | 已记录的问题 | 建议处理 |
|---|---|---|
| `PROCESS_PATTERN` | 过程序列，不是单一已发生事件 | 可作为语义形态候选；保留原文模态、条件和先后关系 |
| `ACTION_CONDITIONED_OUTCOME` | 将现实行动前提与结果形态放在同一个值中 | 拆开条件/前提关系与结果形态 |
| `SCENE_OR_CONTEXT` | 场景内容不等于将主张投射到某个领域的操作 | 保留为语义形态候选；不得与 `projection_mode` 混同 |
| `DIRECTIONAL_AXIS` | 方向或发展轴不证明实际迁移 | 保留为语义形态候选 |
| `DOMAIN_SEMANTIC_BOUNDARY` | 解释边界而非事件或通常意义上的输出形态 | 移入边界/约束职责的候选类别 |
| `CROSS_PALACE_CONSTRAINT` | 是一种特定约束，不足以代表一般关系 | 保留为有明确范围的关系/约束候选，不泛化为所有关系 |
| `STRUCTURAL_CONSTRAINT` | 与前提、条件、关系约束有重叠 | 明确与行动前提、跨宫约束和时间范围的边界 |
| `TEMPORAL_CONDITION` | 时间条件不等于该时间内发生的反应/状态变化 | 保留为条件/范围职责；反应本身另行描述 |
| `EVENT_CANDIDATE` | 候选事件形态不证明现实事件发生，且受 case-only 门控 | 保留为候选形态；另行表达粒度和发生证据边界 |

矩阵还指出两个缺口：

- 当前候选值没有明确的通用“状态/性质描述”类别；不能因为某个主张不是事件，就强行归入场景或约束。
- 评价成分（如褒贬、建设性/破坏性）不能偷偷塞进事件类型或内在性质分类；因果解释关系也不能由一个前提条件自动推出。

因此，本包建议把“语义形态”与“关系/约束职责”作为**概念上不同的职责**。是否以两个字段、一个主张对象加关系边，或现有审核材料加后续 schema 扩展实现，留给 PI 在原则接受后再审；本轮不新增正式共享字段。

### 2.2 `event_specificity` 不是单一的具体程度刻度

现有候选值的含义分别是：

- `PROCESS_SEQUENCE_NOT_SINGLE_EVENT`：过程/序列及其非单事件属性；
- `CONDITIONAL_OUTCOME_NOT_OBSERVED`：条件性结果 + 发生未被确立；
- `SCENE_NOT_OBSERVED_EVENT`：场景类别 + 不是个人已发生事件的证据；
- `EVENT_CLASS_CANDIDATE`：较宽泛的事件类别候选；
- `SPECIFIC_EVENT_CANDIDATE`：较具体的事件候选。

前三项描述的是主张与事件的关系或语义类别，后两项才近似描述事件候选的粒度；“未观察/未确立”又是另一个状态问题。它们不构成单一序数尺度，不能通过给它们排序或统一命名为“具体程度”来修复。

**建议：** 概念上区分：
- 主张与事件/应象的关系或表现形态；
- 仅对事件候选适用的事件粒度；
- 现实事件发生/观察状态（若将来确需机器化表达，应以独立观察证据为依据，不由传统来源主张自动填充）。

矩阵曾建议使用候选名称 `event_relation_or_manifestation_kind`、`event_granularity` 和独立的观察状态。这里仅接受其**拆分原则作为研究建议**；不把这些名称或值域冻结成正式 schema。对于非事件类主张，事件粒度应标为该轴不适用，而不是造一个“非事件粒度”值混入事件候选枚举。

### 2.3 已存在的 `mapping_review` Schema 不应被重复设计

#755 / PR #758 已合入逐目标审核结构，包含 `evidence_role`、`mapping_disposition` 和独立的值状态包装。该结构解决的是**某条来源对某个目标映射的证据角色与研究处置**，不是 `output_kind` 的语义形态分类，也不是事件粒度/现实发生状态。

必须继续区分：

| 概念 | 回答的问题 | 不能替代 |
|---|---|---|
| `source_epistemic` | 原文对 literal claim 的支持程度 | 归一化是否正确、映射是否获批 |
| `normalization_epistemic` | 原文转成计算/概念表示时增加了什么 | 原文是否明确、人工审核是否完成 |
| `review_status` | 来源跨度或归一化经历了何种审核 | 来源认识论状态或映射接受 |
| `mapping_disposition` | 对某一个目标映射的研究/审核处置 | canonical approval |
| canonical approval | 概念/映射是否通过适用的正式门 | Product 可否消费 |
| consumer readiness | 下游消费者是否满足依赖和授权条件 | 来源证据真值 |

旧记录没有 `mapping_review` envelope，表示未必经过该契约下的审核；它**不自动等于** `MISSING`。同样，`SUPPORTED_CANDIDATE` 不等于 canonical mapping。

## 3. 来源边界测试集

以下记录复用 WP06B 根决策包中已接受的来源证据定位与审核状态。本轮不把摘要冒充原文引语，也不把这些记录重新计作独立证据。

| 记录 | 已接受来源定位/状态 | 语义分类建议 | 明确禁止的自动推导 |
|---|---|---|---|
| CA01-035 | SRC-ZZ-003，印刷 p.133 / PDF p.67；原文跨度已在先前 WP06B 包中直接复核 | 过程/发展序列；保留“往往”等模态 | 不得变成每次必然发生的单一事件 |
| CA01-045 | SRC-ZZ-003，印刷 p.133 / PDF p.67；原文跨度已直接复核 | 条件性结果；前提依赖 CA01-042 / CA01-044 与现实行动 | 不得把“勉强求变”写成盘面事实或省略前提 |
| CA05-469 | SRC-ZZ-003，印刷 p.144 / PDF p.72；原文跨度已直接复核 | 职业/行业场景 | 不得映射为命主已经受伤或患病 |
| M01-006 | SRC-ZZ-003，印刷 p.109；复用已接受的直接来源复核记录 | 内外/迁移动向轴 | 不得推出已经完成迁移 |
| CA01-005 / CA01-007 | SRC-ZZ-003，印刷 p.132；复用已接受且标记 `SOURCE_SPAN_VERIFIED` 的行 | 推断前提/跨宫解释约束 | 不得自动生成独立应象节点或现实婚姻事件 |
| W01-002 | SRC-ZZ-003，印刷 p.69；复用已接受的来源行 | 宫位/领域语义边界 | 不得把边界条件当作事件类别 |
| CA09-809 | SRC-ZZ-003，印刷 p.153；case-support-only 负控制 | 具体事件候选只可用于测试防晋升机制 | 不得把个案支持推广为普遍映射或发生概率 |

### 3.1 QI/QR 反例与条件边界

- **QI-01 / QI-14：** 动力学外放/收敛与信息/状态可见性不同；潜藏不自动等于遮蔽，外放不自动等于显露。
- **QI-02 / QI-15：** 被调和后的状态不证明被修饰主体自身具有调和能力；需区分主体、对象、条件、外部修饰与交互结果。
- **QI-08 / QI-06：** 决得快不等于执行强；行动多不等于审慎。
- **QI-04 / QI-16：** 开创不等于目标明确；结果“建设性”不自动证明目标组织清晰。
- **QR-01 / QR-04：** 关系整合不等于资源存在；资源存在不等于资源可用或支持已实际发生。
- **ZZ-PJ-X06：** 既有审计已标记来源条件差异未解决。来源中的“或”不得被加强成合取条件；本包不改写该规则。

## 4. 建议的最小概念模型（全部为候选，不是正式字段）

### A. 主张语义形态（candidate semantic form）

可先用以下类别测试覆盖率，不视为已批准值域：

- `STATE_OR_PROPERTY_DESCRIPTOR`：状态/性质描述（当前候选列表的已识别缺口）；
- `PROCESS_PATTERN`：过程/发展序列；
- `SCENE_OR_CONTEXT`：职业、情境或场景；
- `DIRECTIONAL_AXIS`：方向、比较或发展轴；
- `OUTCOME_DESCRIPTOR`：结果描述（不自动等于事件）；
- `EVENT_CANDIDATE`：候选事件形态，仍受证据层级和 case-only 门控。

### B. 关系、前提与约束职责（candidate relation/constraint role）

这些类别不应与 A 中的语义形态混作同一平面枚举：

- `ACTION_PREREQUISITE`：现实行动前提；
- `STRUCTURAL_CONSTRAINT`：结构性约束/前提；
- `TEMPORAL_SCOPE`：时间范围/时间条件；
- `CROSS_PALACE_CONSTRAINT`：跨宫解释约束；
- `DOMAIN_SEMANTIC_BOUNDARY`：宫位或领域语义边界；
- `CAUSAL_OR_EXPLANATORY_RELATION`：只有来源直接支持时才考虑；不能从条件关系推导出来。

`SCENE_OR_CONTEXT` 不等于 `SCENE_TRANSLATION`；后者属于已有 `projection_mode` 的投影/约束行为语义，不是同一类本体对象。`TEMPORAL_SCOPE` 也不等于时间窗口内发生的状态变化或反应。

### C. 事件关系、粒度与发生状态

- `event_relation_or_manifestation_kind`：研究候选，用于区分过程、条件性结果、场景等与事件的关系；其名称和候选值仍需继续反例测试。
- `event_granularity`：仅在事件候选适用时区分较宽泛的事件类别与较具体的事件候选。
- 现实事件发生/观察状态：逻辑上必须与前两者分开。当前不在 Core 中创建观察记录，也不从来源主张自动填入“已发生”；若未来需要类型化字段，应另行说明消费者需求、证据来源与 Human Gate。

上述 A/B/C 是研究模型，不要求本轮立刻新增共享字段。应先验证当前审核材料能否忠实表达；若机器处理确实需要新增字段，另提最小 schema diff、兼容迁移、缺失值策略、回滚和独立 PI/Human Gate。

## 5. PI 决策卡（请集中审议）

### PI-C1：是否接受“语义形态”与“关系/约束职责”分离？

- **推荐：接受拆分原则，拒绝原 `output_kind` 九值平面枚举直接冻结。**
- 备选 A：接受拆分原则；把具体字段/值域留在后续契约实施门审议。
- 备选 B：维持现有单一 `output_kind` 候选枚举，仅作为临时研究表示，不冻结。
- 不建议：直接把九个现有候选值作为正式值域，因为 `ACTION_CONDITIONED_OUTCOME`、`STRUCTURAL_CONSTRAINT`、`CROSS_PALACE_CONSTRAINT`、`TEMPORAL_CONDITION` 等承担不同职责。

### PI-C2：是否接受“事件关系/表现形态、事件粒度、现实发生状态”分离？

- **推荐：接受概念拆分；不把现有 `event_specificity` 五个值作为单一具体程度尺度。**
- 备选 A：接受拆分原则，精确字段名和值域待后续契约实施单。
- 备选 B：暂时保留 `event_specificity` 作为不可执行的历史研究字段，并在每条记录上明确其混合语义限制。
- 不建议：将五个现有值排序或把“未观察/未确立”与事件粒度混在一起。

### PI-C3：是否维持现有认识论与消费权限边界？

- **推荐：维持。** `source_epistemic`、`normalization_epistemic`、`review_status`、`mapping_disposition`、canonical approval 和 consumer readiness 始终独立。
- 这项原则与现有审核 Schema 和 #755 的逐目标 `mapping_review` 契约一致；除非未来出现具体能力缺口，本包不建议增加替代字段。

## 6. 兼容、迁移与回滚

本轮没有生产迁移：

1. 不回写历史来源行，不修改 `knowledge/qi_ontology.yaml`、`star_cores.yaml`、`star_systems.yaml` 或 Product 文件。
2. 不给候选概念分配正式 ID；JSON 中 canonical IDs 保持 null。
3. 现有 `mapping_review` Schema 保持原样；不得通过改名或扩大其 `evidence_role` 来偷渡语义形态。
4. 如果 PI 接受拆分原则，下一步仍是一个独立的、有界的契约修订/实施工作单；该单先提交具体字段 diff 和兼容方案，再等适用的正式审批。
5. 若 PI 不接受，本包可被标记为 superseded；因为没有生产数据迁移，不需回滚生产数据。

## 7. 不作出的主张

本包不声称：候选类别穷尽了传统斗数语义；QI/QR 维度已被统计证明正交；来源一致性等于现实预测有效；case-only 材料支持发生率或概率；候选映射已 canonical；任何内容已可供 Product/runtime/KIB 消费。

## 8. 复核依据

- [Option C 根决策包](MANIFESTATION_ROOT_DECISION_PACKET_v0.1.md) 与其结构化版本。
- [Option C 元数据契约提案 v0.1](OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.1.md) / `.json`。
- [Option C 元数据契约提案 v0.2](OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.2.md)。
- [Option C 契约验证探针 #747](OPTION_C_CONTRACT_VALIDATION_PROBE_v0.1.md)。
- [十四主星性质矩阵与 QI/QR 覆盖审计](../14star-property-matrix/14STAR_PROPERTY_MATRIX_QIQR_AUDIT_v0.1.md) / `.json`。
- [逐目标 Mapping Review Schema v0.1](MAPPING_REVIEW_SCHEMA_v0.1.json)。
