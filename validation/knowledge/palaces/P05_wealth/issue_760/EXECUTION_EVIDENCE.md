# Execution Evidence — P05 Tianliang source-first audit (Issue #760)

Status: DRAFT — source-first adjudication complete; do not merge until the final PR head's latest exact-head gate passes.

## Source integrity and boundary
- Approved source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》.
- SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.
- Directly inspected physical PDF p44 right half (printed p88), physical p45 left half (printed p89), and physical p45 right half top line (printed p90).
- Scope: printed p88 heading `12 天梁` through the last Tianliang sentence at the top of printed p90; stops before heading `13 七杀`.
- The approved local PDF hash matches the registered source hash. PDF text extraction was used only as a locator; original page images control.

## Reconciliation
- Historical candidates W08-788…W08-800: 13 reviewed exactly once.
- Additional atoms reviewed: W08-801…W08-825 (25); 24 are promoted and W08-820 remains unpromoted because the printed condition `丑来天梁` is unresolved.
- Total source-first records: 38; 37 promotions proposed; W08-820 is held unpromoted pending resolution of W08-SG-005.
- One historical candidate condition correction: W08-798.
- Three source-text anomalies remain OPEN: W08-SG-003, W08-SG-004 and W08-SG-005; no uncertain reading is promoted.
- Accepted main baseline before this batch: 684 reusable rules; expected cumulative count after merge: 721.
- Existing gap dispositions carried forward: W05-SG-002 PARTIALLY_RESOLVED; W06-SG-001…005 and W08-SG-001/002 OPEN. New local gaps bring the tracked residual count from 8 to 11.

## Write set
P05-only paths: Tianliang readjudication, time-scope and gap sidecars, canonical summary, P05 state, P05 tests, and this execution evidence. No Product, Governance, shared Core, historical candidate index, or other-palace paths are changed.

## Validation
- Exact base after Core PR #758 merged: `74864f572cdd04407c241c483f3a34c646f69d3a`.
- Source/state/test head validated before this evidence-only update: `748a31916a57735930e0bde0b4452421294ff6ee`.
- Repository-quality-gate run #40158863609 passed on that exact tested head: https://github.com/15937-ass/ziwei-state-space/actions/runs/40158863609.
- Full pytest, Product JS adapter checks, deterministic P0 repository gate, and Repository Governance v1 all completed successfully on that tested head; the P05 write set was confined to the ten P05-owned paths.
- This evidence-only update does not change source adjudication, rule counts, tests, or the allowed write set. The resulting final PR head must pass its own latest exact-head gate before merge; record that final head and run in the PR conversation.
- No Product/runtime authorization or empirical predictive-validity claim is implied.
