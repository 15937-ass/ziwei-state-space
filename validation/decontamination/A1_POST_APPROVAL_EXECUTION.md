# A1 批准后执行报告

状态：**A1 APPROVED / CORE REFIT APPLIED / P1 NORMALIZATION AUDIT CONTINUES**  
分支：`audit/decontamination-p0-v2`

## 1. Gate A1 已落盘

D-015 已记录以下批准事项：

1. 保留 G2 的 L0-L4 分层架构；
2. QI-16「目标导向性」正式升格为 L1；
3. 原 QI-17「持续意志/韧性」废止，拆分为：
   - QI-17-CAND：意志控制强度
   - QI-18-CAND：毅力/持续性
   - 恢复力/韧性：DERIVED_ONLY
4. QI-14 收窄为「信息/状态遮蔽—显露」；
5. 批准 G3-R：十四正曜气核按全文重拟合；
6. 当前所谓 structural observability 改称 observation-path support。

## 2. qi ontology v0.3

`knowledge/qi_ontology.yaml` 已升级至 v0.3。

主要变化：

- basis 从早期 200-rule pilot 改为当前 Phase-II corpus；
- QI-16 正式进入 L1；
- QI-14 与 QI-01 分离证据；
- QI-05 / QI-07 / QI-09 / QI-10 / QR-03 重建或净化 evidence；
- projection evidence 与 direct state evidence 分层；
- QI-17-CAND / QI-18-CAND 保持 provisional；
- 恢复力不再作为 primitive 候选。

当前 ontology 中引用的 157 个 rule id 均可在 canonical corpus 中解析，无 dangling evidence id。

## 3. 十四正曜 G3-R v0.2

`knowledge/star_cores.yaml` 已升级至 v0.2。

新的证据优先级：

~~~text
DIRECT_STAR
> SAME_STAR_MODIFIER
> SYSTEM_CONTEXT
> PROJECTION
~~~

本轮明确移除/降级：

- 天府使用武曲规则作为 intrinsic QI-15 证据；
- 太阴使用武曲规则作为 intrinsic QI-05 证据；
- 廉贞把六十星系性质直接冻结为单星 QI-11 core；
- 贪狼把紫贪星系性质直接冻结为贪狼 baseline；
- 天相把武曲天相 system-context 直接冻结为 intrinsic QI-15 / QR-02；
- 巨门表达优化同时被写入认知与表达两个 core；
- 太阴“收敛”被重复解释为 QI-14“遮蔽”。

自动 invariant scan 结果：

- DIRECT_STAR evidence subject mismatch = 0
- ontology dangling evidence id = 0
- quarantined ZZ-TT-010 出现在 ontology/core evidence = 0

## 4. QI-16 / 17 / 18

### QI-16

正式状态：

`A1_FORMAL_L1`

定义为目标导向性，不等于：

- 变化量；
- 开创强度；
- 行动强度；
- 成功概率；
- 吉凶。

### QI-17-CAND

意志控制强度：

> 在欲望、情绪、诱因或环境压力下维持自主约束与方向的能力。

### QI-18-CAND

毅力/持续性：

> 在时间、阻力、延迟或重复挫折下维持行动的持续程度。

二者继续做 disjointness test，不自动进入冻结核心向量。

## 5. G4 未被推翻

`knowledge/star_systems.yaml` 已同步 ontology feedback。

保留：

~~~text
base composition
+ interaction_delta
+ mode
+ context gates
~~~

没有发现必须推翻六十星系统一架构的 A1 级冲突。

principal mode 仍属于中尺度状态，不因 QI-16 升格而自动拆成 primitive。

## 6. G5 术语修复

`src/model_spec.py` 与 `theory/state_space_model.md` 已修改。

旧：

~~~text
STRUCTURALLY_OBSERVABLE
PARTIALLY_OBSERVABLE
STRUCTURALLY_AT_RISK
~~~

新：

~~~text
MULTI_PATH_SUPPORTED
SINGLE_PATH_SUPPORTED
NO_DIRECT_PATH
DERIVED_ONLY
~~~

正式名称：

`ObservationPathSupport`

保留 legacy alias 仅为兼容旧代码，但其返回值不再带控制理论 structural-observability claim。

## 7. 原子化迁移

39 条高风险 atomicity candidates 已建立：

`knowledge/logic/p1_atomicity_logic_v0.1.json`

当前：

- ANY_LITERAL_BRANCH：19
- EXPLICIT_AST：11
- DEFINITION_SET：3
- CASE_EVIDENCE_ONLY：4
- STRUCTURE_LITERAL：1
- DISABLED_SOURCE_MISMATCH：1

所有 11 条 EXPLICIT_AST 均已具有显式条件结构，无 MANUAL_AST_PENDING。

raw canonical 未被静默拆写。

## 8. L1/L2 -> L3 边界批审

800 条候选已完成 reproducible triage：

| class | count |
|---|---:|
| MIXED_STATE_AND_PROJECTION | 206 |
| LIKELY_L1_STATE | 142 |
| LIKELY_L2_RELATIONAL | 123 |
| LIKELY_L3_PROJECTION | 162 |
| UNRESOLVED | 167 |

注意：

> 这 800 条目前全部仍是 PENDING_SOURCE_SPAN_NORMALIZATION_REVIEW。

没有因为关键词分类而自动改 canonical。

已建立 16 个 deterministic review batches，每批 50 条：

`validation/decontamination/P1_layer_boundary_review_batches_v0.1.csv`

优先序：

1. mixed state/projection
2. likely L1
3. likely L2
4. likely L3 projection
5. unresolved

## 9. Rule engine 去污染

`src/rule_engine.py` 现在可以按以下顺序建立 effective rule：

~~~text
canonical
-> review metadata
-> source-review metadata
-> schema override
-> provenance override
-> quarantine filter
~~~

因此：

- raw extraction 可以保持 immutable；
- ZZ-TT-010 默认可被排除；
- ZZ-TX-003 的 provenance repair 可以在运行时应用；
- source-span verified 可以作为查询条件；
- trace 输出 source / normalization / review status。

## 10. 回归约束

新增或扩展：

- `tests/test_a1_invariants.py`
- `tests/test_rule_engine.py`
- `tests/test_model_spec.py`
- `tests/test_layer_boundary_audit.py`

当前确定性检查已验证：

- ontology evidence id 全部存在；
- DIRECT_STAR evidence 不跨 subject；
- 39 条 atomicity logic 全覆盖；
- explicit AST 无 pending；
- 800 条 boundary audit 全覆盖；
- ZZ-TT-010 不进入 ontology/core；
- 旧 STRUCTURALLY_OBSERVABLE 标签已从 model spec 移除。

## 11. 当前是否需要 Gate A2

**暂不需要。**

A1 的发现没有推翻：

- G2 分层；
- G4 六十星系统一架构；
- G5 原局本质 + 时序输入 + 状态依赖反应；
- 十二宫局部节点 + 稀疏图；
- 气 -> 模态 -> 投影链。

下一阶段可以继续自动执行 P1 normalization/source review。

只有出现以下情况才升级 Gate A2：

- 需要新增/删除已正式 primitive QI；
- 需要修改六十星系 principal mode 架构；
- 发现 G5 的 natal/temporal 分层与源文冲突；
- 大批 source-span review 表明某一正式 QI 无独立文本支持。

## 12. 自动继续路线

~~~text
LB-01 ... LB-16 source/normalization review
-> verified layer migrations
-> ontology/core regression
-> system-mode regression
-> WP04 remaining modifier gaps
-> WP05 palace full extraction
-> Gate A2 only if architecture-level conflict appears
~~~
