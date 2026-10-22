# Wang Full-Chart Materialization v0.1B — Acceptance Record

Tracking Issue: #588  
Lane: PRODUCT_ONLY  
Status: **IMPLEMENTATION IN PROGRESS — PINNED-ENGINE ARTIFACT NOT YET GENERATED**

## 1. Purpose

Materialize a separate, blind-safe full natal-chart artifact for the 11 cases that have exactly one source-bounded lunar candidate matching the already source-reviewed target-palace anchor.

This artifact is derived from a pinned chart engine. It is not a claim that every field of the reconstructed chart was visually transcribed from the source page.

## 2. Eligibility lock

The only eligible case IDs are:

```text
WANG-CASE-001
WANG-CASE-003
WANG-CASE-006
WANG-CASE-009
WANG-CASE-010
WANG-CASE-012
WANG-CASE-013
WANG-CASE-015
WANG-CASE-019
WANG-CASE-021
WANG-CASE-023
```

They must remain exactly the set selected by `FULL_CHART_RECONSTRUCTION_READINESS_V0_1.json`. The materializer rejects a changed eligible set rather than silently adapting.

The other 13 cases remain unmaterialized:

| Readiness status | Cases | Count |
|---|---|---:|
| `MULTIPLE_ANCHOR_MATCH` | 002, 008, 014, 018, 020, 022 | 6 |
| `NO_ANCHOR_MATCH` | 005, 007, 011, 017, 024 | 5 |
| `BLOCKED_SOURCE_INCOMPLETE` | 004, 016 | 2 |

No candidate is chosen manually. Case 021 remains bound to its unique readiness candidate `WANG-CASE-021:D01:T00`; the nonmatching Zi-time candidate is not promoted.

## 3. Pinned engine contract

- Engine: `iztro-js 2.6.1`
- Entry point: `astro.byLunar`
- Calendar: lunar input, using the exact source-bounded year/month/day and time index
- Algorithm: `zhongzhou`
- Astro type: `heaven`
- Leap fix: `true`
- Day divide: `forward`
- Year divide: `normal`
- Horoscope divide: `normal`

The generated artifact retains engine/source revision, adapter version, input candidate ID, normalized input, source chart span/pages, source-artifact SHA-256 digests, and an independently rechecked target-anchor result.

## 4. Artifact and schema

Intended output:

```text
product/expert_cases/wang_tingzhi/FULL_CHART_MATERIALIZATION_V0_1B.json
```

Each record contains all 12 normalized natal palaces, each with name, stem, branch, body-palace flag, major/minor/adjective stars, and decadal metadata. It also preserves chart-level date/time metadata, soul/body markers, five-elements class, and soul/body palace branches.

The original `BLIND_EVIDENCE_V0_1.json` remains unchanged and continues to mean **target-palace major-star system only**.

## 5. Claim boundary

The only permitted materialization claim is:

```text
SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED
```

It does **not** mean:

- full-source-chart equivalence was verified;
- all reconstructed auxiliary stars or annotations were visually source-reviewed;
- the case establishes canonical Zhongzhou truth;
- an expert-method conclusion or outcome label is ground truth;
- the chart has predictive validity or supplies an empirical probability.

No source subject identity, expert reasoning, expert conclusion, outcome, person-group mapping, or external biography may enter the blind artifact.

## 6. Implementation status

- Dedicated pinned-lunar materializer: **IMPLEMENTED**
- Strict artifact validator: **IMPLEMENTED**
- Strict input-artifact revision locks (source signatures, blind anchor, readiness report): **IMPLEMENTED**
- Validator tests with explicitly synthetic, test-only chart fixtures: **IMPLEMENTED**
- End-to-end materializer tests with an isolated mock engine, deterministic serialization, and fail-closed error/drift cases: **IMPLEMENTED**
- Committed full-chart output artifact: **NOT YET GENERATED**
- Real-engine end-to-end validation on the current PR head: **PENDING**
- Repository quality gate / P0 audit / Product regressions: **PENDING**

Synthetic chart objects and the isolated mock engine validate implementation wiring, schema, determinism, and guardrails only; they are not source evidence and must never be copied into the production artifact.

## 7. Execution dependency

The current Product P1 workflow does not persistently run the Wang reconstruction probe. Governance Issue #584 records the workflow-hook gap and is waiting for the Governance lane to release the work slot after Issue #446.

This Product work unit does not modify `.github/workflows/**`, and it does not work around that ownership boundary. Until an already-authorized runner executes the pinned materializer, the generated chart artifact remains unclaimed and this work unit must not be marked complete or merged as a completed materialization.

## 8. Acceptance matrix

| Requirement | Status |
|---|---|
| Exactly 11 approved case IDs | Implemented; test pending execution |
| Exact unique readiness candidate used for each case | Implemented; test pending execution |
| Pinned lunar engine and Zhongzhou config | Implemented; real-engine run pending |
| Exactly 12 normalized palaces per chart | Implemented; test pending execution |
| Source span/pages, SHA-256 lineage, and exact Git blob revision pins | Implemented; test pending execution |
| Target-anchor recheck on generated chart | Implemented; real-engine run pending |
| Forbidden leakage keys rejected | Implemented; test pending execution |
| Remaining 13 cases stay blocked | Implemented in contract; test pending execution |
| Actual 11-chart artifact committed | **BLOCKED — authorized runner execution not yet available** |
| Exact-head repository quality and Product gates | Pending |

## 9. Next step after materialization

Only after the pinned engine produces and validates the 11-chart artifact should the subsequent `WANG_METHOD_SCOPE_REVIEW_V0_1C` work unit reconsider how the reconstructed full-chart evidence interacts with case-target method scope.

This unit does not broaden MethodPattern scopes or claim that full expert replay is ready.
