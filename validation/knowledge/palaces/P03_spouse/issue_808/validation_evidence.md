# Issue #808 — SP06 exact-head validation contract

## Source audit checkpoint

- Candidate inventory SHA: `37f4539d8e1bc4b28dfe057756a28da71eabfbde`
- Approved source SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`
- Direct scan: printed pp43–45 / PDF physical pp22–23
- Candidate accounting: 100 reviewed = 75 promoted + 25 held + 0 deduplicated
- Source records: 78 = 46 reusable + 32 CASE_SUPPORT_ONLY
- Temporal residuals added: 10 groups / 23 candidate rows; cumulative P03 residuals: 47 groups / 129 rows
- Source coverage gaps: 14 tracked, 4 open/partial
- Condition-membership holds: SP06-508 and SP06-509
- Supplemental records: P03S-SP06-SUP-001, P03S-SP06-SUP-002, P03S-SP06-SUP-003

## Required exact-head gate

Before merge, re-read current main and PR head. Require all of:
1. Full pytest
2. Product JS adapter/syntax check
3. Deterministic P0 repository gate
4. Repository Governance v1
5. P03 shard/write-set validation
6. Base/head/run identity check against the latest main

Record the final exact PR head SHA and matching workflow run IDs/statuses in the final Issue #808 disposition. Any later commit changes the head and requires the exact-head gate to run again.

## Execution boundary

No Core/shared semantic, other-palace, Product/runtime, probability, numeric-weight, decay, or history-feedback change. `conditions_compiled=0`; `execution_unlocked=0`.
