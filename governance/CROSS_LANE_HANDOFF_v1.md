# Cross-lane dependency handoff v1

Status: operational clarification of `GOVERNANCE.md`, `governance/KNOWLEDGE_SHARD_EXECUTION_v1.md` and the Product Knowledge promotion contract. GitHub Issues/PRs and accepted `main` remain authoritative; this file is not a work queue or permission to change source semantics.

## One blocker, one accountable producer and consumer

A cross-lane blocker is recorded in the consumer Issue or a linked, bounded producer Issue. The two Issues must identify:

| Field | Required meaning |
| --- | --- |
| Producer | Lane, shard (for Knowledge), live Issue, permitted paths, and the source or contract it will review. An unassigned roadmap work-package name is not a producer. |
| Consumer | Live Issue or explicitly marked backlog Issue and the exact capability or KIB component waiting. |
| Missing input | Artifact type/schema, source spans or rule IDs, epistemic status, and the particular contract predicate that is unsatisfied. |
| Dependency | Link to the upstream Issue, and whether it needs an accepted `main` artifact, a Human Gate, or an explicitly allowed negative finding. |
| Unblock evidence | Accepted merge commit, artifact paths and digest/schema, source/semantic review, validation run, unresolved gaps, and the consumer's next bounded action. A green upstream PR alone is not accepted input. |
| Safe parallel work | Specific work that does not consume the missing semantics, its lane/WIP slot, and its stop condition. If none exists, say so. |

Do not create a second global status ledger. Keep the links and evidence in the existing Issues/PRs; lane state YAMLs are recovery caches. When a producer closes with zero eligible records or an unresolved source conflict, hand off that **negative result** and the next source or gate decision. Do not leave a consumer indefinitely waiting for a deliverable the producer disproved.

## State transitions and ownership

1. `READY_TO_START` is backlog, not an ACTIVE worker. Before promotion, query live Issues/PRs and enforce Product <=1, Governance <=1, Knowledge Core <=1, palace total <=4 and each palace <=1. An old open roadmap Issue or archived PR without an active bounded work unit does not consume a slot.
2. `ACTIVE` requires the existing Definition of Ready, a current-main branch using the lane/shard prefix, and its own write set. A branch/PR being prepared is execution, not a way to hide a second ACTIVE unit under a backlog label.
3. `WAITING_DEPENDENCY` names the precise missing artifact/gate and producer Issue. Do source-neutral independent work only in a separate bounded unit when that lane slot is free. Do not poll or rewrite the same blocker report as work.
4. A producer PR records accepted source spans, gaps/UNKNOWN, exact-head tests and its merge commit. A palace worker records a `KNOWLEDGE_CORE_GAP` for genuinely shared semantics and continues unrelated local review fail-closed; only Core resolves shared meaning. Human Gate stays with the relevant decision.
5. The consumer rechecks the accepted artifact on current `main`. It may then change from waiting to ready **only if its specific contract predicate is satisfied**. Source evidence, schema validity and an approved gate are distinct; a candidate ledger or eligibility audit is not an executable specification.
6. `DONE` requires the Issue's acceptance, validated PR merge and a handoff link or explicit negative disposition. A stale state-cache field is repaired through its owning lane; it does not override live Issue/PR evidence.

No lane writes into another lane to clear a blocker. A source review, ontology decision, Product adapter implementation, KIB promotion and production activation are separate work units and PRs.

## Knowledge and Product scheduling

| Work | Can proceed while other inputs are pending | Must wait before consumer activation |
| --- | --- | --- |
| Twelve-palace source audit | Distinct palace shards may review accepted-main sources within existing worker limits. A Core gap blocks only affected interpretations; unrelated source review continues. | Cross-palace universal meaning and another unmerged palace branch cannot be adopted locally. |
| WP07B dynamic reaction | Palace-local source/eligibility review and one Core shared-contract unit may run concurrently with different write sets. | A temporal reaction enters Product only after source-reviewed condition, natal antecedent, time-layer and effect contract are accepted; activation is not an event outcome. |
| WP06B ontology | Source-native candidates and a Core root-decision packet may be prepared. | A new universal family/root requires its Human Gate; Product cannot invent nodes. |
| WP06C mapping | Palace-local source candidate indexing can use source wording with unresolved ontology reference and explicit epistemic tier. | Canonical node crosswalk/production mapping waits for accepted relevant WP06B IDs and source-reviewed mapping; case support/hypothesis remains non-executable. |
| Product architecture and validation | Existing deterministic N/E/tau/M0 interfaces, contract fixtures, case reconstruction and independent PL7 data-quality work can progress in the single Product slot, one bounded unit at a time. | New dynamic runtime content, M0 production mapping and Forecast Ledger activation wait for their specific accepted inputs and required vertical-slice validation. |
| Product Knowledge update | Impact tooling and locked-baseline tests are already available. | A fresh candidate KIB must pin accepted source commit/digests, classify semantic impact, perform affected rebuild/recompile/replay, validate, then use a **separate** explicit promotion unit. Knowledge `main` never auto-refreshes the active Product lock. |

An accepted negative source audit can close its bounded review Issue while the consumer remains blocked on a different source/gate. It must not be described as compiler-ready merely to create throughput.

## Merge and stale-PR discipline

- Keep one primary Issue and one lane per PR. Research/PR preparation can overlap across permitted Knowledge shards; Knowledge canonical merge is serialized against current `main`. Rebase/update a merge-ready PR after intervening main changes and re-run its exact-base/head checks. Do not multiply stacked PRs to avoid a blocker.
- Before promoting a waiting unit, inventory live ACTIVE Issues and open PRs. Classify old PRs as current implementation, superseded candidate, archived diagnostic, or independent backlog by reading their Issue, diff and merge status. An open PR is not automatically an active worker or accepted artifact.
- If a PR is already represented by accepted `main`, document equivalence and close it; if not, preserve it without silently merging stale changes. Record the disposition in the Issue. Retire stale branches only after checking that they contain no unique accepted evidence.
- The quality gate tests implementation, not source truth. Source audit, Human Gate, KIB impact and Product runtime authorization remain separate checks.
