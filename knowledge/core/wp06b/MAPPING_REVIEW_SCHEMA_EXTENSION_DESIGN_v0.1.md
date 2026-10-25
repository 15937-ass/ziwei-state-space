# Mapping-review schema extension — design proposal v0.1

**Status:** `PROPOSAL_ONLY_NOT_IMPLEMENTATION`  
**Work unit:** `KB-CORE-MAPPING-REVIEW-SCHEMA-DESIGN-01`  
**Issue:** [#750](https://github.com/15937-ass/ziwei-state-space/issues/750)  
**Decision boundary:** PI authorized design work only on 2026-10-25. This document does not authorize shared-schema implementation.

## 1. Executive recommendation

Recommend **Option A: an optional, separate `mapping_review` envelope attached to one source-to-target candidate mapping**, rather than adding mapping-review fields directly to a canonical Rule object.

The envelope would hold target-specific rationale, source references, a typed evidence role, and a typed review disposition. The proposal also uses a small value-state wrapper so that an absent legacy envelope is not confused with an explicitly missing, unknown, conflicting, or not-applicable value.

This is a design recommendation only. All field names, enum values, examples, and shapes below are proposal-only. No shared schema or controlled vocabulary has been changed.

## 2. Current contract and demonstrated gap

The current Review / Epistemic Schema v0.3 separates:
- `source_epistemic`: directness of support for the literal source claim; values `EXPLICIT`, `INFERRED_FROM_SOURCE`, `UNRESOLVED_SOURCE`.
- `normalization_epistemic`: nature of the transformation into a computational representation; values `SOURCE_PRESERVING`, `INFERRED`, `IMPLEMENTATION`, `HYPOTHESIS`, `UNRESOLVED`.
- `review_status`: review provenance, with reviewer/time and verification companion fields.

The current KB Schema v0.3 supplies rule fields such as `target_type`, `operator`, `condition`, `provenance`, and `normalization_rationale`, and documents a reusable Conflict object. The bounded probe found no dedicated typed `evidence_role` or `mapping_disposition` field in either shared schema.

The design must add no new meaning to existing fields and must not repurpose Option C's `output_kind`, `event_specificity`, or `source_epistemic` axes.

## 3. Design principles

1. **One review record, one target-specific mapping hypothesis.** Two target candidates derived from one source need two distinct rationales. Reusing the same source reference is provenance reuse, not independent evidence.
2. **Review metadata is not a canonical decision.** A disposition must not imply canonical approval, a formal ontology ID, accepted mapping status, or Product consumer readiness.
3. **Source fidelity before normalization.** Preserve alternatives, condition gates, modality, ordering, and unresolved source discrepancies. Never convert source “OR” to “AND” merely to fit a record.
4. **Keep epistemic dimensions independent.** Mapping disposition is not source epistemic status, normalization epistemic status, or review provenance.
5. **Additive and fail-closed.** Existing records without a review envelope remain valid and are treated as not yet assessed by this proposed contract. Do not auto-migrate them to a guessed value.
6. **Proposal-only until a separate Human Gate.** No production schema edits, vocabularies, canonical rows, or consumers are authorized by this work unit.

## 4. Alternative shapes

### Option A — separate per-target `mapping_review` envelope (recommended)

Attach an optional review envelope to a candidate mapping artifact. The Rule object remains unchanged. The envelope carries the review's target, provenance, rationale, evidence role, and research disposition.

**Advantages**
- Clear boundary between source rule semantics and a reviewer's mapping hypothesis.
- Supports different rationales for different targets derived from the same source.
- Optional/additive for legacy data; review metadata can be revised without rewriting source truth.
- Makes the non-canonical status visible at the object boundary.

**Trade-offs**
- A consumer needs an explicit join from the review record to its source and candidate target.
- If the repository later needs machine queries for every semantic role slot, the minimal envelope may not be sufficient.

### Option B — add fields directly to the existing Rule object

Add `evidence_role`, `mapping_disposition`, and rationale/provenance extensions to the current Rule row.

**Advantages**
- Fewer joins for simple consumers.
- May be easier to serialize in existing rule files.

**Trade-offs**
- Risks treating a source rule as if it had one settled target, although one source can support multiple competing target candidates.
- Encourages review lifecycle metadata to be mistaken for canonical rule semantics.
- Can overwrite or collapse target-specific rationales when a source maps to multiple targets.
- Couples shared rule schema changes to review workflow and increases migration risk.

**Decision:** prefer Option A for design purposes. Option B should be reconsidered only if an actual consumer requirement demonstrates that the separate envelope is materially worse.

## 5. Proposed envelope shape (illustrative only)

The following is **not an accepted schema**, does not define formal IDs, and must not be copied into canonical data as if approved.

```yaml
mapping_review:
  review_record_id: "MREV-PROBE-001"  # proposal example only
  source_refs:
    - "SRC-PROBE-001"                # provenance reference; not an evidence count
  target_ref: "QI-15-CAND"            # candidate label; not a formal ontology ID
  rationale: "Target-specific explanation; preserve alternatives and conditions."
  evidence_role:
    state: KNOWN
    value: external_modifier
    conflict_ref: null
  mapping_disposition:
    state: KNOWN
    value: supported_candidate
    conflict_ref: null
```

### 5.1 Candidate `evidence_role` vocabulary

These are candidate values for PI review, not approved controlled values:

| Candidate value | Intended distinction | Important non-equivalence |
|---|---|---|
| `direct_state` | Evidence describes the state itself | Not the same as a downstream projection |
| `state_change` | Evidence describes a change in state | Does not itself assert the cause or operator |
| `external_modifier` | An external condition modifies a state or result | Not necessarily an interaction |
| `interaction` | Two or more states/operators interact | Does not assume additivity |
| `resource_existence` | A resource exists | Does not mean it is available |
| `resource_availability` | A resource is available under stated conditions | Does not mean support was realized |
| `realized_support` | Support was actually provided or realized | Not inferred from existence or availability alone |
| `projection_outcome` | Evidence describes a projected semantic/event outcome | Must not be promoted to direct-state evidence |

**Cardinality proposal:** one primary role per review record. If one source-target candidate genuinely plays multiple roles, use multiple linked review records or a later explicitly approved multi-role design; do not silently accept an untyped list. PI must decide whether this single-role rule is appropriate.

### 5.2 Candidate `mapping_disposition` vocabulary

These values describe research/review handling of a candidate, not canonical acceptance:

| Candidate value | Proposed meaning | Explicitly does not mean |
|---|---|---|
| `candidate_only` | Candidate recorded; no sufficient adjudication yet | Accepted mapping |
| `needs_review` | More source, school-version, or human review is needed | Source claim is false |
| `supported_candidate` | Current review finds the target hypothesis supported enough to retain as a candidate | Canonical approval, formal ID, or Product readiness |
| `not_supported_for_target` | Current evidence does not support this target under the stated scope | The source claim itself is invalid |
| `superseded` | A newer review record replaces this candidate record | Automatic deletion of historical provenance |

No value named `accepted`, `canonical`, or `product_ready` is proposed. Any transition to accepted formal mapping or Product consumption must remain in separate approval workflows.

### 5.3 Value-state wrapper and uncertainty

Candidate wrapper states: `KNOWN`, `UNKNOWN`, `MISSING`, `CONFLICT`, `NOT_APPLICABLE`. These are proposal-only metadata states, not additions to `review_status` or any existing epistemic enum.

- `KNOWN`: `value` is present and belongs to the proposed controlled vocabulary.
- `UNKNOWN`: the field was considered but its value genuinely cannot be determined.
- `MISSING`: the review process expected a value but the value was not supplied.
- `CONFLICT`: contradictory candidate values exist; `conflict_ref` must point to an existing Conflict object and resolution must remain unresolved until properly adjudicated.
- `NOT_APPLICABLE`: the field does not apply to this candidate for a stated reason.

Validation proposal:
- `state=KNOWN` requires a non-null `value` and null/absent `conflict_ref`.
- `state=CONFLICT` requires null `value` and a valid `conflict_ref`.
- Other non-known states require null `value`; any rationale for `MISSING` or `NOT_APPLICABLE` should be recorded in the review rationale or a future approved explanation field.
- An absent `mapping_review` envelope on a legacy row means **not yet reviewed under this contract**, not `MISSING`.
- Never collapse UNKNOWN, MISSING, CONFLICT, and NOT_APPLICABLE into one null or one `review_status` value.

PI must decide whether repeating this wrapper for both fields is worth the extra complexity, or whether only `evidence_role` needs it in the first version.

## 6. QI-15 and QR-04 requirements

### QI-15 role decomposition

The minimum proposed `evidence_role` distinguishes `state_change`, `external_modifier`, and `interaction`. It does **not** yet provide typed slots for bearer/agent, affected target, and condition. Under Option A v0.1 these details remain in target-specific rationale and source-preserving condition/provenance notes.

A richer alternative could add a proposal-only `role_bindings` object with separate bearer/agent, affected target, condition references, and effect kind. That would enable machine filtering but introduces further controlled vocabularies and identity questions. This proposal recommends deferring that extension until a concrete consumer/query requirement is shown. PI should explicitly approve or reject that deferral.

### QR-04 resource distinctions

The proposed evidence roles separate resource existence, availability, and realized support. They must not be inferred from one another. A source that says a resource exists does not prove that it is available; availability does not prove that support was actually realized. If a future consumer needs typed resource state separate from evidence role, that requires a separate design decision.

## 7. Compatibility, migration, validation, and rollback

### Compatibility
- The proposed envelope is optional and additive. Existing Rule objects remain unchanged.
- Readers unaware of `mapping_review` can ignore it; readers that need candidate adjudication must explicitly opt into the new review contract.
- The proposed envelope must not be required for all historical rows as a condition of basic schema validity.

### Migration
- No bulk migration is recommended.
- Create an envelope only when a reviewer has sufficient source/target evidence to populate it.
- Do not infer `evidence_role`, `mapping_disposition`, or review states from legacy `status`, `epistemic_type`, `source_epistemic`, or `normalization_epistemic`.
- Preserve old rows unchanged; absent envelope means not yet assessed under this proposal.

### Validation and failure behavior
1. Each envelope refers to one candidate target and at least one source provenance reference.
2. Target-specific rationales must differ when separate targets require different reasoning; the same source reference is not counted as multiple independent pieces of evidence.
3. Controlled values must be members of the approved enum once and only once a separate Human Gate approves them.
4. Source alternatives, condition gates, modality, and ordering must be preserved. Unresolved contradictions remain conflicts.
5. `source_epistemic`, `normalization_epistemic`, `review_status`, and Option C axes retain their current semantics.
6. Candidate disposition never grants canonical approval or Product readiness.
7. Invalid or contradictory metadata fails closed for any consumer that relies on it; it must not silently fall back to a stronger interpretation.

### Rollback
- Since this is proposal-only, no rollback operation is performed now.
- If a later implementation is approved, the design should permit consumers to ignore the optional envelope and allow the envelope to be withdrawn without deleting source records.
- A future implementation issue must define versioning, dual-read/write behavior if needed, rollback steps, and a migration rehearsal before any production change.

## 8. Human Gate decisions required before implementation

PI must explicitly decide:

1. Approve Option A's separate envelope or choose Option B's inline fields.
2. Approve, revise, or reject each proposed `evidence_role` value and its single-role cardinality.
3. Approve, revise, or reject the proposed `mapping_disposition` values and their research-only meaning.
4. Decide whether the value-state wrapper is needed for both fields or only one; approve the semantics of UNKNOWN/MISSING/CONFLICT/NOT_APPLICABLE.
5. Decide whether QI-15 role bindings and a separately typed QR-04 resource state are deferred or included in the first implementation.
6. Approve compatibility/migration/validation/rollback requirements.
7. Authorize a separate implementation work unit, if desired.

**Until these decisions are made, no shared schema, controlled vocabulary, canonical mapping, ontology, or Product/runtime implementation is authorized.**

## 9. Scope and evidence limits

This design is based on the current v0.3 schema texts and the synthetic probe report. The probe demonstrates a representational gap; it does not establish that any QI/QR mapping is semantically correct or empirically predictive. All IDs and examples in this document are illustrative placeholders only.
