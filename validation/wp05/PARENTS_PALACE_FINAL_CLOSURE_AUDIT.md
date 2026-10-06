# WP05 P12 Parents/Superiors Palace Final Closure Audit

Status: **CLOSED — SOURCE-SPAN + SCHEMA VERIFIED**

## Corpus boundary
- palace: P12 父母宫
- canonical source: SRC-ZZ-003
- chapter source span: printed pp177–187
- checkpoints: PP01–PP04
- final reviewed records: 416
- reusable projection rules: 273
- CASE_SUPPORT_ONLY: 143
- source-explicit history feedback: 3
- unique projection_rule_id: 416 / 416
- source_span_verified: 416 / 416
- invalid time_layer rows: 0
- canonical time_layer/condition schema drift: 0
- next palace chapter: none — P12 is the final palace in 下篇·宫垣论

## Semantic closure
P12 is a dual-scene relational system:

**parent / family-of-origin scene**
→ parent relationship, authority, support, protection, distance, mobility, resources, family structure, inheritance

**superior / manager / supervising-institution scene**
→ superior relationship, authority, support, turnover, promotion/suppression, supervising-institution context

These scenes share palace evidence but are never collapsed into one target.

Key distinctions preserved:
- Sun/Moon parent attribution applies to parent-specific interpretation and is not reused mechanically for superior interpretation;
- 禄权科 may describe parent protection or superior status and does not automatically mean prominent parents;
- 四煞 may describe relational tension rather than inevitable parent harm;
- strong P12 does not automatically benefit a weak P01 unless source-supported protection/benefit exists;
- parent illness/death, bereavement, adoption/remarriage and multiple-parent claims remain high-specificity candidate material.

## Family-structure closure
Historical terms such as 重拜父母、二姓延生、偏房继室、两重父母、出祀/过继 are preserved with provenance but normalized cautiously.

Where the source itself gives a modern reinterpretation, the corpus prefers bounded scene translations such as:
- childhood boarding/foster care;
- physical separation because parents work elsewhere;
- step-parent/remarriage context;
- multiple caregiver or multiple supervisor structures;
- closeness to spouse family while distant from birth parents.

No historical remedy is treated as a causal intervention.

## History closure
P12 has three source-explicit history-feedback relations:
- initially good superior relationship -> misunderstanding -> deterioration;
- sudden superior relationship change -> rights conflict / rupture;
- initial superior support -> later deterioration under adverse context.

All fit the existing PATH_DEPENDENT_GATE. No new memory type is required.

## Timing closure
The source contains:
- annual parent/superior activation;
- a few named major-period positions;
- Sun/Moon period cross-checks;
- annual bereavement conditions.

These remain source timing evidence and do not introduce:
- a new independent clock;
- a universal age threshold;
- event probability;
- persistence/decay coefficients.

## Schema closure
All PP01–PP04 rows serialize in canonical header order:
`palace_id,time_layer,condition,projection_domain,...`

Full-corpus validation on the closure branch:
- rows: 416
- unique IDs: 416
- source verified: 416
- invalid time_layer rows: 0
- time_layer/condition drift rows: 0

## Architecture closure
Across P12, extraction did **not** require:
- a new primitive qi;
- a new memory type;
- a new Human Gate;
- a new independent time scale;
- manually invented numerical weights;
- empirical probabilities;
- decay coefficients.

The existing projection schema, cross-palace constraints, SCENE_TRANSLATION, EVENT_CANDIDATE fail-closed policy and PATH_DEPENDENT_GATE remain sufficient.

## Twelve-palace boundary
The source's 下篇·宫垣论 table of contents enumerates exactly the twelve palaces from 命宫 through 父母宫, with 父母宫 last.

Closing P12 therefore triggers the **WP05 Twelve-Palace Final Closure Audit** rather than another palace extraction unit.
