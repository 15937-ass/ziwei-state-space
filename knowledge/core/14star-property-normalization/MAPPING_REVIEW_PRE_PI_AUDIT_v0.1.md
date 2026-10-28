# Mapping-review 预 PI 审计（PI处置后，2026-10-28）

## 完整性检查

- mapping-review记录：241；唯一ID：241。
- 候选性质：182；所有候选均关联到有效审核记录。
- canonical规则：430；未发现引用不存在的canonical规则ID。
- 目标引用：81种。
- 来源引用：428次使用、360个唯一来源引用。
- 被多个mapping-review记录复用的精确来源引用：59组，共涉及127次引用使用。复用不等于独立证据。
- evidence_role仍为UNKNOWN：1条，当前仅为MR-LZ-SYMBOLIC-ROLE-002。
- 候选性质中canonicalization_authorized=true为0；numeric_strength_assigned=true为0；normalization_epistemic全部为UNRESOLVED。

## Mapping-review处置

| 处置 | 数量 |
|---|---:|
| supported_candidate | 58 |
| candidate_only | 57 |
| needs_review | 100 |
| not_supported_for_target | 26 |
| 合计 | 241 |

## 四条原UNKNOWN记录的处置

1. `MR-TY-QI15-METHOD-RULE-005`：改为`NOT_APPLICABLE`。一般解释方法不直接扮演太阳专属性质证据；`not_supported_for_target`保持不变。
2. `MR-TT-SOURCE-MISMATCH-009`：改为`NOT_APPLICABLE`。来源已确认错配并继续隔离；`not_supported_for_target`保持不变。
3. `MR-LZ-L0-SOURCE-DISAGREEMENT-001`：证据角色改为`direct_state`，因为两份来源均直接陈述传统底座标签；来源值冲突仍未解决，不选定任一标签。
4. `MR-LZ-SYMBOLIC-ROLE-002`：继续`UNKNOWN`。现有枚举没有“传统象征标签”角色，强行归入直接状态或下游投影会误分类；当前目标不支持的处置保持不变。

## 来源范围审计

- 原始差异13项候选、26个rule ID已逐项审查。
- 12项候选、25个rule ID通过补入有依据的直接引用或缩窄候选范围得到处理。
- 只保留`EXP-WQ-06` / `ZZ-WQ-X06`一个有意不重复引用的重叠摘要；详见`MAPPING_REVIEW_CANDIDATE_SOURCE_SCOPE_AUDIT_v0.1.md`。
- `EXP-WQ-10`现在关联L3候选审核记录`MR-WQ-L3-FINANCIAL-ROLE-016`；原`MR-WQ-FINANCIAL-ROLE-002`继续拒绝QI-05映射。

## 不变更项

本审计不修改canonical规则、正式星核、QI本体、共享Schema、Product/runtime、KIB或消费者权限；不批准任何正式映射，不因重复来源引用增加权重。
