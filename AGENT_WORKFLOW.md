# AGENT_WORKFLOW.md

Version: 1.0
Governance: GOVERNANCE.md

## 1. Core rule

Chat is not project state. GitHub Issues define active work; PRs define implementation; main contains accepted state.

## 2. Session bootstrap

For a new session, timeout recovery, hard checkpoint, or possible external merge:
1. read PROJECT_STATE.yaml;
2. read the active lane state;
3. open the active GitHub Issue;
4. open its linked PR if present;
5. read only Issue-required artifacts.

Do not infer current work from old chat, stale branch names or legacy PRs.

## 3. Lanes

Every execution turn has exactly one lane:
- PRODUCT_ONLY
- KNOWLEDGE_ONLY
- GOVERNANCE_ONLY

Read access may be broad. Write access follows governance/PATH_OWNERSHIP.json.

Cross-lane discoveries are recorded as dependency/gap Issues; they are not silently repaired from the wrong lane.

## 4. Issue-first execution

Normal execution requires an Issue satisfying Definition of Ready:
- lane
- goal
- non-goals
- inputs
- deliverables
- acceptance criteria
- dependencies
- risk
- Human Gate classification

One lane has at most one ACTIVE Issue.

## 5. Work-unit cycle

1. recover state;
2. confirm lane and Issue;
3. producer pass;
4. critic/red-team pass;
5. revision;
6. deterministic/local validation;
7. create/update one PR for the Issue;
8. run CI at the hard checkpoint;
9. report status;
10. stop.

Do not automatically chain into the next Issue in the same turn.

## 6. Proposal rule

Substantial architecture/theory/governance changes follow governance/PROPOSAL_PROCESS.md.
Ordinary bugs and bounded implementation work do not create Proposals.

An implementation Issue may not broaden an approved Proposal.

## 7. Autonomy and risk

R0: mechanical bug/fixture/formatting — autonomous.
R1: normal bounded work — GPT review + CI.
R2: phase closure/cross-module integration/material ambiguity — independent review + PI-facing report.
R3: Human Gate/canonical meaning/architecture boundary/causal upgrade — explicit PI approval.

All PI review/Human-Gate material is written in Chinese.

## 8. Product anti-scaffolding

Interface/schema/registry existence is not product completion.
After PL3, new abstraction requires benchmark evidence, a canonical integration gap, or an approved Proposal.
Empty production registries are BLOCKED/UNCOVERED.

## 9. Knowledge integrity

Evidence priority:
1. primary/approved Zhongzhou source;
2. explicit Zhongzhou commentary;
3. transparent inference;
4. research hypothesis.

Lower-priority evidence cannot overwrite higher-priority evidence.
Empirical mismatch creates a Knowledge Gap Report; it does not rewrite source truth.

## 10. Checkpoints and timeout safety

Soft checkpoint: every user-facing execution report; no commit required.

Hard checkpoint: bounded work unit complete, source-review recoverable boundary, phase closure, Human Gate boundary, or substantial unreconstructable work.

Default source-review reasoning sub-batch remains about 50 items; durable integration ceiling remains 100 source-review items unless explicitly approved.

After timeout, inspect GitHub first. Never replay work blindly.

## 11. CI policy

Routine reasoning should not consume Actions.
CI is triggered for PR/hard checkpoints and reruns on new PR commits.
If CI is pending after one status check, record CI_PENDING and stop.
One autonomous repair/retry is allowed for ordinary technical failure; repeated/conceptual failures escalate.

## 12. Pull Request discipline

A PR implements one primary Issue.
Use short-lived branches:
- product/<issue>-...
- knowledge/<issue>-...
- governance/<issue>-...

Scope creep becomes a new Issue/Proposal.
Stacked PRs are exceptional and limited to two levels.

## 13. Mandatory Chinese progress report

【执行轨道】
PRODUCT_ONLY / KNOWLEDGE_ONLY / GOVERNANCE_ONLY

【Issue / Work Unit】
#<id> <title>

【完成】
- ...

【自主处理】
- ...

【验证】
- ...

【GitHub】
Branch:
PR:
CI:

【跨轨依赖】
- none / ...

【Human Gate】
NONE / REQUIRED

【当前状态】
- ...

【下一步】
- next Issue or recovery action

本轮结束。
