# Issue #407 Execution Evidence

Status: **IMPLEMENTATION ACCEPTED; PRODUCT TEST CONTRACT HARDENED**

Execution runtime: GitHub Actions standard public-repository runners.

Merged implementation PR: #409
Merged implementation commit: `d2c048b4639a6c4bc8cb1561c6489203444aaf3f`

## Accepted Product result

- Career rules: **134 -> 165 accepted NATAL rules**
- Review-04 selected mappings: **31/31**
- readiness mapped-ID scope: **352 -> 452**
- scoped disposition: **165 compiled / 287 blocked-context / 0 unselected static candidates**
- no Knowledge file was changed by Product #407

## Why the first run failed

The first full-suite run produced **1739 passed / 3 failed** while all four Product P1/B02
regressions were already green.

All three failures were stale Product test assumptions, not rule-runtime failures:

1. a transformation-negative scenario asserted that a 天同 fixture must produce no Career evidence;
   Review-04 legitimately added general 天同 evidence, so the assertion was too broad;
2. Review-02 integration tests froze the future global registry total at 134;
3. Review-03 integration tests froze the future global registry total at 134.

Those tests were repaired to own only their intended invariant: required/forbidden scoped rules,
source handoff integrity, and selected batch membership. They no longer claim that future Product
batches cannot add valid coexisting evidence.

## Final implementation validation

Final implementation head before squash merge:
`0884fd02e9684f3aa6ca907ee2d5b0a7ed809da6`

Results:
- repository-quality-gate #1665: **PASS**
- full pytest: **1748 passed / 0 failed**
- JS syntax: **PASS**
- deterministic P0 audit: **PASS**
- Product governance validation: **PASS**
- product-p1-dual-engine #461: **PASS**
- product-p1-b02-calendar #83: **PASS**
- product-p1-b02b-zi-day #58: **PASS**
- product-p1-b02c-temporal #52: **PASS**

## Recurrence prevention

The closing Product PR additionally hardens the remaining historical expansion-sensitive tests:

- Review-04 batch tests verify their own 31-rule selection and full handoff consistency without
  pinning the global registry forever at 165;
- transformation scenario tests require the intended rules and forbid the relevant wrong
  transformation rules without asserting that no future valid general rule may coexist;
- CLI and full-chart integration tests verify required evidence as a subset rather than freezing
  the complete future active-rule list.

One canonical inventory test intentionally continues to own the exact current provider count/set,
and the readiness audit intentionally owns the exact current aggregate counts. Those are the two
places that should change when a future Product batch is explicitly accepted; historical batch
tests should not.

This closing/hardening PR must pass the full G8 Product gates on its exact head before Issue #407
is closed.

## Limits

These deterministic gates establish Product source/condition/projection integrity and regression
consistency only. They do not establish empirical predictive accuracy, temporal production,
numeric probability, causal truth or guaranteed real-world career outcomes.
