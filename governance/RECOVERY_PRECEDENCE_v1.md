# Recovery Precedence v1.1 — PI-first / optional reference

Status: ACTIVE REFERENCE. This file is not a mandatory per-conversation read.

## 1. Authority

For the current task, apply this order:

1. Platform/safety constraints, factual integrity, source provenance and the non-negotiable research Constitution.
2. **The current explicit PI instruction** controls task scope, priority, resource choice and stop condition. The PI may explicitly revise earlier PI decisions and plans.
3. Latest durable PI-approved decisions on accepted main, unless the current PI has explicitly revised them.
4. Live GitHub Issue/PR for execution and implementation status; accepted main for canonical artifacts.
5. Lane state YAML as a cache; plans and roadmaps as direction; historical files and old chat as reference only.
6. Agent-generated suggestions or inferred future work have no independent authorization.

A current PI instruction can change what the project works on. It cannot make an unmerged branch canonical, turn an unsupported statement into source evidence, or override platform/safety constraints. When the instruction is clear, execute it; do not let an older plan silently veto it.

## 2. Minimal recovery

Do not perform a full-project census by default.

For a repository task:
1. Identify the one requested objective and write lane.
2. Read the matching live Issue and linked PR, if they exist.
3. Read only the files needed to complete that objective.
4. Read PROJECT_STATE or a lane cache only when an authority pointer or a real state conflict requires it.
5. Before final merge, follow the Integration Lease in Issue #888 and the exact-head gate.

For an explicit “continue [lane]” request, check that lane's live Issue/PR first. Only if no active unit exists, consult that lane's plan pointer. Do not load all three plans or all lane histories.

A live GitHub Issue/PR overrides a stale state cache for execution status. Accepted main overrides unmerged branches for canonical content.

## 3. Historical material

Do not infer a task from historical status words or old artifacts. This includes:
- legacy `tasks/*.yaml`;
- README “Current phase” text;
- historical `READY_FOR_PI` markers;
- archived checkpoints, old proposals, completed validation reports and superseded protocols;
- old chats or copied prompts that conflict with the current PI instruction.

These records may preserve evidence and history; they do not create current work authorization. Do not delete historical evidence merely to make recovery easier.

## 4. Automation and validation

All ChatGPT Automations found for this account were paused on 2026-10-31. No scheduled or background research agent, autonomous task creator, repository writer or merger is authorized unless the PI explicitly approves it.

GitHub Actions PR pull_request checks and workflow_dispatch remain deterministic validation tools, not autonomous research agents. Do not confuse this distinction with a blanket Actions disablement. The G7 protocol is historical; do not reuse G7-era restrictions as current policy. Automatic push triggers and scheduled agent workflows are not authorized.
