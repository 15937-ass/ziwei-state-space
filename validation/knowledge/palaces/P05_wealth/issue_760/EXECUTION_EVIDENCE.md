# Execution Evidence — P05 Tianliang source-first audit (Issue #760)

Status: DRAFT — exact-head repository validation pending.

## Source integrity and boundary
- Approved source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》.
- SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.
- Directly inspected physical PDF p44 right half (printed p88), physical p45 left half (printed p89), and physical p45 right half top line (printed p90).
- Scope: printed p88 heading `12 天梁` through the last Tianliang sentence at the top of printed p90; stops before heading `13 七杀`.
- The approved local PDF hash matches the registered source hash. PDF text extraction was used only as a locator; original page images control.

## Reconciliation
- Historical candidates W08-788…W08-800: 13 reviewed exactly once.
- Additional directly supported atoms: W08-801…W08-825 (25).
- Total source-first records: 38; clear target promotions proposed: 38.
- One historical candidate condition correction: W08-798.
- Three source-text anomalies remain OPEN: W08-SG-003, W08-SG-004 and W08-SG-005; neither anomaly is silently normalized into a canonical target.
- Accepted main baseline before this batch: 684 reusable rules; expected cumulative count after merge: 722.
- Existing gap dispositions carried forward: W05-SG-002 PARTIALLY_RESOLVED; W06-SG-001…005 and W08-SG-001/002 OPEN. New local gaps bring the tracked residual count from 8 to 11.

## Write set
P05-only paths: Tianliang readjudication, time-scope and gap sidecars, canonical summary, P05 state, P05 tests, and this execution evidence. No Product, Governance, shared Core, historical candidate index, or other-palace paths are changed.

## Validation
- Exact base at branch creation: `28668b1354e8c9f86991b8c25a5b8ea62afce898`.
- Exact head and GitHub Actions run: pending.
- Full pytest, Product JS adapter checks, deterministic P0 gate, Repository Governance v1, and P05 shard/write-set validation: pending. Do not merge until all required exact-head gates pass.
- No Product/runtime authorization or empirical predictive-validity claim is implied.
