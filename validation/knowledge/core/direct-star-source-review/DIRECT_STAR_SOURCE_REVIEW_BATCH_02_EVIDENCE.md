# DIRECT_STAR 来源优先审查第二批 — 验收证据

状态：`PROPOSAL_ONLY_NOT_CANONICAL`

- Issue：[#728](https://github.com/15937-ass/ziwei-state-space/issues/728)
- 工作单元：`KB-CORE-DIRECT-STAR-SOURCE-REVIEW-BATCH-02`
- Activation main：`e72d81a3dfd0aa3286fabaf1d6852aa48cc945c3`
- Branch：`knowledge/core-728-direct-star-source-review-batch-02`
- 目标：后七颗主星现有 DIRECT_STAR 引用，33 个唯一 rule ID。
- 来源 SHA-256 已核对：SRC-ZZ-002 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`；SRC-ZZ-001 `7ebafc8e3477430e2f8e69c6925ecc373d3c28966955f7035078c4949b7475a2`。
- PDF 页面图像检查：SRC-ZZ-002 物理扫描页 10–16（印刷页 19–32）；SRC-ZZ-001 物理扫描页 42（印刷页 83）与 44（印刷页 87）。
- 行级 CSV：`knowledge/core/direct-star-source-review/DIRECT_STAR_SOURCE_REVIEW_BATCH_02_v0.1.csv`
- 报告：`knowledge/core/direct-star-source-review/DIRECT_STAR_SOURCE_REVIEW_BATCH_02_v0.1.md`
- 测试：`tests/test_knowledge_core_direct_star_source_review_batch_02.py`

## 静态覆盖核验

- 行数：33；唯一 rule ID：33；重复 ID：0。
- 星曜分布：太阴=5, 贪狼=4, 巨门=3, 天相=2, 天梁=6, 七杀=5, 破军=8。
- 每行均有 source ID、PDF 扫描页、印刷页、原文短引、当前气核引用、证据角色评估和条件范围说明。
- 每行 `source_span_status=VERIFIED_VISUAL_SCAN`；这仅是本轮研究审查状态，不覆盖 canonical `source_span_verified=false`。
- 每行 `source_epistemic=EXPLICIT`；`normalization_epistemic` 前后均为 `UNRESOLVED`。
- 每行均为 `PROPOSAL_ONLY_NOT_CANONICAL`。
- canonical source rows、source registry、star cores、ontology、star systems、Product/runtime、registry/locks/state caches 均未修改。

## 验证要求

此文件是验收证据的初始草案。提交后必须在最新 main 基线上运行 exact-head 全仓质量门：pytest、Product JS adapter syntax、deterministic P0 repository gate、Repository Governance v1。旧 head 的验证不得用于新 head 的合并授权。

最终 head SHA、精确 base SHA、完整 workflow run URL、各步骤结果和任何剩余限制将在 live Issue #728 / PR 中记录。为避免自引用验证循环，最终 exact-head run 通过后不再编辑本文件；验收真相以 live Issue/PR 和对应 GitHub Actions run 为准。

## 限制与未决项

- 当前研究仅核验源文可追溯性，不接受 QI/QR mapping、不改变 canonical semantics、不授权 Product consumption。
- `ZZ-PJ-X06` 的 canonical 条件比已检查原文更具体，需保留差异；本轮不修改原条件。
- 多个规则共享同段/同句；按唯一 rule ID 计数，不声称其为独立证据。
- 本审查不证明十四主星属性空间完备或现实预测有效。
