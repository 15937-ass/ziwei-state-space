# P07 Migration M06 Source-Review Evidence

- Issue: #645
- Lane / shard: KNOWLEDGE_ONLY / P07 迁移宫
- Branch: `knowledge/p07-645-migration-m06-canonical`
- Source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》, printed pp.119–122
- Scan pages visually inspected: PDF pp.60–61
- Scope: source-first re-adjudication of M06-501…M06-590 only

## Source review checkpoint

- 90/90 candidate IDs accounted for.
- 89 canonical rule records; M06-590 is a chapter-boundary marker, not a projection rule.
- 76 reusable projections; 13 CASE_SUPPORT_ONLY; 1 boundary marker.
- 33 candidate source-page labels corrected; 48 source-resolution changes recorded.
- 24 historical “前格” antecedents expanded; no unresolved inherited-condition shorthand remains.
- One source-wording ambiguity is explicitly recorded for M06-503: the scan reads “在迁移宫的驻突发”. Only a broad “突发” scene is retained; no specific accident/injury claim is inferred. This is a text ambiguity, not a coverage gap.
- M06-579 historical PATH_DEPENDENT_GATE re-adjudicated to a source-internal ordered outcome; canonical history gate count for this batch is 0.
- Only M06-540…542 retain explicit YEAR scope; no new temporal layer or generic event timer.
- No new source-coverage gaps in printed pp.119–122.
- Four printed-p118 Tianxiang gaps and P07-M03-GAP-001 / P07-M03-GAP-012 remain carried forward.
- Accepted cumulative accounting after M06: 590 reviewed, 519 reusable, 70 CASE_SUPPORT_ONLY, 1 source-boundary marker; 10 previously accepted history-feedback gates remain unchanged.

## Source and count integrity

The legacy M06 tail summary's cumulative 521 reusable / 69 CASE_SUPPORT_ONLY is not treated as canonical. It conflicts with the accepted M05 baseline of 443 / 57 and counts M06-590's chapter boundary as a reusable projection. The source-first accounting is 519 / 70 / 1 boundary marker.

## Validation

The source artifacts and deterministic regression tests are committed on the work branch. Repository validation is **pending until the exact final PR head** runs the standard repository quality gate, including full pytest, Product JS adapter checks, deterministic P0 audit, Repository Governance v1, and exact-main/base/head comparison. No command is reported as passing before execution. The final validation run and exact base/head SHAs must be recorded in the PR conversation.

## Boundaries

- No Product, Core, Governance, global closure audit, or other-palace files changed.
- No source truth is changed by empirical feedback.
- No probability, numeric weight, decay, causal claim, new qi primitive, new memory type, or Product/runtime authorization is introduced.
- M06 does not close the four printed-p118 Tianxiang gaps or the two carried-forward M03 gaps.
