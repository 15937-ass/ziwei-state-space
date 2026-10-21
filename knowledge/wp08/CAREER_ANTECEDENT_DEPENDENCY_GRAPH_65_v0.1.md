# Career Antecedent Dependency Graph 65 v0.1

Status: **65 / 65 explicit references represented — graph resolved, Product compiler not implemented**

Issue #505 corrects the initial 50-row count: closure v0.13 has **65** rows with `antecedent_mode=EXPLICIT_RULE_REFERENCE`. Of these, 50 still carry `ANTECEDENT_DEPENDENCY`; 15 already have their reference gate source-resolved. A complete graph must retain both groups.

## Graph census

- explicit-reference nodes: **65**
- explicit edges: **66**
- single-parent nodes: **64**
- multi-parent nodes: **1** (CA05-473)
- exact `前格`: **28**
- `前格` + continuation: **36**
- non-`前格` additive continuation: **1** (CA09-847)
- cycles: **0**
- max explicit-reference depth: **2**
- only internal reference edge: **CA02-171 -> CA02-170**; CA02-170 then points to base rule CA02-169.

## Why this matters

The old `ANTECEDENT_DEPENDENCY` label mixed two questions: whether the source reference itself was known, and whether a runtime compiler could traverse it. The first question is now explicit and auditable for all 65 rows. The second remains intentionally unresolved at Product/runtime level.

There is therefore no license to parse “前格” by nearest-text heuristics. The parent rule IDs already stored in canonical knowledge are the only authority for this graph.

## CA05-473

The source gives a civil public-office branch and a martial public-office branch, then says `亦以煞曜不居本宫为贵`. The two parent IDs therefore represent **alternative source branches**, with one shared local qualifier:

`AND[ANY_PARENT_BRANCH(CA05-471, CA05-472), LOCAL_DELTA(煞曜不居本宫)]`

They must not be compiled as `CA05-471 AND CA05-472`.

## Compiler-gated rows

Among the 50 rows still carrying `ANTECEDENT_DEPENDENCY`:
- dependency only: **27**
- dependency + other blockers: **23**
- dependency-only with blocker-free parent: **3** — CA05-420, CA07-639, CA07-682
- dependency-only whose parent remains source-underdetermined: **24**

The three candidates are only **Knowledge-side dependency compiler candidates**. This issue does not remove their blocker, compile a condition, or unlock execution.
