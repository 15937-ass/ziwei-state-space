# HG-WP06B-MANIFESTATION-ROOT-01

Status: **PENDING HUMAN REVIEW**

## Decision
Choose the root-structure policy for KB-WP06B Manifestation Ontology.

This is a Human Gate because a universal root family would become a new canonical semantic primitive for all later manifestation mappings.

## Option A — Universal life-domain roots
Create fixed universal FAMILY roots such as health, relationship, finance/resource, career/organization, mobility/location, property/environment, psychological/cognitive, family/lineage, conflict/legal and reputation/status.

### Advantages
- intuitive navigation;
- easy product UX;
- straightforward analytics.

### Risks
- many roots are partly derived from modern domain organization rather than explicit source taxonomy;
- overlapping phenomena can be forced into arbitrary single parents;
- palace categories may leak into manifestation semantics.

## Option B — Palace-scoped roots
Create one root family per palace/domain, then place manifestation channels under the relevant palace root.

### Advantages
- very close to WP05 source organization;
- provenance is easy to understand.

### Risks
- duplicates the same manifestation across palaces;
- incorrectly treats palace of evidence as identity of observable manifestation;
- makes cross-palace convergence and later empirical calibration harder.

## Option C — Federated source-derived roots, no synthetic universal root **(RECOMMENDED)**
Allow multiple parent-null FAMILY nodes, but create a FAMILY only when:
- the source explicitly generalizes the phenomenon; or
- several source-verified labels transparently share the abstraction without adding new causal meaning.

Use `domain` as an independent tag rather than forcing domain to be the tree parent.

Cross-palace evidence converges onto the same manifestation node through source_rule_ids and later WP06C mappings.

### Advantages
- most source-faithful;
- avoids inventing a modern universal taxonomy;
- avoids palace duplication;
- supports gradual ontology growth;
- compatible with the current product adapter because `parent_id` is nullable and `domain` is separate.

### Cost
- the first ontology is less visually tidy;
- some top-level families remain multiple roots until evidence supports a higher abstraction.

## Recommendation
**Approve Option C.**

It best matches the project's canonical principle:

> traditional source first; explicit UNKNOWN / no-universal-rule is a valid result.

It also prevents us from turning a convenient product navigation taxonomy into “traditional truth”.

## Exact approval effect
If Option C is approved:
- no universal domain root is invented;
- source-label inventory and deduplication proceed automatically;
- ordinary source-supported child nodes do not need repeated Human Gates;
- a later proposal to merge several roots under a new universal family triggers a new Human Gate.

If A or B is chosen, the selected root vocabulary must be frozen before source-label canonicalization.

## No effect on product probabilities
This gate changes ontology semantics only.

It does not authorize:
- probability;
- frequency;
- weight;
- posterior;
- hazard;
- learned ranking;
- automatic promotion from case evidence.
