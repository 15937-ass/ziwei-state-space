# Execution Evidence — P03 SP01 source-first re-adjudication

- Issue: #792
- Lane/shard: `KNOWLEDGE_ONLY / P03 夫妻宫`
- Branch: `knowledge/p03-792-spouse-audit`
- Activation main: `127d3e9d2fc2acf80177c1fbe4073ce0d39235b2`
- Source: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》
- Approved source SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`
- Directly reviewed candidate-batch scan images: PDF physical pp17–18, corresponding to printed pp33–36; bounded candidate claims are SP01-001…SP01-100 on printed pp33–35.
- Section boundary inventory: printed pp33–51 / PDF physical pp17–26; the P03 section ends immediately before the 子女宫 heading on printed p51.
- Historical inventory: nine read-only CSV indexes, 836 unique candidate IDs, 136 historical `case_support_only=true` flags, six historical `PATH_DEPENDENT_GATE` flags.

## Disposition

- 100 candidates directly re-adjudicated.
- 89 candidate rows promoted after source review; 90 source records produced because SP01-054 is split into source-explicit 大运 and 流年 records.
- 75 reusable records and 15 `CASE_SUPPORT_ONLY` records.
- Nine candidates held with explicit reasons; two candidates deduplicated into shared/source-broader records.
- Four explicit source coverage / continuation items carried forward; two temporal-scope residuals retained.
- Historical candidate CSVs remain unchanged and read-only.

## Execution boundary

`history_feedback=0`; `conditions_compiled=0`; `execution_unlocked=0`; Product/runtime authorization false. No shared Core semantics, other-palace artifacts, Governance, or Product files changed. No new primitives, independent time scale, quantitative weight, probability, or decay was introduced.

Exact-head full pytest, Product JS adapter checks, deterministic P0 audit, Repository Governance v1 / P03 write-set validation, and exact-main/base/head verification must pass before merge.
