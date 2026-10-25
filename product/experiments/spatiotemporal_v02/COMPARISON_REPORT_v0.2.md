# Product experiment v0.2 — natal coordinate comparison

Status: TEST_ONLY_NOT_CANONICAL

## Decision

Keep the index implementation as the baseline. For the pinned set of 11 engine-materialized natal charts, the index and permutation-matrix views agree under the declared Z12 coordinate encoding. This does not demonstrate a production migration benefit.

## Input and claim boundary

The input is the pinned Wang full-chart materialization artifact, Git blob 3778e5f3d66c1e5ab44461360b6d9f71b3f8be56. It contains 11 charts with 12 unique branches and 12 unique palace names each; all 11 target anchors are reconfirmed.

The artifact's only materialization claim is SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED. Full-source-chart equivalence is explicitly not verified for any of the 11 charts. This is an engine-materialized natal coordinate fixture set, not source-transcribed full-chart ground truth.

## Results

- 11 charts; 132 palace records; 748 star objects represented in 8,976 branch-by-occupancy cells.
- 132 index-versus-matrix offset checks passed.
- 132 inverse checks and 1,584 cyclic composition checks passed.
- Reversing the input palace array preserved all 11 branch-indexed views.
- Same-palace, opposition, trine, four-directions, three-directions and two-sided flanking offsets each passed 132 coordinate checks.
- All four pinned inputs matched their Git blob and SHA-256 values.

## Not evaluated

- Full source-chart equivalence.
- PL1 v0.2 six-layer temporal snapshot mapping.
- Cross-layer traditional reaction semantics.
- Runtime performance advantage.
- Predictive validity or probability calibration.

No production runtime, Knowledge semantics, KIB lock, registry or source artifact was changed. No canonical acceptance or runtime effect is allowed.
