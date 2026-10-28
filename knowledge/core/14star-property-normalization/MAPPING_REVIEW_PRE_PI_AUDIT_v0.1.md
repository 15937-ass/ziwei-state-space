# Mapping-review 预 PI 审计（2026-10-28）

## 完整性检查

- mapping-review 记录：240；唯一 ID：240。
- 候选性质：182；所有 182 项均关联到现有 mapping-review 记录。
- canonical 规则：430；mapping-review 中未发现引用不存在的 canonical 规则 ID。
- 目标引用：81 种。
- 来源引用：412 次使用、356 个唯一来源引用。
- 被多个 mapping-review 记录复用的精确来源引用：47 组，共涉及 103 次引用。复用只表示同一来源定位被多个目标/论证引用，不应重复计为独立证据。
- 4 项 evidence_role 仍为 UNKNOWN，已单独列入待审清单。
- 候选性质中，canonicalization_authorized=true 为 0；numeric_strength_assigned=true 为 0；normalization_epistemic 全部为 UNRESOLVED。

## Mapping-review 处置

| 处置 | 数量 |
|---|---:|
| supported_candidate | 58 |
| candidate_only | 56 |
| needs_review | 100 |
| not_supported_for_target | 26 |
| 合计 | 240 |

## 仍需 PI 留意

1. 复用来源引用不得自动产生独立证据权重；跨目标复用必须按原文跨度、条件与目标层级分别审议。
2. `MR-TY-QI15-METHOD-RULE-005` 的 evidence_role 为 UNKNOWN，且处置为 `not_supported_for_target`：一般方法规则不能直接支撑太阳专属映射。
3. `MR-TT-SOURCE-MISMATCH-009` 的 evidence_role 为 UNKNOWN，且处置为 `not_supported_for_target`：与 `ZZ-TT-010` 来源错配问题保持一致，继续隔离。
4. `MR-LZ-L0-SOURCE-DISAGREEMENT-001` 的 evidence_role 为 UNKNOWN，处置为 `needs_review`：两份中州派来源存在传统五行标签差异，需保留来源归属，不推导 QI 数值。
5. `MR-LZ-SYMBOLIC-ROLE-002` 的 evidence_role 为 UNKNOWN，处置为 `not_supported_for_target`：传统象征标签不直接转为现代人格/关系变量。

## 不变更项

本审计不修改 canonical 规则、正式星核、QI 本体、共享 Schema、Product/runtime、KIB 或消费者权限；不批准任何候选映射，也不为重复来源引用增加权重。


## 详细复用清单

47组精确来源引用及其被引用的mapping-review记录已逐项列入 `MAPPING_REVIEW_SOURCE_REF_REUSE_AUDIT_v0.1.md`。清单仅用于去重和审议，不改变既有处置，也不增加证据权重。
