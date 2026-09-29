# WP04 化忌专章 source review v0.1

Status: **10/10 SOURCE SPANS REVIEWED — ALL 40 TRANSFORMATION SOURCE UNITS NOW REVIEWED**

本轮完成化忌专章十个 source units：太阳、太阴、廉贞、巨门、天机、文曲、天同、文昌、武曲、贪狼。

- 化忌 source units reviewed: **10/10**
- newly added core closure rows: **47**
- 四化 cumulative closure rows: **174**
- transformation source units reviewed: **40/40**
- source mismatch: **0**
- architecture Gate: **NO**

## 关键结构

化忌同样不能解释为统一“负权重”。

源文中至少存在：

- 状态削弱：如天机机变、武曲资源流动性；
- 模式转换：如武曲“决断→决裂”、天机“思考→思虑”；
- 关系/资源/名誉等 L3 投影；
- 文昌与文曲化忌在**错误责任来源**上的结构差异；
- 巨门部分结构的“视凶实吉”，说明同一化忌可经系统状态转为激发；
- 职业/技能环境的风险重定向；
- 多处跨期情绪或关系后效，但仍可装入 A2-R1 typed history，不需要新增记忆类型。

## 健康与历史语义

原文包含大量传统健康、生育、性别及婚恋应象。本轮只在必要时以
`traditional_*_projection_only` 保存其**传统文本标签**，不将其提升为现代医学、性别或社会因果规则。

## OCR

文曲化忌标题在 PDF 提取中出现“文曲(已干化忌)”字形。本轮按 OCR variant 记录，不用该字形改写理论映射。

## 下一步

四化专章 40/40 source units 已完成 source review。下一步进入统一 **canonical reconciliation**：

1. closure row ↔ legacy 56 rows 对齐；
2. 标记 DIRECT_CONFIRMATION / CONTEXT_SCOPE_SEPARATE / GENERALIZES_LEGACY / NEW_CANONICAL_CANDIDATE / NORMALIZATION_REPAIR_REQUIRED / TRADITION_VARIANT；
3. 生成 field-level normalization overrides，但不覆盖 raw legacy catalog；
4. 更新 operator index 与 coverage；
5. regression + deterministic P0 gate；
6. 若无新理论冲突，则把四化闭环作为独立 checkpoint 后再开杂曜 source-coverage PR。
