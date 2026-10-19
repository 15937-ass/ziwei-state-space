# 事业宫原局单一四化条件映射审查：CA04–CA09 v0.1

状态：**8 条条件完成映射；未创建任何可执行规则**
工作单元：`KB-WP07A-CAREER-DIRECT-TRANSFORM-MAP-CA04-CA09`
来源：`SRC-ZZ-003`，《中州派紫微斗数深造讲义（下）》事业宫章节。

## 一、审查范围

本批仅纳入 CA04–CA09 中条件文本恰为单星单一四化的八条来源记录。全部记录在 canonical main 中均为 `SOURCE_SPAN_VERIFIED`、`NATAL` 且 `CASE_SUPPORT_ONLY=false`。本批不重写原文，不把场景象义转换为现实事件或概率。

## 二、映射清单

| 来源规则 | 来源位置 | 原始条件 | 原始投影目标 | 模式 | 执行状态 |
|---|---|---|---|---|---|
| CA04-327 | 印刷页 140 | 太阳化忌 | `conflict_resolution_or_problem_solving_work_required` | SCENE_TRANSLATION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA05-403 | 印刷页 142 | 天同化忌 | `work_can_begin_early_while_career_establishment_occurs_relatively_early` | TIMING_TRIGGER | BLOCKED_TIMING_TRIGGER_REQUIRES_TEMPORAL_SPEC |
| CA05-469 | 印刷页 144 | 廉贞化忌 | `blood_or_injury_symbolism_related_industry_scene` | SCENE_TRANSLATION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA07-671 | 印刷页 150 | 巨门化禄 | `speech_based_career_expression_strengthened` | FUNCTIONAL_PROJECTION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA07-672 | 印刷页 150 | 巨门化权 | `speech_based_career_expression_is_supported` | FUNCTIONAL_PROJECTION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA07-673 | 印刷页 150 | 巨门化忌 | `marginal_or_partly_political_scene` | SCENE_TRANSLATION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA08-765 | 印刷页 152 | 天梁化权 | `authority_based_legal_supervisory_or_secretarial_scene` | SCENE_TRANSLATION | STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE |
| CA08-766 | 印刷页 152 | 天梁化科 | `social_status_should_precede_wealth` | FUNCTIONAL_PROJECTION | BLOCKED_PATH_DEPENDENT_TARGET |

八条条件均映射为 `TRANSFORMATION_PRESENT(palace=P09, star, mutagen)`。运行时事实与映射条件结构相符；原始 `projection_domain`、`projection_target`、`projection_mode` 和 `history_feedback` 均按 canonical main 原值保存。

## 三、两条执行门控

- **CA05-403（天同化忌）**：条件可被现有原子表达，但原始 `projection_mode=TIMING_TRIGGER`，目标涉及工作起步和事业建立的时间关系。因此标记 `BLOCKED_TIMING_TRIGGER_REQUIRES_TEMPORAL_SPEC`。不从单一原局条件推造具体年龄或时间窗口。
- **CA08-766（天梁化科）**：保留原始 `history_feedback=PATH_DEPENDENT_GATE`。源文将清贵/社会地位与财富的先后关系明确联系起来，因此标记 `BLOCKED_PATH_DEPENDENT_TARGET`，不把它缩减为无条件财富结论。

其余六条仅是静态投影候选，仍然全部标记 `executable_registry_entry=false`；这并不表示产品已实现这些推断。

## 四、来源解释边界

- **CA04-327 太阳化忌**：印刷页 140 将其事业性质与排难解纷类工作联系；不将压力或是非解释为必然发生的个人事件。
- **CA05-469 廉贞化忌**：印刷页 144 的事业论述将其象义引申至带血光性质的行业，并举饮食、化验等场景；此处只保存职业场景投影，不是疾病或伤害预测。
- **CA07-671/672/673 巨门三种四化**：印刷页 150 讨论口舌行业，并分别区分化禄、化权、化忌的行业倾向。原文还说明，若从事口舌职业且煞刑不重，不应直接推成官非诉讼。
- **CA08-765 天梁化权**：印刷页 152 将其与权威性工作联系，举法律、监察、秘书等例。
- **CA08-766 天梁化科**：印刷页 152 强调先争取社会地位、名誉，再谈财富；本批保留该次序与原始门控标记。
- **CA05-403 天同化忌**：保留 canonical target 与 TIMING_TRIGGER 模式，但不在静态原局条件映射中添加年龄或时序规则。

## 五、排除项

| 来源规则 | 排除原因 |
|---|---|
| CA04-329 | “太阳化禄或化权”是多四化析取条件，留待 OR/alternatives 专项审查 |
| CA04-332 | 需要太阳亮度、吉星及无四煞刑耗等复合条件；不能丢掉未被运行时表达的亮度条件 |
| CA04-368 | 依赖前格/前段语境 |
| CA06-558 | 需要“入庙”亮度事实，现有运行时未发出该事实 |
| CA07-624 | “贪狼化禄化权”复合语义未在本批擅自定解 |
| CA09-853 | 目标具有明确路径依赖 |

## 六、验证与结论

确定性测试核对：八条规则 ID 集合、来源 ID/页码、审核状态、原局层级、CASE_SUPPORT_ONLY、原始 history_feedback、条件文本与投影字段；并验证现有运行时能产生对应绑定四化事实。测试同时确保 CA05-403 与 CA08-766 的执行限制不会被忽略，且所有映射均不进入可执行注册表。

本批的成果是把八条简单原局四化条件纳入可追溯的形式化知识层。复杂星系、亮度、排除条件、时间触发和路径语义仍然留在各自的审查边界内。