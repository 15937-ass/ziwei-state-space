# Zhongzhou Knowledge Base Schema v0.1

## 1. Rule object

在 Rule Schema v0.2 基础上增加：

- `rule_family`
- `applicability_scope`
- `prerequisite_rule_ids`
- `excludes_rule_ids`
- `conflicts_with_rule_ids`
- `overrides_rule_ids`
- `derived_operator_id`
- `source_case_ids`
- `coverage_unit_id`

## 2. Coverage unit

用于判断“有没有抽完”：

~~~yaml
coverage_unit_id: ZZ-UP-STAR-TY-001
source_id: SRC-ZZ-002
chapter: 十四正曜
section: 太阳
page_start: 9
page_end: 10
status: not_started | extracting | reviewed | complete
rule_count: 0
case_count: 0
unresolved_count: 0
review_version: null
~~~

知识库的“完整”必须依赖 coverage unit，而不能只看规则总数。

## 3. Inference edge

~~~yaml
edge_id: INF-0001
from:
  type: rule
  id: ZZ-TY-016
to:
  type: latent_state
  id: QI-01
relation: modifies
condition:
  - 太阳过强
effect:
  type: compensation_required
provenance:
  - SRC-ZZ-002:p9
~~~

## 4. Conflict object

~~~yaml
conflict_id: CF-0001
rules:
  - RULE-A
  - RULE-B
type: direct | conditional | terminology | school_version | OCR
status: open | resolved_by_scope | unresolved
resolution: null
human_required: false
~~~

## 5. Case object

~~~yaml
case_id: CASE-ZZ-001
source:
  source_id: SRC-ZZ-003
  location: 财帛宫章
input_structure:
  natal: {}
  temporal: {}
expected_reasoning:
  - RULE-X
  - RULE-Y
expected_semantic_output:
  - 财务资源变化
purpose:
  - tests_state_dependent_reaction
status: reviewed
~~~

## 6. Inference template

~~~yaml
template_id: TEMP-NATAL-TEMPORAL-REACTION
inputs:
  - natal_essence
  - temporal_input
  - active_mode
  - palace_graph
steps:
  - collect_applicable_rules
  - resolve_scope
  - apply_modifier_operators
  - compute_mode_constraints
  - project_to_palace_semantics
outputs:
  - semantic_state
  - provenance_chain
  - unresolved_conflicts
~~~

## 7. Epistemic requirements

每个 inference conclusion 必须输出：

- `source_supported`
- `formalization_supported`
- `hypothesis_used`
- `uncertainty`
- `conflicts`

LLM 不允许生成没有证据链的“中州派结论”。
