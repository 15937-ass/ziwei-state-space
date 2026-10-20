# Issue #400 Execution Evidence

Status: **ACCEPTED ON MAIN**

Execution runtime: GitHub Actions standard public-repository runners.

Merged implementation PR: #402
Merged commit: `665006e6c580ed03b677b1e39b60f6566a57bfd8`

## Accepted Product result

- Career rules: **104 -> 134 accepted NATAL rules**
- Review-03 selected mappings: **30/30**
- readiness mapped-ID scope: **252 -> 352**
- scoped disposition: **134 compiled / 218 blocked-context / 0 unselected static candidates**
- source rows outside this Product readiness scope: **536**

## Compatibility issue resolved

The initial Review-03 full-suite run produced **1654 passed / 7 failed**.
All seven failures came from historical Product tests that assumed a 武曲 transformation
fixture could activate exactly one rule.

Review-03 correctly adds three general 武曲 rules whose approved Product conditions are simply
事业宫有武曲:

- CA04-336 — finance/taxation work scene
- CA04-338 — metal/engineering/technical-craft orientation
- CA04-341 — action orientation distinct from financial planning

Therefore:
- 武曲化科 correctly activates CA04-336 + CA04-338 + CA04-341 + CA04-347;
- 武曲化忌 correctly activates CA04-336 + CA04-338 + CA04-341 + CA04-349;
- plain 武曲 activates the three general rules but not the transformation-specific rules;
- wrong star or wrong palace still fails closed.

The repair changed only Product tests/expectations. It did not add exclusion conditions,
modify source meaning, or touch Knowledge files.

## Final implementation validation

Final implementation head before squash merge:
`cf7afd640179af1353b79dd655829f03e2319f2e`

Results:
- repository-quality-gate #1654: **PASS**
- full pytest: **1661 passed / 0 failed**
- JS syntax: **PASS**
- deterministic P0 audit: **PASS**
- Product governance validation: **PASS**
- product-p1-dual-engine #454: **PASS**
- product-p1-b02-calendar #76: **PASS**
- product-p1-b02b-zi-day #51: **PASS**
- product-p1-b02c-temporal #45: **PASS**

## Limits

These deterministic gates establish Product source/condition/projection integrity and regression
consistency only. They do not establish empirical predictive accuracy, temporal production,
numeric probability, causal truth or real-world career outcome certainty.
