# QI/QR PI 决策包验证记录 v0.1

状态：PROPOSAL_ONLY_NOT_CANONICAL  
Issue：[#735](https://github.com/15937-ass/ziwei-state-space/issues/735)  
Draft PR：[#736](https://github.com/15937-ass/ziwei-state-space/pull/736)

## 1. 基线与范围

- 仓库：15937-ass/ziwei-state-space
- 目标分支：main
- 工作分支：knowledge/core-735-qi-qr-pi-decision-package
- PR 创建时 GitHub 返回的 base SHA：70dff227581a95fcb4c34342892676b9e1c7a300
- PR 创建时的初始 head SHA：56275575ac865ce5e93fe104f413186a7d5ad945
- 测试路径修正 commit：90508484e4bf3565aa56a05f27bbe2075adc23e0
- 最小 CORE_STATE 恢复缓存同步 commit：b336b29cfd3b2de836badef3edd6ba84fb891288
- 测试加入恢复缓存断言的 commit：901edae22c4c06c2b6fcb192ffb97d99e60ef501
- 测试断言与契约非目标措辞对齐的 commit：72021033c02e5e88e4d1a0ce1e758e81a38e26ac
- 本记录更新会继续推进 PR head；最终 exact head 以 PR #736 实时元数据为准，必须在该 head 上读取 CI 结果。

文件清单：
- knowledge/core/qi-qr-overlap-audit/QI_QR_OVERLAP_PI_DECISION_PACKAGE_v0.1.md
- knowledge/core/wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.2.md
- tests/test_knowledge_core_qi_qr_pi_decision_package.py
- knowledge/states/CORE_STATE.yaml（仅按 Recovery Precedence v1 对活动 Issue/branch/PR 做最小恢复缓存同步）
- 本验证记录

若 main 继续移动，必须按仓库 exact-head 规则重新同步并验证，不能复用旧 head 的绿灯。

## 2. 覆盖检查

- 八组覆盖：测试检查 OVERLAP-01 至 OVERLAP-08 恰好各一次。
- 候选保护：测试检查 QI-17-CAND / QI-18-CAND 不正式化。
- 来源差异保护：测试检查 ZZ-PJ-X06 的条件差异继续标记未解决，且不在本包改写。
- 契约边界：测试检查 Option C 三轴与 QI/QR 映射审查分离，并保留 UNKNOWN、MISSING、CONFLICT、NOT_APPLICABLE 区分。
- canonical/产品保护：测试检查本包仅为提案，不授权 canonical ontology 或 Product adapter 修改。
- 恢复缓存一致性：测试检查 CORE_STATE.yaml 指向 Issue #735、工作分支和 PR #736。

## 3. 外部方法论参考

本包链接 Noy & McGuinness 的 Ontology Development 101、W3C SKOS、Cronbach & Meehl 的构念效度论文、Campbell & Fiske 的区分效度论文、House et al. 的社会支持结构/过程研究、Duckworth et al. 的毅力研究，以及 BFO 2020 资料。

这些资料仅用于方法论比较，不被用作紫微斗数现实预测有效性的证据。

## 4. 验证状态

- 文件写入：已完成（GitHub connector 返回了提交 SHA）。
- 本地 pytest：本执行环境未直接运行，不能宣称通过。
- PR exact-head CI：待读取 PR #736 当前 head 对应的 GitHub Actions 结果。
- 生产/正式语义变更：无；本工作只新增非 canonical 提案、测试和验证说明，并对 CORE_STATE.yaml 做了治理要求的最小执行状态同步。
- 合并状态：未合并；PR 应保持 Draft，直到当前 exact head 的要求检查通过并完成 PI 审阅。

## 5. 限制与后续

- 本轮不证明八组维度正交或冗余。
- 本轮不修改 canonical ontology、来源 CSV/JSON、星核、星系、Product/runtime、registry、lock 或 governance contract。
- ZZ-PJ-X06 条件范围差异仍需独立来源复核。
- QI-04、QI-06、QI-16 的定义收窄仅为后续提案；canonical 定义没有在本轮改变。
- PI 审阅 v0.2 提案后，若需要新增共享语义原语或正式修改 canonical 定义/映射，应另开有界工作单并经过适用 Human Gate。


## Rebased replacement PR (2026-10-24)
- The Product-owned historical snapshot test fix was merged at `5a7be5651f1682fe1c5c039f99d77cb1852d9ed3` after all Repository Quality Gate checks passed.
- Stale Draft PR #736 remains a historical branch and is superseded by [Draft PR #743](https://github.com/15937-ass/ziwei-state-space/pull/743).
- Replacement branch: `knowledge/core-735-qi-qr-pi-decision-package-r2`.
- Replacement PR base SHA: `5a7be5651f1682fe1c5c039f99d77cb1852d9ed3` (current main at branch creation).
- The active Core recovery cache and regression test now reference Issue #735, the replacement branch, and PR #743.
- All proposal artifacts remain `PROPOSAL_ONLY_NOT_CANONICAL`; this rebasing step does not authorize canonical ontology or Product/runtime changes.
- Exact-head validation is pending; do not merge before all required checks pass.
