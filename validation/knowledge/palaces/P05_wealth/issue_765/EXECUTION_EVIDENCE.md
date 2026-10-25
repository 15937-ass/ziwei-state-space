# Execution Evidence — P05 Qisha source-first audit (Issue #765)

Status: DRAFT — merge requires the latest exact-head repository-quality-gate run to pass.

## Source integrity and boundary
- Approved source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》.
- SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.
- Directly inspected physical PDF p45 right half (printed p90) and physical p46 left half (printed p91).
- Scope: printed p90 heading `13 七杀` through the final 七杀 sentence on printed p91; stops before heading `14 破军`.
- The approved local PDF hash matches the registered source hash. PDF text extraction was a secondary locator; original page images control.

## Reconciliation
- Historical candidates W09-845…W09-888: 44 reviewed exactly once.
- Additional source atoms W09-901…W09-904: 4 reviewed; three promoted, one held due unresolved compressed wording.
- Total source-first records: 48; 44 promotions proposed; W09-865, W09-881, W09-882 and W09-904 remain unpromoted.
- Three candidate condition/scope corrections: W09-865, W09-881 and W09-882.
- Nine local source ambiguities remain OPEN: W09-SG-006…014. Clear subclauses are scoped separately; no uncertain condition is silently normalized.
- Accepted main baseline before this batch: 721 reusable rules; expected cumulative count after merge: 765.
- Existing gap dispositions carried forward: W05-SG-002 PARTIALLY_RESOLVED; W06-SG-001…005 and W08-SG-001…005 OPEN. New local gaps bring tracked residual count from 11 to 20.

## Write set
P05-only paths: Qisha readjudication, time-scope and gap sidecars, canonical summary, P05 state, P05-local tests, and this execution evidence. No Product, Governance, shared Core, historical candidate index, or other-palace paths are changed.

## Validation
- Exact base: `5e3b26d8ad5d49152bf9cc44339f53e9db43d803` (Tianliang PR #762 merged).
- The latest PR head and its exact-head run must be recorded in the PR handoff. Merge requires full pytest, Product JS adapter checks, deterministic P0, Repository Governance v1 and P05 shard/write-set validation to pass on that exact head.
- No Product/runtime authorization or empirical predictive-validity claim is implied.
