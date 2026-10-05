# WP05 P09 Career/Official Palace Semantic Boundary Audit

Status: **SOURCE-VERIFIED — EXISTING ONTOLOGY CONFIRMED**

## Source scope
Canonical source: SRC-ZZ-003, Career/Official Palace opening, printed pp132–133.

## Source-grounded boundary
The source explicitly reframes the ancient 官禄宫 reading for a modern occupational environment.

- Primary P09 scene is **career / occupation / industry nature**, not a literal lookup from an ancient office title to one modern job.
- A second P09 scene is **organizational role / work function**: administrative, management, technical, service, professional, independent, collaborative and comparable role properties must be separated from industry labels.
- P09 is opposite P03 夫妻宫 and in triad with P01 命宫 and P05 财帛宫. The source requires these relations to refine career interpretation.
- P03 may modify career through spouse influence or suitability for joint enterprise, but **career outcome and marriage outcome remain distinct**. P09 itself remains primary for career judgment.
- P01 and P05 help distinguish the person's overall mode and material/resource channel from the P09 occupational role. **Career prominence does not imply financial gain or retention**, and financial structure does not replace career structure.
- Ancient 官宦 / 商人 / 工匠 / 武职 labels are historical scene language. Modern normalization must first preserve the underlying occupational or functional property, then use auditable SCENE_TRANSLATION; it must not silently map one ancient label to one modern profession.
- Exact modern occupations remain scene-level or concrete-event projections unless the source independently supports a reusable occupational mechanism.

## Ontology decision
No new palace primitive is required.

Existing ontology is confirmed:
- P09 primary_semantic_scope = career;occupation;industry_nature
- P09 secondary_semantic_scope = organizational_role;career_spouse_interaction
- SC-P09-A = career_industry
- SC-P09-B = organizational_role

The existing P03/P05/P09 decontamination rules already encode the required separation between marriage, career, and financial outcomes.

## Modeling consequences
Career extraction will preserve at least four separable targets:

1. industry_nature
2. organizational_role
3. career_development_or_stability
4. career_collaboration_or_spouse_interaction

Modern occupation examples are not allowed to create new L1 primitives merely because the source names an occupation.

## Human Gate
None.

The opening source requires no new primitive qi, operator family, memory type, cross-palace long-memory mechanism, independent time scale, numeric weight, probability or decay term.

## Next anchor
Begin CA01 source-span extraction at the Career Palace opening and Ziwei section.
