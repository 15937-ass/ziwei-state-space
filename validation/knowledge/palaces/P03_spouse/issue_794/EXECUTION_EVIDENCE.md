# Execution Evidence — P03 SP02 source-first re-adjudication

- Issue: #794
- Lane/shard: `KNOWLEDGE_ONLY / P03 夫妻宫`
- Branch: `knowledge/p03-794-spouse-audit-sp02`
- Activation main/base SHA: `0b372a188f2edf1bef3544c30c94388b6a88a131`
- Source: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》, 下篇·宫垣论·夫妻宫
- Approved source SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`
- Historical candidate CSV: `validation/wp05/SP02_spouse_projection_review_101_200.csv`
- Historical CSV blob SHA: `0bc7a6f9c03790cf8b7c610a19ca55d78b3cf007`
- Directly inspected scan images: PDF physical pp18–19, corresponding to printed pp35–38; bounded candidate claims SP02-101…200 are on printed pp35–37.
- Original scan visually inspected; text extraction used only as a locator.
- Exact branch head at evidence-file creation is recorded in the commit returned by this file write; the final PR head and exact-head CI status must be re-fetched from PR metadata after the PR is opened. Do not treat the preceding artifact commit as the final PR head.

## Source-first disposition

- 100 historical candidates directly re-adjudicated.
- 77 candidate rows promoted into 79 source records; SP02-190 was split into three source-native outcome branches.
- 60 reusable projection/method records; 19 `CASE_SUPPORT_ONLY` records.
- 23 candidate rows held with explicit temporal-scope reasons; zero deduplications.
- Three prior source gaps resolved (SP01-GAP-002, -003, -004); seven source-coverage residuals remain open, including the earlier printed-p33 gap.
- Ten temporal-scope residual groups cover the 23 held candidates.
- Historical candidate CSVs remain unchanged/read-only.

## Execution boundary

`history_feedback=0`; `conditions_compiled=0`; `execution_unlocked=0`; Product/runtime authorization false. No shared Core semantics, other-palace artifacts, Governance, or Product files changed. No new primitives, independent time scale, quantitative weight, probability, or decay was introduced.

## Validation

Exact-head full `python -m pytest -q`, Product JS adapter syntax, deterministic repository audit with `--fail-on-p0`, Repository Governance v1 / P03 write-set validation, and exact-main/base/head verification remain required before merge. Record the final PR head SHA and passing run identifiers in the PR/Issue final gate note after all file writes are complete.
