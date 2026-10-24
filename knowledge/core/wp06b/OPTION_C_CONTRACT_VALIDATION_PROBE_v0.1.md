# Option C contract validation probe v0.1

Status: `PROBE_ONLY_NOT_CANONICAL`  
Work unit: `KB-CORE-QIQR-OPTION-C-CONTRACT-VALIDATION-PROBE-01`  
Issue: [#747](https://github.com/15937-ass/ziwei-state-space/issues/747)  
Inputs: `knowledge/REVIEW_SCHEMA_v0.3.md`, `knowledge/KB_SCHEMA.md`, and the PI-approved `OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.2.md`.

## Purpose and method

This is a small synthetic representability probe, not a source adjudication and not a production schema migration. The fixture uses only `PROBE-*` IDs and explicitly says its source sentence is not a real quotation. It tests which requirements can be represented with existing typed fields, which require a non-canonical review envelope, and which reveal a concrete typed-schema gap.

## Supported by existing typed fields / Non-canonical review-envelope only / Typed-schema gap

## Capability matrix

| Requirement | Existing typed support | Probe result |
|---|---|---|
| Source support and normalization epistemic state | `source_epistemic`, `normalization_epistemic` with the v0.3 enums | Supported |
| Review provenance | `review_status`, reviewer identity/time, source-span and normalization verification fields | Supported |
| Rule type and operation | `target_type`, `operator`, `condition`, `provenance`, `normalization_rationale` in KB schema | Supported for existing meanings |
| One rationale per target mapping | `normalization_rationale` can hold a rationale, but the shared rule schema does not itself define a target-mapping review record | Requires a per-target non-canonical review envelope to preserve atomicity |
| Explicit typed evidence role | No `evidence_role` field in current Review Schema v0.3 or KB Schema v0.3 | **Typed-schema gap** |
| Explicit typed mapping disposition | No `mapping_disposition` field in current Review Schema v0.3 or KB Schema v0.3 | **Typed-schema gap** |
| QI-15 bearer/agent, target, condition and effect kind | Existing `target_type`, `operator`, and `condition` carry general rule semantics; they do not type all four role slots independently | Non-canonical review-envelope only; typed-role gap if machine filtering is required |
| QR-04 resource existence / availability / realized support | Can be explained in rationale/condition text, but no dedicated typed distinction is defined by these two schemas | Non-canonical review-envelope only; typed-role gap if machine filtering is required |
| Preserve source “OR” alternatives | `condition` can retain the source wording as text; the current schemas do not define a dedicated Boolean-alternative structure | Text fidelity supported; structured alternatives remain a possible future gap |
| UNKNOWN / MISSING / CONFLICT / NOT_APPLICABLE | Conflict object supports open/resolved/unresolved conflict handling; the four states are not one interchangeable review status enum | Keep them distinct in the non-canonical envelope; do not overload `review_status` |
| Canonical approval and Product readiness | Neither is implied by review/epistemic fields | Must remain separate approval/consumer gates outside the source epistemic fields |
| QI-17-CAND / QI-18-CAND | Current PI decision package keeps both candidate-only | Supported as a governance boundary; no formal IDs or accepted mappings in this probe |

## Minimal proposal-only schema diff candidate

The probe confirms a concrete gap for machine-readable target-mapping review metadata. If a future PI/Human Gate authorizes a shared contract extension, the smallest candidate is a **separate per-target mapping-review record**, not new values in Option C's three axes:

```yaml
mapping_review:
  source_refs: [PROBE-SRC-001]        # source provenance, not independent evidence count
  target_ref: QI-15-PROBE             # candidate target reference only
  rationale: "target-specific reason"
  evidence_role: "external_modifier"  # proposed typed field; controlled vocabulary TBD
  disposition: "candidate_only"       # separate from canonical approval
```

This is a proposal illustration only. `evidence_role` and `disposition` are **not** approved shared fields or controlled values. Canonical approval and Product consumer readiness remain separate gates and must not be inferred from `disposition`. QI-15 role slots and QR-04 resource states may need further vocabulary design only if a concrete consumer requirement demonstrates that prose-only envelope metadata is insufficient.

## Human Gate / stop condition

- No shared schema file was changed.
- No controlled vocabulary, canonical ontology, source row, accepted mapping, formal ID, Product adapter/registry/KIB lock/runtime, or consumption permission was changed.
- The typed-schema gap is documented, not implemented. Any actual shared-schema addition requires a separate PI/Human Gate and its own compatibility, migration, missing-value, validation, and rollback plan.
- The fixture is synthetic. It does not establish that any QI/QR mapping is correct, concepts are orthogonal, or Zi Wei Dou Shu has empirical predictive validity.

## Acceptance and next step

The full exact-head quality gate must pass, including pytest, Product JS adapter checks, deterministic P0 gate, Repository Governance v1, and Core write-set validation. If this report is accepted, the next decision is whether to authorize a separate schema-design Human Gate; do not automatically implement the proposed fields.
