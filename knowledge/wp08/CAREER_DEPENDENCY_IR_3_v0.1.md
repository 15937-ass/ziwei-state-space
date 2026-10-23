# Career Dependency IR 3 v0.1

Status: **3 / 3 KNOWLEDGE IR READY — NO PRODUCT CONDITION COMPILATION**

Issue #508 takes the only three dependency-only Career rows whose explicit parents are fully assessed and blocker-free, and materializes their inheritance as a machine-readable Knowledge IR.

## The three rows

- **CA05-420 -> CA05-419**: the source's `前格` reuses the condition “天同化忌又见左辅右弼”; the child projection is the further conclusion that personal execution / self-reliance remains required.
- **CA07-639 -> CA07-638**: `前格` reuses “贪狼与左辅右弼同度”; the child projection is that the operation has visible scale/presence.
- **CA07-682 -> CA07-681**: `前格` reuses “子午巨门得禄”; the child projection is “不宜出锋头”.

All three have `local_delta = null`.

## What inheritance means here

The IR is deliberately narrow:

`RULE_CONDITION(parent_id) -> child condition scope`

It **does not** inherit the parent's projection, outcome, target, valence or causal wording. It also never discovers a parent from textual adjacency. The parent ID was already source-adjudicated by the 65-node dependency graph.

## Why the blocker can move

For these three rows only, the remaining `ANTECEDENT_DEPENDENCY` blocker represented a missing Knowledge-side dependency representation, not a source-meaning gap. The parent condition is locally represented, the parent has no current blocker, the edge is explicit, and there is no child delta.

Therefore v0.15 may move them from `DEPENDENCY_COMPILER_GATED` to `LOCAL_STRUCTURE_READY` while still keeping:

- Product condition compilation: **0**
- runtime authorization: **0**
- execution unlock: **0**

This follows the same boundary used elsewhere in Knowledge: resolving a representation gate does not itself execute the rule.

## Negative controls

- **CA02-171** is not promoted. Its immediate parent CA02-170 is row-locally clear, but the chain inherits an open-valence blocker from CA02-169.
- **CA03-236** is not promoted because CA03-234 remains source-underdetermined.
- **CA04-323** is not promoted because it has independent local blockers and its parent condition is outside this closure's readiness assessment.

## Closure impact

- ANTECEDENT_DEPENDENCY: **50 -> 47**
- DEPENDENCY_COMPILER_GATED: **27 -> 24**
- LOCAL_STRUCTURE_READY: **23 -> 26**
- no-current-blocker rows: **23 -> 26**
- source-underdetermined rows: **201 -> 201**
- source-resolution changes: **45 -> 45**
- conditions compiled: **0**
- execution unlocked: **0**
