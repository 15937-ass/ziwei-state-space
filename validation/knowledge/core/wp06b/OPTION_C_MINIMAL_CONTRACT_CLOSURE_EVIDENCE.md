# WP06B Option C contract closure — execution evidence

Status: IN_PROGRESS; first PR-head validation failed on one stale historical regression assertion. Corrections are committed; a new exact-head run is required.

## Work unit
- Issue: #841
- Branch: `knowledge/core-841-option-c-minimal-contract-closure-resync`
- Work unit: `KB-CORE-WP06B-OPTION-C-MINIMAL-CONTRACT-CLOSURE-01`
- Scope: non-canonical contract review, boundary fixtures, deterministic tests.
- No production schema, source rows, canonical ontology, Product/runtime/KIB or consumer permission is changed.

## Current observed base
- Main base for the latest-main reconstruction: `73408788df904f3d34e4131739d3d40cfa7c942e`.
- The work branch was reconstructed from this main SHA after main advanced. Final acceptance still requires an exact-head run whose PR base remains this current main.

## First PR-head validation observation

- Run: `40694277319` on head `1339abe4ab8070a46dacf089cbbc710e72549398`.
- Result: **FAIL** at the pytest step; `2910 passed, 1 failed, 132 subtests passed`.
- Sole failure: `tests/test_knowledge_core_14star_property_normalization.py::test_research_closure_metadata_matches_merged_pr_and_final_quality_gate`.
- Cause: the historical #757 closure regression required `CORE_STATE.status=IDLE` forever. That was valid immediately after #757 closed, but becomes stale once a later authorized Core work unit (#841) is active.
- Correction: the regression now asserts that #757 remains the last completed work unit recorded for that closure and is not reactivated, while allowing a later bounded Core Issue/PR to occupy the slot.
- Red-team semantic correction: QI/QR cases whose `output_kind` cannot yet be determined now use axis state `UNKNOWN`, not `UNRESOLVED`, to avoid conflation with `normalization_epistemic=UNRESOLVED` and `source_epistemic=UNRESOLVED_SOURCE`.
- Because pytest failed first, Product JS, deterministic P0, and Repository Governance v1 were skipped in that run. No PASS is claimed.

## Planned exact-head checks
1. Focused test: `tests/test_knowledge_core_option_c_minimal_contract_closure.py`.
2. Full pytest suite.
3. Product JS adapter syntax/check.
4. Deterministic P0 audit.
5. Repository Governance v1 and Core write-set validation.
6. Re-run all required checks if main advances after the recorded validation base.

## Limits
The fixtures assert source-faithful classification boundaries and governance invariants only. They do not assert real-world predictive validity, canonical acceptance, or Product readiness. Final test counts and workflow URLs must be filled only from actual exact-head run results.
