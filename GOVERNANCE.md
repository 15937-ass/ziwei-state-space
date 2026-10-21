# Repository Governance v1.0

Status: **ACTIVE**  
Tracking: #275  
Migration implementation: PR #276 merged.  
Recovery routing: `governance/RECOVERY_PRECEDENCE_v1.md`.

## 1. Purpose

This repository is managed as an artifact-centered research and product program. Chat is an execution interface, never a source of project truth.

The governance goals are:
- prevent theory drift and chat-driven scope changes;
- keep knowledge, product and governance writes isolated;
- make every work unit recoverable after timeout or model/session changes;
- separate specification, implementation, validation, calibration and production readiness;
- keep main as accepted canonical state.

## 2. Authority hierarchy

When artifacts disagree, higher levels win:

1. PROJECT_CONSTITUTION.md
2. approved Human Gate / approved Proposal
3. frozen architecture and Roadmaps
4. Phase Contract
5. GitHub Issue / bounded Work Unit
6. Pull Request implementation record
7. Chat/session text

No lower layer may silently change a higher layer.

**Important:** this hierarchy governs semantic/design authority, not “which work unit is active right now.” Daily execution status follows `governance/RECOVERY_PRECEDENCE_v1.md`: live lane GitHub Issue = execution truth, linked PR = implementation truth, and lane State YAML = recovery cache. A Roadmap can constrain an Issue but cannot make its own historical “current/next” paragraph the active task.

## 3. Governance layers

- Constitution: non-negotiable epistemic and research boundaries.
- Roadmaps: long-horizon direction; not daily task queues.
- Proposals: substantial architecture/theory/governance changes.
- Phase Contracts: entry criteria, required work and graduation criteria.
- GitHub Issues: authoritative daily work units.
- Pull Requests: implementation of one Issue.
- CI: deterministic verification.
- State YAML: recovery cache/pointer only.

## 4. Execution lanes

Exactly one write lane is active per execution turn:

### PRODUCT_ONLY
Owns product runtime, adapters, product tests, product benchmarks and product state.

### KNOWLEDGE_ONLY
Owns canonical knowledge, source review, knowledge validation and knowledge state.

### GOVERNANCE_ONLY
Owns governance, shared workflow, CI policy, state schemas, Roadmaps, Proposals and Human-Gate integration.

All lanes may read the repository. They may only write paths allowed by governance/PATH_OWNERSHIP.json.

## 5. Work lifecycle

Normal work:

Roadmap/Phase -> GitHub Issue -> short-lived branch -> PR -> CI -> merge -> Issue close.

Substantial design change:

Proposal Issue -> Proposal document -> PI/Human Gate decision -> APPROVED -> implementation Issues -> PRs.

A PR must implement one primary Issue. Scope discoveries become new Issues or Proposal candidates; they do not silently expand the current PR.

## 6. WIP limits

- Product lane: at most 1 ACTIVE work unit.
- Knowledge lane: at most 1 ACTIVE work unit.
- Governance lane: at most 1 ACTIVE migration/design work unit.

Backlog items may be recorded but are not executed until promoted to READY/ACTIVE.

## 7. Definition of Ready

A Work Unit may become ACTIVE only when it has:
- lane;
- goal;
- non-goals;
- required inputs;
- deliverables;
- acceptance criteria;
- dependencies;
- risk level;
- Human Gate classification.

## 8. Definition of Done

A Work Unit closes only when:
- required deliverables exist;
- acceptance criteria are satisfied or explicitly resolved as BLOCKED/UNKNOWN where allowed;
- tests/audits pass;
- the PR is merged;
- out-of-scope discoveries are recorded separately;
- no hidden cross-lane modification remains.

Explicit INSUFFICIENT_SOURCE, SOURCE_CONFLICT, NO_UNIVERSAL_RULE, UNCALIBRATED and BLOCKED_CONTENT are valid completed findings when the work unit is designed to classify evidence.

## 9. Risk levels

- R0: mechanical formatting/fixture/local bug; autonomous.
- R1: normal bounded work unit; GPT producer/critic/validator + CI.
- R2: phase closure, cross-module integration, material design ambiguity; independent review and PI-facing report.
- R3: Human Gate, canonical meaning, architecture boundary, causal upgrade; PI approval required.

## 10. Capability maturity

Never use one word "complete" for all maturity dimensions. Product capabilities are assessed independently for:
- Specification
- Implementation
- Canonical Content
- Internal Validation
- Empirical Calibration
- Production Readiness

Interface implementation is not production readiness.

## 11. Branch and PR rules

New branches use:
- product/<issue>-<slug>
- knowledge/<issue>-<slug>
- governance/<issue>-<slug>

Branches are short-lived. Stacked PRs are exceptional, maximum two levels, and the child must be rebased to main promptly after the base merges.

main is accepted canonical state, not a workspace.

## 12. State-file rule

PROJECT_STATE.yaml, product/PRODUCT_STATE.yaml, knowledge/KNOWLEDGE_STATE.yaml and governance/GOVERNANCE_STATE.yaml are recovery pointers.

GitHub Issues/PRs are authoritative for execution status. If a state cache disagrees with GitHub, GitHub wins and the cache is repaired.

State files must not duplicate long completed-history lists already preserved by Git.

## 13. Product anti-scaffolding rule

After PL3 interface construction, a new adapter/registry/interface is not created merely because a Roadmap noun exists. New abstraction must be justified by:
- a concrete benchmark failure;
- a canonical integration gap; or
- an approved Proposal.

Empty production registries are BLOCKED/UNCOVERED, never fidelity PASS.

## 13A. Product Knowledge dependency and promotion

Product artifacts that claim a frozen Knowledge baseline must be able to verify the exact Knowledge inputs they consumed. A human-readable `knowledge_version` or baseline commit string alone is not sufficient when the runtime reads mutable current-checkout files.

For reproducibility-critical Product paths:
- active Product Knowledge is pinned through an immutable/content-addressed Product lock or equivalent approved manifest;
- Knowledge `main` is research truth, not an implicit mutable production dependency;
- Knowledge updates become Product candidates and require impact analysis before adoption;
- unrelated Knowledge edits must not force full Product rebuilds;
- semantic changes propagate through explicit dependencies and require the corresponding rebuild/recompile/replay/rematerialize/retrain action;
- promotion requires the validation scope appropriate to the affected Product capability;
- failed candidates do not alter the active Product lock;
- historical forecasts, datasets, models and evidence artifacts preserve their original Knowledge lineage;
- incompatible Knowledge-derived training labels/features may not be silently mixed without an explicit migration.

The controlling Product architecture is Proposal #491 and the active Product Roadmap.

## 14. Knowledge integrity

Empirical mismatch may create a Knowledge Gap Report but may not silently rewrite canonical knowledge. User feedback never changes source truth. School attribution, conflicts and UNKNOWN states are preserved.

## 15. Chat and recovery

After timeout/new session:
1. read `PROJECT_STATE.yaml`;
2. read `governance/RECOVERY_PRECEDENCE_v1.md`;
3. read the selected lane state as a cache;
4. query live GitHub Issues for that lane;
5. use the bounded active/open Issue as execution truth and its linked PR as implementation truth;
6. read only Issue-required artifacts.

If a lane-state cache disagrees with live GitHub Issue/PR state, GitHub wins and the cache is repaired.

README phase text, legacy `tasks/*.yaml`, historical validation reports, completed acceptance records, archived checkpoints, old proposal files, superseded protocols, and historical `READY_FOR_PI` markers are not execution truth merely because they contain `ACTIVE`, `CURRENT`, `NEXT`, or `PENDING`.

Roadmaps are long-horizon architecture/direction, not daily task queues. Historical Human Gates do not become current again unless the active lane state and/or live Issue names them as pending.

Do not reconstruct authoritative project state from old chat text or from isolated status words in historical artifacts.

## 16. Administrative controls

Repository settings should enforce:
- pull request required before merge;
- required repository quality gate;
- force pushes blocked on main;
- linear history where compatible.

Until connector/admin permissions allow automation, these settings are tracked as an explicit governance administration task.
