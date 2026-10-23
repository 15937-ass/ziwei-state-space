# Validation Evidence — Issue #505 Career Antecedent Dependency Contract

Runtime: ChatGPT repository session over canonical main and approved Zhongzhou source evidence.

## Scope correction
The initial work-unit count of 50 captured only rows still carrying ANTECEDENT_DEPENDENCY. Before implementation the canonical closure was re-counted and showed **65 explicit antecedent-reference rows** total: 50 compiler-gated + 15 already reference-resolved. The implementation therefore covers all 65.

## Graph result
- explicit-reference nodes: 65
- explicit edges: 66
- exact 前格: 28
- 前格 + continuation: 36
- explicit non-前格 additive continuation: 1
- cycles: 0
- maximum explicit-reference depth: 2
- only internal reference chain: CA02-171 -> CA02-170 -> CA02-169
- unresolved parent IDs: 0

## Source adjudication
CA05-473 is explicitly represented as branch union, not parent conjunction:
AND[ANY_PARENT_BRANCH(CA05-471,CA05-472), LOCAL_DELTA(煞曜不居本宫)].

## Readiness
Among 50 compiler-gated rows:
- dependency-only: 27
- dependency + local blockers: 23
- dependency-only parent-ready: 3 (CA05-420, CA07-639, CA07-682)
- dependency-only inheriting source-underdetermination: 24

No condition is compiled and no execution is unlocked.

## Critic correction

A pre-merge critic pass found that the first graph draft used the label `REFERENCE_GATE_ALREADY_RESOLVED_RULE_READY` for 11 rows based only on their **row-local** blocker list. That was unsafe because all 11 inherit parent/ancestor source uncertainty.

The corrected graph:
- removes the ambiguous RULE_READY label;
- propagates parent blockers transitively;
- records CA02-171 inheriting `OPEN_VALENCE_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED` through CA02-170 -> CA02-169;
- records already-reference-resolved/no-local-blocker = 11 but effective-condition-ready = 0;
- marks parent IDs outside the contextual-activation closure as unassessed rather than blocker-free;
- preserves the same three compiler candidates: CA05-420, CA07-639, CA07-682.

## Final deterministic gate
Exact-head G8 repository-quality-gate is required before merge: full pytest, JS syntax check where present, P0 audit, and Knowledge governance validation.
