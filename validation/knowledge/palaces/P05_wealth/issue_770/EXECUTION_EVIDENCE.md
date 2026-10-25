# Execution Evidence — P05 Pojun source-first audit (Issue #770)

Status: DRAFT — source audit is complete; merge requires the latest exact-head repository-quality-gate run to pass.

## Source integrity and boundary
- Approved source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》.
- SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.
- Directly inspected physical PDF p46 left half (printed p91) and physical p46 right half (printed p92); physical p47 left half confirms the next heading is printed p93 `疾厄宫`.
- Scope: printed p91 heading `14 破军` through the final 破军 sentence on printed p92; stops before printed p93 `疾厄宫`.
- The local PDF hash matches the registered source hash. PDF text extraction was only a secondary locator; original page images control.

## Reconciliation
- Historical candidates W09-889…W09-900: 12 reviewed exactly once against original page images.
- Additional source atoms W09-905…W09-922: 18 reviewed; 17 promoted and W09-909 held due the unresolved printed connective `同破财损耗极大`.
- Total source-first records: 30; 29 promotions proposed; W09-909 remains unpromoted.
- Candidate condition/scope corrections: W09-897 preserves the source's `破军化禄，或会禄权科者` disjunction; W09-900 preserves the adverse-recovery gate `无吉化吉会，且见煞曜`.
- Two source-local ambiguities remain OPEN: W09-SG-015 (`同破财损耗极大`) and W09-SG-016 (`纵会占化吉曜者亦然`). Clear neighboring clauses are scoped separately; no silent emendation.
- Accepted P05 baseline before this batch: 765 reusable rules; expected cumulative count after merge: 794.
- Inherited gap dispositions remain unchanged: W05-SG-002 PARTIALLY_RESOLVED; W06-SG-001…005, W08-SG-001…005 and W09-SG-006…014 OPEN. The two new gaps bring the tracked residual count from 20 to 22.

## Write set
P05-only paths: Pojun readjudication, time-scope and gap sidecars, canonical summary, P05 state, P05-local tests, and this execution evidence. No Product, Governance, shared Core, historical candidate index, previously accepted Qisha/Tianliang records, or other-palace paths are changed.

## Validation
- Exact base: `cb48ac8fe6316eb9644448c99c596b72d72776c3` (accepted Qisha PR #767 merged).
- Branch: `knowledge/p05-770-source-first-pojun-p91-p92`.
- Draft PR: #771. Exact final head and repository-quality-gate run will be recorded in the PR handoff after the final state-pointer commit.
- Merge requires full pytest, Product JS adapter checks, deterministic P0, Repository Governance v1 and P05 shard/write-set validation to pass on that exact head.
- No Product/runtime authorization or empirical predictive-validity claim is implied.
