# Option C 最小元数据契约提案 v0.1

**状态：`PROPOSAL_ONLY_NOT_CANONICAL`。仅供 PI 审阅，不是已冻结 schema。**  
**Issue：** #709 · **决策依据：** 已合并的 WP06B Option C 方向决定（PR #704，main `cdc4fce773ea5133f2210c6ea8e87022678fff2f`）。

## 1. 本提案要解决什么

PI 已选择 C：来源本位根森林 + 正交元数据轴。下一步不是立即给所有候选分配正式 ID，而是把三条轴的含义和缺失语义讲清楚，避免把不同问题塞进一个字段：

- **`output_kind`：** 规范化主张是什么语义形态？
- **`event_specificity`：** 这个候选与事件的关系有多具体？它是否只是过程、条件结果或场景，而不是已发生的事件？
- **`source_epistemic`：** 原始来源对 literal claim 的支持程度如何？

这三条轴不是同一层级，也不是同一个值域。它们都不能替代来源审查。

## 2. 复用现有契约：不能重造认识论枚举

当前 main 的 `knowledge/REVIEW_SCHEMA_v0.3.md` 已冻结 `source_epistemic` 的允许值：

- `EXPLICIT`
- `INFERRED_FROM_SOURCE`
- `UNRESOLVED_SOURCE`

同一 schema 还把以下两项独立规定：

- `normalization_epistemic`：`SOURCE_PRESERVING`、`INFERRED`、`IMPLEMENTATION`、`HYPOTHESIS`、`UNRESOLVED`
- `review_status`：`MODEL_EXTRACTED`、`MODEL_SELF_REVIEWED`、`SOURCE_SPAN_VERIFIED`、`HUMAN_VERIFIED`

因此：

1. 不给 `source_epistemic` 新增 `EXPLICIT_SOURCE_WORDING`、`SOURCE_SPAN_VERIFIED` 或 `CASE_SUPPORT_ONLY` 这类值。前者是本决策包中的描述性候选标签，后两者分别属于 review/evidence 边界。
2. `SOURCE_SPAN_VERIFIED` 不等于 `source_epistemic=EXPLICIT`。如果接受的 CSV/JSON 没有单独记录 `source_epistemic`，本提案建议把它标为 **MISSING**，不自动补值。
3. `case_support_only` 仍然是独立的证据边界，不能被 source epistemic 吸收。
4. `source_epistemic` 应附着在来源断言或每条 source reference 上，不宜把多条来源的不同认识论状态压成一个 ontology node 的总标签。

## 3. 候选轴一：`output_kind`

建议位置：Knowledge 的 `NormalizedClaim / MappingProposal` 审查层；只有当概念本身确有稳定语义时，才考虑把它投影到候选概念上。以下值**全是待 PI 审核的候选值**。

| 候选值 | 含义 | 示例 |
|---|---|---|
| `PROCESS_PATTERN` | 发展过程或序列，不等于单一已发生事件 | CA01-035 |
| `ACTION_CONDITIONED_OUTCOME` | 必须满足现实行动前提才适用的结果 | CA01-045 |
| `SCENE_OR_CONTEXT` | 职业／情境场景，不等于个人事件 | CA05-469 |
| `DIRECTIONAL_AXIS` | 方向或发展轴，不等于已经迁移 | M01-006 |
| `DOMAIN_SEMANTIC_BOUNDARY` | 宫位／领域的解释边界 | W01-002 |
| `CROSS_PALACE_CONSTRAINT` | 跨宫解释约束或关系，不自动构成应象 | CA01-005、CA01-007 |
| `STRUCTURAL_CONSTRAINT` | 推断前提或结构条件 | CA01-002、W01-005 |
| `TEMPORAL_CONDITION` | 时间范围或触发条件，不等于结果事件 | CA01-046、M01-001 |
| `EVENT_CANDIDATE` | 事件候选；仍受证据等级和 case-only 门控 | CA09-809、CA05-493 |

**重要边界：** `output_kind` 是语义形态；`projection_mode` 是规则如何投影／约束；`abstraction_level` 是本体拓扑或抽象层级。即使两个字段名称相似，也不能互相推导。

## 4. 候选轴二：`event_specificity`

Product 的 PL3-M ontology adapter 已有 `event_specificity` 字段，但现有测试 fixture 中的 `ABSTRACT`、`SCENE_LEVEL` 是 **TEST_ONLY 示例值**，不能当作已冻结的生产词表。

建议候选值：

| 候选值 | 含义 | 示例 |
|---|---|---|
| `PROCESS_SEQUENCE_NOT_SINGLE_EVENT` | 过程／发展序列，不是单一观察事件 | CA01-035 |
| `CONDITIONAL_OUTCOME_NOT_OBSERVED` | 有现实行动前提的条件结果；没有证明已经发生 | CA01-045 |
| `SCENE_NOT_OBSERVED_EVENT` | 场景不是已观察事件 | CA05-469 |
| `EVENT_CLASS_CANDIDATE` | 广义事件类别候选，不是观察事实 | 后续经审查的候选 |
| `SPECIFIC_EVENT_CANDIDATE` | 具体事件候选，但仍不表示事件已发生 | CA09-809 仅作负控制 |

- 对方向轴、领域边界、跨宫约束等非事件语义，提案建议将该轴状态标记为 `NOT_APPLICABLE`，而不是强行写一个事件标签。
- **不建议**在 ontology 候选上设置 `OBSERVED_EVENT`。现实中是否发生属于独立的经验观察层，不能由本体分类断言。
- `UNKNOWN`、`MISSING`、`CONFLICT` 和 `NOT_APPLICABLE` 不是同义词，也不应全部塞进 event-specificity 值域。

## 5. 状态与缺失语义提案

为避免字段缺失、已审但未知、冲突与不适用混为一谈，提案给候选审查层增加一个尚未批准的 `metadata_axis_status` 状态映射：

| 状态 | 建议含义 | 值的处理 |
|---|---|---|
| `RESOLVED` | 已审查并有证据支持一个值 | 必须提供合法值和来源引用 |
| `UNKNOWN` | 已经审查，但目前无法判定 | 值为空；记录不确定原因 |
| `MISSING` | 输入字段或审查结果尚不存在 | 值为空；不得根据别的字段自动补齐 |
| `CONFLICT` | 存在互不兼容的解释 | 值为空；保留双方并引用现有 Conflict 记录，不自动裁决 |
| `NOT_APPLICABLE` | 该轴对当前语义对象确实不适用 | 值为空；本提案仅允许用于非事件对象的 `event_specificity` |

额外规则：

- `source_epistemic=UNRESOLVED_SOURCE` 与 `metadata_axis_status.source_epistemic=UNKNOWN` 不同。前者表示“已经审过，来源支持本身未解决”；后者表示“该轴当前还不能被判定”。
- 对 `output_kind`，规范化主张通常应有类型；不能因为难以分类就标成 `NOT_APPLICABLE`。
- 对存在来源的断言，`source_epistemic` 应有独立认识论判断；如果字段没记录，使用 `MISSING`，而不是把 `SOURCE_SPAN_VERIFIED` 转换成 `EXPLICIT`。
- `CONFLICT` 应复用 `knowledge/KB_SCHEMA.md` 中既有的 Conflict 对象／记录机制。状态字段不代替冲突双方的证据。

**这里有一个尚待 PI 决定的设计选择：** 是采用这个按轴记录的 `metadata_axis_status`，还是仅复用现有 review/conflict 结构。如果选前者，它是新增共享语义原语，不能因它“只是状态字段”而绕过审批。

## 6. 来源例子：怎样避免把来源与归一化混为一谈

### CA01-035 — 过程模式

- 来源原文已在扫描页复核：“事业宫见火铃，主波折。故往往经艰苦而始能底定事业。”
- 候选 `output_kind=PROCESS_PATTERN`；`event_specificity=PROCESS_SEQUENCE_NOT_SINGLE_EVENT`。
- 原文层的 `source_epistemic=EXPLICIT` 是针对逐字主张；“过程模式”这个归一化分类仍应作为候选 `normalization_epistemic=INFERRED` 审查。
- 必须保留“往往”，不得改成必然，也不能把它变成某一个具体事件。

### CA01-045 — 行动条件下的结果

- 来源原文包含“勉强求变”，且上下文依赖 CA01-042 / CA01-044。
- 候选 `output_kind=ACTION_CONDITIONED_OUTCOME`；`event_specificity=CONDITIONAL_OUTCOME_NOT_OBSERVED`。
- 即使原文条件明确，也不能仅凭命盘激活断言现实行动已经发生；缺少行动前提时应 fail-closed。

### CA05-469 — 职业场景

- 来源原文：“若廉贞化忌，则宜从事与血液有关的事业。”
- 候选 `output_kind=SCENE_OR_CONTEXT`；`event_specificity=SCENE_NOT_OBSERVED_EVENT`。
- 不得映射成命主个人受伤、患病或已发生伤害事件。

### M01-006、W01-002、CA01-005 — 不可擅自补齐的元数据

- 这些被接受的 CSV／readjudication JSON 并没有单独编码 `source_epistemic`；因此本提案把该字段状态设为 `MISSING`，而不是自动写 `EXPLICIT`。
- M01-006 是方向／发展轴；W01-002 是领域语义边界；CA01-005 是跨宫推断约束。三者的 `event_specificity` 候选状态均为 `NOT_APPLICABLE`。
- 来源跨度已验证与“本体类型已经确定”是两件事。

### CA09-809 — 具体事件候选负控制

- 允许在非生产样本中用 `output_kind=EVENT_CANDIDATE`、`event_specificity=SPECIFIC_EVENT_CANDIDATE` 来测试边界。
- `case_support_only=true` 仍然独立生效；即使候选分类已判定，也不得晋升为 canonical root 或 mapping。

## 7. 迁移、兼容与回滚

1. **不修改旧来源行。** 本提案引用当前 main 的来源记录，不回写 palace-owned CSV/JSON。
2. **不改变既有认识论枚举。** `source_epistemic`、`normalization_epistemic` 和 `review_status` 沿用 v0.3。
3. **不改变 `projection_mode`。** 它仍是规则投影／约束方式，不变成父子层级或输出类型。
4. **Product 兼容只做只读审计。** 本提案不改 Product adapter、registry、lock、runtime 或 mapping。未来如需传递 `output_kind` 或改变 `event_specificity` 序列化，必须有独立 Product 影响审计与授权。
5. **fail-closed。** `UNKNOWN`、`MISSING` 或 `CONFLICT` 状态不能被默认值消除；缺少必要前提、冲突未解决或 case-only 证据都不能进入 canonical mapping/runtime。
6. **回滚。** 本轮仅有提案文件，回滚是将该版本标记为 superseded/删除提案，不涉及生产迁移。未来冻结 schema 前须另列版本迁移、兼容窗口和回滚步骤。

## 8. 非目标与 Human Gate

本提案不：

- 创建 universal manifestation root；
- 创建 canonical root、manifestation ID 或 ontology node ID；
- 冻结正式本体 schema 或共享元数据枚举；
- 晋升正式映射；
- 修改 Product 注册表、KIB lock、runtime 或消费权限；
- 估计概率、频率、权重或现实预测有效性。

当前 Human Gate 的方向性决定已记录为 C。**本提案中的值域与 `metadata_axis_status` 仍未获批准。** PI 必须先批准或修改详细契约；如果冻结了超出当前方向批准范围的新共享语义原语，应先通过适用的额外 Human Gate。

## 9. 请 PI 审阅的具体问题

1. 是否接受上述候选 `output_kind` 值域，或需合并／拆分哪些类别？
2. 是否接受上述 `event_specificity` 值域，尤其是把 `NOT_APPLICABLE` 作为状态而非事件值？
3. 是否接受按轴的 `metadata_axis_status`，还是优先复用现有 review/conflict 结构？
4. 是否确认 `source_epistemic` 只复用 v0.3 的三个值，并按每条来源断言／引用记录？
5. 是否接受缺失、未知、冲突、不适用的上述区分与 fail-closed 规则？

本文件是提案，以上问题未得到 PI 确认前，不得将候选值写入生产 ontology/mapping registry。
