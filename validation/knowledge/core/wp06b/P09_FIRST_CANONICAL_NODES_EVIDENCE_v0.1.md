# Core #874 — First P09 canonical manifestation nodes evidence

Status: LATEST_MAIN_VALIDATION_PENDING

## Scope
- Issue: #874
- Work unit: `KB-CORE-WP06B-P09-FIRST-CANONICAL-NODES-01`
- Branch: `knowledge/core-874-p09-first-canonical-nodes`
- Activation base: `4801b564f1d4c877a563fa0676fe78c30bd95dea`
- Node identity only. No canonical mapping promotion or Product activation.

## Accepted inputs
- #864 / PR #865 target-specific formal mapping-review pilot.
- #866 PI acceptance of G1A/G2A/G3A.
- #868 / PR #869 canonical node schema + stable-ID policy.
- P09 source candidate index and accepted source/context audits for CA01-035 / CA01-045 / CA05-469.

## Eligibility result
- `KMN-000001` / CA01-035: ACCEPT node identity. Fire/Bell shorthand remains unresolved at mapping-trigger level; source modality 往往 retained.
- `KMN-000002` / CA01-045: ACCEPT node identity. CA01-042/044 and real-world action prerequisite 勉强求变 retained; execution remains blocked.
- `KMN-000003` / CA05-469: ACCEPT node identity under G2A traceable INFERRED normalization; personal injury/illness/accident event target remains explicitly unsupported.

## Stable-ID allocation
Accepted main had no production KMN assignments. This bounded batch allocates exactly:
- KMN-000001
- KMN-000002
- KMN-000003

Next allocatable ID after acceptance is KMN-000004.

## Explicit non-changes
- canonical mapping promotions: **0**
- executable mappings: **0**
- Product/KIB/runtime files changed: **0**
- universal root/family/shared primitive created: **0**
- probability/numeric strength/empirical validity: **0**

## Validation
Pending exact-head full pytest, Product JS check, deterministic P0 and Governance v1.


## Latest-main resynchronization

- Original implementation base was `e0d069c0df032e65a86c742319c6a4df864479bd`.
- Main advanced to `56d18ee6cb4d69e8b17fb11b77b57f7bdaca00c0` only through Governance #872 final-answer-gate files.
- No #874 Knowledge/Core/node/index/evidence path overlapped.
- The eight #874 paths are reconstructed on current main; a fresh exact-head full gate is required.


## First exact-head validation attempt

- Run `40830557653` on head `2b9258d070db13b88a3883ec2bdd852101ff164a` / base `56d18ee6cb4d69e8b17fb11b77b57f7bdaca00c0`.
- Pytest result: **3036 passed, 132 subtests passed, 1 failed**.
- Sole failure: `test_ca05469_is_inferred_career_scene_not_personal_injury_event`.
- Cause: test-only Python list/string concatenation when assembling diagnostic text; no node artifact, source boundary, stable ID, or mapping semantics failed.
- Fix: wrap `identity_rationale` as a one-element list in the assertion helper. Contract content is unchanged.
- JS/P0/Governance were skipped because pytest failed and must pass on the repaired exact head.


## P02 resynchronization after first repaired head started

- Main advanced from `56d18ee6cb4d69e8b17fb11b77b57f7bdaca00c0` to `4801b564f1d4c877a563fa0676fe78c30bd95dea` through P02 #871 / PR #876 Tiantong source-audit files only.
- No #874 path overlaps that palace-local merge.
- P02 is now `ACTIVE_NO_ACTIVE_WORK`; successor #877 has no PR at this checkpoint.
- The repaired #874 content is reconstructed on current main and must pass a fresh exact-head full gate.
