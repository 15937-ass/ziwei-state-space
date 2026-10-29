# Product #908 — Manifestation Adapter Contract v0.2 Acceptance

## 1. Scope

This bounded Product unit hardens only the already accepted P1 Product-owned gaps **PG-001..PG-005**.

It does not reinterpret Knowledge, consume an unmerged Core checkpoint, populate production manifestation registries, promote KIB/K_manifest, authorize runtime, or add probability.

P2-only **PG-006 / PG-007** remain explicit follow-up pressure and are not silently folded into this work unit.

## 2. Design

The implementation adds a separate, versioned research/compatibility layer:

`src/product/manifestation_adapter_contract_v0_2.py`

The existing production-facing v0.1 ontology adapter and router remain unchanged.

### PG-001 — canonical review axes

`CanonicalReviewAxis` preserves both `state` and `value` for `output_kind` and `event_specificity`.

The adapter no longer needs to flatten a reviewed canonical axis into the coarser Product v0.1 vocabulary merely to retain it.

### PG-002 — provenance and lifecycle retention

The v0.2 envelopes retain:

- source refs;
- review provenance;
- mapping review refs;
- canonical identity/status;
- identity rationale;
- supersession lineage;
- ambiguity and unresolved notes.

This is retention only. It does not upgrade any item to executable or Product-consumable.

### PG-003 — external action prerequisite binding

`ActionPrerequisiteBinding` maps a source-explicit real-world prerequisite to the existing Product namespace:

`A_t.actions`

The binding mode is fixed to `EXTERNAL_EXPLICIT_ONLY`.

`chart_inference_allowed=false` is enforced by the dataclass contract, so a chart pattern cannot silently create an action fact.

### PG-004 — execution and negative boundaries

`ExecutionBoundaryV02` retains:

- canonical mapping status/approval;
- execution readiness;
- Knowledge executable/product-consumable flags;
- execution blockers;
- forbidden inferences;
- negative-boundary review refs.

The Product v0.2 envelope itself always keeps `runtime_authorized=false`.

### PG-005 — separate epistemics

`source_epistemic` and `normalization_epistemic` are separate first-class fields on both node and mapping envelopes.

The v0.2 contract deliberately has no single `evidence_tier` field that would collapse the two axes.

## 3. Production boundary

This work unit does **not** change:

- `product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json`;
- `product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json`;
- `src/product/manifestation_ontology.py`;
- `src/product/manifestation_router.py`.

Production ontology/mapping registries remain empty and fail-closed.

Probability remains `UNKNOWN`; predictive validity remains unclaimed.

## 4. Deterministic validation

`tests/test_product_manifestation_adapter_contract_v0_2.py` checks:

- canonical review axes are retained;
- provenance, identity and supersession survive the envelope;
- `勉强求变` binds only to `A_t.actions` and cannot be inferred from chart;
- unresolved semantics remain unresolved;
- negative boundaries and forbidden inferences remain first-class;
- source and normalization epistemics stay separate;
- serialization is deterministic;
- production registries remain empty.

## 5. Next Product step

After this unit is accepted, Product still must address the P2-specific interface pressure:

- **PG-006** structured OR / cross-palace condition contract;
- **PG-007** DECADE_YEAR temporal-layer binding.

Those should be a separate bounded Product unit before a formal P3 crosswalk freeze is claimed.
