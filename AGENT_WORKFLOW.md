# AGENT_WORKFLOW.md

Version: 2.0 — PI-first / low-context

## 1. Authority

The current explicit PI instruction controls the current task, scope, priority and stop condition. The PI may explicitly revise an earlier PI-approved plan or decision. Platform/safety constraints, factual integrity, source provenance and accepted-main boundaries remain binding.

The PI reserves research mission/priority/resource/WIP decisions, school and theory interpretation, canonical source conflicts, shared semantic primitives, Human Gates, major architecture/cross-lane boundaries, and authorization of probability, causal, empirical-calibration or predictive-validity claims.

The current ChatGPT conversation is a first-class repository operator and may use every GitHub operation exposed by connected tools. This operational capability does not bypass PI authority, lane ownership, source integrity or validation. Direct-to-main is not routine.

## 2. One task, one bounded scope

- Execute one PI-requested objective per turn, in one write lane.
- Use the matching live Issue/PR when repository implementation is required. An Issue/PR records execution state; it does not outrank a newer explicit PI instruction about priority or scope.
- Do only the work necessary to satisfy the requested objective and its acceptance criteria.
- No autonomous scope expansion, speculative architecture, new abstractions, new research directions, new Issues/Proposals, or extra follow-up tasks.
- Out-of-scope discoveries may be recorded briefly with evidence and impact; do not implement them or create another work unit without PI authorization.
- Do not chain into the next Issue in the same turn. Finish, report and stop.

## 3. Low-context recovery

Default repository context is limited to:
1. the current PI instruction;
2. one matching live Issue and linked PR, if applicable;
3. the files directly required by that work unit.

Read PROJECT_STATE.yaml only when repository authority pointers are needed. State YAML files are caches, not independent task authorities. Read a lane cache only when the selected task depends on it or a live-state conflict must be diagnosed.

Do not routinely read all lane states, all Issues/PRs, RECOVERY_PRECEDENCE, full roadmaps, THREE_STREAM_START_HERE, historical proposals or unrelated validation reports. Read a plan pointer only when the PI asks to continue a lane and no active work unit exists. On timeout/session change, recover the current work unit and its delta; do not replay the whole project.

A global three-stream census is optional. Perform it only when the PI asks or a demonstrated cross-lane dependency makes it necessary.

## 4. Lane ownership and WIP

Every repository write turn has exactly one lane: PRODUCT_ONLY, KNOWLEDGE_ONLY or GOVERNANCE_ONLY. Read access may be broad; writes follow governance/PATH_OWNERSHIP.json.

Preserve current limits:
- Product WIP <= 1;
- Core WIP <= 1;
- palace shards follow governance/KNOWLEDGE_SHARD_EXECUTION_v1.md and the PI-approved one-palace-at-a-time schedule;
- Governance WIP <= 1.

Cross-lane discoveries are reported or handed off; never repair another lane's files from the wrong lane. Unmerged branches are not canonical inputs.

## 5. Work and integration

For repository implementation, preserve the normal Issue → branch → PR → validation → merge discipline.

During ACTIVE_BUILD, run relevant bounded tests and checks. Do not repeat unchanged reads or validations merely to create activity. One ordinary technical repair/retry is allowed; repeated or conceptual failure is reported rather than hidden by weakening a test.

Validation intensity follows the existing risk level:
- R0: diff/format checks and directly changed tests.
- R1: affected module/contract tests and relevant deterministic validators.
- R2: affected domain suites plus independent review; full repository gate when shared contracts or cross-module behavior are affected.
- R3: explicit PI approval, full exact-head gate and relevant independent/differential checks.

PR CI runs changed-scope tests, not the full repository suite. The full suite and P0 repository audit are reserved for the exact-head integration gate when required by R2/R3 or the live Issue. An isolated R0/R1 Issue may explicitly approve a narrower exact-head gate. Never broaden or narrow the gate silently after seeing a result.

Only the Integration Lease holder in Issue #888 may synchronize to current main, run the Issue-approved exact-head gate, merge and release the lease. Never merge on stale validation or consume unmerged work as accepted knowledge.

Context rule: do not read the entire tests directory or full CI logs by default. Use the changed-file list, selected-test summary and only the relevant failing traceback excerpt. Rerun only when the code/head changes or a failure requires one bounded repair; do not rerun an unchanged green result for reassurance.

GitHub Actions are validation-only:
- PR pull_request workflows may run deterministic tests;
- workflow_dispatch is a manual validation fallback;
- no scheduled/background agent, autonomous research, task creation, repository write or merge workflow is authorized;
- automatic push triggers remain prohibited.

All ChatGPT Automations found for this account were paused on 2026-10-31. Do not create or re-enable an automated executor without explicit PI approval. If an old prompt claims that GitHub Actions are disabled based on G7-era rules, discard that instruction; deterministic PR validation remains distinct from autonomous agents.

## 6. Human Gates and escalation

Routine source review within approved scope, implementation, formatting, targeted tests, evidence bookkeeping and ordinary Git mechanics do not require repeated PI permission.

Stop only the affected decision path when the next safe action genuinely requires a PI-reserved judgment. Present the evidence, the exact question, materially different options and consequences, then ask one concise question in Chinese. Continue unrelated work only if it remains inside the PI-approved task scope.

Never infer PI approval from silence, an unrelated earlier approval, a green CI run or an agent-generated proposal.

## 7. Checkpoint and closeout

Preserve material progress in the existing Issue/PR or versioned artifact: completed range, changed artifacts, source/evidence references, unresolved items, validation identity/result and exact resume point. Do not create a second status ledger.

Ordinary closeout is concise:
- Result;
- Changed artifacts;
- Validation actually performed;
- Blocker or PI decision, if any;
- At most one necessary next action.

No mandatory six-section report, no mandatory PI-judgment YES/NO boilerplate, and no mandatory global three-stream census. Use one primary outcome class only when it helps distinguish substantive progress from validation/status work; it is not a per-turn reporting ritual.

An ordinary end-user QuickRead, DetailedRead, or other fortune-reading turn is not repository work unless it actually performs repository implementation, review, governance or status recovery.
