# QI/QR PI 决策包执行证据 v0.1

状态：PROPOSAL_ONLY_NOT_CANONICAL  
Issue：[#735](https://github.com/15937-ass/ziwei-state-space/issues/735)  
当前 Draft PR：[#743](https://github.com/15937-ass/ziwei-state-space/pull/743)  
历史替代 PR：[#736](https://github.com/15937-ass/ziwei-state-space/pull/736) 已关闭且未合并，不再是执行对象。

## 1. 当前工作身份

- 仓库：`15937-ass/ziwei-state-space`
- 目标分支：`main`
- 当前工作分支：`knowledge/core-735-qi-qr-pi-decision-package-r2`
- 当前 PR base SHA：`5a7be5651f1682fe1c5c039f99d77cb1852d9ed3`
- 本次证据文档更新前、已完成验证的 proposal head：`6e8d00c33ca2e546dae065d801d1f95566866ead`
- 对应 GitHub Actions：[`repository-quality-gate` run #40086846064](https://github.com/15937-ass/ziwei-state-space/actions/runs/40086846064)
- 本次更新仅重写本验证记录，不改动决策包、Option C 提案、测试逻辑或正式知识/产品文件。由于提交会产生新的 PR head，必须等待新 head 的完整验证再次通过后才能考虑合并。

## 2. 交付物清单

1. `knowledge/core/qi-qr-overlap-audit/QI_QR_OVERLAP_PI_DECISION_PACKAGE_v0.1.md`
2. `knowledge/core/wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.2.md`
3. `tests/test_knowledge_core_qi_qr_pi_decision_package.py`
4. `knowledge/states/CORE_STATE.yaml`（仅执行恢复缓存；指向 Issue #735、当前分支和 PR #743）
5. 本验证记录

## 3. 覆盖与边界检查

- 决策包逐对覆盖 OVERLAP-01 至 OVERLAP-08；测试要求八组各出现一次。
- QI-17-CAND / QI-18-CAND 保持候选状态；不分配正式 ID，不接受 canonical mapping。
- ZZ-PJ-X06 条件差异继续标记为 unresolved；不把来源中的“或”改成更强的合取条件。
- Option C v0.2 仍是非 canonical 提案；与 v0.1 的历史版本并存，不冻结生产 schema。
- 分开 source_epistemic、normalization_epistemic、review_status、mapping disposition、canonical approval 与 Product consumer readiness。
- 不把共享规则 ID 当成独立证据，不把无共享规则 ID当成已证明正交；不引入无数据支持的分数、权重或概率。

## 4. 验证结果

在 proposal head `6e8d00c33ca2e546dae065d801d1f95566866ead` 上，GitHub Actions run #40086846064 的 `repository-quality-gate` 已完成，结论为 **success**：

- 完整测试套件：通过；
- Product JS adapter 检查：通过；
- deterministic P0 repository gate：通过；
- Repository Governance v1：通过。

注意：本文件本次更新将推进 PR head。旧 head 的绿色结果不自动授权合并；必须确认新 head 对应的完整 quality-gate 也通过，并记录其精确 SHA 与运行结果。PR #743 继续保持 Draft、未合并。

## 5. 方法论参考及证据限制

本决策包引用 Noy & McGuinness 的 Ontology Development 101、W3C SKOS、Cronbach & Meehl 的构念效度研究、Campbell & Fiske 的区分效度研究、House 等关于社会支持结构/过程的研究、Duckworth 等关于长期目标与毅力的研究，以及 BFO 2020。它们仅提供本体建模和构念区分的方法参考，不是紫微斗数现实预测有效性的实证证据。

本轮只完成研究决策包和非 canonical 契约提案，不证明八组概念已经正交或冗余，不修改 `knowledge/qi_ontology.yaml`、`star_cores.yaml`、`star_systems.yaml`、canonical 来源行、Product adapter/registry/KIB lock/runtime 或消费权限。QI-04、QI-06、QI-16 的定义收窄仍是待审提案；任何 canonical 修改或新共享语义原语都需要独立工作单与适用 Human Gate。

## 6. 重开/替代历史

- 原 Draft PR #736 基于旧 main，因 Product-owned stale-cache test 的跨线阻塞修复而关闭未合并。
- Product 测试修复经正确的 Product-owned PR #742 合并，main 当前基线为 `5a7be5651f1682fe1c5c039f99d77cb1852d9ed3`。
- 当前工作在 PR #743 / 分支 `knowledge/core-735-qi-qr-pi-decision-package-r2` 上继续；Core recovery cache 和回归测试均指向 Issue #735 / PR #743。
- 不要合并旧 PR #736，也不要把本提案提前写入正式本体或启用 Product 消费。
