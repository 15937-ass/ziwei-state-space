# Product Source-Only Vertical-Slice Blocker Handoff v0.1

Tracking Issue: #655  
Lane: PRODUCT_ONLY  
Work unit: PRODUCT_SOURCE_ONLY_VERTICAL_SLICE_BLOCKER_HANDOFF  
Snapshot date: 2026-10-22

## Purpose

This handoff records the source-owned Knowledge inputs that remain absent from the active Product dependency set. It separates the current active Product KIB from candidate/other Knowledge files on main and from historical impact reports.

All immutable source artifacts in `source_artifacts` remain pinned by Git blob SHA, and the tests recompute each digest from the exact file bytes. Recovery-state YAMLs are different: `product/PRODUCT_STATE.yaml`, `knowledge/KNOWLEDGE_STATE.yaml`, and the recorded Knowledge shard state files are mutable recovery caches. Their status is captured in dated, checkpointed snapshot metadata (`snapshot_date` and `snapshot_main_commit`), not as immutable source-artifact digests. Advancing a cache later must not invalidate this historical handoff; the normative source and contract artifacts remain strictly pinned.

## Verified Product baseline

- Active lock: PRODUCT_KNOWLEDGE_LOCK_V0_3.
- Active bundle: KIB-PRODUCT-20261021-V0_3, promoted by Product Issue #518.
- Active bundle source commit: eaa33deeb77a4f982bc13121c06cad657975177b.
- auto_refresh is false.
- K_response is active with 22 locked artifacts. The active component contains Career temporal-eligibility evidence, but that audit has 0/9 candidates eligible for the current temporal compiler; it is not a canonical temporal-reaction specification.
- K_manifest is EMPTY_NOT_READY with zero artifacts.
- The production temporal-response, manifestation ontology, and manifestation mapping registries are all empty and blocked.

The existing PRODUCT_KNOWLEDGE_IMPACT_V0_1.json is a bootstrap report for KIB v0.1 and candidate KIB-CANDIDATE-ISSUE-500-V0_1. It is not a current promotion decision for active KIB v0.3. A new explicit candidate and impact report are required when accepted source artifacts become available.

## Live Knowledge work check

The Knowledge coordinator reports no current known live work. CORE, P09 Career, and P10 Property shard caches each report ACTIVE_NO_ACTIVE_WORK with null active issue/PR. Repository issue/PR searches for KB-WP07B, KB-WP06B, KB-WP06C and the corresponding producer names did not verify an active Knowledge producer Issue/PR. The current Product handoff Issue #655 is excluded from those results.

The future gate HG-WP06B-MANIFESTATION-ROOT-01 is not a current request by itself. The Knowledge coordinator explicitly says historical/future gates are not current PI requests unless a live shard Issue names them.

## Dependency conclusions

### KB-WP07B — Temporal Reaction Specification

The production registry remains EMPTY_UNTIL_KB_WP07B_STRUCTURED_NORMALIZATION.

- The active K_response bundle contains the Career eligibility summary and CSV, but the Career audit reports 9 candidates audited, 0 eligible, 8 blocked, 1 case-support-only exclusion, and no executable pilot.
- Closed Knowledge Issue #544 audited 35 P10 temporal rows and reported zero eligible reactions under the current contract (19 blocked reusable candidates and 16 case-support-only exclusions). That issue is historical eligibility work, not an active shared temporal-reaction specification.
- No active Knowledge producer Issue/PR for the shared specification was verified.

The required source-owned artifact must preserve natal/temporal separation, source-explicit path dependence, time-layer precedence/conflict, unresolved state, and the distinction between temporal activation and a real-world event.

### KB-WP06B — Manifestation Ontology

The production ontology registry remains EMPTY_PENDING_KB_WP06B and the active K_manifest component contains zero artifacts. No active Knowledge producer Issue/PR was verified.

The Knowledge-owned artifact must carry stable node identity, hierarchy, domain, abstraction level, source-supported labels, source rule IDs, event specificity, ambiguity notes, and source-supported probability status. Product must not invent ontology nodes or probabilities.

### KB-WP06C — Manifestation Hypothesis Registry

The production mapping registry remains EMPTY_PENDING_KB_WP06C and the active K_manifest component contains zero artifacts. No active Knowledge producer Issue/PR was verified.

The Knowledge-owned mapping artifact must preserve the distinctions EXPLICIT, TRANSPARENT_INFERENCE, CASE_SUPPORT_ONLY, and HYPOTHESIS. Case frequency must not be promoted into a canonical mapping or turned into probability without source support.

## Product-side consumption sequence

When a valid Knowledge artifact is accepted on main:

1. Verify the source artifact, source commit, schema/contract version, exact digest, and semantic digest.
2. Build an explicit candidate KIB from active KIB v0.3; do not use Knowledge main as an implicit active dependency.
3. Verify the candidate and produce a fresh active-v0.3 versus candidate semantic-impact report.
4. Apply only the direct and reachable rebuilds required by the report: K_response currently maps to READINESS_REBUILD; K_manifest maps to MANIFESTATION_REBUILD. Future artifacts are IF_PRESENT until they exist.
5. Supply deterministic evidence for every required validation and evaluate the promotion gate. Missing validation means BLOCKED.
6. Only a separate explicit Product promotion work unit may update the active lock after PROMOTABLE; preserve the previous bundle for rollback.

## What this handoff does not do

- It does not add temporal rules, manifestation ontology nodes, or manifestation mappings.
- It does not change the active KIB or lock.
- It does not convert eligibility evidence into executable semantics.
- It does not activate Forecast Ledger.
- It does not claim canonical fidelity, expert-method fidelity, or predictive validity.

Forecast Ledger remains gated until the source-only N -> E -> tau -> M0 vertical slice is executable.
