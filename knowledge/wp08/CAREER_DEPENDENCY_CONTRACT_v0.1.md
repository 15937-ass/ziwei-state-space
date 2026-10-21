# Career Dependency Contract v0.1

Status: **KNOWLEDGE REPRESENTATION CONTRACT — NO PRODUCT EXECUTION**

This contract defines how already source-adjudicated Career antecedent references may be represented. It is not a general Chinese-language parser and not a global Zhongzhou inheritance rule.

## Hard rules

1. **ID over adjacency.** An antecedent exists only when canonical knowledge contains an explicit antecedent rule ID. Nearest text, previous sentence, or tokens such as 前格/又见/更见 cannot create a new edge.
2. **Parent composition is explicit.** One parent means `SINGLE_PARENT`. Multiple parents require a source-adjudicated composition; the only current case is CA05-473 = `SOURCE_BRANCH_UNION_SHARED_QUALIFIER`.
3. **Uncertainty propagates.** Resolving the graph does not resolve a parent's source blocker. A target with a source-underdetermined parent remains fail-closed.
4. **Local delta is independent.** Text after 前格, or additive text such as 更见, is preserved as a local continuation. It is compiled only if its own semantics are separately resolved.
5. **No runtime claim.** Knowledge graph resolution is not Product compilation. `conditions_compiled=0`, `execution_unlocked=0`.

## Current corpus shape

The graph is small and structurally bounded: 65 nodes, 66 edges, no cycles, maximum explicit-reference depth 2. Only one edge points to another explicit-reference node: CA02-171 -> CA02-170; CA02-170 -> CA02-169 completes that two-hop chain.

The surface distribution is 28 exact 前格, 36 前格 with local continuation, and one explicit additive continuation (CA09-847). These counts describe this corpus only.

## Readiness

The 50 compiler-gated rows divide into 27 dependency-only and 23 dependency-plus-local-blocker rows. Of the dependency-only rows, only CA05-420, CA07-639 and CA07-682 currently have blocker-free antecedents. The other 24 must carry inherited source-underdetermination even after a future dependency compiler exists.

No Human Gate is needed for this representation. A Human Gate is required before any future step that proposes implicit parent inference, a universal “前格” parser, or cross-domain inheritance semantics.
