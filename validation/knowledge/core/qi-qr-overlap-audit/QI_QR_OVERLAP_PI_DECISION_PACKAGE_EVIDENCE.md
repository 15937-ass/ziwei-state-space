# QI/QR PI 决策包验证记录 v0.1

状态：PROPOSAL_ONLY_NOT_CANONICAL  
Issue：[#735](https://github.com/15937-ass/ziwei-state-space/issues/735)

## 1. 基线与范围

- 仓库：15937-ass/ziwei-state-space
- 目标分支：main
- 分支：knowledge/core-735-qi-qr-pi-decision-package
- 创建工作分支时观察到的 main/base SHA：4171b2f0cf809a98541b344fee4100a7eb63f8a0
- 本记录创建前的工作分支 head SHA：60328bd236e414aba00de94aaa7abc5c911524cd
- 文件清单：
  - knowledge/core/qi-qr-overlap-audit/QI_QR_OVERLAP_PI_DECISION_PACKAGE_v0.1.md
  - knowledge/core/wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.2.md
  - tests/test_knowledge_core_qi_qr_pi_decision_package.py
  - 本验证记录

SHA 是本次仓库操作时观察到的版本快照。PR 创建后以 GitHub PR 的 base/head SHA 和该 head 上的 CI 为最终验证依据；如果 main 已移动，必须重新同步并按 exact-head 规则验证。

## 2. 覆盖检查

- 八组覆盖：由测试检查 OVERLAP-01 至 OVERLAP-08 恰好各一次。
- 候选保护：测试检查 QI-17-CAND / QI-18-CAND 不正式化。
- 来源差异保护：测试检查 ZZ-PJ-X06 的条件差异继续标记未解决，且不在本包改写。
- 契约边界：测试检查 Option C 三轴与 QI/QR 映射审查分离，并保留 UNKNOWN、MISSING、CONFLICT、NOT_APPLICABLE 区分。
- canonical/产品保护：测试检查本包仅为提案，不授权 canonical ontology 或 Product adapter 修改。

## 3. 外部方法论参考

本包链接 Noy & McGuinness 的 Ontology Development 101、W3C SKOS、Cronbach & Meehl 的构念效度论文、Campbell & Fiske 的区分效度论文、House et al. 的社会支持结构/过程研究、Duckworth et al. 的毅力研究，以及 BFO 2020 资料。

这些资料仅用于方法论比较，不被用作紫微斗数现实预测有效性的证据。

## 4. 验证状态

- 文件写入：已完成（通过 GitHub connector 返回的 commit SHA）。
- 本地 pytest：本执行环境未直接运行，不能宣称通过。
- PR exact-head CI：待 PR 创建后由 GitHub Actions 返回结果。
- 生产/正式语义变更：无；本工作只新增非 canonical 提案、测试和验证说明。
- 合并状态：未合并；PR 应保持 Draft，直到当前 exact head 的要求检查通过并完成审阅。

## 5. 限制与后续

- 本轮不证明八组维度正交或冗余。
- 本轮不修改 canonical ontology、来源 CSV/JSON、星核、星系、Product/runtime、registry、lock、state cache 或 governance contract。
- ZZ-PJ-X06 条件范围差异仍需独立来源复核。
- QI-04、QI-06、QI-16 的定义收窄仅为后续提案；canonical 定义没有在本轮改变。
- PI 审阅 v0.2 提案后，若需要新增共享语义原语或正式修改 canonical 定义/映射，应另开有界工作单并经过适用 Human Gate。
