# WP06C P09 三候选正式 Mapping Review 试批 v0.1

**状态：`FORMAL_MAPPING_REVIEW_COMPLETED_NOT_CANONICAL`**  
**工单：** #864 / `KB-CORE-WP06C-P09-FORMAL-MAPPING-REVIEW-PILOT-01`

## 1. 这轮实际做了什么

本轮不是把三条规则直接塞进 Product，也不是创建 canonical ontology ID。它把 #673 已经完成来源核对的三条 P09 候选，第一次按 #841 PI 已接受的 D1–D5 契约做**逐目标正式 mapping-review**。

每个来源候选至少审核两个 target：

- 一个来源真正支持的候选 target；
- 一个最容易被误推、但来源不支持的错误 target。

因此“来源支持什么”和“来源绝对不能被解释成什么”同时被机器可读地保存。

## 2. 结果摘要

| 来源 | 正向 target | 正向 disposition | 明确拒绝的 target |
|---|---|---|---|
| CA01-035 | `career_setbacks_before_stabilization` | `supported_candidate` | 单一已发生事业事件 |
| CA01-045 | `forced_change_can_create_career_difficulty` | `supported_candidate`，但必须保留“勉强求变”现实行为前提 | 无条件、仅凭命盘断言事业困难 |
| CA05-469 | `blood_or_injury_symbolism_related_industry_scene` | `supported_candidate` 场景映射 | 命主个人受伤／患病／事故事件 |

三个正向 review 都只是 **supported candidate**，不是 canonical mapping。

## 3. D1–D5 在真实映射中的表现

### D1：三轴与审核角色可以保持正交

- CA01-035：`PROCESS_PATTERN` + `PROCESS_SEQUENCE_NOT_SINGLE_EVENT`
- CA01-045：`ACTION_CONDITIONED_OUTCOME` + `CONDITIONAL_OUTCOME_NOT_OBSERVED`
- CA05-469：`SCENE_OR_CONTEXT` + `SCENE_NOT_OBSERVED_EVENT`

这些 output/event 语义没有被塞进 `evidence_role`。逐目标审核的 `evidence_role` 仍独立记录。

### D2：不需要为了三条真实记录把 output_kind 冻成穷尽枚举

三条都能用当前已观察候选类型表达，没有暴露新的共享 output kind；因此没有理由现在补一个“万能其他类”。

### D3：没有暴露新的全局 metadata-axis schema 缺口

当前非 canonical review artifact 足以保留 `KNOWN/UNKNOWN/MISSING/CONFLICT/NOT_APPLICABLE` 的边界。没有证据支持新增全局共享字段。

### D4：source epistemic 不从 review status 推导

本轮沿用来源候选索引中已有的来源状态；CA05-469 的 `source_epistemic=EXPLICIT` 与 `normalization_epistemic=INFERRED` 同时保留，没有因为来源已核验就把归一化推断冒充原文显式表达。

### D5：mapping review 与 canonical / Product gate 分开

当前结果仍满足：

- canonical ontology ID = null；
- canonical mapping approval = false；
- executable = false；
- Product/KIB/runtime consumer readiness = false；
- probability = UNKNOWN。

## 4. 三个关键结论

### CA01-035

来源支持“事业发展经历波折／艰苦后趋于底定”的**过程候选**。  
必须保留“往往”，且“火铃”究竟要求两星同时还是任一仍未决。  
因此可以保留正向 process target，但不能把它变成某个已经发生的单一事件、必然结果或确定时间。

### CA01-045

来源支持的不是“命盘一出现某组合就必然事业困难”，而是**在前格条件之上又发生‘勉强求变’这一现实行为时**的条件性结果。  
CA01-042 / CA01-044 和“勉强求变”都必须保存。  
因此正向 target 可以被保留为 supported candidate，但执行仍被现实行为前提阻断。

### CA05-469

这是本轮最重要的负控制。  
来源位于事业语境，支持把相关象义翻译成职业／行业场景；它不支持把场景进一步偷换为命主本人受伤、患病或发生事故。  
因此同一来源对“职业场景 target”可为 supported candidate，对“个人伤病事件 target”明确为 `not_supported_for_target`。

## 5. 当前没有发现的新 schema 问题

六条 mapping-review 均可用现有 v0.1 envelope 表达；这轮不需要：

- 新增共享 evidence role；
- 新增全局 metadata-axis-status；
- 修改 D1–D5；
- 发明通用 manifestation root；
- 修改 Product registry。

## 6. 下一道真正的 Human Gate

这轮试批完成以后，技术问题已经从“现有契约能不能做真实 mapping review”转成：

> 是否要开始给这些经过来源审查的稳定 target 建立**共享 canonical ontology node identity**，以及是否允许其中任何一条从 `supported_candidate` 晋升为 canonical mapping？

这已经超出 #841 的 D1–D5 授权范围。

因此：

- 本试批本身可以作为 non-canonical mapping-review 结果合并；
- 下一步如果要创建稳定 canonical node/ID、接受具体 canonical mapping，必须交 PI 决定；
- Product registry 继续保持 empty/fail-closed。

## 7. 明确未授权

本轮不授权任何 ontology ID、canonical mapping、生产 schema、Product/KIB/runtime 消费、概率、权重、posterior 或经验预测效度。
