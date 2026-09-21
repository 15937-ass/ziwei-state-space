# RULE_SCHEMA.md

Version: 0.1  
Status: DRAFT

## Purpose

Convert Zhongzhou natural-language statements into atomic, auditable rules without prematurely assigning empirical weights.

## Atomicity principle

One row should express one principal relation:

> Subject + Context + Condition -> Effect on Target

If a sentence contains multiple effects, split it into multiple rules.

## Required fields

| Field | Meaning |
|---|---|
| rule_id | Stable unique identifier |
| school | e.g. Zhongzhou |
| source_work | Exact work title |
| source_location | Page/section/chapter |
| subject_type | star / star_system / modifier / palace / temporal_layer / relation |
| subject | Main entity |
| context | Palace, natal/limit context, day/night etc. |
| condition | Triggering conjunction/condition |
| target_type | qi_state / structural_relation / projection / outcome_descriptor |
| target | What is changed |
| operator | enhance / weaken / transform / inhibit / activate / condition / compare / project |
| direction | positive / negative / mixed / nonlinear / unknown |
| parameter | Symbolic parameter name if required |
| constraint | e.g. alpha>0, alpha1>alpha2 |
| epistemic_type | EXPLICIT / INFERRED / HYPOTHESIS / IMPLEMENTATION |
| evidence_text | Short paraphrase or minimal quote |
| confidence | high / medium / low |
| status | draft / reviewed / approved / rejected |
| notes | Ambiguities and caveats |

## Recommended optional fields

- `depends_on_rule_ids`
- `conflicts_with_rule_ids`
- `time_scope`: natal / decade / year / month / generic
- `sex_scope`
- `day_night_scope`
- `palace_scope`
- `star_position_scope`
- `reviewer`
- `version`

## Example

```yaml
rule_id: ZZ-TJ-0001
school: Zhongzhou
subject_type: star
subject: 天机
context: natal
condition: 化权
target_type: qi_state
target: 稳定性
operator: enhance
direction: positive
parameter: alpha_ZZ_TJ_0001
constraint: alpha_ZZ_TJ_0001 > 0
epistemic_type: EXPLICIT
status: draft
```

## Comparison rules

Statements such as “A is stronger/better than B” should become order constraints rather than fabricated numeric distances:

```text
alpha_A > alpha_B
```

## Nonlinear rules

Statements describing moderation, excess, conditional reversal, or context-dependent effects should be marked:

```text
direction = nonlinear
```

and the proposed functional form belongs in a separate HYPOTHESIS/IMPLEMENTATION rule, not inside the source-derived EXPLICIT rule.

## Rule splitting example

Textual statement:
“Star X meets modifier M, increasing decisiveness but also increasing isolation.”

Create two rules:
1. X + M -> decisiveness ↑
2. X + M -> isolation ↑

Do not collapse them into a single vague “overall good/bad” score.

## Promotion criteria

A rule may move from `draft` to `approved` only if:
1. provenance is complete;
2. atomicity is satisfied;
3. epistemic type is correct;
4. target terminology exists in the approved ontology or is marked provisional;
5. no unresolved direct contradiction is hidden.
