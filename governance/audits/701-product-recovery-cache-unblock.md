# Governance #701 — Product recovery cache unblock

Date: 2026-10-23  
Lane: GOVERNANCE_ONLY  
Risk: R1; Human Gate: NONE  
Execution record: https://github.com/15937-ass/ziwei-state-space/issues/701

## Problem and bounded result
Product #696 / Draft PR #698 records an active Issue and PR. The Governance-owned v0.4 test nevertheless required an idle execution snapshot forever. Repository run #39928963396 failed on that obsolete assertion (2603 passed, 1 failed), before its later JS/P0/Governance steps ran.

Replace only that frozen daily-state assertion with pointer-consistency checks. Keep the existing v0.4 entry checkpoint, progress, next-work and all epistemic-boundary assertions. Valid idle caches have null Issue/PR; valid active caches have a positive integer Issue and either a null or positive integer PR. Null PR permits the Issue-first/pre-PR stage. Boolean/string/nonpositive IDs, unsupported statuses, missing/duplicate fields and malformed execution blocks are rejected.

The helper reads only the controlled top-level execution fields; it is not a general YAML parser or a live GitHub verifier. Live Issue/PR still outranks state caches. No new package dependency is introduced.

## Slot reconciliation
The PI authorized the preceding concrete Governance-unblock recommendation with “可以的，继续下一轮”.
- #446 now explicitly releases its slot to #701 and is PAUSED_REQUIRES_RECONSTITUTION, not completed.
- PR #447 is paused/Draft. Its branch and original hardening deliverables are preserved; stale validation is not acceptance.
- #701 is the sole active Governance unit for this repair.
- #700 is the next nominee only after this unit is accepted and closed, with a fresh live census and explicit activation. This PR does not implement #700 or select A/B/C.
- #584 remains waiting. Other old Governance PRs are preserved, not automatically activated. PR #699 is not a valid activation or an ownership exception.

The state-file handoff is a short recovery pointer; live Issues/PRs remain authoritative. The mainline execution cache can remain idle at the accepted boundary; it must not claim future acceptance of its own PR.

## Changed paths
- tests/test_governance_product_v04.py
- governance/GOVERNANCE_STATE.yaml
- governance/audits/701-product-recovery-cache-unblock.md

No Product/Knowledge semantic/runtime files, ownership allowlists, workflows, source records, KIB locks, mappings, probabilities or maturity claims change.

## Validation evidence and acceptance boundary
Accepted input main: 085e65c509fc5f9fed8230d00d2fc07a0e01b79b.  
Real Product comparison snapshot: aca8e83a306f56bc06b403361360e9e412fbb40f, product/PRODUCT_STATE.yaml.

Local preflight:
- Python compilation passed.
- Reproduced the original assertion failure against the actual Product #698 state file.
- Direct Python execution of all nine focused test functions passed against accepted-main state.
- The same nine functions passed against the actual Product #698 active state.
- Fixture checks include consistent idle/active/pre-PR cases, thirteen invalid pointer combinations and five malformed-block cases.
- These are direct function checks, not a local full pytest run.

Required before acceptance: the existing repository-quality-gate on this exact Governance PR head, including full pytest, Product JS syntax, deterministic P0 audit and Governance base/head validation. Exact resulting head/run references and final counts belong to the linked PR's Validation section; no pending check is represented here as passed. No additional workflow or required check is introduced.

## Product handoff
Even after this Governance PR is accepted, PR #698 is not automatically accepted or merge-ready. Its Product owner must incorporate the accepted Governance commit into its own branch, rerun full exact-head/current-main validation and applicable Product regressions, and review/accept that separate Product unit. This Governance unit does not update its branch or merge it.

## Rollback
Revert the narrow Governance PR if its recovery invariant regresses. Preserve Issues/PRs/branches and the slot-release history. Hardening and ontology decisions remain independent.
