# Wang Full-Chart Materialization v0.1B — Acceptance Record

Tracking Issue: #588  
Lane: PRODUCT_ONLY  
Status: **PINNED-ENGINE ARTIFACT GENERATED; FORMAL VALIDATION PASS; FINAL-HEAD REGRESSION GATES PENDING**

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
- Committed full-chart output artifact: **GENERATED AND COMMITTED IN THIS PR**
- Real-engine end-to-end validation: **PASS** — Product P1 run [#39705521292](https://github.com/15937-ass/ziwei-state-space/actions/runs/39705521292) on execution head `708c615c574019f7d092a8cd23d223d9bd916c35`; formal validator passed against all three immutable inputs.
- Exact final-head repository quality gate / P0 audit / Product regressions: **PENDING — rerun after artifact commit**

Synthetic chart objects and the isolated mock engine validate implementation wiring, schema, determinism, and guardrails only; they are not source evidence and must never be copied into the production artifact.

## 7. Execution evidence and governance boundary

The materializer was executed once on the existing, authorized Product P1 dual-engine public runner without changing `.github/workflows/**` or workflow triggers. The one-off invocation and output capture were temporarily instrumented in `tools/p1_independent_compare.py`; that root-tool modification is **not retained in the final branch tree**.

- Workflow run: [Product P1 dual-engine #39705521292](https://github.com/15937-ass/ziwei-state-space/actions/runs/39705521292)
- Execution commit: `708c615c574019f7d092a8cd23d223d9bd916c35`
- Runtime: Node.js 20 runner; `iztro-js 2.6.1`; `astro.byLunar`; `algorithm=zhongzhou`
- Result: exactly 11 eligible charts generated; all 11 have 12 distinct palace records and independently rechecked target anchors.
- Formal validator: **PASS** — `src/product/wang_full_chart_materialization.py`, including source artifact Git-blob pins and SHA-256 lineage.
- Durable evidence: `validation/product/issue_588/EXECUTION_EVIDENCE.md`.

The separate persistent probe-hook gap remains tracked by Governance Issue #584 and remains subject to Issue #446. This one-off Product execution does not activate or modify that Governance work unit. No Governance, Knowledge, root-tool, or workflow change is retained in the final PR.

## 8. Acceptance matrix

| Requirement | Status |
|---|---|
| Exactly 11 approved case IDs, in canonical order | **PASS** — pinned-engine run and formal validator |
| Exact unique readiness candidate used for each case | **PASS** — validator cross-checks readiness lineage and candidate set |
| Pinned engine/version/configuration | **PASS** — `iztro-js 2.6.1`, `astro.byLunar`, Zhongzhou lunar contract |
| Exactly 12 distinct normalized palaces per chart | **PASS** — 11/11 charts |
| Source span/pages, SHA-256 and Git-blob lineage | **PASS** — formal validator |
| Target-palace identity and fourteen-major-star anchor recheck | **PASS** — 11/11 `UNIQUE_ANCHOR_MATCH_RECONFIRMED` |
| Source candidate ambiguity preserved | **PASS** — WANG-CASE-021 retains indices 0 and 12; one readiness anchor match at T00 |
| Leakage controls | **PASS** — formal validator and committed-artifact regression test |
| Remaining 13 cases stay unmaterialized | **PASS** — 6 multiple-match, 5 no-match, 2 source-blocked |
| Actual 11-chart artifact committed | **PASS** — see `FULL_CHART_MATERIALIZATION_V0_1B.json` and execution evidence |
| Exact final-head repository quality and Product gates | **PENDING** — run after this artifact/evidence commit |

## 9. Next step after materialization

Only after the pinned engine produces and validates the 11-chart artifact should the subsequent `WANG_METHOD_SCOPE_REVIEW_V0_1C` work unit reconsider how the reconstructed full-chart evidence interacts with case-target method scope.

This unit does not broaden MethodPattern scopes or claim that full expert replay is ready.
