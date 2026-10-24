# QI/QR PI 决策包执行证据 v0.2

状态：PROPOSAL_ONLY_NOT_CANONICAL  
Issue：[#735](https://github.com/15937-ass/ziwei-state-space/issues/735)  
PR：[#743](https://github.com/15937-ass/ziwei-state-space/pull/743)，开放且未合并  
工作分支：`knowledge/core-735-qi-qr-pi-decision-package-r2`

## 1. 本次基线同步与工作身份

- 当前 main SHA：`57644d82366b8e2f612100546b78fe85d8609801`
- 同步前 main：`5a7be5651f1682fe1c5c039f99d77cb1852d9ed3`
- main 新增提交：P05 巨门来源优先审计与其执行状态缓存更新均已合入；Core 分支同步时以最新 main tree 为基础保留 Core 自有文件。
- 同步前 Core head：`26f38fc8adbb341aecfbcb10affa52a8e13d893e`
- 同步前该 head 的完整质量门：run [#40088465582](https://github.com/15937-ass/ziwei-state-space/actions/runs/40088465582)，结论 success；2,689 tests 与 132 subtests 通过，Product JS、确定性 P0 与 Repository Governance v1 均通过。
- 本次提交额外记录 PI 六项接受结果，并新增相应回归断言。因此同步后的新 head 必须重新运行完整质量门；上述旧 head 结果不代替新 head 验证。

## 2. 交付物清单

1. `knowledge/core/qi-qr-overlap-audit/QI_QR_OVERLAP_PI_DECISION_PACKAGE_v0.1.md`
2. `knowledge/core/wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.2.md`
3. `knowledge/states/CORE_STATE.yaml`（仅执行恢复缓存，指向 Issue #735、当前分支和 PR #743）
4. `tests/test_knowledge_core_qi_qr_pi_decision_package.py`
5. 本验证记录

## 3. 决策覆盖与边界

- 决策包逐对覆盖 OVERLAP-01 至 OVERLAP-08；测试要求八组各出现一次。
- 八组均记录当前登记名称/定义、来源/归一化边界与改变决策的条件。
- QI-17-CAND / QI-18-CAND 保持候选状态；不分配正式 ID，不接受 canonical mapping。
- ZZ-PJ-X06 条件差异继续标记为 unresolved；不把来源中的“或”改成更强的合取条件。
- Option C v0.2 仍是非 canonical 提案，不冻结生产 schema。
- PI 已接受六项设计输入，但只授权后续独立、有限范围的非 canonical 契约验证工作；没有授权 canonical ontology 修改、正式 mapping 接受、生产词表扩展或 Product/runtime 消费。

## 4. 契约复用与验收边界

- 保持 `output_kind`、`event_specificity`、`source_epistemic` 的既有语义与值域。
- 优先复用 `REVIEW_SCHEMA_v0.3`、`KB_SCHEMA` 的 `target_type`、`operator`、`condition`、`provenance`、`normalization_rationale`、`review_status` 与 Conflict object。
- 分开 source epistemic、normalization epistemic、review status、mapping disposition、canonical approval 与 Product consumer readiness。
- UNKNOWN、MISSING、CONFLICT、NOT_APPLICABLE 保持可区分。
- 不把共享规则 ID 当成独立证据，不把无共享规则 ID当成已证明正交；不引入无数据支持的分数、权重或概率。

## 5. 本次修改范围与限制

本次仅更新非 canonical 决策/契约文档、对应回归测试、验证记录与 Core 执行恢复缓存。未修改 `knowledge/qi_ontology.yaml`、`knowledge/star_cores.yaml`、`knowledge/star_systems.yaml`、canonical 来源行、Product adapter/registry/KIB lock/runtime 或消费权限。没有新增 schema 字段，也没有接受正式 mapping。

## 6. Exact-head validation follow-up

- Run #2529 on head `a72a24c9dd50ee8df6b6d7ce1edf9ae9478511e6` completed with 2,694 tests passed and 132 subtests passed, but one existing contract-phrase assertion failed.
- Failure: `test_contract_keeps_option_c_axes_separate_from_qi_qr_mapping_review` required the explicit wording “不塞入 Option C 三轴”. The semantic boundary was already described, but the exact compatibility phrase was absent.
- This patch restores the explicit wording in the PI-approved contract text; it does not weaken or remove the test. The corrected exact head must pass the full quality gate before merge.

## 7. 下一步

- 等待同步后新 head 的完整 repository-quality-gate 通过。
- PR #743 通过 PI 审议后只合并上述非 canonical 提案包。
- 关闭 Issue #735 后，另开一个 Core 工作单做有边界的非 canonical contract validation probe；Core WIP 仍为 1，不并行启动。
- 只有当该 probe 证明既有 schema 不足时，才提出最小 schema 差异，并另行经过 Human Gate。
