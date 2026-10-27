# Capability-aware hybrid QuickRead v0.1

Status: bounded Product contract; no production deployment claim.

## Purpose

QuickRead is a small read-only brief adapter. It helps the user see which parts of a requested reading are supported by the accepted runtime, which can be grounded in reviewed source material, and which are supplied only as explicit model supplementation.

It is not a second rule engine, a second knowledge registry, a chart calculator, or an LLM client.

## Request and scope

A request names the question, target chart identifier, output length, mode, and a finite list of scope slots. A slot identifies one domain, target time layer, capability kind, and the evidence namespaces required to support a claim. Only requested slots form the coverage denominator.

For example, a natal career slot may require CANONICAL evidence. A specific-year response slot must require both CANONICAL and TEMPORAL namespaces, with a TEMPORAL source reference whose time layer matches the requested year layer. This prevents a natal-only rule from being relabeled as a specific-year result.

## Three evidence lanes

| Lane | What it means | Requirements | Coverage effect |
| --- | --- | --- | --- |
| RUNTIME | A result actually produced by an accepted runtime | Rule ID listed in the capability manifest; reviewed source references marked EXECUTABLE; required namespaces present | Counts only toward runtime evidence coverage |
| SOURCE | An interpretation grounded in accepted material that is not represented as an executed runtime result | Reviewed source ID and location; allowed use is RETRIEVAL_ONLY, SEMANTIC_ONLY, or CASE_SUPPORT_ONLY; required namespaces present | Counts only toward source evidence coverage |
| MODEL_SUPPLEMENT | Additional interpretation proposed by the LLM to fill a gap | No rule ID or source reference; explicit MODEL_SUPPLEMENT label and uncertainty note | Counts only as model supplementation; never increases runtime or source coverage |

CASE_SUPPORT_ONLY material must name its case scope and may not be generalized into a canonical rule. Blocked, unknown, unreviewed, or untraceable evidence is not silently promoted.

## Modes

- HYBRID: include runtime and source evidence, and allow a downstream LLM to propose clearly labeled supplements for uncovered slots when normalized chart context is supplied.
- AUDIT: include runtime evidence only. This mode is useful for checking the actual capability of the project without LLM completion.
- SOURCE_FIRST: include runtime and reviewed source evidence, but do not request model supplementation.

The module does not make any LLM/API call. A caller may pass the generated payload to its chosen verbalizer and then validate the returned model-supplement items with the dedicated validator.

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

The caller supplies a manifest containing the observed main SHA, knowledge version, runtime version, and per-slot capability records. Rebuilding the manifest from newly accepted inputs lets QuickRead consume newer capabilities without changing its policy or hardcoding a knowledge version into the verbalizer.

In v0.1, manifest construction is an explicit input contract. This module does not scan GitHub, infer acceptance from issue text, refresh Product registries, or mutate state. The future adapter that gathers current accepted artifacts must use the repository's authoritative state and allowed-use contracts; it must not treat unmerged PRs, archives, or blocked artifacts as executable knowledge.

## Payload contract

The payload contains the request, version identifiers, scoped evidence grouped by lane, coverage, unresolved slots, normalized chart context, and concise verbalizer instructions. The caller should pass normalized chart facts rather than raw birth records or personal identity.

The verbalizer must not invent rule IDs, source IDs, source locations, or runtime execution. A model-only addition remains a model-only addition. For non-NATAL slots, the supplied evidence must contain the requested temporal layer before a claim may be described as runtime/source-supported.

## Non-goals

- No edits to the Agent Skill or Governance-owned files.
- No canonical rule, Knowledge, KIB, registry, ResponseProfile, M0, probability, or predictive-validity changes.
- No external model/API call, UI, database, persistence, telemetry, background refresh, or full chart engine.
- No automatic promotion of model output into canonical knowledge.

## Synthetic example

The companion fixture deliberately describes three slots: one with runtime evidence, one with source evidence, and one with a model supplement only. The expected report counts one runtime-evidenced slot, one source-evidenced slot, and one model-supplemented slot. The last slot remains uncovered by runtime and source evidence even though the model offers a supplement. These are synthetic values, not a report of current production coverage.
