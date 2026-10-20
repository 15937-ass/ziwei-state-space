# Issue #407 Execution Evidence

Status: **FINAL VALIDATION GREEN; EVIDENCE-SYNC RERUN REQUIRED**

Execution runtime: GitHub Actions standard public-repository runners.

## Candidate result

- Career rules after merge: **134 -> 165**
- Review-04 selected mappings: **31/31**
- readiness mapped-ID scope: **352 -> 452**
- scoped disposition: **165 compiled / 287 blocked-context / 0 unselected static candidates**
- no Knowledge file is edited

## First Product run and repair

The first full-suite run after Review-04 integration produced:

- **1739 passed / 3 failed**
- all four Product P1/B02 regressions were green.

All three failures were Product-owned historical assumptions:

1. a generic "wrong star" transformation test expected 天同化科 to produce no Career evidence,
   but Review-04 legitimately adds general 天同 rules that activate on 天同 regardless of 化科;
2. Review-02 batch tests pinned the global registry total at 134;
3. Review-03 batch tests pinned the global registry total at 134.

Repairs:
- transformation fail-closed assertions are now scoped to the transformation-specific 武曲 rules,
  while valid general 天同 rules are allowed to coexist;
- historical Review-02/03 batch tests now verify their selected subset and handoff integrity without
  freezing the future global Product rule count.

No rule condition, source meaning, Knowledge artifact or runtime evaluator was weakened.

## Final semantic/runtime validation

Validated candidate head:
`9459a5b31f3a5557d73e9137db6900b759900c67`

The run was triggered after main had advanced to:
`2edbd201ed25a1de00121346b43f5f60db47d0c1`

Results:
- repository-quality-gate #1664: **PASS**
- full pytest: **1748 passed / 0 failed**
- JS syntax: **PASS**
- deterministic P0 audit: **PASS**
- Product governance validation: **PASS**
- product-p1-dual-engine #460: **PASS**
- product-p1-b02-calendar #82: **PASS**
- product-p1-b02b-zi-day #57: **PASS**
- product-p1-b02c-temporal #51: **PASS**

## Evidence-sync rerun

This commit updates only Product execution evidence after the green semantic/runtime run.
The automatic PR workflows must pass again on this exact head before merge.

## Limits

These deterministic gates establish Product source/condition/projection integrity and regression
consistency only. They do not establish empirical predictive accuracy, temporal production,
numeric probability, causal truth or guaranteed real-world career outcomes.
