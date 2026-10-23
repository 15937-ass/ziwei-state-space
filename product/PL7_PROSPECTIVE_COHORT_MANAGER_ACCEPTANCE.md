# PL7-Q2 Prospective Cohort Manager v0.1

Tracking Issue: #696  
Lane: PRODUCT_ONLY  
Work unit: PRODUCT_PL7_Q2_PROSPECTIVE_COHORT_MANAGER_V0_1  
Status: deterministic lifecycle manager; no inference/runtime change

## Purpose

Manage the lifecycle of prospective cohort windows and the follow-up queue using the accepted PL7 contracts. The manager is a pure, deterministic projection over caller-supplied plans, responses, and state snapshots. It does not persist personal data or infer event outcomes.

## Lifecycle and queue contract

- Registration reuses the existing prospective plan compiler, retains the locked plan/window/checkpoint provenance, and records a canonical SHA-256 plan fingerprint. Every transition rejects a plan/digest mismatch.
- Window lifecycle is separate from follow-up status. The lifecycle states are PLANNED, OPEN, CLOSED, CANCELLED, and TERMINATED_EARLY.
- A window opens only on/after its locked start and no later than its end. Normal close-out is only available on/after the end date. A missed window may be administratively closed, but it remains INCOMPLETE unless the accepted audit finds every target close-out complete.
- Early withdrawal/loss-to-follow-up requires an explicit disposition, reason, termination date, and observed-through date. Censoring metadata does not carry an event status.
- The queue view is sorted deterministically by window start, window end, and plan ID. It reports next actions without mutating the supplied states.

## Follow-up completeness

The manager reuses the existing PL7 data-quality audit and records the audit's expected, matched, complete, missing, no-response, and unresolved close-out counts.

- Missing responses, NO_RESPONSE, UNSURE, unconfirmed answers, duplicate plan-target-checkpoint responses, and ambiguous/missing event time remain unknown/incomplete.
- Missingness is never treated as EVENT_NOT_OCCURRED; no observation is automatically created or promoted.
- The Q1 audit remains the source of detailed findings. Q2 records lifecycle state and a compact audit summary rather than implementing a second audit engine.

## Frozen boundaries

- No canonical Zi Wei rules, ontology mappings, KIB lock, production registries, weights, probabilities, calibration, or Forecast Ledger changes.
- No database, network, UI, LLM parser, or raw narrative storage.
- PL7-Q3 parser, PL7-Q4 corpus builder, and PL7-Q5 privacy/consent/deletion remain separate work units.
- Fixture/contract validation is not a real-cohort quality result or predictive-validity claim.

## Validation evidence

Pre-final validation on the current-main-synced implementation (before this evidence section was committed):

- Execution runtime: GitHub Actions standard public runners.
- Base commit: `3407150866a5ace99552daa674356b92610f080e`.
- Validated pre-final head: `952102868857b928488f6be4234485e865132ced`.
- Repository quality gate: **PASS** — 2,607 pytest tests passed in 249.26s; Product JS adapter check, deterministic P0 audit, and Repository Governance v1 all passed. [Run #39944977993](https://github.com/15937-ass/ziwei-state-space/actions/runs/39944977993)
- Applicable Product regressions: **PASS** — [dual engine #39944977766](https://github.com/15937-ass/ziwei-state-space/actions/runs/39944977766), [Zi-day #39944977588](https://github.com/15937-ass/ziwei-state-space/actions/runs/39944977588), [calendar #39944977844](https://github.com/15937-ass/ziwei-state-space/actions/runs/39944977844), and [temporal #39944978034](https://github.com/15937-ass/ziwei-state-space/actions/runs/39944978034).

Because this note changes the PR head, a final exact-head validation is still required before merge. The PR description must record the final head SHA and final workflow results; do not merge unless the final repository quality gate and all applicable Product regressions pass.
