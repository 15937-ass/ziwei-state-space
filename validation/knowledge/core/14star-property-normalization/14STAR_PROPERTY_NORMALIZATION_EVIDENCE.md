# 执行证据 — Issue #757 / 十四主星基础性质归一化

## 当前检查点

- Lane / shard：`KNOWLEDGE_ONLY / CORE`
- Work unit：`KB-CORE-14STAR-PROPERTY-NORMALIZATION-BASELINE-01`
- 状态：`IN_PROGRESS_STAGE_A_TAIYIN_PILOT`
- Activation base main：`74864f572cdd04407c241c483f3a34c646f69d3a`
- Working branch：`knowledge/core-757-14star-property-normalization`
- 当前检查点范围：太阳已通过 exact-head CI 的候选卡与太阴当前候选卡/逐目标映射审核；不代表完整十四星交付。

## 输入与来源

- 已接受的映射审核契约：`knowledge/core/wp06b/MAPPING_REVIEW_SCHEMA_v0.1.json`，由 #755 / PR #758 合入 main。
- 既有矩阵：`knowledge/core/14star-property-matrix/14STAR_PROPERTY_MATRIX_QIQR_AUDIT_v0.1.{md,csv,json}`，状态仍为研究草案。
- 既有直接来源审查：`knowledge/core/direct-star-source-review/DIRECT_STAR_SOURCE_REVIEW_BATCH_01_v0.1.csv`，太阳七条既有行级记录被复用，太阴 25 条视觉来源审查另存于 `knowledge/core/14star-property-normalization/TAIYIN_SOURCE_SPAN_REVIEW_v0.1.csv`；不修改 #720 Batch 01 的固定覆盖表。
- 原文：`SRC-ZZ-002`《中州派紫微斗数深造讲义（上）》，来源登记 SHA-256 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`，太阳 PDF 扫描页 5 / 印刷页 9–10；太阴 PDF 扫描页 10 / 印刷页 19–20。
- 已核对项目所附原文 PDF 的第 5 个与第 10 个 PDF 页面，并确认 PDF SHA-256 与 `sources/source_index.csv` 一致；太阳 40 条规则未全审；太阴本轮仅覆盖书页 19–20 的 25 条规则，书页 42 的 `ZZ-TYI-010` 未审。

## 变更与限制

- 新建/更新候选基线 JSON/Markdown、缺口清单、PI 审议草稿、太阳与太阴试点测试、执行证据及 Core 状态；新增独立的 25 条太阴来源审查 CSV，不修改 #720 Batch 01 固定覆盖表。
- `knowledge/star_cores.yaml`、`knowledge/star_systems.yaml`、`knowledge/qi_ontology.yaml`、`knowledge/rules/stars/major_stars_canonical_v0.1.csv` 未修改。
- 未新增正式 ontology ID、共享枚举、数值权重、概率、时间阈值或 Product 消费权限。
- 当前是研究检查点；PR exact-head gate 在 PR 建立后执行。尚未将本文件标记为最终验收证据。

## 验证

- 当前提交前：结构/枚举预检将与 #755 实际合入的 validator 对照。
- 太阳 exact head `bb7d4a25551438c2a519a906e12e86dbb392d1d3` 的 repository-quality-gate Run #40159112167 已通过：pytest、Product JS adapter、确定性 P0 与 Repository Governance v1 均成功。太阴新提交尚待新的 exact-head CI。
- Product 回归：由当前路径过滤与 CI 实际结果决定；不预先宣称通过。

## 下一步

太阳检查点已通过 exact-head CI。当前继续太阴：检验收敛最优区域、OR 条件、昌曲门控、跨星/跨宫关系与下游结果能否在不引入新共享枚举的情况下被保存；新 head 必须重新通过 exact-head CI 后再进入天相。
