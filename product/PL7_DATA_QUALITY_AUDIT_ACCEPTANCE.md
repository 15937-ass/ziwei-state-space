# PL7 Longitudinal Data Quality Audit v0.1

Tracking Issue: #668  
Lane: PRODUCT_ONLY  
Work unit: PRODUCT_PL7_DATA_QUALITY_AUDIT_V0_1  
Status: deterministic audit utility; no production inference change

## Purpose

Provide a repeatable, source-neutral audit for caller-supplied PL7 observations (schema v0.1/v0.2), prospective check-in plans, and check-in responses. The implementation reuses the existing observation and plan compilers; it does not replace their validation rules.

The audit is a parallel PL7 data-quality task. It does not unblock the primary Product dependency on Knowledge-owned temporal-response and manifestation artifacts.

## Inputs and output

Entry point:

```python
audit_longitudinal_data_quality(
    observations=[...],
    plans=[...],
    checkin_responses=[...],
)
```

The return value is JSON-serializable and deterministic for identical inputs. Findings are sorted by severity, code, entity type, identifiers, and stable details. Invalid rows are reported without stopping the entire audit.

An empty input returns `NO_DATA`, not `PASS`. The function reads only caller-supplied values and makes no network or repository-data lookup.

## Audit dimensions

- Duplicate observation/plan/response IDs: distinguish identical repeated payloads from identifier collisions. Duplicate plan-target-checkpoint responses are separately reported. Nothing is automatically deduplicated.
- Window conflicts: report contradictory resolved outcomes for the same person and target where target windows overlap. Overlap alone is not a conflict.
- Target definition and ontology version: report target-ID drift across supplied observations and plans. This is consistency checking only; no canonical ontology registry is available here to validate that a version exists or is semantically correct.
- Follow-up completeness: compare each valid plan-target with its required `WINDOW_CLOSE` checkpoint. Missing responses, `NO_RESPONSE`, `UNSURE`, unconfirmed answers, and missing event-time detail are distinct findings.
- Missingness risk: nonresponse and absent close-out responses receive review flags for potential informative missingness. This is **not** a determination that missingness is MNAR.
- Exposure separation: visible-forecast plans are surfaced for separate analysis and must not be pooled into blind-benchmark data.
- Reference integrity: invalid observation/plan payloads and unmatched plan, target, or checkpoint references are surfaced rather than silently repaired.

## Frozen boundaries

- A mid-window `NO` means `NO_EVENT_YET`; it is never a negative sample.
- A window-close `NO_RESPONSE`, `UNSURE`, `UNKNOWN`, or `CENSORED` is not `EVENT_NOT_OCCURRED`.
- An observation is not promoted from a check-in response by this audit.
- The audit does not impute dates, change targets, select among duplicate rows, resolve conflicting outcomes, or modify source artifacts.
- No Zi Wei rule semantics, Product runtime, active KIB, probabilities, weights, or Forecast Ledger state changes.

## Validation boundary

The regression suite contains 21 focused tests. The tests use committed demonstration fixtures and synthetic perturbations. The repository currently contains no established real cohort dataset for this audit, so test success is **fixture/contract evidence only**. It is not a real-cohort data-quality result, calibration result, canonical fidelity result, or predictive-validity result.

## Acceptance evidence

- Exact observation and plan validators are reused.
- Stable JSON-ready findings and summary counts are emitted.
- Duplicate IDs, outcome conflicts, ontology drift, missing/duplicate close-outs, invalid references, nonresponse, uncertainty, mid-window negative protection, visible exposure, and no-data behavior have regression coverage.
- Full repository quality gate, pytest, deterministic P0 audit, Repository Governance v1, and applicable Product regressions must pass on the final PR head.
