# Issue #806 — SP05 exact-head validation contract

## Source audit checkpoint

- Candidate inventory SHA: `c47e7fd5757c5eea1fbe67f85b67f31958666acd`
- Approved source SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`
- Direct scan: printed pp41–43 / PDF physical pp21–22
- Candidate accounting: 100 reviewed = 64 promoted + 35 held + 1 deduplicated
- Each of the 100 candidate dispositions records its source literal and verified source location/span, including held and deduplicated rows
- Source records: 66 = 46 reusable + 20 CASE_SUPPORT_ONLY
- Temporal residuals after cumulative reconciliation: 37 groups / 106 candidate rows
- Source coverage gaps: 11 tracked, 4 open/partial
- Semantic hold: SP05-465; duplicate: SP05-500 → P03S-464
- Supplemental source records: P03S-SP05-SUP-001 and P03S-SP05-SUP-002

## Required exact-head gate

Before merge, the current PR head and current `main` must be re-read. Require all of:
1. Full pytest
2. Product JS adapter/syntax check
3. Deterministic P0 repository gate
4. Repository Governance v1
5. P03 shard/write-set validation
6. Base/head/run identity check against the latest `main`

The final exact PR head SHA and matching workflow run IDs/statuses are to be recorded in the final Issue #806 disposition (or PR thread), not cached here. Any commit added after a gate run changes the head and requires the exact-head gate to run again.

## Execution boundary

No Core/shared semantic, other-palace, Product/runtime, probability, numeric-weight, decay, or history-feedback change. `conditions_compiled=0`; `execution_unlocked=0`.
