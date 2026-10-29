# WP06B Option C contract closure — execution evidence

Status: PI_DECISIONS_RECORDED_FINAL_VALIDATION_PENDING. PI accepted D1–D5 on 2026-10-29; final merge still requires a fresh exact-head green gate against current main.

## Work unit
- Issue: #841
- Branch: `knowledge/core-841-option-c-minimal-contract-closure-resync`
- Work unit: `KB-CORE-WP06B-OPTION-C-MINIMAL-CONTRACT-CLOSURE-01`
- Scope: non-canonical contract review, boundary fixtures, deterministic tests.
- No production schema, source rows, canonical ontology, Product/runtime/KIB or consumer permission is changed.

## Current observed base
- Main base for the latest-main reconstruction: `677e669954bfb38b3d9dd082fe5b0f0d7faf3c80`.
- The work branch was reconstructed from this main SHA after main advanced. Final acceptance still requires an exact-head run whose PR base remains this current main.

## First PR-head validation observation

- Run: `40694277319` on head `1339abe4ab8070a46dacf089cbbc710e72549398`.
- Result: **FAIL** at the pytest step; `2910 passed, 1 failed, 132 subtests passed`.
- Sole failure: `tests/test_knowledge_core_14star_property_normalization.py::test_research_closure_metadata_matches_merged_pr_and_final_quality_gate`.
- Cause: the historical #757 closure regression required `CORE_STATE.status=IDLE` forever. That was valid immediately after #757 closed, but becomes stale once a later authorized Core work unit (#841) is active.
- Correction: the regression now asserts that #757 remains the last completed work unit recorded for that closure and is not reactivated, while allowing a later bounded Core Issue/PR to occupy the slot.
- Red-team semantic correction: QI/QR cases whose `output_kind` cannot yet be determined now use axis state `UNKNOWN`, not `UNRESOLVED`, to avoid conflation with `normalization_epistemic=UNRESOLVED` and `source_epistemic=UNRESOLVED_SOURCE`.
- Because pytest failed first, Product JS, deterministic P0, and Repository Governance v1 were skipped in that run. No PASS is claimed.

## Corrected semantic-head validation

- Run: `40797509674`.
- Validated PR head: `8ecd82a19d5961e3a684bde5ff14b215bea32ef4`.
- PR base / main at the successful semantic-head validation: `73408788df904f3d34e4131739d3d40cfa7c942e`.
- Result: **SUCCESS**.
- Pytest: **2916 passed, 132 subtests passed** in 319.13s.
- Product JS adapter check: **PASS**.
- Deterministic P0 repository gate: **PASS**.
- Repository Governance v1 / Core write-set validation: **PASS**.
- Main was rechecked after the run and remained `73408788df904f3d34e4131739d3d40cfa7c942e`.
- This run validates the corrected proposal, tests, and latest-main reconstruction before the evidence/state recording commit. The final PR head after this recording is acceptable only if its own automatic pull-request gate is green; no stale-green substitution is allowed.

## Required final-head checks
1. Focused test: `tests/test_knowledge_core_option_c_minimal_contract_closure.py`.
2. Full pytest suite.
3. Product JS adapter syntax/check.
4. Deterministic P0 audit.
5. Repository Governance v1 and Core write-set validation.
6. Re-run all required checks if main advances after the recorded validation base.

## Limits
The fixtures assert source-faithful classification boundaries and governance invariants only. They do not assert real-world predictive validity, canonical acceptance, or Product readiness. Final test counts and workflow URLs must be filled only from actual exact-head run results.


## Latest-main resynchronization after validated semantic head

- Main subsequently advanced to `677e669954bfb38b3d9dd082fe5b0f0d7faf3c80` through P11 palace-local source-audit changes only.
- The six #841 Core/test/evidence paths were reconstructed without semantic change onto this main commit.
- The prior successful Run `40797509674` remains evidence for the corrected semantic content, but **is not the final acceptance gate** after this resynchronization.
- The current reconstructed PR head requires its own green pull-request quality gate against `677e669954bfb38b3d9dd082fe5b0f0d7faf3c80` before PI review is clean.


## PI decision record — 2026-10-29

- PI response: `D1–D5 全部接受，按建议继续。`
- D1–D5 are recorded as accepted governance decisions for the minimum semantic review contract.
- This acceptance authorizes the next bounded WP06C formal mapping-review work under existing gates.
- It does **not** authorize individual canonical mappings, canonical ontology IDs, production schema changes, Product/KIB/runtime consumption, probability assignment, numeric strength, or empirical predictive-validity claims.
- Main advanced after the pre-PI gate to `6b87b904d548ead46bf3d858cc1e50d29cf0cb8e` through palace-local P11/P02 audit work. The #841 decision-bearing candidate is reconstructed on this main and requires a fresh exact-head pull-request gate before merge.
