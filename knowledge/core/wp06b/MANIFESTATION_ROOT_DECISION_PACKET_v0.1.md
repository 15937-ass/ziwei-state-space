# WP06B Manifestation Root Decision Packet v0.1

**状态：Human Gate 材料；非 canonical ontology，不是产品可消费 artifact。**  
**工作单元：** `KB-WP06B-MANIFESTATION-ROOT-SOURCE-REVIEW`（Issue #672）  
**Human Gate：** `HG-WP06B-MANIFESTATION-ROOT-01` — `PENDING_PI_DECISION`  
**本分支基线：** `2143ac7030b531cd46836cf034baba6f801bdf8e`  
**来源：** `SRC-ZZ-003`，《中州派紫微斗数深造讲义（下）》。

## 1. 需要 PI 决定的问题

是否建立一个跨领域的通用应象语义根，还是保留多个有来源依据的根，并把输出类型、事件具体度和来源证据等级作为正交字段？

本包只提供证据、方案与后果，不创建根节点，不分配 manifestation ID，也不替 PI 批准 Human Gate。

## 2. 为什么不能直接把“应象”理解为“具体事件”

已接受的 WP05 canonical rows 展示出多种不同的输出形态。它们来自同一中州派来源，但不能因此被假定为同一种本体层级。

| 来源规则 | 印刷页／source span | accepted projection target | projection mode | 本包中的候选抽象描述 | 证据边界 |
|---|---|---|---|---|---|
| CA01-035 | p133 / `ZZ003-P133` | `career_setbacks_before_stabilization` | FUNCTIONAL_PROJECTION | 职业发展过程 | 原文“往往”须保留；火铃量词未决 |
| CA01-045 | p133 / `ZZ003-P133` | `forced_change_can_create_career_difficulty` | FUNCTIONAL_PROJECTION | 现实行动条件下的结果 | 依赖 CA01-042 / CA01-044；“勉强求变”不是盘面事实 |
| CA05-469 | p144 / `ZZ003-P144` | `blood_or_injury_symbolism_related_industry_scene` | SCENE_TRANSLATION | 职业／行业场景 | 是血液相关行业场景，不是命主伤病事件 |
| W01-002 | p69 / `ZZ003-P69` | `earning_difficulty_modified_by_fortune_palace` | PALACE_SEMANTIC_BOUNDARY | 资源获取条件／财务难易 | 不是单一可观察事件 |
| M01-006 | p109 / `ZZ003-P109` | `home_vs_away_development_axis` | FUNCTIONAL_PROJECTION | 迁移／内外发展轴 | 不等于已经发生迁移 |
| CA01-007 | p132 / `ZZ003-P132` | `career_structure_can_affect_marriage_context` | CROSS_PALACE_CONSTRAINT | 关系域中的跨宫约束 | 不是已观察到婚姻事件的证明 |
| CA09-809 | p153 / `ZZ003-P153` | `life_threatening_hazard_candidate` | EVENT_CANDIDATE | 具体事件候选 | `case_support_only=true`，仅作排除用负控制 |
| CA01-005 | p132 / `ZZ003-P132` | `career_refinement_requires_life_and_wealth_context` | CROSS_PALACE_CONSTRAINT | 推断前提／跨宫约束 | 不是应象节点 |

### 直接复核与复用边界

- P09 的 CA01-035、CA01-045、CA05-469 已直接对照所提供 PDF 扫描页复核：PDF p.67 / 印刷 pp.133–134，以及 PDF p.72 / 印刷 p.144。
- P05 W01-002、P09 CA01-005／CA01-007／CA09-809 仅复用 `main` 上标记 `SOURCE_SPAN_VERIFIED` 的 canonical CSV 行；本工作单元没有宣称重新逐字校勘这些页面。
- P07 M01-006 使用已接受的 `knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_READJUDICATION_100_v0.1.json`（`DIRECT_SOURCE_RECHECK_CONFIRMED` 且 `canonical_promotion=true`）；旧 `validation/wp05/M01_migration_projection_review_001_100.csv` 是 `PRE_G12_READ_ONLY_ACCELERATION_INPUT`，不作为 canonical evidence。
- 本包不使用 P03/P06 中当前 palace state 仍标记 `CANONICAL_REVALIDATION_NOT_STARTED` 的 CSV 行作为 canonical evidence。
- P07 M01-006 使用已接受的 `knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_READJUDICATION_100_v0.1.json`（`DIRECT_SOURCE_RECHECK_CONFIRMED` 且 `canonical_promotion=true`）；旧 `validation/wp05/M01_migration_projection_review_001_100.csv` 是 `PRE_G12_READ_ONLY_ACCELERATION_INPUT`，不作为 canonical evidence。
- 来源文件 SHA-256：`6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`。

## 3. 核心发现

1. **projection_mode 不等于 ontology hierarchy。** `FUNCTIONAL_PROJECTION`、`STATE_EXPRESSION`、`RELATIONAL_PROJECTION`、`SCENE_TRANSLATION`、`EVENT_CANDIDATE` 与 `STRUCTURAL_CONSTRAINT` 是现有规则行的投影／约束模式。不能仅凭这些值就把它们串成父子层级。
2. **事件具体度是另一条轴。** 发展过程、关系状态、职业场景和具体事件候选并非天然同义。尤其不能把职业场景映射直接升级成个人伤病事件。
3. **case-only 证据不能决定 canonical root。** CA09-809 的 `case_support_only=true`，只作为负控制，不能用来证明通用事件家族或现实发生率。
4. **来源跨度已核验不等于规范化目标逐字显式。** 对缺少单独 epistemic 字段的旧 canonical CSV，本包明确记录该缺口，不把它默认为 `EXPLICIT`。
5. **没有证据时应保留多根／未知。** 技术上的统一查询需求不能替代来源支持的语义根。

## 4. 供 PI 选择的三种方案

### OPTION A — 通用语义根

建立一个跨领域的 manifestation 根，再向下划分 family、channel 与 observable event label。

- 优点：统一入口和层级查询简单。
- 风险：现有来源没有直接给出一个能同时覆盖过程、状态、关系、场景和具体事件的通用语义根；可能把异质输出压成同一种东西。
- 门槛：属于新增跨领域共享语义，必须经 `HG-WP06B-MANIFESTATION-ROOT-01` 明确批准。

### OPTION B — 来源本位根森林

允许多个 `parent_id=null` 的来源本位根，不制造统一语义父节点。

- 优点：保留 source-native 差异，不凭技术便利发明传统概念；产品 adapter 已支持根节点。
- 风险：跨领域检索需要显式元数据或接口，不能靠共同父节点实现。

### OPTION C — 来源本位根森林 + 正交元数据轴

保留来源本位根森林，并将 `output_kind`、`event_specificity`、`source_epistemic` 分开建模；不把 `projection_mode` 直接当作 ontology hierarchy。

- 优点：能区分状态、关系、过程、职业场景和具体事件候选，也能把来源显式性与规范化推断分开。
- 风险：需要另行冻结最小字段契约；字段若被提升为通用语义原语，也可能需要 Human Gate。

**供 PI 讨论的初步建议：OPTION C。** 这是风险较低的审查建议，不是已选方案，不会被代码或测试当作批准结果。

## 5. Human Gate 前不允许发生的事

- 不创建通用根或任何 accepted manifestation node。
- 不给候选家族分配 `manifestation_id`。
- 不将 `EVENT_CANDIDATE` 或 `CASE_SUPPORT_ONLY` 提升为 canonical mapping。
- 不将规则投影模式直接当作 ontology 层级。
- 不填充 `product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json` 或 `product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json`。
- 所有候选保持 `probability_status=UNKNOWN`；无频率、概率、权重、分数或 posterior。

## 6. 当前状态与交付

- JSON 机器可读包：`knowledge/core/wp06b/MANIFESTATION_ROOT_DECISION_PACKET_v0.1.json`
- 本说明：`knowledge/core/wp06b/MANIFESTATION_ROOT_DECISION_PACKET_v0.1.md`
- 回归测试：`tests/test_knowledge_core_wp06b_manifestation_root_decision.py`
- 执行证据：`validation/knowledge/core/wp06b/EXECUTION_EVIDENCE.md`
- 当前 gate 状态仍为 `PENDING_PI_DECISION`。PI 选择前，ontology 与 mapping production registry 继续为空。
