# Core #868 — Canonical manifestation node contract evidence

Status: LATEST_MAIN_FINAL_VALIDATION_PENDING

## Work unit
- Issue: #868
- Branch: `knowledge/core-868-canonical-manifestation-node-contract`
- Original activation base: `2265684c4078536d7d27688b1d096338fd5e2864`
- Current resynchronized base: `38384b956e98e2986ab8d31bc53356d387d96691`
- Scope: Knowledge-owned canonical node schema + stable-ID policy only.

## PI authority
- #841 / PI D1–D5: minimum semantic review contract.
- #866 / PI G1A/G2A/G3A: policy-gated ordinary node canonicalization, traceable inference with epistemic preservation, and Knowledge-owned semantics with later Product adapter.

## Contract decisions implemented
- Production Knowledge namespace: `KMN-NNNNNN`, opaque six-digit identity.
- Monotonic allocation on accepted main; never reuse or renumber.
- `parent_id=null` means no accepted parent in current artifact, not a universal root.
- Non-null parent must resolve in the same canonical artifact.
- Current `output_kind` and `event_specificity` values remain non-exhaustive; the schema freezes state semantics, not an exhaustive value enum.
- Canonicalization gate allows source epistemic EXPLICIT/INFERRED_FROM_SOURCE and normalization SOURCE_PRESERVING/INFERRED only, with verified source/normalization and supported target review.
- MISSING/CONFLICT block canonicalization; UNKNOWN may remain only when identity is stable.
- Product readiness remains separate and false by default.

## Explicit non-changes
- No production KMN IDs assigned.
- No canonical mapping promoted.
- No universal family/root/shared primitive created.
- No Product/KIB/runtime file changed.
- No probability, numeric strength, or empirical-validity claim.

## Prior-base semantic-head validation

- Run: `40827124434`
- Validated head: `9ceec790709d7727b0bc43a2295b6b07cc87722f`
- Base at that run: `2265684c4078536d7d27688b1d096338fd5e2864`
- Pytest: **2974 passed, 132 subtests passed**
- Product JS adapters: **PASS**
- Deterministic P0 repository gate: **PASS**
- Repository Governance v1: **PASS**
- This proves the red-team-tightened semantic content on that base, but it is not the final merge gate after main advanced.

## Latest-main resynchronization

- Main advanced to `c63c0d8aa0305c838861a17ceaa85d514ab43222` only through P02 palace-local Solar source-audit files; none overlap #868's six Core/test/evidence paths.
- The #868 files are reconstructed unchanged in semantic content on this current main.
- A fresh exact-head PR quality gate is required before merge.


## Red-team contract tightening

Before final validation, four fail-closed gaps were corrected:
1. Added required `unresolved_notes` so the schema matches the Issue's explicit ambiguity/unresolved preservation requirement.
2. The canonical node schema now directly rejects epistemic states that G1A/G2A block (`UNRESOLVED_SOURCE`, `IMPLEMENTATION`, `HYPOTHESIS`, `UNRESOLVED`) instead of relying only on prose policy.
3. Review-layer `MISSING/CONFLICT` remain valid review semantics, but the canonical node schema accepts only `KNOWN/UNKNOWN/NOT_APPLICABLE`; this prevents policy/schema divergence.
4. Parent graphs must be acyclic, supersession requires explicit forward links/reason, and tests now assert Product production registries remain empty.


## Second resynchronization after validated current-main head

- Run `40827934669` validated head `ab21e301415188bb9cdb901434ef003a1cd093d2` on base `c63c0d8aa0305c838861a17ceaa85d514ab43222`.
- Result: **2979 passed, 132 subtests passed**; Product JS, deterministic P0 and Governance v1 all PASS.
- Main then advanced one commit to `c62f4914a528185ebc36c06a7dec1e8eae541a81` through Product #798 QuickRead files only.
- Those Product files are baseline content and are **not** part of #868's diff; no #868 Knowledge contract path overlapped.
- The six #868 files are reconstructed on `c62f4914a528185ebc36c06a7dec1e8eae541a81` and require a fresh exact-head gate before merge.


## Third resynchronization — P02 merge window

- Main advanced to `38384b956e98e2986ab8d31bc53356d387d96691` through P02 SB04/Wuqu source-audit files only; none overlap #868.
- P02 state at this checkpoint is `ACTIVE_NO_ACTIVE_WORK`; successor #871 has no PR and remains waiting admission.
- The six #868 paths are reconstructed on this main for a clean exact-head merge window.
- Contract semantics are unchanged from the previously successful red-team validation.
