# A0 批准后执行报告

状态：**A0 APPROVED / DETERMINISTIC P0 = 0 IN EFFECTIVE v0.3 VIEW**  
执行分支：`audit/decontamination-p0-v2`

## 1. Gate 结论已落盘

PI 已批准 Gate A0 的五项原则：

1. source_epistemic 与 normalization_epistemic 分离；
2. review_status 四级化；
3. 历史 GPT-only reviewed 降级为 MODEL_SELF_REVIEWED；
4. L1/L2 state operator 与 L3 projection 重新分层；
5. deterministic linter 成为强制 schema gate。

批准记录已写入 `DECISION_LOG.md` 的 D-014。

## 2. P0 修复结果

A0 最终确认 **61 条 deterministic schema violation**：

- 六十星系：58 条 `target_type=inference_rule`
- 六十星系：1 条 `target_type=evaluation`
- 六十星系：1 条 `valence=mixed`
- 六煞：1 条 `operator_type=time_scale_effect`

修复后，按 v0.3 effective view 重新检查：

> **P0 = 0**

注意：这里的“修复”只表示 schema 一致性恢复，不等于这些规则已经完成 source-span 或 normalization 语义核验。

## 3. 六十星系采用非破坏式修复

六十星系 canonical v0.1 共 2193 条。A0 不直接覆盖该大文件，而将它视为 immutable raw extraction。

新增：

- `knowledge/review/sixty_systems_review_v0.3.csv`
  - 2193/2193 条都有 v0.3 review metadata；
- `knowledge/migrations/a0_sixty_systems_schema_overrides_v0.1.csv`
  - 60 条受控 schema override；
  - 59 条 target_type repair；
  - 1 条 valence repair。

运行时/审计时：

~~~text
raw canonical
+ review metadata sidecar
+ controlled schema overrides
= effective v0.3 view
~~~

这样保留原始 extraction，可追踪每次修复，而不是把历史数据静默覆盖。

## 4. 全库 review-status 迁移

A0 已迁移：

| artifact | records | v0.3 review status |
|---|---:|---|
| 十四正曜 canonical | 430 | MODEL_SELF_REVIEWED |
| 六十星系 canonical metadata | 2193 | MODEL_SELF_REVIEWED |
| 辅佐八曜 | 103 | MODEL_SELF_REVIEWED |
| 六煞 | 81 | MODEL_SELF_REVIEWED |
| 四化 | 56 | MODEL_SELF_REVIEWED |
| 杂曜 | 73 | MODEL_SELF_REVIEWED |
| 六十星系派生 operator edges | 654 | MODEL_SELF_REVIEWED |

没有任何历史 GPT-only 记录被自动标记为 HUMAN_VERIFIED。

对于历史迁移记录：

- `source_span_verified=false`
- `normalization_verified=false`
- normalization 默认 `UNRESOLVED`

只有确定性的工程 schema repair 被标记为 `normalization_epistemic=IMPLEMENTATION` 并附 rationale。

## 5. P1 review queues 已建立

### 5.1 Atomicity

统一 heuristic 后有 **39 条**高风险原子性候选：

`validation/decontamination/P1_atomicity_queue_v0.1.csv`

这些候选只表示“需要回原文检查逻辑结构”，不表示源文错误或 hallucination。

当前机器预分类包括：

- SPLIT_OR_SET
- STRUCTURED_GATE_REQUIRED
- KEEP_COMPOSITE_DEFINITION
- CASE_LEVEL_KEEP
- SOURCE_REVIEW_REQUIRED

任何实际拆分仍须 source-span review 后进行。

### 5.2 L1/L2 -> L3 layer boundary

六十星系中有 **800 条**：

~~~text
target_type = outcome_descriptor
AND
operator in {enhance,weaken,transform,inhibit,activate}
~~~

已全部进入：

`validation/decontamination/P1_layer_boundary_queue_v0.1.csv`

这些记录需要逐步判断：

1. 真正的 latent/relational state change；
2. projection strength；
3. 直接 semantic output；

三者不得继续混写。

## 6. Linter 已升级

`src/audit_repository.py` 当前检查：

- controlled enum；
- duplicate ID；
- v0.3 epistemic fields；
- review provenance；
- source-span verification flag；
- normalization rationale；
- HUMAN_VERIFIED 与 reviewer_type 一致性；
- 六十星系 raw + sidecar + overrides 的 effective view；
- atomicity P1 heuristic；
- state/projection P1 boundary heuristic。

对应 regression tests 位于：

`tests/test_audit_repository.py`

## 7. 分支修复说明

初始审计分支 `audit/decontamination-p0` 曾尝试通过 GitHub contents API 一次性覆盖 2193 行六十星系 CSV；该大文件写入在分支上产生异常空内容。

因此该分支不再作为合并候选。

新的 `audit/decontamination-p0-v2` 从异常写入之前的安全提交重新建立，并改用：

> immutable raw canonical + review sidecar + migration override

避免再次对大 canonical 文件做破坏性覆盖。

## 8. A0 后下一阶段

接下来自动进入：

~~~text
P1 source-span review
-> atomicity 修复方案
-> layer-boundary 分层审计
-> ontology backward audit
-> G2/G3/G4/G5 差异报告
-> Gate A1（只提交真正需要改动冻结/候选理论的事项）
~~~

在 Gate A1 之前，不自动：

- 新增 primitive qi；
- 合并/删除现有 QI/QR；
- 重写十四正曜核心气核；
- 改变六十星系 principal mode；
- 修改 G1–G6 的冻结理论边界。
