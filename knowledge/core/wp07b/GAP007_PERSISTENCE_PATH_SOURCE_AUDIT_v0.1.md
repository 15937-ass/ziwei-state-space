# WP07B GAP-007 persistence/path source audit v0.1

**Issue:** #945  
**Verdict:** DESCRIPTIVE_PATH_SUBTYPES_CONFIRMED_NO_EXECUTION  
**Source:** SRC-ZZ-003, 《中州派紫微斗数深造讲义（下）》  
**PDF SHA-256:** `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`

## Executive result

GAP-007 contains two distinct source forms. Both remain fail-closed, but they must not be represented as one shared persistence operator:

1. **CA09-851 — multi-year consecutive annual window.**
2. **TP03-248 — same-year antecedent branch with an event-consequence path.**

The source supports descriptive classification only. No timer, duration threshold, favorable-year predicate, event-history operator, probability, or execution behavior is authorized.

## 1. CA09-851 — Career printed p154 / PDF physical p77

Direct visual review confirms the sentence:

> 故当破军守事业宫时，只须连续有三四年良好的流年，即能创出事业基础。

The preceding context compares 破军 and 七杀; the following paragraph turns to 破军化禄. The temporal clause itself contains three distinct elements:

- `连续`: an explicit sequence requirement;
- `三四年`: literal approximate duration evidence, not a precise 3-year or 4-year threshold;
- `良好流年`: a period-valence judgement with no independent criterion in this source span.

The accepted Career temporal eligibility row remains `BLOCKED_MULTIYEAR_SEQUENCE`; its condition is not compiled. The current PL3-T adapter consumes one normalized temporal snapshot and the reaction compiler matches facts in one selected layer. It cannot represent the required sequence of consecutive annual observations.

### Cross-gap reconciliation

C5 #922 already defines `PERIOD_VALENCE_OR_SUPPORT` descriptively for Career phrases such as `前格流年大运良好` and `于年限不佳时`. CA09-851's `良好流年` belongs to the same source-evaluated period-valence class. C9 therefore adds CA09-851 to a versioned GAP-006 v0.2 addendum (13 rows); C5 v0.1 remains immutable.

The source handoff also references `CA09-850 / Pojun career context` with `REFERENCED_CONTEXT_REQUIRES_SEPARATE_VALIDATION`, while the Career review marks `context_is_complete_antecedent=false`. C9 preserves this as a GAP-001 descriptive cross-link; it does not rewrite or validate CA09-850.

**Disposition:** CA09-851 remains blocked by multi-year sequence, duration-as-evidence, undefined favorable-period criterion, and referenced-context validation. The existing `HG-WP07B-TEMPORAL-PERSISTENCE-01` and `HG-WP07B-FAVORABILITY-AND-GROUPS-01` remain future/not pending.

## 2. TP03-248 — Property printed p163 / PDF physical p82

Direct visual review confirms the annual structure:

> 流年田宅宫贪狼落陷，火铃同度，更见刑耗诸曜，流煞冲会，亦主火灾，见吉，则主火灾后损耗不大之装修。

The canonical condition `前格见吉` refers to the immediately preceding annual fire-risk structure. `见吉` is a same-year branch modifier. `火灾后` describes the downstream consequence; it does not prove that a fire event occurred or create a prior-event fact.

The antecedent `TP03-247` is explicitly `CASE_SUPPORT_ONLY` / `EVENT_CANDIDATE`. It cannot be promoted to an executable required antecedent. The source's `吉` remains an open valence shorthand.

**Disposition:** TP03-248 is a same-year antecedent/event-consequence path subtype, not a multi-year persistence rule. It remains `BLOCKED_PATH_AND_CASE_PARENT` and fail-closed under GAP-001, GAP-006, GAP-007 and the parent CASE_SUPPORT_ONLY exclusion in GAP-013. The persistence Human Gate does not apply to this row.

## 3. Refined GAP-007 member taxonomy

| Rule | Descriptive subtype | Other relevant blockers | Executable |
|---|---|---|---|
| CA09-851 | MULTI_YEAR_CONSECUTIVE_ANNUAL_WINDOW | GAP-001 context validation; GAP-006 favorable-period criterion | No |
| TP03-248 | SAME_YEAR_ANTECEDENT_BRANCH_WITH_EVENT_CONSEQUENCE | GAP-001 parent; GAP-006 open 吉; GAP-013 parent case-only | No |

GAP-007 remains an umbrella blocker family with two non-interchangeable subtypes. `HG-WP07B-TEMPORAL-PERSISTENCE-01` applies only to CA09-851. Any future executable event-history/path primitive for TP03-248 would require a separately scoped PI Human Gate; none is pending.

## 4. No implementation

- No exact 3-year / 4-year threshold.
- No generic PERSISTENCE, DURATION, EVENT_SEQUENCE, or GOOD_YEAR operator.
- No inference that a missing annual fact means the year was good.
- No inferred fire occurrence or event-history fact.
- No source ledger, canonical WP05 projection, P09/P10 palace file, Product, KIB, runtime, schema, or registry mutation.
- No probability, hazard rate, score, frequency, causal or empirical-validity claim.

## 5. Handoff

The versioned GAP-006 v0.2 and temporal source handoff v0.2 preserve the new cross-gap classification without rewriting accepted v0.1 inputs. All 44 temporal candidates remain zero-eligible under the current contract.
