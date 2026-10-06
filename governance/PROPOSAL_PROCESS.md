# Proposal Process v1.0

## When a Proposal is required

Required for substantial changes such as:
- new primitive qi/state;
- natal/temporal boundary changes;
- new persistence/decay/long-memory semantics;
- top-level manifestation ontology change;
- probability or causal semantic changes;
- product architecture changes;
- repository governance changes;
- major dependency/platform changes.

Not required for ordinary bugs, fixtures, source-explicit rules under approved schemas, routine adapters, or a normal bounded work unit.

## Proposal identity

The tracking GitHub Issue number is the Proposal ID.

Example:
- Issue #310
- governance/proposals/310-short-title.md

## Status machine

DRAFT -> REVIEW -> APPROVED -> IMPLEMENTING -> IMPLEMENTED

Terminal alternatives:
REJECTED / SUPERSEDED / WITHDRAWN

APPROVED means the design is allowed to be implemented. It does not mean implementation is complete.

## Required sections

- Status / Tracking Issue
- Motivation
- Goals / Non-Goals
- Current Problem
- Proposed Design
- Alternatives
- Compatibility
- Knowledge Impact
- Product Impact
- Risks / Failure Modes
- Test Plan
- Migration Plan
- Rollback Plan
- Graduation Criteria
- Human Gate
- Decision
- Implementation History

## Decision authority

R3/Human-Gate proposals require explicit PI approval in Chinese-facing material.
R2 governance/architecture proposals require a recorded decision.
Implementation PRs may not broaden an approved Proposal without a follow-up Proposal or amendment.
