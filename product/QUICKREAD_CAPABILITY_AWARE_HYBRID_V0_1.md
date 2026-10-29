# Capability-aware hybrid QuickRead v0.1

Status: bounded Product contract; no production deployment claim.

## Purpose

QuickRead is a small read-only brief adapter. It helps the user see which parts of a requested reading are supported by the accepted runtime, which can be grounded in reviewed source material, and which are supplied only as explicit model supplementation.

It is not a second rule engine, a second knowledge registry, a chart calculator, or an LLM client.

## Request and scope

A request names the question, target chart identifier, output length, mode, and a finite list of scope slots. A slot identifies one domain, target time layer, capability kind, and the evidence namespaces required to support a claim. Only requested slots form the coverage denominator.

For example, a natal career slot may require CANONICAL evidence. A specific-year response/manifestation slot must require both CANONICAL and TEMPORAL namespaces, and every TEMPORAL reference must match the requested year layer. This prevents a natal-only rule or a different time layer from being relabeled as a specific-year result. CASE_SUPPORT_ONLY slots must declare a case scope and match it exactly.

## Three evidence lanes

| Lane | What it means | Requirements | Coverage effect |
| --- | --- | --- | --- |
| RUNTIME | A result actually produced by an accepted runtime | Rule ID listed in the capability manifest; explicit execution ID; exact target ID; main, knowledge and runtime versions matching the manifest; executable source references listed in the manifest; required namespaces present | Counts only toward runtime evidence coverage |
| SOURCE | An interpretation grounded in accepted material that is not represented as an executed runtime result | Reviewed source ID and location; allowed use is RETRIEVAL_ONLY, SEMANTIC_ONLY, or CASE_SUPPORT_ONLY; required namespaces present | Counts only toward source evidence coverage |
| MODEL_SUPPLEMENT | Additional interpretation proposed by the LLM to fill a gap | No rule ID or source reference; explicit MODEL_SUPPLEMENT label and uncertainty note | Counts only as model supplementation; never increases runtime or source coverage |

CASE_SUPPORT_ONLY material must name a case scope, match the requested slot's case scope, and may not be generalized into a canonical rule. Runtime evidence is rejected if its target, execution identifier, versions, rule ID, or executable source references do not match the manifest. Temporal references for other layers are rejected rather than mixed into the current target. Blocked, unknown, unreviewed, or untraceable evidence is not silently promoted.

## Modes

- HYBRID: include runtime and source evidence, and allow a downstream LLM to propose clearly labeled supplements for uncovered slots when normalized chart context is supplied.
- AUDIT: include runtime evidence only. This mode is useful for checking the actual capability of the project without LLM completion.
- SOURCE_FIRST: include runtime and reviewed source evidence, but do not request model supplementation.

The capability contract itself does not make any LLM call. The companion `quickread_main_reader.py` module resolves the latest public GitHub `main` commit, discovers supported provider/source-ledger files, verifies immutable Git blob SHAs, and returns a scoped payload. A caller may pass that payload to its chosen verbalizer and then validate the returned model-supplement items with the dedicated validator.

## Coverage report

The report separately counts:

- runtime-capable slots from the manifest;
- source-available slots from the manifest;
- slots with runtime evidence actually supplied for this request;
- slots with source evidence actually supplied for this request;
- slots with model supplements;
- slots still uncovered by runtime and source evidence.

Ratios use the explicitly requested slots as denominator. The uncovered count remains visible even when the LLM has filled a slot, so model completion cannot make project capability appear larger than it is. This is a per-request coverage report, not a global percentage of all Zi Wei Dou Shu knowledge.

## Versioning and upgrade boundary

The caller supplies a manifest containing the observed main SHA, knowledge version, runtime version, and per-slot capability records. The companion main reader rebuilds this manifest from the latest accepted inputs on every call, so QuickRead can consume newly merged knowledge without hardcoding a knowledge version into the verbalizer.

The reader resolves `main` to one commit SHA, fetches selected artifacts by that immutable SHA, and verifies their Git blob hashes. It does not infer acceptance from issue text, read unmerged PRs, refresh Product registries by mutation, or change repository state. It fails closed if the main tree is truncated, the network fails, a file exceeds limits, or a blob hash does not match.

The companion reader uses **progressive source retrieval**. Its 12-item default is only the first-pass per-slot batch budget for a brief reading. It reports how much eligible source evidence remains and returns a main-pinned continuation containing already-seen evidence identities. Follow-up questions or a detailed reading can request later unseen batches without repeating the first batch. The continuation is rejected if `main` changed, so a conversation cannot silently mix accepted knowledge from different repository snapshots. Newly introduced scope slots start their own first pass.

## Payload contract

The payload contains the request, version identifiers, scoped evidence grouped by lane, coverage, unresolved slots, normalized chart context, and concise verbalizer instructions. The caller should pass normalized chart facts rather than raw birth records or personal identity.

The verbalizer must not invent rule IDs, source IDs, source locations, execution IDs, or runtime execution. Runtime evidence carries the exact target and version identity of the run that produced it. A model-only addition remains a model-only addition. For non-NATAL slots, the supplied evidence must contain the requested temporal layer, and no mismatched temporal reference may be mixed in, before a claim may be described as runtime/source-supported.

## Non-goals

- No edits to the Agent Skill or Governance-owned files in this Product PR.
- No canonical rule, Knowledge, KIB, registry, ResponseProfile, M0, probability, or predictive-validity changes.
- No LLM call, UI, database, persistence, telemetry, background refresh, or full chart engine.
- The companion reader performs read-only HTTPS requests to the public GitHub API/raw content for current `main`; it never treats PRs, branches, Issue text, archives, or model memory as accepted knowledge.
- Source retrieval is limited to the supported source-first palace ledger format; other Knowledge formats require separately reviewed adapters.
- No automatic promotion of model output into canonical knowledge.

## Synthetic example

The companion fixture deliberately describes three slots: one with runtime evidence, one with source evidence, and one with a model supplement only. The expected report counts one runtime-evidenced slot, one source-evidenced slot, and one model-supplemented slot. The last slot remains uncovered by runtime and source evidence even though the model offers a supplement. These are synthetic values, not a report of current production coverage.
