# RULE_SCHEMA_v0.2_PROPOSAL.md

Status: PROPOSED — generated from WP-01 pilot red-team findings.

## Purpose

Preserve the distinction between:
1. what the source explicitly says,
2. how the research normalizes that statement,
3. whether the effect changes a latent state,
4. whether that change is favorable in a particular context.

## Core fields

| Field | Meaning |
|---|---|
| rule_id | Stable identifier |
| school | Source school |
| source_work | Source title |
| source_location | Page/section/chapter |
| subject_type | star / star_system / modifier / palace / temporal_layer / relation |
| subject | Main entity |
| context | Human-readable context summary |
| time_scope | natal / decade / year / month / generic |
| palace_scope | Structured palace list when applicable |
| condition | Trigger condition |
| target_type | qi_state / structural_relation / projection / outcome_descriptor |
| target_literal | Source-near target wording |
| target_normalized | Research-normalized target |
| target_mapping_type | literal / normalized / inferred |
| operator | define / assert / enhance / weaken / transform / inhibit / activate / compare / project / condition |
| state_change | increase / decrease / transform / none / nonlinear / unknown |
| valence | favorable / unfavorable / mixed / context_dependent / not_applicable / unknown |
| parameter | Symbolic parameter |
| constraint | alpha>0, alpha_A>alpha_B, etc. |
| epistemic_type_source | EXPLICIT / INFERRED |
| formalization_status | LITERAL / NORMALIZED / HYPOTHESIS / IMPLEMENTATION |
| evidence_text | Short paraphrase/minimal quotation |
| extraction_confidence | high / medium / low |
| status | draft / reviewed / approved / rejected |
| notes | Caveats |

## Why separate `state_change` from `valence`

Example: 武曲的“刚烈性”在不同宫位并非同一价值。

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

For ordered relations use explicit constraints:

```text
operator: compare
constraint: effect(武曲化禄) > effect(廉贞化禄)
```

If a chain has multiple comparisons, split it into atomic pairwise constraints.

## Source-vs-model separation example

Source:
“太阳过份强烈，则宜见收敛性的星曜。”

Formalization:

```yaml
target_literal: 收敛性的星曜
target_normalized: 收敛性补偿
target_mapping_type: normalized
epistemic_type_source: EXPLICIT
formalization_status: NORMALIZED
state_change: nonlinear
valence: context_dependent
```

## Promotion criterion

A rule is approved only if:
- source provenance is complete;
- source claim is atomic;
- normalized target does not masquerade as source wording;
- state-change and valence are not conflated;
- comparison chains are split;
- contexts are structured where required.
