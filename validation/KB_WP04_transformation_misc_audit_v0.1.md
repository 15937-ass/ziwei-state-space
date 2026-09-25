# KB-WP04 四化与杂曜算子阶段审查 v0.1

状态：**A4 RED-TEAM PASSED WITH NON-BLOCKING NOTES**  
范围：`knowledge/operators/transformation_rules_v0.1.csv` + `knowledge/operators/misc_stars_v0.1.csv`  
核心来源：SRC-ZZ-002《中州派紫微斗数深造讲义（上）》

## 1. 本批实际产物

- 四化规则：56 条
- 杂曜规则：73 条
- 四化+杂曜新增合计：129 条
- 四化：56/56 标记为 `EXPLICIT`
- 杂曜：72 条 `EXPLICIT`，1 条 `INFERRED`
- 四化+杂曜规则状态：129/129 = `reviewed`
- 四化+杂曜 Source ID：129/129 完整
- 四化+杂曜 Source location：129/129 完整
- 无连续经验权重
- 无新增 primitive qi
- 无河洛、钦天、华山等外派规则混入

## 2. A4 核心审查结论

### 2.1 否决“化禄=统一正增益、化忌=统一负增益”

本批文本提供多组反例，因此四化必须是 **subject-dependent + context-dependent operator**：

- 天机：化权偏“用于世”，化科偏“聪敏归正”，化禄偏实用机变；三者不是同一方向的简单大小关系。
- 太阴：化禄与化忌都可使意志薄弱，但分别偏感情/物质；化权、化科反而增强意志。
- 天梁：化禄偏精明，化科偏正直；化权是否转为正直取决于是否有吉曜。
- 太阳：午宫低煞时化忌可转为沉稳；子宫化忌也可沉稳，而化权反可能虚浮。
- 贪狼：化忌可降低欲望，并非统一“负向放大”。

结论：
```text
T_hua != constant scalar gain
T_hua = T(star/system, palace/context, co-stars, temporal layer)
```

### 2.2 状态依赖增益获得强文本支持

已抽取的规则明确出现：

- 运限太阳化禄输出受原局强弱调制；
- 鸾喜作为婚育应期触发器，必须由正曜星系“吉利稳定”门控；
- 同一个天刑，对天机表现为变动阻力，对天梁则表现为原则性增强；
- 天姚与煞忌、红鸾天喜、昌曲组合时作用方向不同。

这支持第一篇既定的非线性状态方程，而不支持固定 LTI 增益解释。

### 2.3 杂曜应分为四种功能，不应全部当作普通星曜状态

本批可归纳为：

1. **state modifier**：天刑、天姚、华盖、大耗等；
2. **relational / pair structure**：红鸾—天喜、天刑—天姚、孤辰—寡宿；
3. **context gate / trigger**：鸾喜应期、流煞冲起等；
4. **projection modifier**：恩光天贵、台辅封诰等在事业/财帛宫的荣誉、资源输出。

该分类与 G2 分层本体兼容，无需新增 primitive qi。

## 3. 暂存的局部/系统状态

以下状态在文本中有明确区分，但证据不足以提升为全局 primitive qi，因此暂作为 local/system state：

- `talent_deployment`
- `material_orientation`
- `spiritual_orientation`
- `volitional_strength`
- `shrewdness`
- `system_darkness`
- `planning_design_capacity`
- `affective_drive`
- `self_discipline`
- `indulgence_drive`
- `talent_capacity`
- `recovery_resilience`

处理原则：
> 允许局部状态存在；只有跨星曜、跨星系重复并显示独立动力学意义时，才提交 primitive-qi Gate。

本批没有触发该 Gate。

## 4. Schema 审计

发现原 `operator_schema.yaml v0.1` 与已经存在的 reviewed operator 文件存在工程层 schema drift：

既有规则已经使用：
- `projection`
- `structural_relation`
- `pair_interaction`
- `gate`

但 v0.1 allowed enum 未包含这些类型。

已更新为 `operator_schema.yaml v0.2`，仅做工程枚举对齐，不改变 G2 ontology，也不改变任何核心理论定义。

## 5. 风险项

### R-1：OCR/文本字形误差
上册存在“巨/臣”“天官/天宫”“地劫/地幼”等 OCR 噪声。当前规则以语义明确段落为主；涉及星名歧义的规则不得自动升级为 approved canonical。

### R-2：投影与潜变量混淆
“名誉、婚姻、生育、得财、考试”等不得进入 primitive qi；本批均保留在 L3 projection 或 contextual output。

### R-3：历史性标签
古代职业、死亡、性别评价等只保留为文本语义/历史投影，不直接转写为现代确定性预测。

## 6. 当前判定

```text
WP04-A 四化算子：可进入下一轮扩充
WP04-B 杂曜算子：已建立首批50条，可继续穷尽页117-120及星系章节中的条件性杂曜规则
Human Gate：NO
Ontology change：NO
Core operator change：NO
School conflict：NO
```

下一机械步骤：
1. 继续扫描上册全部杂曜命中，扩充 misc catalog；
2. 对 60 星系规则反向索引四化/杂曜条件，补齐“system-specific operator edges”；
3. 去重并建立 modifier -> affected state/system 的索引；
4. 更新 WP04 coverage 指标。


## 7. 六十星系反向覆盖审计（追加）

已对 2193 条六十星系规则执行 modifier trigger 反向扫描，并生成：

- `knowledge/operators/system_operator_edges_v0.1.csv`
- 识别 654 条四化/杂曜相关 system-specific operator edges
- 覆盖 60/60 星系
- 高频触发：化忌 309、化禄 223、化权 95、化科 83
- 已建立 `knowledge/coverage/wp04_system_edge_coverage_v0.1.csv`

同时对 62 个候选小星/阶段标记执行 usage inventory：
- 31 个在六十星系规则中实际出现；
- 经补充抽取后，这 31 个均已在当前 operator catalogs 中获得表示；
- `wp04_misc_gap_analysis_v0.1.csv` 当前剩余 gap = 0。

注意：这里的“gap=0”仅表示**已扫描候选集合中、实际被60星系调用的 modifier 均已有 catalog representation**，不等同于宣布整本上册所有杂曜语义已经穷尽。

## 8. 当前全 operator 库指标（追加）

四个基础 catalog 合计：
- 辅佐八曜：103
- 六煞：81
- 四化：56
- 杂曜/阶段：73
- 总计：313 条 reviewed operator rules
- EXPLICIT：312
- INFERRED：1
- unique modifier expressions：188

另有六十星系派生 operator edges：654 条。

**Human Gate：仍未触发。**
