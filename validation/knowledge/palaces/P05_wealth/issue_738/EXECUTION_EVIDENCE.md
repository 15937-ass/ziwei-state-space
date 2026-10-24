# Issue #738 — 巨门来源重审执行证据

## Source and boundary
- Repository: `15937-ass/ziwei-state-space`
- Issue: #738
- Source: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》
- Verified source SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`
- Printed scope: p86 heading `10 巨门` through printed p87 immediately before `11 天相`
- PDF scan mapping: physical p43 right half = printed p86; physical p44 left half = printed p87
- Source page images were inspected directly; extracted text was used only as a secondary locator.

## Candidate census and disposition
- Acceleration input: `validation/wp05/W08_wealth_projection_review_701_800.csv`
- IDs reviewed: W08-701…W08-742, exactly 42 rows; W08-743 onward is out of scope.
- Historical candidate labels were not accepted as evidence. Each row was independently rechecked against the source image.
- Canonical promotions proposed: 42; CASE_SUPPORT_ONLY: 0.
- Source-condition/target revisions: 16 (W08-704, W08-709, W08-711, W08-712, W08-714, W08-717, W08-726, W08-728, W08-729, W08-733, W08-734, W08-735, W08-736, W08-738, W08-739, W08-740).
- New local source gaps: 0; new canonical gap supplements: 0.
- Source-stated NATAL path annotations: W08-720, W08-721, W08-723, W08-725.
- Source life-stage wording: W08-719 preserves `中年后` without a numeric threshold or independent time scale.
- Existing gaps carried forward unchanged: W05-SG-002 = PARTIALLY_RESOLVED; W06-SG-001…005 = OPEN.

## Expected post-merge checkpoint
- Existing P05 canonical reusable rules: 600.
- Proposed additions in this batch: 42.
- Proposed cumulative total after merge: 642 reusable rules; CASE_SUPPORT_ONLY remains 0.
- Next source anchor: printed p87 heading `11 天相`, opening `天相坐财帛宫，有些情形与天府相似`.
- This batch does not claim full P05 source coverage and does not authorize Product/runtime consumption.

## Validation
- Base SHA and final PR head SHA: to be recorded from the created PR and exact-head validation run.
- Full repository pytest, Product JS adapter checks, deterministic P0 gate, Repository Governance v1, and shard/write-set validation: **PENDING**.
- No PASS is claimed until all required checks pass on the exact final PR head.
