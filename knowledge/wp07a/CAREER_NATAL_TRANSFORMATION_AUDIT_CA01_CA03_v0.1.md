# 事业宫原局四化条件原子化审查：CA01–CA03 v0.1

状态：**17 条完成条件映射；均未创建可执行规则**
工作单元：`KB-WP07A-CAREER-NATAL-TRANSFORMATION-MAP-CA01-CA03`
来源：`SRC-ZZ-003`，《中州派紫微斗数深造讲义（下）》事业宫章节。

## 一、范围与源文边界

本次只处理 CA01–CA03 中 17 条条件为单星四化、或带明确宫支限定的原局规则。原始语料在主分支中均为 `SOURCE_SPAN_VERIFIED`、`NATAL`、`CASE_SUPPORT_ONLY=false`。

原书事业宫总论（印刷页 132）提醒：事业宫星曜可显示适宜职业性质，但要进一步细化职业判断，仍须参考命宫、财帛宫等结构；相同的行业标签在现实中也可能对应不同工作。因此，本文件只映射“来源条件 → 已有运行事实 → 原始投影目标”，不将单条事业宫规则解释为完整职业结论。

## 二、映射结果

| 来源规则 | 来源页 | 原始条件 | 条件原子 | 原始投影目标 | 模式 | 执行状态 |
|---|---|---|---|---|---|---|
| CA01-052 | 印刷页 133 | 紫微化权 | TRANSFORMATION_PRESENT | `work_independence_strengthened` | FUNCTIONAL_PROJECTION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA01-053 | 印刷页 133 | 紫微化权 | TRANSFORMATION_PRESENT | `authority_does_not_itself_imply_wealth_or_high_rank` | STRUCTURAL_CONSTRAINT | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA01-054 | 印刷页 133 | 紫微化科 | TRANSFORMATION_PRESENT | `reputation_exceeds_financial_return` | FUNCTIONAL_PROJECTION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA01-055 | 印刷页 133 | 紫微化科 | TRANSFORMATION_PRESENT | `independent_professional_work_scene` | SCENE_TRANSLATION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA01-070 | 印刷页 134 | 子午紫微化权 | BRANCH_PRESENT + TRANSFORMATION_PRESENT（子或午） | `career_advantage_strengthened` | FUNCTIONAL_PROJECTION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA01-071 | 印刷页 134 | 子午紫微化权 | BRANCH_PRESENT + TRANSFORMATION_PRESENT（子或午） | `career_advantage_can_coexist_with_marriage_tension` | CROSS_PALACE_CONSTRAINT | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA01-078 | 印刷页 134 | 子午紫微化科 | BRANCH_PRESENT + TRANSFORMATION_PRESENT（子或午） | `reputation_exceeds_financial_return` | FUNCTIONAL_PROJECTION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA02-155 | 印刷页 136 | 天机化禄 | TRANSFORMATION_PRESENT | `hualu_does_not_remove_tianji_instability` | STRUCTURAL_CONSTRAINT | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA02-158 | 印刷页 136 | 天机化权 | TRANSFORMATION_PRESENT | `career_becomes_more_stable_after_prior_change` | FUNCTIONAL_PROJECTION | BLOCKED_PATH_DEPENDENT_TARGET |
| CA02-160 | 印刷页 136 | 天机化科 | TRANSFORMATION_PRESENT | `planning_management_or_design_work_suited` | SCENE_TRANSLATION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA02-164 | 印刷页 136 | 天机化忌 | TRANSFORMATION_PRESENT | `career_changes_recur_after_each_period_of_settlement` | FUNCTIONAL_PROJECTION | BLOCKED_PATH_DEPENDENT_TARGET |
| CA02-194 | 印刷页 136 | 子午天机化忌 | BRANCH_PRESENT + TRANSFORMATION_PRESENT（子或午） | `career_can_trigger_personal_attack` | FUNCTIONAL_PROJECTION | BLOCKED_EVENT_LIKE_TARGET_REQUIRES_MANIFESTATION_REVIEW |
| CA03-252 | 印刷页 137-138 | 巳亥天机化忌 | BRANCH_PRESENT + TRANSFORMATION_PRESENT（巳或亥） | `insurance_scene_suited` | SCENE_TRANSLATION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA03-254 | 印刷页 138 | 天机化科 | TRANSFORMATION_PRESENT | `career_change_property_remains` | STRUCTURAL_CONSTRAINT | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA03-279 | 印刷页 138 | 太阳化禄 | TRANSFORMATION_PRESENT | `career_reputation_or_brand_value_strengthened` | FUNCTIONAL_PROJECTION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA03-283 | 印刷页 138-139 | 太阳化科 | TRANSFORMATION_PRESENT | `reputation_dependent_professional_scene` | SCENE_TRANSLATION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA03-285 | 印刷页 139 | 太阳化忌 | TRANSFORMATION_PRESENT | `dispute_resolution_or_speech_based_work_scene` | SCENE_TRANSLATION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |

结果：
- 指定 17 条全部完成映射，0 条因现有原子类型不足而阻塞。
- 普通四化条件使用绑定 `palace=P09 + star + mutagen` 的 `TRANSFORMATION_PRESENT`。
- 5 条子午/巳亥限定条件另外加入 `BRANCH_PRESENT(palace=P09, branch=...)`，并以 alternatives 表示“指定宫支之一成立”。宫支条件不会被丢弃。
- 所有 `projection_domain`、`projection_target`、`projection_mode` 均直接读取并保留 canonical CSV 原值。

## 三、不能把“条件可映射”误认为“可以直接执行”

- **CA02-158（天机化权）**：来源包含先发生一次改变、之后才趋于稳定的顺序关系，标记为 `BLOCKED_PATH_DEPENDENT_TARGET`。
- **CA02-164（天机化忌）**：来源描述安定后再变更及计划错误，包含反复/路径语义，标记为 `BLOCKED_PATH_DEPENDENT_TARGET`。
- **CA02-194（子午天机化忌）**：来源目标涉及人身攻击，虽然保留原始投影，但标记为 `BLOCKED_EVENT_LIKE_TARGET_REQUIRES_MANIFESTATION_REVIEW`；本映射不授权产品将其作为确定发生的现实事件或概率。

其余 14 条只标记为静态投影候选，仍然不是可执行注册表条目；未来产品实现仍需单独验证规则激活、证据追踪、冲突与输出语义。

## 四、排除清单

| 来源规则 | 原因 | 本次处理 |
|---|---|---|
| CA04-368 | “前格武曲化科”依赖前格/前段上下文 | 不压缩为单一武曲化科条件 |
| CA05-403 | 输出模式为 `TIMING_TRIGGER`，涉及时间关系 | 不纳入静态投影候选 |
| CA06-558 | “天府入庙化科”要求入庙/亮度事实，而当前 runtime 不发出亮度原子 | 阻塞，不丢弃入庙条件 |
| CA07-624 | “贪狼化禄化权”组合语义需要进一步回源确认 | 不猜测同星多四化的表达含义 |
| CA09-852 | 已在 PR #305 的原子化试点中映射 | 避免重复定义 |

## 五、来源与运行事实验证

审查参考了原书事业宫章节印刷页 133–139（对应已上传 PDF 的页面范围），并逐条核对主分支 CA01–CA03 的来源记录。映射测试覆盖：
- 来源 ID、位置、审核状态、原局层级、`CASE_SUPPORT_ONLY` 与 `history_feedback` 元数据；
- 投影域、目标、模式与 canonical CSV 完全一致；
- 条件仅使用现有 `TRANSFORMATION_PRESENT` 与 `BRANCH_PRESENT`；
- 宫支限定条件在指定宫支成立时可匹配，在其他宫支下不能匹配；
- 不创建可执行规则、不修改来源行、不改历史计数、不改产品 runtime/生产注册表。

## 六、结论

本次把 CA01–CA03 中一组源文明确的四化条件变成可审计的形式化映射，同时将“来源条件能否表达”与“输出是否适合直接执行”分开。路径依赖与事件式目标没有被技术上的条件匹配能力掩盖，相关输出仍需后续知识/产品契约审查。