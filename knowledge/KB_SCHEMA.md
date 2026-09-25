# Zhongzhou Knowledge Base Schema v0.3

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

### 1.1 Controlled vocabularies

Phase-II rule files must use the following controlled values.

**target_type**
- `qi_state`
- `relational_state`
- `structural_relation`
- `outcome_descriptor`

**operator**
- `define`: establish identity/taxonomy
- `assert`: source states a property without directional modification
- `condition`: scope/condition constraint
- `enhance`: increase/strengthen an existing property
- `weaken`: decrease/attenuate an existing property
- `transform`: qualitatively change one property/mode into another
- `inhibit`: suppress activation without necessarily decreasing the underlying baseline
- `activate`: trigger a dormant/conditional property
- `compare`: source-grounded ordering or contrast
- `project`: map latent/relational state to an L3 semantic output
- `gate`: a condition determines whether another operator/mechanism is active
- `couple`: two or more states/operators interact without assuming additivity

**state_change**
- `none`
- `increase`
- `decrease`
- `transform`
- `nonlinear`

**valence**
- `favorable`
- `unfavorable`
- `context_dependent`
- `not_applicable`

Any new controlled value requires schema revision and must not silently appear in a CSV.

### 1.2 Source-language boundary

`evidence_text` in the GitHub knowledge base is a concise paraphrase/near-source note for traceability, not a wholesale reproduction of copyrighted source text. Full source PDFs remain outside the repository.

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

## 7. Epistemic and review requirements

Phase-II canonical/operator artifacts must additionally carry the v0.3 audit fields:

- `source_epistemic`: EXPLICIT | INFERRED_FROM_SOURCE | UNRESOLVED_SOURCE
- `normalization_epistemic`: SOURCE_PRESERVING | INFERRED | IMPLEMENTATION | HYPOTHESIS | UNRESOLVED
- `review_status`: MODEL_EXTRACTED | MODEL_SELF_REVIEWED | SOURCE_SPAN_VERIFIED | HUMAN_VERIFIED
- `reviewer_type`
- `reviewer_id`
- `reviewed_at`
- `source_span_verified`: true | false
- `normalization_verified`: true | false
- `normalization_rationale`

Legacy `epistemic_type_source` / `epistemic_type` and `status` fields may be retained temporarily for backwards compatibility, but they must not be interpreted as v0.3 source-span or human verification.

See `knowledge/REVIEW_SCHEMA_v0.3.md`.

## 8. Inference requirements

每个 inference conclusion 必须输出：

- `source_supported`
- `formalization_supported`
- `hypothesis_used`
- `uncertainty`
- `conflicts`

LLM 不允许生成没有证据链的“中州派结论”。
