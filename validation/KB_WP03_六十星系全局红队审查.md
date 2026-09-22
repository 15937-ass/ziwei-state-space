# KB-WP03 六十星系全文规则库：全局红队审查 v0.2

状态：**WP03 RULE EXTRACTION REVIEWED**

> REVIEWED 仅表示《中州派紫微斗数深造讲义（上）》六十星系章已经完成结构化抽取、来源校核、schema审计和全局一致性检查；不表示传统理论已经得到经验验证，也不等于推演引擎已完成。

## 一、最终覆盖

来源：SRC-ZZ-002，《中州派紫微斗数深造讲义（上）》六十星系章，印刷页33–164。

- G1 系统1–10：314条
- G2 系统11–20：332条
- G3 系统21–32：365条
- G4 系统33–42：369条
- G5 系统43–52：422条
- G6 系统53–60：376条

**总计：2178条 reviewed rules，60/60系统覆盖。**

另生成 `knowledge/sixty_system_modes_canonical_v0.1.csv`，60个系统各有且仅有一个 principal mode 入口。

## 二、工程完整性审计

- 60个 system_no 全部存在；
- 60个 principal mode 全部存在；
- required fields 缺失 = 0；
- duplicate rule_id = 0；
- source_id 全部来自 SRC-ZZ-002；
- epistemic_type_source 全部为 EXPLICIT；
- status 全部为 reviewed；
- canonical mode 引用的60个 rule_id 全部真实存在。

## 三、全局结构画像

2178条规则中，最大的类别是 temporal_reaction，共1005条；其次是 cross_system_interaction 364条、mode_modifier 351条、mode_definition 234条。说明中州派六十星系章的核心不是静态“星情词典”，而是本质—条件—运限反应关系。

现有 delta_status 中：interaction_delta 217条，case_level 141条，另有 projection_only / interaction_candidate 等早期保留层。后续 KB-WP07 应把这些层作为推演引擎的不同证据权重，而不是混成同一规则等级。

## 四、源文冲突与OCR审计

此前系统35天相巳亥存在一项OCR疑义。已回核原PDF版面，确认原文为：刑忌所夹反主开创力，但艰辛。规则 `ZZ-SYS-35-005` 已修正，`CF-KB-0035-001` 标记 resolved。

当前 open source conflicts = 0。

## 五、对G4/G5模型的全局反馈

### 1. principal mode 是中尺度派生状态，不是吉凶分数

60组星系的principal mode包括精神/物质、稳定/动荡、决断/短虑、受拖累/不受拖累、物欲/情欲、稳重/浮薄、尖刻/明断等。它们描述“系统如何组织同一组驱动力”，而不是简单好坏强弱。

因此保持：

`z_s = M_s(q_stars, modifiers, structure)`

而不是：

`z_s = scalar_goodness`

### 2. 四化必须是星曜特异、结构依赖的算子

相同化禄、化权、化科、化忌在不同星系、不同principal mode、不同时间层可以产生相反或非单调结果。六十星系全文进一步否定“禄=固定正值、忌=固定负值”的简单加权。

### 3. 原局本质决定运限反应函数

全文大量出现“同一运限输入，对不同原局本质产生不同结果”。这直接支持 state-dependent reaction：

`response = R(natal_essence, system_mode, temporal_input, context)`

### 4. 时间尺度必须显式建模

原文多次区分大限与流年：同一星系在大限可能形成长期结构、路径依赖或心理反应，而流年仅表现为短时触发。KB-WP07需要显式 time_scale。

### 5. historical_context / path dependence 已具文本证据，但暂不重开G5

多个系统说明前一运限形成的冷退、因循、顽嚣、怯懦等反应会影响后运。建议在未来版本加入 `historical_context_t` 扩展接口，但Paper-1冻结模型仍以“原局本质 + 当前时序输入 -> 反应”为主。

### 6. human response 必须与 astro input 分离

源文频繁要求守成、进取、退居幕后、离乡、持盈保泰、慎选合作、避免妄动等。它们属于人的反应政策，不应混入命盘输入。未来若研究controllability，应把 `u_t^human` 与 `u_t^astro` 分开，并以外部因果数据检验。

## 六、知识库边界

疾病、事故、婚姻、诉讼、自毁等内容仅作为传统文本语义和教材案例标签保存，不转换成现代医学、心理学、法律或因果预测结论。

## 七、KB-WP03结论

六十星系全文规则抽取阶段已经完成到 **60/60 REVIEWED**。

此时可以进入后续工作：

1. KB-WP04：辅佐八曜、六煞、化曜的完整算子库；
2. KB-WP06：教材案例结构化与 regression-case 挂接；
3. KB-WP07：evidence-first 推演引擎与端到端回归；
4. 在KB-WP06/07完成后，再把相应 coverage 从 REVIEWED 升级为 COMPLETE。