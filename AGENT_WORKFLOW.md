# AGENT_WORKFLOW.md

Version: 0.4

## Repository bootstrap — mandatory

Before selecting a branch, Gate, work package, or next action, every agent/session must read `PROJECT_STATE.yaml`.

`PROJECT_STATE.yaml` is the canonical machine-readable pointer to:
- current phase and execution state;
- active branch and PR;
- last approved Gate and pending Gate;
- canonical human-review artifact;
- work that is currently blocked.

Do **not** infer current state from old chat messages, legacy PRs, stale branches, or branch names.

If `execution_state` is `FROZEN_FOR_GATE_*`, only repair/metadata/test work that does not change theory is permitted until the PI explicitly approves the pending Gate.

## Principle

Use a controlled **producer -> critic -> revision -> validator -> human gate** workflow.

Do not rely on free-form multi-agent debate.

All agents read and write shared artifacts; chat memory is not the source of truth.

## Human-facing language rule

All materials that require PI review or approval must be written in **Chinese**, including:
- Human Gate reports;
- decisions requiring PI approval;
- red-team summaries escalated to the PI;
- unresolved conceptual questions requiring human judgment;
- merge/approval recommendations.

Machine-readable field names may remain English for engineering consistency, but every human-review artifact must provide clear Chinese explanation.

## Roles

### A0 — Research Manager
- decomposes work packages;
- checks dependency order;
- enforces constitution and schemas;
- does not invent domain theory.

### A1 — Literature Extractor
Input: approved source passages.  
Output: atomic rules conforming to `RULE_SCHEMA.md`.

Forbidden:
- adding unstated theory,
- assigning empirical numbers,
- silently merging contradictory statements.

### A2 — Ontology Researcher
Input: reviewed `rules.csv`.  
Output: candidate latent qi dimensions and definitions.

Must provide:
- supporting rule IDs,
- redundancy analysis,
- dependency/derivation hypotheses,
- candidate status.

### A3 — Mathematical Formalizer
Input: approved rules + ontology.  
Output:
- latent-state definitions,
- symbolic operators,
- nonlinear response forms,
- structural constraints.

May formalize; may not change domain meaning.

### A4 — Red-Team Auditor
Challenges:
- hidden contradictions,
- redundant dimensions,
- circular definitions,
- unfalsifiable mapping,
- provenance errors,
- accidental mixing of schools,
- event labels masquerading as primitive qi.

Produces `validation/conflicts.csv` and `validation/unresolved_questions.csv`.

### A5 — Software Engineer
Implements approved structures only.
Every core rule implementation should be testable and traceable to rule IDs.

### A6 — Paper Writer
Uses only frozen artifacts and approved results.
Must not invent missing theory to improve narrative flow.

## Human gates

- G1: rule schema
- G2: qi ontology
- G3: 14-star cores
- G4: 60-star-system logic
- G5: state-space formulation
- G6: conclusions and limitations
- A0/A1/...: post-G6 audit Gates when corpus-wide review exposes architecture-level changes

## Standard work-package cycle

1. Read `PROJECT_STATE.yaml`.
2. Manager defines bounded source scope.
3. Extractor produces rules.
4. Auditor checks provenance and atomicity.
5. Extractor revises.
6. Manager produces a **Chinese review summary**.
7. PI approves/rejects/escalates.
8. Approved artifact is versioned and `PROJECT_STATE.yaml` is advanced.

## Checkpoint and timeout safety

To keep research recoverable when a chat/tool session times out, all corpus-scale work must use bounded checkpoints.

- Default source-review batch: **50 records/items**.
- Hard ceiling per PR: **100 source-review items**, unless the change is purely mechanical and explicitly approved in advance.
- After every batch, persist all review outputs, sidecars, progress counters, and tests to GitHub **before** starting the next batch.
- A batch is not considered complete until its artifacts are committed and the repository contains enough state to resume from a fresh session without relying on chat memory.
- Do not chain multiple large review batches, multiple PRs, CI waits, merges, and state-sync work into one conversational turn when they can be checkpointed separately.
- If a session times out, first inspect GitHub commit/PR/workflow state. Do **not** assume the work failed and do not replay completed source review blindly.
- Purely operational checkpointing does not create a new Human Gate; only theory/ontology/architecture changes use the existing Gate rules.

## Evidence priority

1. primary/approved Zhongzhou text,
2. explicit Zhongzhou commentary,
3. transparent inference,
4. research hypothesis.

Lower-priority evidence cannot silently overwrite higher-priority evidence.

## Quality targets for Paper 1

- 100% approved rules traceable to source;
- no unmarked inferred/hypothetical rule;
- unresolved contradictions preserved;
- reproducible transformation from approved rule set to executable representation;
- separate internal-fidelity evaluation from external predictive claims.
