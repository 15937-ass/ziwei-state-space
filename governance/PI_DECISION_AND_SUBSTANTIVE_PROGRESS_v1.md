# PI Decision Rights and Substantive Progress Contract v1

Status: **ACTIVE BUILD / GOVERNANCE CONTRACT**
Work unit: `PI_DECISION_AND_SUBSTANTIVE_PROGRESS_CONTRACT_V1`
Owner: Governance
Operational integration: `AGENT_WORKFLOW.md` §§5, 7 and 13; canonical session entry: `CHATGPT_START_HERE.md`.

## 1. Purpose and scope

This contract keeps the PI focused on research direction, resource allocation and judgments that genuinely require human authority, while allowing execution agents to complete already-authorized work without repeatedly asking for routine permission.

It also distinguishes durable research/engineering progress from administration, status movement and validation ceremony.

It applies to every repository-work turn in Knowledge, Core, Product and Governance, including implementation, review, recovery, validation and read-only census. It does not create a fourth execution lane, change any lane's WIP limit, authorize work outside an admitted Issue, or replace path ownership, Human Gates, the Integration Queue, or the six-section Chinese closeout report.

## 2. PI-reserved decisions

The PI retains decision authority over:

- research mission, substantive priority changes, resource allocation and lane/shard WIP allocation;
- interpretation of Ziwei theory, school attribution, source conflicts that could change canonical meaning, and shared semantic primitives;
- Human Gates and acceptance of research meaning where the applicable contract requires PI judgment;
- major architecture boundaries, cross-lane scope changes, and changes to the project's epistemic or authority model;
- claims or design choices that would assert or authorize probability, causal effects, empirical calibration, predictive validity, or production authority beyond existing approval.

An execution agent must not infer approval from silence, a previous unrelated approval, a green CI run, or the existence of an implementation artifact.

## 3. Autonomous execution within approved scope

Without asking the PI again, execution agents should autonomously:

- inspect sources and extract/classify evidence under already-approved schemas and source boundaries;
- implement bounded work already authorized by the live Issue and approved plan;
- run relevant tests, reproduce and repair ordinary local defects, and perform producer/critic/revision passes;
- maintain provenance, record UNKNOWN/conflict, preserve fail-closed behavior, and prepare evidence-backed handoffs;
- perform routine formatting, documentation consistency, checkpointing, recovery, issue/PR updates and deterministic CI;
- execute branch, lease, exact-head validation and merge mechanics strictly under the existing repository protocols.

Routine Git operations, ordinary CI/test failures, formatting, repeated status checks, and already-specified next steps are not PI decisions. Do not route them to the PI merely to obtain another approval.

## 4. Escalation rule

Escalate only when the next safe action requires one of the PI-reserved decisions in §2.

When escalation is necessary:

1. stop only the affected decision path; continue independent work that remains inside the approved scope;
2. present the source/evidence, the exact unresolved question, materially different options, consequences and a recommendation;
3. ask one concise question in Chinese;
4. state what can safely continue while the decision is pending.

Do not escalate routine execution details. Do not silently choose a new school interpretation, canonical meaning, shared semantic primitive, WIP/priority change, architecture boundary or epistemic claim on the PI's behalf.

## 5. One primary outcome class per repository-work turn

Every repository-work turn receives exactly one primary outcome class. The class describes what the turn actually established, not how much activity occurred.

### `SUBSTANTIVE_DELTA`

Use only when the turn creates a durable, evidence-backed improvement, such as:

- a source-grounded finding or resolved ambiguity;
- an implemented behavior or repaired defect;
- a hypothesis that is meaningfully supported, rejected or narrowed by a valid test;
- a durable artifact that improves the project's ability to reason, reproduce, validate or operate.

Record the exact artifact/evidence and its limitations. A commit or file change without a substantive improvement is not enough.

### `BLOCKER_IDENTIFIED`

Use only when a real blocker is demonstrated. Record:

- evidence that the blocker exists;
- the owner and dependency;
- the exact missing input or condition that would unblock it;
- safe independent work that can continue.

A vague concern, an unverified assumption or a preference is not a blocker.

### `VALIDATION_ONLY`

Use when a required validation/recheck is completed but no separate substantive change is established. Record the exact commit SHA, workflow/run ID, attempt, job and result where available. Validation is a quality gate; it is not by itself new research progress.

### `STATUS_ONLY`

Use when the turn only restores or reports status, reads live Issues/PRs, performs a census, or confirms that nothing changed. Explicitly state that no substantive progress was made.

### `NO_SUBSTANTIVE_PROGRESS`

Use when work was attempted but produced neither a durable delta nor a demonstrated blocker. State what was attempted, why it did not establish a result, and the precise next action. Do not pad the report or relabel activity as progress.

If a turn contains both implementation and validation, choose the single primary class that best describes the durable outcome; record validation as supporting evidence rather than assigning multiple primary classes.

## 6. What counts as evidence-backed progress by lane

### Knowledge

A substantive result identifies the source span and its provenance, preserves exact conditions and exceptions, and records whether the material is reusable, case-only, conflicting, UNKNOWN or unresolved. Temporal scope and school attribution remain explicit. Counts may describe coverage but are not quality scores.

### Core

A substantive result identifies the shared semantic distinction, relation, dependency or boundary that is now supported, rejected or still UNKNOWN; links it to accepted source evidence; and explains which downstream ambiguity it resolves or why it remains unresolved. Schema/operator counts are not quality scores. A formal representation does not itself authorize execution.

### Product

A substantive result demonstrates a user-visible end-to-end capability or a reproducible implementation correction, including evidence consumption, provenance, UNKNOWN/failure handling and cross-domain behavior where relevant. Interface existence, orchestration scaffolding or synthetic fixtures alone do not establish production readiness, real-case fidelity or empirical validity.

### Governance

A substantive result changes or clarifies an enforceable repository policy, test, recovery rule or ownership boundary and demonstrates that the change is internally consistent. Creating an Issue/PR, changing a status, adding a document without an adopted contract, or moving a branch is not progress by itself.

## 7. Anti-ceremony and maturity boundaries

The following are not substantive progress on their own:

- commit count, lines changed, file count, number of Issues/PRs or workflow runs;
- Issue/PR state transitions, branch creation, queue position or lease acquisition/release;
- repeated reads, duplicate reports, unchanged test reruns or newly created scaffolding;
- a rule/schema/operator count without evidence that a real distinction was resolved;
- synthetic fixtures presented as actual-chart use, or internal fidelity presented as empirical validation.

Reuse valid validation evidence under the identity/reuse rules in `AGENT_WORKFLOW.md` §10.2. Rerun tests when relevant inputs or code change, not merely to create activity.

Keep these maturity dimensions separate: source fidelity, formal/specification consistency, implementation correctness, internal validation, empirical calibration, causal identification, predictive validity and production readiness. Advancement on one dimension does not silently promote another. No single numeric KPI replaces evidence-based acceptance.

## 8. PI-facing closeout

Use the existing six-section Chinese report in `AGENT_WORKFLOW.md` §13; do not create a second status ledger or a seventh reporting system.

For the current work unit, the report must make recoverable:

- the actual question/problem worked on;
- the one primary outcome class from §5;
- the exact substantive delta, demonstrated blocker, validation identity, or explicit statement that there was no substantive result;
- unresolved uncertainty and the exact next action;
- whether PI judgment is required; if YES, ask only the specific reserved decision.

Routine Git mechanics stay out of the main report unless they block progress or create repository risk. Durable evidence belongs in the existing Issue/PR and repository artifacts, not only in chat.

## 9. Non-interference and precedence

- The live Issue/PR and accepted `main` remain execution truth; this contract does not create a parallel queue or status cache.
- The existing Integration Queue in Issue #888 remains the sole main-integration serialization mechanism.
- Existing lane ownership, WIP limits, palace schedule, cross-lane handoff and Human Gates remain unchanged.
- Product and Knowledge are not made dependent on Governance reporting artifacts.
- This contract does not authorize semantic, runtime, KIB, probability, causal, empirical or predictive-validity changes outside the current approved work unit.

## 10. Acceptance of this contract

The contract is correctly implemented when:

1. every repository-work turn can be assigned one truthful primary outcome class;
2. status/validation/administrative activity cannot be reported as substantive progress by itself;
3. PI-reserved decisions and autonomous execution are clearly separated;
4. routine Git/CI/test/formatting work is not escalated to the PI;
5. Knowledge/Core/Product/Governance progress is evidence-based and maturity boundaries remain explicit;
6. the existing six-section Chinese closeout report carries the required evidence without a duplicate ledger;
7. deterministic regression tests protect these requirements.
