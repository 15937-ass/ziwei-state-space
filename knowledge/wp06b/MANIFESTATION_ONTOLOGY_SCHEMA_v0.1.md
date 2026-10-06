# KB-WP06B Manifestation Ontology Schema v0.1

Status: **SCHEMA FROZEN — TAXONOMY NOT YET CANONICAL**

## 1. Purpose
KB-WP06B defines the canonical vocabulary for **what source-supported manifestations are allowed to exist as candidates**.

It does not define:
- population frequency;
- probability;
- personalized posterior;
- severity score;
- hazard;
- numeric weight;
- a deterministic chart -> event jump.

Those belong downstream.

## 2. Boundary with KB-L3 and KB-WP06C
The canonical flow is:

```text
KB-L3 symbolic/state activation
    ↓
KB-WP06C source-supported mapping
    ↓
KB-WP06B manifestation node
    ↓
product router
    ↓
[empirical probability later]
```

Therefore **latent activation is not an ontology node**. It remains an upstream inference object. WP06B starts at manifestation family level.

## 3. Node contract
The knowledge artifact must be consumable by the already-implemented PL3-M adapter.

Required fields:
- `manifestation_id`
- `parent_id`
- `domain`
- `abstraction_level`
- `source_supported_labels`
- `source_rule_ids`
- `event_specificity`
- `ambiguity_notes`
- `probability_status`
- `source_refs`

### manifestation_id
Stable knowledge-owned identifier.

Rules:
- immutable after canonical release;
- never encode probability/rank;
- do not use palace number as the semantic identity;
- one manifestation concept = one ID.

### parent_id
Nullable.

Rules:
- parent must exist when non-null;
- no self-parent;
- no cycle;
- a parent relation means **semantic abstraction**, not empirical causation or frequency.

### domain
A namespace/tag for the life domain in which the manifestation is observed.

Domain is **not automatically the tree parent**. This prevents palace taxonomy from being mistaken for manifestation ontology.

### abstraction_level
Frozen v0.1 vocabulary:
- `FAMILY`
- `CHANNEL`
- `OBSERVABLE_LABEL`

Meaning:
- FAMILY: broad source-supported manifestation class;
- CHANNEL: distinguishable route/form inside a family;
- OBSERVABLE_LABEL: most concrete normalized label that still remains suitable for canonical ontology.

Concrete historical claims that are too specific to generalize can still appear as OBSERVABLE_LABEL only when source evidence supports the normalization and the node is marked appropriately.

### source_supported_labels
One or more source-backed phrases/normalized labels.

Rules:
- preserve source meaning;
- do not silently modernize into a stronger medical/legal/social diagnosis;
- historical terminology may be retained in provenance/ambiguity notes while the normalized label stays bounded.

### source_rule_ids
One or more source-reviewed canonical rule IDs from WP05/WP04/etc.

No node can be created from model intuition alone.

### event_specificity
Must match the product adapter:
- `ABSTRACT`
- `SCENE_LEVEL`
- `CONCRETE_EVENT`

### ambiguity_notes
Required whenever:
- source language has multiple plausible modern readings;
- historical context does not map one-to-one to a modern event;
- a label is only conditionally distinguishable from sibling channels.

### probability_status
Canonical v0.1 value is always:

```text
UNKNOWN
```

Forbidden fields include:
- probability
- frequency
- weight
- score
- posterior
- likelihood
- hazard
- odds
- rank_probability

### source_refs
Every canonical node must include source refs with:
- source_id;
- source_location;
- review_status = SOURCE_SPAN_VERIFIED or HUMAN_VERIFIED;
- source_span_verified = true.

## 4. Canonicalization tiers
WP06B uses three ontology review states outside the product registry status:

- `SOURCE_LABEL_ONLY`: source/review label collected, no ontology merge yet.
- `ONTOLOGY_CANDIDATE`: proposed merge/parentage; not canonical.
- `CANONICAL_NODE`: hierarchy and normalization approved.

Only CANONICAL_NODE records may be exported into a product `CANONICAL_READY` registry.

## 5. CASE_SUPPORT_ONLY handling
CASE_SUPPORT_ONLY does not mean “discard”.

It means:
- may support a concrete leaf candidate;
- cannot by itself justify a broad universal family;
- cannot be used to infer frequency;
- cannot silently generalize from one historical statement to all contexts.

A broad parent node requires either:
1. multiple source-reviewed child labels that transparently share the abstraction; or
2. an explicit source-level generalization.

## 6. Cross-palace duplication policy
The same manifestation may be supported by multiple palaces.

Do not create duplicate ontology concepts merely because the palace differs.

Palace/rule provenance remains in:
- source_rule_ids;
- source_refs;
- WP06C mappings.

Ontology identity follows the manifestation, not the palace.

## 7. Clinical / sexuality / family-history policy
P06, P11 and P12 closure boundaries remain binding.

In particular:
- named disease claims do not become diagnosis nodes unless the source label itself is represented as a bounded candidate and product safety permits it;
- historical psychiatric/sexuality language is not upgraded into modern diagnosis or identity;
- historical family structures are not generalized into universal modern family categories.

## 8. Negative / null outcome
“No observed external event” is **not automatically a traditional manifestation node**.

It belongs to empirical observation/censoring unless the source explicitly supports a meaningful non-manifestation state.

This prevents ontology structure from silently inventing negative labels.

## 9. Root-taxonomy gate
The schema does not freeze universal root families.

Choosing whether the ontology should use:
- synthetic universal roots;
- palace/domain roots;
- or federated source-derived roots

changes the ontology's core semantics and therefore requires:

`HG-WP06B-MANIFESTATION-ROOT-01`

No canonical node population proceeds past FAMILY level until that gate is resolved.

## 10. Compatibility
This schema is intentionally aligned with:
- `product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json`;
- `src/product/manifestation_ontology.py`;
- `product/PL3M_MANIFESTATION_ONTOLOGY_ADAPTER_ACCEPTANCE.md`.

No product code/state is modified by this knowledge artifact.
