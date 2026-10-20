# Proposal #374 — Conversation repository authority

Status: APPROVED / IMPLEMENTING
Tracking Issue: #374
Risk: R3

## Motivation
PI requires the current ChatGPT conversation mode to be a first-class repository operator rather than a bounded editing interface.

## Proposed Design
The current ChatGPT conversation may use every GitHub repository operation that the connected tools actually expose, including file, branch, Issue, PR, review, merge, workflow, and other repository-management operations. Work/Codex is not required merely to perform GitHub writes.

This is an operational-capability grant, not a semantic-governance bypass. Issue-first execution, lane ownership, PR discipline, validation requirements, Human Gates, Zhongzhou source integrity, and product maturity boundaries remain in force.

Normal work remains Issue -> branch -> PR -> validation -> merge. Direct-to-main is not made the routine workflow merely because a tool could permit it.

The connector/tool surface is the technical ceiling. If an operation is not exposed by the connected tooling, governance authorization does not create that API capability.

## Compatibility
G8 public Actions may continue as the deterministic shell runtime. Work/Codex remains optional when available.

## Knowledge Impact
None.

## Product Impact
None.

## Risks
The main risk is confusing repository capability with authority to change canonical meaning. Existing lanes and Human Gates remain the control.

## Test Plan
Update governance contract tests and run governance validation; statically verify no Product or Knowledge semantic files change.

## Migration Plan
Amend the effective G8 authority split, mark G7 historical/superseded, update AGENT_WORKFLOW and GOVERNANCE_STATE, and add governance tests.

## Rollback Plan
Revert the implementation PR and restore G8 bounded-edit wording.

## Human Gate
Approved by PI in the current conversation on 2026-10-20.

## Decision
APPROVED. Because G7 is already superseded by G8 for routine execution, the effective change must amend G8 while also correcting G7's historical status.
