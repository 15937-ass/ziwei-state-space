# AGENT_WORKFLOW.md

Version: 0.5

## Repository bootstrap — mandatory but minimal

GitHub is the persistent source of truth for project state and frozen artifacts, but it is **not** the workspace for model reasoning.

At the start of a **new session**, after a timeout/recovery, after a hard checkpoint, or when another lane may have changed dependencies:

1. read `PROJECT_STATE.yaml`;
2. if the lane is PRODUCT_ONLY, also read `product/PRODUCT_STATE.yaml`;
3. read only the files required by the current work unit.

Do **not** scan the whole repository by default.

Within a continuing session, if no hard checkpoint, external merge, timeout, or state inconsistency occurred, reuse the already verified state instead of repeatedly re-reading GitHub.

`PROJECT_STATE.yaml` remains the global/bootstrap state.  
`product/PRODUCT_STATE.yaml` owns the product work-unit pointer.  
Knowledge-side progress continues to use the knowledge fields in `PROJECT_STATE.yaml` until a dedicated knowledge state file is explicitly justified.

Do **not** infer current state from old chat messages, legacy PRs, stale branches, or branch names when a Git recovery read is required.

If a global or lane state is frozen for a Human Gate, only repair/metadata/test work that does not change the frozen theory boundary is permitted until the PI explicitly approves the Gate.

---

## Execution lanes

Every execution turn must have exactly one active lane.

### PRODUCT_ONLY

The agent may read the whole repository when needed for dependency awareness, but it only advances product work.

Typical writable ownership:
- `product/**`;
- `src/product/**`;
- `tests/test_product_*`;
- product-specific validation / benchmark / data artifacts.

Knowledge artifacts are read-only in this lane. If product work exposes a knowledge gap, record it in the user report first. Persist a cross-lane handoff only when the gap is a durable blocker or a hard-checkpoint artifact is otherwise being written.

The agent must not silently repair or extend canonical knowledge while in PRODUCT_ONLY.

### KNOWLEDGE_ONLY

The agent may read the whole repository when needed for product-interface awareness, but it only advances canonical knowledge work.

Typical writable ownership:
- `knowledge/**`;
- knowledge-side `validation/**`;
- approved source/coverage artifacts;
- knowledge-side audit utilities and tests when directly required by the work unit.

Product implementation artifacts are read-only in this lane.

The agent must not implement product features while in KNOWLEDGE_ONLY.

### Shared / governance artifacts

Files such as:
- `PROJECT_STATE.yaml`;
- `PROJECT_CONSTITUTION.md`;
- `AGENT_WORKFLOW.md`;
- `DECISION_LOG.md`;
- `PRODUCT_ROADMAP.md`;
- `KNOWLEDGE_BASE_ROADMAP.md`;
- shared theory contracts;

are not routine lane outputs. Modify them only for an explicit governance, Gate, architecture, or coordinated state-sync task.

**Rule:** agents have broad read permission for project awareness, but narrow write permission for the active lane.

---

## GPT-first / Git-light execution policy

Reasoning and production work should happen on the GPT side whenever possible.

GPT-side work includes:
- task decomposition;
- literature/source interpretation;
- rule extraction;
- ontology reasoning;
- producer/critic/revision cycles;
- code design and drafting;
- red-team analysis;
- ordinary consistency checks;
- bounded local/Python validation when available;
- Human Gate classification;
- progress reporting.

GitHub is used for:
- minimal state recovery reads;
- reading the exact target artifacts needed for the current work unit;
- durable hard checkpoints;
- version control of approved/stable outputs;
- necessary acceptance/closure CI.

Do **not** use GitHub API calls as a substitute for model reasoning.

Do **not** repeatedly list/search the repository when the needed state/file paths are already known.

GitHub connector/API activity and GitHub Actions compute minutes are different resources. Both should be used efficiently, but Actions minutes are the scarce execution resource that must not be spent on routine conversational progress.

---

## GitHub Actions budget policy

Default for an ordinary GPT execution turn:

```text
GitHub Actions triggered = 0
```

Actions are justified only when one of the following applies:
- a product work-unit acceptance requires repository CI;
- a knowledge closure/integration checkpoint requires repository validation;
- a Human Gate changes canonical structure or architecture;
- a formal merge/release/benchmark requires CI;
- a failure cannot be responsibly resolved with GPT-side/local checks alone.

Do not trigger CI after every small edit, source sub-batch, formatting change, or progress report.

If an intermediate recovery checkpoint is needed for work under paths that auto-trigger Actions on `main`, prefer a non-main recovery branch without opening a PR solely for checkpointing, when repository policy allows.

Do not open a PR merely to run checks that will immediately run again on the same integration to `main`.

If CI is still running after one status check, record `CI_PENDING`, report progress, and end the turn. Do not poll repeatedly in the same conversational turn.

If CI fails:
- diagnose the failure;
- one autonomous repair/retry is allowed when the fix is within approved boundaries;
- repeated or conceptually ambiguous failure is escalated rather than looped indefinitely.

---

## Principle

Use a controlled **producer -> critic -> revision -> validator -> human gate** workflow.

Do not rely on free-form multi-agent debate.

The GPT side may internally perform multiple role passes before presenting a result. Those role passes do not require GitHub writes.

GitHub stores durable project results; chat is not the long-term source of truth for frozen state.

---

## Autonomy levels

### AUTO — solve without asking the PI

Within the active lane and existing frozen boundaries, the agent should independently handle:
- ordinary code bugs;
- import/test-fixture/schema mistakes;
- formatting and documentation synchronization;
- deterministic refactors that preserve semantics;
- source normalization already covered by approved schema;
- routine unit-test repair;
- bounded retry after a technical failure;
- choosing another same-lane work unit when the current one is blocked by a noncritical cross-lane dependency.

### ESCALATE — investigate first, then report

Escalate when:
- two source-normalization interpretations remain materially plausible;
- a product contract appears incompatible with frozen canonical knowledge;
- a cross-lane dependency blocks all meaningful same-lane work;
- repeated technical failure suggests a design problem rather than a local bug.

Do not change canonical meaning merely to unblock execution.

### HUMAN GATE — stop for PI approval

Existing G1–G6 / A0–A2 rules remain in force. In particular, stop for approval before:
- adding a primitive qi/state variable;
- changing natal essence;
- changing the natal/temporal boundary;
- promoting empirical results into canonical traditional rules;
- inventing fixed numeric effects not supported by source;
- adding default persistence/decay or long-term memory semantics;
- allowing black-box AI to replace the canonical symbolic layer;
- upgrading association into causal action advice;
- making another architecture-level change already defined as a Human Gate by the roadmaps.

All Human Gate material must be written in Chinese.

---

## Human-facing language rule

All materials that require PI review or approval must be written in **Chinese**, including:
- Human Gate reports;
- decisions requiring PI approval;
- red-team summaries escalated to the PI;
- unresolved conceptual questions requiring human judgment;
- merge/approval recommendations.

Machine-readable field names may remain English for engineering consistency, but every human-review artifact must provide clear Chinese explanation.

---

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
Input: reviewed rules.  
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

Produces or updates the appropriate validation artifacts when a hard checkpoint is due.

### A5 — Software Engineer
Implements approved structures only.
Every core rule implementation should be testable and traceable to rule IDs.

### A6 — Reporter / Paper Writer
For execution work, produces the required Chinese progress report.
For manuscript work, uses only frozen artifacts and approved results and must not invent missing theory to improve narrative flow.

---

## Human gates

- G1: rule schema
- G2: qi ontology
- G3: 14-star cores
- G4: 60-star-system logic
- G5: state-space formulation
- G6: conclusions and limitations
- A0/A1/...: post-G6 audit Gates when corpus-wide review exposes architecture-level changes
- additional product/knowledge Human Gates defined in the active roadmaps remain authoritative

---

## Standard work-unit cycle

1. Confirm the active lane.
2. Recover minimal Git state only when required by the bootstrap rule.
3. Define **one bounded work unit**.
4. Perform producer/critic/revision/validator work primarily on the GPT side.
5. Resolve ordinary technical issues autonomously.
6. Classify cross-lane dependencies and Human Gate conditions.
7. Persist a hard checkpoint only when the hard-checkpoint criteria are met.
8. Produce the mandatory Chinese progress report.
9. Stop. Do not automatically chain into the next work unit in the same turn.

One user turn should normally advance at most **one bounded work unit**.

---

## Soft checkpoint vs hard checkpoint

### Soft checkpoint — every execution turn

A soft checkpoint is the user-facing progress report.

It does **not** require a Git commit.

It records:
- active lane;
- work completed this turn;
- autonomous fixes/decisions;
- validation performed;
- GitHub reads/writes used;
- Actions triggered or not triggered;
- cross-lane dependency status;
- Human Gate status;
- next work unit.

### Hard checkpoint — durable project milestone

Use Git only when durable persistence is justified, for example:
- a bounded work unit is complete;
- a source-review group reaches the planned recoverable hard boundary;
- a closure/acceptance artifact is complete;
- canonical data or code is ready to be versioned;
- before/after a Human Gate;
- before ending a session with substantial work that would otherwise be difficult to reconstruct.

A progress report is **not** itself a reason to commit.

For large source review:
- internal GPT-side sub-batches may be smaller;
- existing hard ceiling remains **100 source-review items per durable integration unit** unless explicitly approved otherwise;
- avoid separate main-branch commits/CI for every tiny sub-batch;
- if recovery durability is needed before integration, use a non-main checkpoint when practical.

---

## Checkpoint and timeout safety

To keep work recoverable without turning GitHub into the reasoning workspace:

- default source-review reasoning sub-batch: about **50 records/items**;
- durable integration ceiling: **100 source-review items** unless the change is purely mechanical and explicitly approved;
- do not chain multiple large batches, multiple PRs, CI waits, merges, and state-sync work into one conversational turn;
- before a likely timeout, create a recovery checkpoint only if substantial unreconstructable work exists;
- after a timeout, first inspect the minimum Git state needed to determine what actually persisted;
- do **not** assume failure and do not replay completed work blindly;
- purely operational checkpointing does not create a new Human Gate;
- if CI is pending, stop the turn rather than waiting indefinitely.

---

## Cross-lane dependency protocol

When the active lane discovers a dependency owned by the other lane:

1. classify whether it blocks the current work unit;
2. do not modify the other lane;
3. if non-blocking, continue with same-lane work;
4. if blocking, search for a meaningful same-lane fallback work unit;
5. only if no useful same-lane fallback exists, report `BLOCKED_BY_CROSS_LANE_DEPENDENCY`;
6. persist a handoff artifact only when it is a durable blocker worth tracking, not for every minor observation.

---

## Mandatory Chinese progress report

Every execution turn ends with a compact report using this structure:

```text
【执行轨道】
PRODUCT_ONLY / KNOWLEDGE_ONLY

【本轮工作】
<bounded work unit>

【完成】
- ...

【GPT 自主处理】
- ...

【验证】
<local/GPT-side tests, repository tests if any>

【GitHub 使用】
读取：<minimal files/state>
写入：<none / commit or checkpoint>
Actions：<0 / triggered; if pending say CI_PENDING>

【跨轨依赖】
<none / dependency and impact>

【Human Gate】
NONE / REQUIRED: <gate>

【当前状态】
<current lane state>

【下一步】
<next bounded work unit>

本轮结束。
```

Keep the report concise. Do not repeat the full project history each turn.

---

## Evidence priority

1. primary/approved Zhongzhou text,
2. explicit Zhongzhou commentary,
3. transparent inference,
4. research hypothesis.

Lower-priority evidence cannot silently overwrite higher-priority evidence.

---

## Quality targets for Paper 1

- 100% approved rules traceable to source;
- no unmarked inferred/hypothetical rule;
- unresolved contradictions preserved;
- reproducible transformation from approved rule set to executable representation;
- separate internal-fidelity evaluation from external predictive claims.
