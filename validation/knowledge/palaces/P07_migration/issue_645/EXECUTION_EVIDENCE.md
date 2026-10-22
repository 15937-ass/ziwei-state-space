# Execution Evidence — Knowledge P07 M06 Source Re-adjudication

- Issue: #645
- Branch: `knowledge/p07-645-migration-m06-canonical`
- Lane/shard: KNOWLEDGE_ONLY / P07 迁移宫
- Source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》, printed pp.119–122
- Scan pages inspected: PDF scan p60 (printed pp.119–120), p61 (printed pp.121–122)

## Source-review result

- Candidate census: 90/90, M06-501…M06-590.
- Canonical records prepared: 90.
- Conditions normalized: 90.
- Source locations corrected: 33.
- Source/semantic adjudications changed: 30.
- Reusable records: 77.
- CASE_SUPPORT_ONLY: 13.
- Historical PATH_DEPENDENT_GATE re-adjudicated: M06-579; canonical gate count for this batch: 0.
- Source time layers: NATAL for baseline structure; YEAR only for M06-540…542.
- Residual source gaps carried: P07-M05-GAP-001…004 and P07-M03-GAP-001 / P07-M03-GAP-012.

## Validation

This file is a preparation record. Do not mark any gate PASS until the exact final PR head has actual results.

- Changed-unit tests: PENDING
- Full repository pytest: PENDING
- Product JS adapter checks: PENDING
- Deterministic P0 audit: PENDING
- Repository Governance v1: PENDING
- Exact-main/base/head comparison: PENDING

## Boundaries

- Historical M06 candidate CSV and legacy PR #172 are non-canonical comparison inputs.
- No source gap is silently closed.
- No new primitive, history type, time layer, probability, weight, decay, causal claim, or Product/runtime permission.
- M06 reaching the printed-p122 chapter boundary does not mean all P07 source gaps are closed.
