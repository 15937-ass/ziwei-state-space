# PL3 Inference Snapshot Contract v0.1

Status: **PRODUCT ENGINEERING CONTRACT**

## Purpose and boundary

This contract validates the normalized full-chart snapshot consumed by `run_career_inference` and the Product module CLI. It targets the PL1 full-export format with `schema_version=0.2` and both `natal` and `temporal` sections.

This is distinct from `NORMALIZED_CHART_SCHEMA_v0.1.md`, which describes the single natal `chart.palaces` format used by earlier differential-comparison stages. The full inference exporter is `tools/iztro_full_export.mjs` (or the corresponding Rust/Python adapter).

Validation is structural only. It does not infer missing stars, repair empty scopes, derive elapsed years, normalize source rules, or choose an interpretation.

## Required root fields

- `schema_version`: exactly `0.2`;
- `engine`: object with non-empty `name`, `version`, and `adapter_version`;
- `input`: object; adapter-specific input fields may vary;
- `natal.palaces`: object containing exactly twelve palace records;
- `temporal`: non-empty array of target snapshots.

## Natal palace contract

Each palace record must contain:
- `name`, `stem`, `branch`;
- `is_body_palace`;
- `major_stars`, `minor_stars`, and `adjective_stars` arrays.

Each natal star record must be an object with a non-empty `name`. Optional engine-specific star metadata is preserved.

## Temporal target contract

Each target item must contain:
- `target.target_id`: non-empty and globally unique within the snapshot;
- `target.solar_date`: non-empty text;
- `target.time_index`: integer or null;
- top-level `solar_date` and `lunar_date`: non-empty text;
- `scopes`: object containing all six scopes required by the existing adapter: `decadal`, `age`, `yearly`, `monthly`, `daily`, and `hourly`.

Each scope requires `index`, `name`, `stem`, `branch`, `palace_names`, `mutagen`, `nominal_age`, and `stars`. The `stars` groups must align with `palace_names`; every star entry must be an object with a non-empty `name`.

`yearly_dec_stars` may be null. When present, it must be an object containing array-valued `suiqian12` and `jiangqian12`.

## Target selection and errors

The caller must supply a target ID. The validator rejects missing or duplicate target IDs and does not silently select the first match. Missing scope objects, malformed arrays, unsupported schema versions, or missing engine provenance produce deterministic `ValueError` diagnostics before any provider is loaded.

The validator checks the selected target's six scopes, while enforcing unique, non-empty IDs across the temporal target list. It does not require unrelated target scopes to be fully materialized when they are not selected for the current run.

## Integration

`run_career_inference` validates the snapshot before loading the Career provider or production reaction registry. Python callers and the CLI therefore share the same input contract. A valid snapshot can still produce `PARTIAL_TEMPORAL_REGISTRY_EMPTY`; structural validity is not evidence of a temporal conclusion or real-world prediction accuracy.
