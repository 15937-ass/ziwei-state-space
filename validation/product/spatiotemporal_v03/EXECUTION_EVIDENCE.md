# Spatiotemporal guarded-temporal probe v0.3 — execution evidence

Status: **TEST_ONLY engineering validation; no canonical semantics or production migration approved.**

## Source and fixture pins

- Producer workflow run: `40161980768`.
- Producer artifact: `12586873751`, digest `sha256:730158ea500b26b458ca836091a23bf209363e8121437bf0296f374dc5936a8f`.
- Reduced fixture SHA-256: `05f1dd790faae77ce0caf34af259e0b85c597056f3e18ac207a8e581ee1d2524`.
- Source-row hashes are computed from exact UTF-8 CSV row text, excluding line terminators, and verified against `validation/product_chart_regression/regression_inputs_v0.1.csv`.
- The pinned upstream `iztro v2.6.1` type contract and exact source blob IDs are recorded in `fixture_manifest_v0.3.json`.

## Exact-head validation policy

Every edit to this branch, including this evidence file, creates a new head and invalidates previous-head validation as evidence for the new head. Therefore:
- The authoritative final result for the latest head is the exact-head run set and commit recorded in Issue #772.
- Do not infer current-head success from a run against an older head.
- The most recent validation snapshot before this evidence-file update was head `b5cb543a9ad7ca7f37718d3e62f750a2c9eac445`, base `20c5716a6bf609fc86e1b6668595a10f84ccc934`: repository quality gate passed with 2751 tests and 132 subtests; all four applicable Product P1 workflows passed. The evidence-file update requires a fresh exact-head run.

## Scope boundary

Only the v0.3 experiment files, tests, and execution evidence are changed. No production runtime, canonical temporal registry, Knowledge/Core/Governance, KIB lock, PL1 exporter/schema, or workflow changes are authorized. No canonical semantics, production migration, or predictive-validity claim is authorized.
