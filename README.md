# ziwei-state-space

A research repository for formalizing **Zhongzhou Zi Wei Dou Shu (中州派紫微斗数)** as a theory-constrained latent-state dynamical system.

> **Current-state bootstrap:** read `PROJECT_STATE.yaml` before selecting a branch, Gate, work package, or next action. Do not infer project state from legacy PRs, stale branches, or old chat messages.

## First-paper scope

The first paper does **not** attempt to prove the empirical validity of Zi Wei Dou Shu. Its goal is to make a bounded body of Zhongzhou-school knowledge:

1. machine-readable,
2. mathematically explicit,
3. computationally executable,
4. internally auditable and reproducible,
5. ready for later constrained system identification on real longitudinal cases.

Core pipeline:

```text
Primary texts
  -> atomic rules
  -> candidate qi-state ontology
  -> star cores
  -> 60 star-system cores
  -> modifier operators
  -> palace projections
  -> natal/temporal response model
  -> executable prototype
  -> internal fidelity & consistency evaluation
```

## Epistemic stance

“Qi (气)” is treated operationally as a **latent state variable** in the formal model, not as an empirically established physical energy.

The first paper separates:

- **internal formalization validity**: whether the textual theory can be represented consistently and reproducibly;
- **external predictive validity**: whether the formalized model predicts real-world events above baselines.

Only the former is in scope for Paper 1.

## Repository map

- `PROJECT_STATE.yaml` — canonical machine-readable current state and Gate pointer
- `PROJECT_CONSTITUTION.md` — non-negotiable research rules
- `RULE_SCHEMA.md` — atomic rule annotation protocol
- `AGENT_WORKFLOW.md` — GPT-centered producer/reviewer workflow
- `DECISION_LOG.md` — frozen and pending research decisions
- `sources/` — corpus metadata (no copyrighted source files committed by default)
- `knowledge/` — rules, ontology, star/system/operator knowledge
- `theory/` — formal definitions and state-space model
- `validation/` — conflicts, open questions, annotation review
- `src/` — executable implementation
- `tests/` — automated tests
- `paper/` — manuscript materials

## Current phase

**Phase II knowledge-base construction + P1 source/normalization audit + Gate A2 PI review.**

Execution is currently **FROZEN_FOR_GATE_A2** for architecture-sensitive research changes. Repair-only metadata/documentation/test work is allowed.

No continuous numerical weights should be invented before a later system-identification stage unless they are clearly marked as illustrative and excluded from empirical claims.

### Current audit baseline

Gate A0 closed deterministic schema drift; Gate A1 approved the full-corpus backward ontology audit.

Current formal state:
- QI ontology: v0.3
- fourteen-star cores: G3-R v0.2
- QI-16 goal-directedness: formal L1
- QI-17/QI-18: separate provisional will-control / persistence candidates
- structural-observability wording: replaced by observation-path support
- raw canonical extraction remains provenance-preserving; semantic repairs use auditable sidecars

See `validation/decontamination/A1_POST_APPROVAL_EXECUTION.md`.

### Gate A2 status

Gate A2 has been triggered by source-supported cross-period path dependence discovered during LB-06. Three rules are held as `A2_ARCHITECTURE_HOLD`: they are source-supported, not quarantined, but are not executable under the current memoryless G5 reaction model.

The proposal is to keep natal essence fixed and add a strictly source-gated acquired/history state. **No G5 architecture change is applied until PI approval.**

Canonical review entry:

`validation/decontamination/GATE_A2_CANONICAL.md`

Historical A2 drafts remain for audit trace only and are not valid current Gate entry points.
