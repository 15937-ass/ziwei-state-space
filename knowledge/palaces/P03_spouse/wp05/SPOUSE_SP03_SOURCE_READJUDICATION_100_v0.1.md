# P03 SP03 — source-first re-adjudication of spouse candidates 201–300

**Status:** source review complete; exact-head validation status is authoritative in the live PR and its matching GitHub Actions run; this file does not claim CI status.  
**Issue:** #797  
**Lane / shard:** `KNOWLEDGE_ONLY / P03 夫妻宫`  
**Source:** `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》, 下篇·宫垣论·夫妻宫  
**Approved scan SHA-256:** `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`  
**Historical index SHA:** `f28a3df5f4006f5a1069896514f565f9af8f86a0`

## Source boundary

Directly inspected the original scan images for PDF physical pp19–20, covering printed pp37–39 for this batch. Physical p19 contains printed pp37–38; physical p20 contains printed pp39–40. Printed p40 was used only to confirm the page boundary and is outside this batch. The local PDF SHA-256 matches the approved source pin. Text extraction was used only to locate passages; the original scan is authoritative.

The historical index `validation/wp05/SP03_spouse_projection_review_201_300.csv` is read-only acceleration input. Its `SOURCE_SPAN_VERIFIED` flags are not proof. The old `validation/wp05/SP03_SPOUSE_PROJECTION_REVIEW.md` says 100/100 verified, but the accepted SP02 source-section inventory explicitly marks the relevant SP03 spans as inventory-only/not rule-reviewed. The historical 81/19 split was therefore not reused as a target.

## SP03-201…300 result

| Measure | Result |
| --- | ---: |
| Historical candidate rows directly reviewed | 100 |
| Candidate rows promoted as source-grounded records | 87 |
| Source records produced, including four unindexed gap claims | 91 |
| Reusable projection/method records | 72 |
| `CASE_SUPPORT_ONLY` records | 19 |
| Held for unsupported/over-specific temporal layer | 13 |
| Deduplicated rows | 0 |
| Historical feedback | 0 |
| New shared semantics / primitives / quantitative weights | 0 |

The historical rows `SP03-211…213`, `SP03-224…226`, `SP03-258…261`, and `SP03-280…282` remain held. The first group says “流年大运的枢纽” while the index assigns only YEAR; the other groups say “吉凶克应之枢纽” without naming YEAR or DECADE. None is silently compiled as a YEAR trigger.

## Important source-first corrections

- `SP03-201/202`: preserve the separate female/male branches; the male branch retains “妻子有独立事业，否则便多是非”.
- `SP03-204/205`: direct scan states a general age-gap relation and that 天寿 makes the difference larger. These are treated as source-grounded relational projections, not automatically copied from the historical case-only flag; no numeric age threshold is inferred.
- `SP03-207/209/210`: preserve alternatives (premarital setbacks OR reunion with a former partner; and premarital setbacks OR a period of separation after marriage).
- `SP03-215/217/241`: where the original sentence omits the subject of “化禄/化忌”, the record explicitly preserves the ellipsis instead of adding an unstated star subject.
- `SP03-250/251`: retain the parent context of 子午武府, the male-chart condition and the antecedent 武曲化禄 where required; do not treat the subordinate clauses as context-free rules.
- `SP03-267/275/285/291/293/299`: preserve source alternatives as OR; do not turn them into all-required AND. The repeated wording in the printed accident clause for `SP03-285` is preserved rather than silently rewritten.
- `SP03-284/295`: retain the Sun/Moon strength comparison and 福德宫 dependency as cross-palace context.
- Health, accident, second-marriage, informal-marriage and narrow occupational claims remain `CASE_SUPPORT_ONLY` where appropriate. Traditional illness wording is not modern medical prediction.

## Carry-forward source gaps

- **P03-SP02-GAP-001 (printed p37): PARTIALLY RESOLVED.** The explicit “以不见煞为佳” and “申宫又劣于寅宫” claims are recorded. The transit clause still visibly reads `机录像`; the interpretation remains unresolved. “经行至” does not uniquely specify YEAR versus DECADE, so that timing clause remains held. Do not replace it with `机梁紫破`.
- **P03-SP02-GAP-002 (printed p37): RESOLVED.** Two supplemental records preserve the female and male branches separately, both as `CASE_SUPPORT_ONLY`.
- **P03-SP02-GAP-003 (printed p37): RESOLVED.** `SP03-201/202` preserve the female/male branches and the male “否则” qualifier.
- **P03-SP02-GAP-004 (printed p35) and GAP-005 (printed p36): CARRIED FORWARD.** They are outside the primary span and remain open unless later direct evidence genuinely resolves them.
- **P03-SP01-GAP-001 (printed p33): still open.**

Nine historical gap entries remain tracked; four are open or partially open. Four new grouped temporal residuals were added, covering 13 candidate rows. Cumulative temporal residuals are now 16 groups / 40 candidate rows.

## Cumulative P03 checkpoint

Across SP01, SP02 and SP03:
- 300 candidate rows reviewed.
- 253 candidate rows promoted; 45 held; 2 deduplicated.
- 258 source records (207 reusable; 51 `CASE_SUPPORT_ONLY`).
- 4 source-coverage gaps remain open/partially open; 9 gap entries are tracked.
- 16 temporal residual groups / 40 candidate rows remain explicit.

## Execution boundary

`conditions_compiled=0`; `execution_unlocked=0`. No Product/runtime authorization, shared Core semantic change, other-palace write, history-feedback promotion, new qi/memory/time primitive, numeric weight, probability or decay is implied. Source fidelity, structural checks, internal reconstruction and empirical validity remain separate.

## Validation

The exact PR base/head and matching GitHub Actions run are recorded in the live PR after the artifact commit. Required gates: full `python -m pytest -q`, Product JS adapter syntax, deterministic P0 audit, Repository Governance v1 and P03 write-set validation. A historical green run or the old SP03 report is not substituted for this exact-head gate.

## Next source anchor

After this bounded batch is accepted, continue with **SP04-301…400**, beginning at printed p39 / PDF physical p20 and continuing through the Wuqu Chen-Xu / Si-Hai and Tian Tong/Lianzhen material. The SP04 historical index remains read-only; inspect the original scan directly. Do not start that batch inside this Issue.
