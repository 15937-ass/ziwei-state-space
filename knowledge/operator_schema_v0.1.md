# KB-WP04 Modifier / Operator Schema v0.1

目标：把辅佐、煞、化、杂曜从“吉凶星清单”重构为可执行条件算子。

每条规则至少包含：

- operator_rule_id
- source_id / source_location
- modifier
- modifier_class
- subject_scope
- condition
- operator_type
- target_state
- state_change
- valence
- time_scope
- palace_scope
- literal_claim
- normalized_claim
- epistemic_type_source
- status
- notes

operator_type 受控词表：
- enhance
- weaken
- transform
- gate
- pair_interaction
- structural_relation
- projection
- time_scale_effect

原则：
1. 不把吉曜=+1、煞曜=-1。
2. 同一曜可在不同星系中产生相反作用。
3. 对星/单星、阴阳配合、同度/夹/会/冲必须显式编码。
4. 原文“他力/自力”作为作用来源分类，不直接视为吉凶。
5. 疾病、事故、婚恋等只保留 traditional_semantic_label。
