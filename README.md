# Latent-State Research Framework

A research repository for formalizing a theory-constrained latent-state dynamical system. This repository separates source-grounded formalization, executable implementation, internal consistency checks, and later empirical evaluation.

> **Current-state bootstrap:** read `PROJECT_STATE.yaml` before selecting a branch, Gate, work package, or next action. Do not infer project state from legacy PRs, stale branches, or old chat messages.

## Initial research scope

The initial study does **not** claim empirical validation of the underlying interpretive framework. Its goal is to make a bounded body of theory:

1. machine-readable,
2. mathematically explicit,
3. computationally executable,
4. internally auditable and reproducible,
5. ready for later constrained system identification on real longitudinal cases.

Core pipeline:

```text
Primary sources
  -> atomic rules
  -> candidate latent-state ontology
  -> component cores
  -> component-system cores
  -> modifier operators
  -> domain projections
  -> baseline/temporal response model
  -> executable prototype
  -> internal fidelity & consistency evaluation
```

## Epistemic stance

Latent variables are treated operationally as variables in a formal model, not as empirically established physical quantities.

The initial study separates:

- **internal formalization validity**: whether the source-grounded theory can be represented consistently and reproducibly;
- **external predictive validity**: whether the formalized model predicts real-world events above baselines.

Only the former is in scope for the initial paper.

## Repository map

- `PROJECT_STATE.yaml` — canonical machine-readable current state and Gate pointer
- `PROJECT_CONSTITUTION.md` — non-negotiable research rules
- `RULE_SCHEMA.md` — atomic rule annotation protocol
- `AGENT_WORKFLOW.md` — producer/reviewer workflow
- `DECISION_LOG.md` — frozen and pending research decisions
- `sources/` — source-corpus metadata (no copyrighted source files committed by default)
- `knowledge/` — rules, ontology, component/system/operator knowledge
- `theory/` — formal definitions and state-space model
- `validation/` — conflicts, open questions, annotation review
- `src/` — executable implementation
- `tests/` — automated tests
- `paper/` — manuscript materials

## Current phase

**Phase II knowledge-base construction — P1 layer-boundary audit complete; WP04 source-coverage closure next.**

A0, A1, and A2-R1 are approved. The full P1 layer-boundary normalization audit is merged to `main`:

- 800 / 800 candidates source-normalization reviewed;
- 1,199 auditable child records generated;
- typed history transitions: 43;
- pending layer-boundary candidates: 0;
- no new primitive state, relational axis, operator family, or history-memory type required.

The consolidated checkpoint is documented in:

- `validation/decontamination/P1_LAYER_BOUNDARY_FINAL_REPORT.md`
- `validation/KB_WP03_post_P1_validation_summary.md`

No continuous numerical weights should be invented before a later system-identification stage unless they are clearly marked as illustrative and excluded from empirical claims.

### Current formal baseline

- latent-state ontology: v0.3
- component cores: G3-R v0.2
- State-16 goal-directedness: formal L1
- State-17/State-18: separate provisional will-control / persistence candidates
- structural-observability wording: replaced by observation-path support
- raw canonical extraction remains provenance-preserving; semantic repairs use auditable sidecars
- A2-R1 history memory remains exactly:
  - `ACQUIRED_DISPOSITION`
  - `PATH_DEPENDENT_GATE`

### Current automatic sequence

`WP04 source-coverage closure -> WP05 domain corpus -> WP06 structured cases -> WP07 evidence-first inference engine`.

WP03 extraction remains 60/60 systems and 2,193 canonical rules. P1 has validated the audited layer boundaries, while full end-to-end validation remains pending WP06/WP07.

Canonical state is always `PROJECT_STATE.yaml`.

## License

The software in this repository is licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE). Commercial use requires separate permission from the rights holder. Third-party materials, source texts, and contributions remain subject to their own rights and terms; this license does not grant rights that the licensor does not own.
