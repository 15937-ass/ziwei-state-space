# Option C metadata-contract proposal — execution evidence

- Issue: #709
- Work unit: `KB-WP06B-OPTION-C-METADATA-CONTRACT-PROPOSAL-01`
- Branch: `knowledge/core-709-option-c-metadata-contract-proposal`
- Activation main/base: `cdc4fce773ea5133f2210c6ea8e87022678fff2f`
- Status: proposal-only; awaiting PI review of detailed values and status semantics.
- Accepted architecture decision: Option C direction-only, PR #704 merged at `cdc4fce773ea5133f2210c6ea8e87022678fff2f`.
- Source-schema authority: `knowledge/REVIEW_SCHEMA_v0.3.md` (blob `38daee9b65390e79e5ba164faa19dfc459f6786b`) and `knowledge/KB_SCHEMA.md` (blob `06e26c90a0040fa607ae32a4bb5e5fa30ed3212b`).
- Product compatibility reference only: `product/PL3M_MANIFESTATION_ONTOLOGY_ADAPTER_ACCEPTANCE.md`; no Product files are changed.

## Main findings

- Reuse the existing `source_epistemic` enum: `EXPLICIT`, `INFERRED_FROM_SOURCE`, `UNRESOLVED_SOURCE`.
- Keep `normalization_epistemic` and `review_status` independent and unchanged.
- Accepted WP05 projection CSVs have no `source_epistemic` column; the accepted P07 readjudication JSON also has no separate `source_epistemic` field. The proposal therefore represents those values as MISSING rather than inferring them from `SOURCE_SPAN_VERIFIED` or `DIRECT_SOURCE_RECHECK_CONFIRMED`.
- The existing Product adapter has an `event_specificity` field, but its fixture values `ABSTRACT` and `SCENE_LEVEL` are test-only and do not establish a production vocabulary.
- The new `output_kind` values and `metadata_axis_status` wrapper are proposals only; they are not accepted schema or runtime values.

## Hard boundaries

- No source or palace record is modified.
- No canonical root/node IDs or production mappings are assigned.
- Product ontology and mapping registries remain empty; Product code, locks, and runtime permissions remain unchanged.
- All probability status remains `UNKNOWN`.
- The 36-record fixture and 5 synthetic controls are design checks, not random samples or empirical predictive-validity evidence.

## Validation

Pending final PR head: full repository pytest, Product JS adapter checks, deterministic P0 gate, Repository Governance v1, and exact-main/head validation. Do not treat earlier PR #704 validation as validation of this new proposal branch.
