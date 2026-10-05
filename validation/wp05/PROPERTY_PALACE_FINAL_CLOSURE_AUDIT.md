# WP05 P10 Property/Home Palace Final Closure Audit

Status: **CLOSED — SOURCE-SPAN + SCHEMA VERIFIED**

## Corpus boundary
- palace: P10 田宅宫
- canonical source: SRC-ZZ-003
- chapter source span: printed pp156–165
- checkpoints: TP01–TP04
- final reviewed records: 358
- reusable projection rules: 308
- CASE_SUPPORT_ONLY: 50
- source-explicit history feedback: 14
- unique projection_rule_id: 358 / 358
- source_span_verified: 358 / 358
- invalid time_layer rows: 0
- canonical time_layer/condition schema drift: 0
- next printed chapter: 福德宫

## Semantic closure
P10 is not a single “property luck” score. The source supports several distinct projection families:

**residence / household condition**
→ **property acquisition, inheritance, preservation and loss**
→ **relocation / renovation / workplace movement**
→ **service-institution rise, decline and personnel environment**
→ **family-caused property relations**
→ **property dispute / contract / litigation**
→ **residence quality and environmental sensitivity**
→ **time-layer event activation**

Key distinctions preserved:
- ownership is not the same as speculative investment return;
- residence movement is not the same as purchase/sale;
- employer/service-institution condition is not the same as P09 career role;
- family-caused property outcomes may project through other family palaces;
- inherited property, existing platform and self-acquired property are distinct;
- severe fire, bereavement, litigation, fraud, structural damage and supernatural/pest claims remain CASE_SUPPORT_ONLY.

## History closure
All 14 P10 stateful items fit the existing PATH_DEPENDENT_GATE.

Representative source-explicit sequences include:
- existing/inherited property -> decline;
- sudden increase -> sudden loss;
- prolonged property burden -> decline;
- sale -> later purchase;
- decline -> later self-acquisition;
- ancestral breakdown -> later recovery;
- existing property -> transformed self-created base.

No new history-memory type is required.

## Timing closure
The source includes life-stage language such as middle/later life and a few explicit age thresholds. These remain source timing evidence only.

P10 does not introduce:
- a new independent clock;
- universal age thresholds;
- transition probabilities;
- property-value weights;
- decay coefficients.

## Schema closure
All TP01–TP04 rows serialize in canonical header order:
`palace_id,time_layer,condition,projection_domain,...`

Full-corpus validation on the closure branch:
- rows: 358
- unique IDs: 358
- source verified: 358
- invalid time_layer rows: 0
- time_layer/condition drift rows: 0

## Architecture closure
Across P10, source extraction did **not** require:
- a new primitive qi;
- a new memory type;
- a new Human Gate;
- a new independent time scale;
- manually invented numerical weights;
- empirical probabilities;
- decay coefficients.

The existing projection schema, cross-palace constraints, SCENE_TRANSLATION, EVENT_CANDIDATE fail-closed policy and PATH_DEPENDENT_GATE remain sufficient.

## Chapter boundary
The source starts **福德宫** immediately after the final Pojun paragraph. P10 therefore closes without inferred continuation.

## Next work
Proceed to **P11 福德宫 semantic-boundary audit**, then begin source-span extraction under the same source-first, schema-validated, no-invented-weight discipline.
