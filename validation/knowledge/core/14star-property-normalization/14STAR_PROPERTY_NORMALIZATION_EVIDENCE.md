# 执行证据 — Issue #757 / 十四主星基础性质归一化

## 当前检查点

- Lane / shard：`KNOWLEDGE_ONLY / CORE`
- Work unit：`KB-CORE-14STAR-PROPERTY-NORMALIZATION-BASELINE-01`
- 状态：`IN_PROGRESS_STAGE_A_SOLAR_PILOT`
- Activation base main：`74864f572cdd04407c241c483f3a34c646f69d3a`
- Working branch：`knowledge/core-757-14star-property-normalization`
- 当前检查点范围：太阳候选卡与逐目标映射审核记录；不代表完整十四星交付。

## 输入与来源

- 已接受的映射审核契约：`knowledge/core/wp06b/MAPPING_REVIEW_SCHEMA_v0.1.json`，由 #755 / PR #758 合入 main。
- 既有矩阵：`knowledge/core/14star-property-matrix/14STAR_PROPERTY_MATRIX_QIQR_AUDIT_v0.1.{md,csv,json}`，状态仍为研究草案。
- 既有直接来源审查：`knowledge/core/direct-star-source-review/DIRECT_STAR_SOURCE_REVIEW_BATCH_01_v0.1.csv`，太阳相关七条行级记录被复用。
- 原文：`SRC-ZZ-002`《中州派紫微斗数深造讲义（上）》，来源登记 SHA-256 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`，PDF 扫描页 5 / 印刷页 9–10。
- 已读取项目所附原文 PDF 的第 5 个 PDF 页面；本检查点只做太阳试点范围分类，不重审太阳全部 40 条 canonical 规则。

## 变更与限制

- 新建候选基线 JSON/Markdown、缺口清单、PI 审议草稿、太阳试点测试。
- `knowledge/star_cores.yaml`、`knowledge/star_systems.yaml`、`knowledge/qi_ontology.yaml`、`knowledge/rules/stars/major_stars_canonical_v0.1.csv` 未修改。
- 未新增正式 ontology ID、共享枚举、数值权重、概率、时间阈值或 Product 消费权限。
- 当前是研究检查点；PR exact-head gate 在 PR 建立后执行。尚未将本文件标记为最终验收证据。

## 验证

- 当前提交前：结构/枚举预检将与 #755 实际合入的 validator 对照。
- 完整 pytest、P0 审计、治理/ Core write-set 检查：待本检查点 PR 的 exact-head CI。
- Product 回归：由当前路径过滤与 CI 实际结果决定；不预先宣称通过。

## 下一步

完成太阳试点检查点后，继续太阴；重点检验相对描述、收敛基调与条件分支能否在不引入新共享枚举的情况下被保存。
