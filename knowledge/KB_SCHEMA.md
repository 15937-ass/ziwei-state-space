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


## 9. Mapping-review envelope v0.1 (separate contract)

The machine-readable contract is `knowledge/core/wp06b/MAPPING_REVIEW_SCHEMA_v0.1.json`. It validates the **value** of an optional `mapping_review` object attached to a candidate mapping/review artifact. This is a separate, non-canonical review record, not a new field that changes the canonical Rule object v0.3. Legacy artifacts remain valid without the envelope; absence means **not yet reviewed under this contract**, not `MISSING`.

### 9.1 Record fields

| Field | Contract |
|---|---|
| `schema_version` | Must be the string `0.1`; version of this separate envelope, not the Rule Schema version. |
| `review_record_id` | Non-empty record identifier, unique within the collection of mapping-review records; not an ontology/formal target ID. |
| `source_refs` | One or more distinct provenance references to existing source/rule/span records. These references are provenance, **not an independent-evidence count**. A source may be referenced by separate target records without becoming multiple independent pieces of evidence. |
| `target_ref` | Exactly one non-empty target reference. A reference to a candidate or existing target does not itself establish canonical acceptance. |
| `rationale` | Non-empty, target-specific explanation of why this target is or is not supported under the stated scope. |
| `evidence_role` | One typed value-state wrapper describing the role of the evidence. It is not a source epistemic status or an Option C axis. |
| `mapping_disposition` | One typed value-state wrapper describing research/review handling of the candidate only. |

### 9.2 Candidate evidence-role values

The following controlled values are part of envelope v0.1:

| Value | Meaning and boundary |
|---|---|
| `direct_state` | Direct evidence about the target state. The associated target's existing `target_type` remains authoritative for whether the target is a `qi_state`, `relational_state`, `structural_relation`, or `outcome_descriptor`; this role does not replace target typing. |
| `state_change` | Evidence describes a change in state; it does not independently identify the cause/operator. |
| `external_modifier` | Evidence describes an external condition modifying a state/result; this does not necessarily imply an interaction. |
| `interaction` | Evidence describes two or more states/operators interacting without assuming additivity. |
| `resource_existence` | A resource exists; this does not prove it is available. |
| `resource_availability` | A resource is available under stated conditions; this does not prove support was realized. |
| `realized_support` | Support was actually provided or realized; it must not be inferred from existence or availability alone. |
| `projection_outcome` | Evidence describes a projected semantic/event outcome; it must not be promoted to direct-state evidence. |

Each record has exactly one primary evidence role. Multi-role arrays are invalid in v0.1. QI-15 bearer/agent, target, and condition bindings remain in existing source conditions/provenance and the target-specific rationale; a typed role-binding extension would require a separate design gate. QR-04 resource existence, availability, and realized support remain distinct roles.

### 9.3 Candidate mapping-disposition values

| Value | Meaning | Does not imply |
|---|---|---|
| `candidate_only` | Candidate is recorded but not sufficiently adjudicated. | Accepted mapping or formal ID. |
| `needs_review` | Further source, school-version, or human review is needed. | The source claim is false. |
| `supported_candidate` | Current review supports retaining this target hypothesis as a candidate. | Canonical approval, formal-ID approval, or Product readiness. |
| `not_supported_for_target` | Current evidence does not support this target under the stated scope. | The source claim itself is invalid. |
| `superseded` | This review record is no longer current because a newer review replaces it. | Deletion of historical provenance or automatic canonical acceptance. |

There is no `accepted`, `canonical`, or `product_ready` disposition. Canonical approval, formal mapping acceptance, and Product consumer readiness are independent gates outside this envelope.

### 9.4 Value-state semantics

Both `evidence_role` and `mapping_disposition` use the same wrapper:

- `KNOWN`: `value` is a member of the field's controlled vocabulary; `conflict_ref` must be absent or null.
- `UNKNOWN`: the field was considered but its value cannot currently be determined; `value` must be null.
- `MISSING`: the process expected a value but it was not supplied; `value` must be null.
- `CONFLICT`: contradictory values/interpretations remain; `value` must be null and `conflict_ref` must reference an existing Conflict object. The JSON Schema and local shape validator check the reference's shape, not cross-file existence/resolution.
- `NOT_APPLICABLE`: the field does not apply in the stated context; `value` must be null.

For non-`CONFLICT` states, `conflict_ref` must be absent or null. The `value` key is explicit even when null. Do not collapse `UNKNOWN`, `MISSING`, `CONFLICT`, and `NOT_APPLICABLE` into one null or overload `review_status`.

### 9.5 Source fidelity, compatibility, and validation

- One record names exactly one target and one primary role. Multiple targets require separate records and separate target-specific rationales.
- Preserve source alternatives, OR/AND structure, modality, ordering, and condition gates in the referenced source/rule records. Never rewrite a source OR into AND to fit the envelope.
- Reusing a `source_ref` across different target records is allowed but is not independent evidence.
- The extension is optional and additive. No bulk migration is required; do not infer fields from legacy `status`, `epistemic_type`, `source_epistemic`, or `normalization_epistemic`.
- A consumer that elects to validate the envelope must fail closed on invalid records. The standard-library validator is `tools/knowledge_core_mapping_review_schema.py`; it checks record shape, field/value-state invariants, source-reference uniqueness, and duplicate review-record IDs within a collection.
- The extension does not alter `source_epistemic`, `normalization_epistemic`, `review_status`, `output_kind`, or `event_specificity`. It does not authorize source-row edits, canonical ontology/mapping changes, formal IDs, or Product/runtime consumption.
- Rollback is an additive-document/schema/test revert; no source-data migration or consumer rollback is required because no consumer is enabled.
