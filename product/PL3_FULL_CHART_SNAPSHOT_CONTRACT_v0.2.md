# PL3 Full-Chart Snapshot Contract v0.2

Status: **PRODUCT INPUT CONTRACT — STRUCTURAL VALIDATION ONLY**

## Purpose

Career inference accepts the PL1 full-exporter snapshot with `schema_version = "0.2"`. This contract validates the shape and provenance of the input before the Product loads any natal provider or builds an inference profile.

Machine-readable schema: `product/PL3_FULL_CHART_SNAPSHOT_SCHEMA_v0.2.json`  
Runtime validator: `src/product/full_chart_snapshot_contract.py`

The Python validator is the dependency-free runtime gate. Its tests pin the key requirements in the JSON Schema so the two representations do not silently drift.

## Required top-level contract

- `schema_version` must be exactly the string `"0.2"`.
- `engine` must provide non-empty `name`, `version`, `source_revision`, and `adapter_version`.
- `input` must be an object.
- `natal.palaces` must map exactly the twelve earthly branches to palace objects. Each palace must provide `name`, `stem`, `branch`, `is_body_palace`, `major_stars`, `minor_stars`, and `adjective_stars`. The embedded branch must match its mapping key.
- Every natal star object must preserve the PL1 v0.2 fields `name`, `type`, `brightness`, `mutagen`, and `scope`; nullable metadata stays null and is never guessed.
- `temporal` must be a non-empty array. Each item must have a unique non-empty `target.target_id`, a valid target date, an integer time index, a matching top-level temporal solar date, a non-empty lunar date, and all six required scopes.
- Each of the six scopes must preserve the adapter-required fields `index`, `name`, `stem`, `branch`, `palace_names`, `mutagen`, `nominal_age`, and `stars`. Scope arrays and star groups are type-checked, and star-group count must equal `palace_names` length.
- `yearly_dec_stars` may be absent or null. If present, it must contain array fields `suiqian12` and `jiangqian12`.
- The requested `target_id` must exist exactly once in the temporal array.

## Failure behavior

The validator returns a deterministic ordered list of structural errors. `run_career_inference` raises a concise `ValueError` containing those errors **before loading a provider or building a profile**. The CLI uses the same service entry point and therefore the same contract.

The validator does not mutate the input, insert defaults, infer missing facts, coerce strings into numbers, select a replacement target, or repair a malformed snapshot. Unknown scope keys are rejected rather than silently ignored by the adapter.

## Explicit boundaries

This is a transport/schema contract, not a Zi Wei rule validator. It does not determine whether a chart engine is astrologically correct, whether two schools are equivalent, whether a rule is supported by the source, or whether a real-world prediction is accurate. It does not change canonical NATAL rule matching or the current `PARTIAL_TEMPORAL_REGISTRY_EMPTY` result when the production temporal reaction registry is empty.
