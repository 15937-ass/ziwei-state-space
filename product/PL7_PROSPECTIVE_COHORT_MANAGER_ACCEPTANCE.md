# PL7-Q2 Prospective Cohort Manager v0.1

Tracking Issue: #696  
Lane: PRODUCT_ONLY  
Work unit: PRODUCT_PL7_Q2_PROSPECTIVE_COHORT_MANAGER_V0_1  
Status: deterministic lifecycle manager; no inference/runtime change

## Purpose

Manage the lifecycle of prospective cohort windows and the follow-up queue using the accepted PL7 contracts. The manager is a pure, deterministic projection over caller-supplied plans, responses, and state snapshots. It does not persist personal data or infer event outcomes.

## Lifecycle and queue contract

- Registration reuses the existing prospective plan compiler and retains the locked plan/window/checkpoint provenance.
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

To be completed against the exact final PR head. Required: full pytest, Product JS adapter checks, deterministic P0 audit, Repository Governance v1, and applicable Product regressions.
