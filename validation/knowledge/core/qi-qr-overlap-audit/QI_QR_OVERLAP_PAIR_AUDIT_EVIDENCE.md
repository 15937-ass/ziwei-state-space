# QI/QR 重叠对审计 — 验收证据

状态：`PROPOSAL_ONLY_NOT_CANONICAL`

- Issue：[#731](https://github.com/15937-ass/ziwei-state-space/issues/731)
- 工作单元：`KB-CORE-QIQR-OVERLAP-PAIR-AUDIT-01`
- Activation main：`46dc68d0fcf9ccc99c74b8f7088050c483130014`
- Branch：`knowledge/core-731-qi-qr-overlap-pair-audit`
- 范围：8 组已登记的 QI/QR 重叠对。
- 来源输入：当前 ontology/star cores/star systems、14-star matrix v0.1、两批 DIRECT_STAR source-first review。
- 已明确保留的限制：不修改 canonical ontology；不接受映射；不将候选维度升格；不授权 Product consumption；不宣称维度正交、完备或经验有效。
- 特殊守门项：`ZZ-PJ-X06` 的 canonical 条件比已核验源文更具体；本工作单记录该差异但不修订规则。

## 静态覆盖

- Pair rows：8；unique pair IDs：8。
- Pair order matches Issue #731 exactly.
- Every row has current definitions, evidence rule IDs, source locations, a distinction hypothesis, counterexample/limitation, research disposition and unresolved question.
- CSV and JSON preserve `normalization_epistemic=UNRESOLVED`, `PROPOSAL_ONLY_NOT_CANONICAL`, `canonicalization_authorized=false`, and `product_consumption_authorized=false`.

## Exact-head validation

An earlier exact-head gate passed on `77d80c4b6294adba693c05773f75e724c78415a5` in run #40057306308. While that run was green, `main` advanced to `3fe08830887b964a82e954c362d8aaaa127265ae`; therefore the prior result is historical, not final merge authorization. This branch is being replayed onto the newer main, and this evidence update creates a new head that must pass a fresh exact-head gate. The final head, base, workflow URL and actual results will be recorded in live Issue #731 / PR. Do not rely on a stale green check. This evidence file will not be edited after the final exact-head gate passes.

## Limitations

The audit distinguishes current ontology definitions and source-supported examples but does not establish numerical orthogonality, semantic completeness, empirical predictive validity, or authorization to change canonical QI/QR definitions. The candidate pair `QI-17-CAND/QI-18-CAND` remains candidate-only.
