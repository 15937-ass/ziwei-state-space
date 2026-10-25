# Product spatial-temporal experiment v0.2: natal coordinate probe

## Purpose

This is a bounded, TEST_ONLY follow-up to the first spatial-temporal engineering probe. It checks branch-indexed occupancy and permutation-matrix views against 11 pinned, engine-materialized natal charts. It also checks the project's existing Z12 offset constraints.

The input charts are not source-transcribed ground truth. The materialization artifact explicitly claims SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED, and its full_source_chart_equivalence_verified flag is false for all 11 cases. Only target-anchor identity was independently reconfirmed. This work therefore tests coordinate encoding, not full-chart correctness or predictive validity.

## Fixed inputs

- The 11-case artifact at product/expert_cases/wang_tingzhi/FULL_CHART_MATERIALIZATION_V0_1B.json.
- The branch order read from src/product/structure_primitives.py.
- The Z12 coordinate model in knowledge/relation/RELATION_SEMANTICS_v0.1.json.
- The pinned materializer's expected eligible case IDs.

The probe checks Git blob and SHA-256 pins before using the data. It orders palace records by the explicit earthly-branch order, never by the artifact's array order. Each occupancy row includes the palace-name identity token and the star objects from all three star fields.

## Reproduce

From the repository root:

    PYTHONPATH="$PWD" python -m product.experiments.spatiotemporal_v02.probe
    PYTHONPATH="$PWD" python -m product.experiments.spatiotemporal_v02.probe --output product/experiments/spatiotemporal_v02/COMPARISON_REPORT_v0.2.json
    PYTHONPATH="$PWD" python -m pytest -q tests/test_product_spatiotemporal_natal_coordinate_probe.py

## Acceptance target

- All 11 pinned case IDs are present in the expected order.
- Every chart has 12 unique branches and 12 unique palace names; target-anchor identity is reconfirmed.
- For every chart: 12 index/matrix offset comparisons, 12 inverse checks and 144 cyclic composition checks.
- Reversing the palace array does not change the branch-indexed view.
- Same-palace, opposition, trine, four-directions, three-directions and two-sided flanking offsets match the existing Z12 contract.
- The checked-in JSON report is exactly reproducible.

## Boundaries

No temporal scopes are present in this artifact. Do not infer them or claim PL1 v0.2 six-layer validation. No source-equivalence, traditional cross-layer semantics, runtime performance, predictive validity, production execution, KIB update or registry activation is in scope. No production source or source artifact is modified.
