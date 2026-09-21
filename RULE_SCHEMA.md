# RULE_SCHEMA.md

Version: 0.2  
Status: ACTIVE — approved at G1

## Purpose

Convert Zhongzhou natural-language statements into atomic, auditable rules while preserving the distinction between:
1. what the source explicitly says,
2. how this research normalizes that statement,
3. how a latent state changes,
4. whether that change is favorable in a particular context.

## Atomicity principle

One row should express one principal relation:

> Subject + Context + Condition -> Effect on Target

If a statement contains multiple independent effects, split it into multiple rules.

## Core fields

| Field | Meaning |
|---|---|
| rule_id | Stable unique identifier |
| school | Source school |
| source_work | Exact source title |
| source_location | Page/section/chapter |
| subject_type | star / star_system / modifier / palace / temporal_layer / relation |
| subject | Main entity |
| context | Human-readable context summary |
| time_scope | natal / decade / year / month / generic |
| palace_scope | Structured palace list when applicable |
| condition | Triggering condition |
| target_type | qi_state / structural_relation / projection / outcome_descriptor |
| target_literal | Source-near target wording |
| target_normalized | Research-normalized target |
| target_mapping_type | literal / normalized / inferred |
| operator | define / assert / enhance / weaken / transform / inhibit / activate / compare / project / condition |
| state_change | increase / decrease / transform / none / nonlinear / unknown |
| valence | favorable / unfavorable / mixed / context_dependent / not_applicable / unknown |
| parameter | Symbolic parameter name if required |
| constraint | e.g. alpha>0, alpha_A>alpha_B |
| epistemic_type_source | EXPLICIT / INFERRED |
| formalization_status | LITERAL / NORMALIZED / HYPOTHESIS / IMPLEMENTATION |
| evidence_text | Short paraphrase or minimal quotation |
| extraction_confidence | high / medium / low |
| status | draft / reviewed / approved / rejected |
| notes | Ambiguities and caveats |

## State change is not valence

Example: 武曲的“刚烈性”在不同宫位可能增加，但其评价不同.

```text
state_change: increase
valence: context_dependent
```

This prevents “more of a property” from being conflated with “better”.

## Definition rules

Identity/ontology statements use:

```text
operator: define
state_change: none
valence: not_applicable
```

Example:

```text
天机 -> 五行属性 = 阴木
```

## Comparison rules

Ordered relations must be represented as explicit pairwise constraints.

Example:

```text
effect(武曲化禄) > effect(廉贞化禄)
effect(廉贞化禄) > effect(禄存)
```

Do not hide order information only in notes.

## Source-vs-model separation

A source statement and the model-normalized target are distinct.

Example source:
“太阳过份强烈，则宜见收敛性的星曜。”

Possible formalization:

```yaml
target_literal: 收敛性的星曜
target_normalized: 收敛性补偿
target_mapping_type: normalized
epistemic_type_source: EXPLICIT
formalization_status: NORMALIZED
state_change: nonlinear
valence: context_dependent
```

The normalized wording must not be presented as if it were the author's original terminology.

## Context structure

Human-readable `context` is retained, but executable contexts should also use structured fields such as:

```yaml
time_scope: [natal]
palace_scope: [财帛宫, 事业宫]
```

## Confidence semantics

`extraction_confidence` means confidence in the source-to-rule extraction, not confidence that the astrological proposition is empirically true.

## Promotion criteria

A rule may move from `draft` to `approved` only if:
1. provenance is complete;
2. atomicity is satisfied;
3. source epistemic type is correct;
4. source wording and normalized target are distinguishable;
5. state-change and valence are not conflated;
6. comparison chains are split;
7. contexts are structured where required;
8. unresolved contradictions are preserved rather than hidden.
