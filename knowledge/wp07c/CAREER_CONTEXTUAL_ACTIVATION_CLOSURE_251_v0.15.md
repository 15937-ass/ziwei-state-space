# Career Contextual Activation Closure v0.15

Status: **251 / 251 — DEPENDENCY IR PILOT 3 INTEGRATED, NO PRODUCT EXECUTION**

Issue #508 materializes exact-parent condition-reference IR for CA05-420, CA07-639 and CA07-682.

## v0.14 -> v0.15

- dependency IR targets: **3 / 3**
- `ANTECEDENT_DEPENDENCY`: **50 -> 47**
- `DEPENDENCY_COMPILER_GATED`: **27 -> 24**
- `LOCAL_STRUCTURE_READY`: **23 -> 26**
- no-current-blocker rows: **23 -> 26**
- source-underdetermined rows: **201 -> 201**
- cumulative source-resolution changes: **45 -> 45**
- source-condition repairs: **13 -> 13**
- conditions compiled: **0**
- execution unlocked: **0**

The three rows inherit only the canonical condition scope of an explicit single parent. Parent projection/outcome semantics are not copied. No text-adjacency parser is introduced.

Negative controls CA02-171, CA03-236 and CA04-323 remain blocked/unpromoted, proving that immediate row-local emptiness, parent uncertainty and independent local blockers are still fail-closed boundaries.
