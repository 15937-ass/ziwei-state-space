# QI/QR PI 决策包验证记录 v0.1

状态：PROPOSAL_ONLY_NOT_CANONICAL  
Issue：[#735](https://github.com/15937-ass/ziwei-state-space/issues/735)  
Draft PR：[#736](https://github.com/15937-ass/ziwei-state-space/pull/736)

## 1. 基线与范围

- 仓库：15937-ass/ziwei-state-space
- 目标分支：main
- 工作分支：knowledge/core-735-qi-qr-pi-decision-package
- PR 创建时 GitHub 返回的 base SHA：70dff227581a95fcb4c34342892676b9e1c7a300
- PR 创建时 GitHub 返回的 head SHA：56275575ac865ce5e93fe104f413186a7d5ad945
- 随后修正测试仓库根目录定位后的 head commit：90508484e4bf3565aa56a05f27bbe2075adc23e0
- 本记录更新后，PR head 会再推进一次；最终 exact head 以 PR #736 的实时元数据为准，必须在该 head 上读取 CI 结果。

文件清单：
- knowledge/core/qi-qr-overlap-audit/QI_QR_OVERLAP_PI_DECISION_PACKAGE_v0.1.md
- knowledge/core/wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.2.md
- tests/test_knowledge_core_qi_qr_pi_decision_package.py
- 本验证记录

若 main 继续移动，必须按仓库 exact-head 规则重新同步并验证，不能复用旧 head 的绿灯。

## 2. 覆盖检查

- 八组覆盖：测试检查 OVERLAP-01 至 OVERLAP-08 恰好各一次。
- 候选保护：测试检查 QI-17-CAND / QI-18-CAND 不正式化。
- 来源差异保护：测试检查 ZZ-PJ-X06 的条件差异继续标记未解决，且不在本包改写。
- 契约边界：测试检查 Option C 三轴与 QI/QR 映射审查分离，并保留 UNKNOWN、MISSING、CONFLICT、NOT_APPLICABLE 区分。
- canonical/产品保护：测试检查本包仅为提案，不授权 canonical ontology 或 Product adapter 修改。
- 测试路径修正：测试以 parents[1] 定位仓库根目录，避免将仓库父目录误当作根目录。

## 3. 外部方法论参考

本包链接 Noy & McGuinness 的 Ontology Development 101、W3C SKOS、Cronbach & Meehl 的构念效度论文、Campbell & Fiske 的区分效度论文、House et al. 的社会支持结构/过程研究、Duckworth et al. 的毅力研究，以及 BFO 2020 资料。

这些资料仅用于方法论比较，不被用作紫微斗数现实预测有效性的证据。

## 4. 验证状态

- 文件写入：已完成（GitHub connector 返回了提交 SHA）。
- 本地 pytest：本执行环境未直接运行，不能宣称通过。
- PR exact-head CI：待读取 PR #736 当前 head 对应的 GitHub Actions 检查结果。
- 生产/正式语义变更：无；本工作只新增非 canonical 提案、测试和验证说明。
- 合并状态：未合并；PR 应保持 Draft，直到当前 exact head 的要求检查通过并完成 PI 审阅。

## 5. 限制与后续

- 本轮不证明八组维度正交或冗余。
- 本轮不修改 canonical ontology、来源 CSV/JSON、星核、星系、Product/runtime、registry、lock、state cache 或 governance contract。
- ZZ-PJ-X06 条件范围差异仍需独立来源复核。
- QI-04、QI-06、QI-16 的定义收窄仅为后续提案；canonical 定义没有在本轮改变。
- PI 审阅 v0.2 提案后，若需要新增共享语义原语或正式修改 canonical 定义/映射，应另开有界工作单并经过适用 Human Gate。
