# WP05 Career/Official Palace Final Closure Audit

Status: **CLOSED — SOURCE-SPAN + SCHEMA VERIFIED**

## Corpus boundary
- palace: 事业宫 / 官禄宫 / P09
- canonical source: SRC-ZZ-003
- chapter source span: printed pp132–155
- checkpoints: CA01–CA09
- final reviewed records: 888
- reusable projection rules: 869
- CASE_SUPPORT_ONLY: 19
- source-explicit history feedback: 37
- unique projection_rule_id: 888 / 888
- source_span_verified: 888 / 888
- canonical time_layer/condition schema drift: 0
- next printed chapter: 田宅宫

## Semantic closure
Career Palace is modeled as a bounded career/occupation/organizational-role system rather than a single “career good/bad” score.

The reusable structure is:

**P09 industry nature / work mechanism**
→ **organizational role and responsibility**
→ **development / preservation / change / volatility**
→ **status / reputation / authority**
→ **resource and P05 wealth interaction**
→ **collaboration / support / subordinate structure**
→ **mobility / internal-external role orientation**
→ **P01 and other cross-palace constraints**
→ **star-system modifiers**
→ **temporal triggers and explicit history feedback**

Key distinctions preserved:
- career success, social status, authority, reputation and personal wealth are not collapsed into one result variable;
- industry type and organizational responsibility are separate;
- ancient military/civil/artisan/merchant labels are translated as auditable scenes, not fixed modern occupations;
- independent responsibility does not automatically mean entrepreneurship;
- Hualu/Huaquan/Huake do not automatically imply equivalent personal wealth;
- existing-platform development and self-created career are distinct;
- fame-before-profit, hardship-before-achievement, setback-before-change and other ordered relations are represented only when source-explicit;
- concrete imprisonment, fatal hazard, blood injury, corruption, litigation, exact event-count and similarly high-specificity claims remain CASE_SUPPORT_ONLY.

## History closure
All 37 P09 source-explicit stateful items fit the already approved memory architecture:
- PATH_DEPENDENT_GATE: 35
- ACQUIRED_DISPOSITION: 2

CA09 provides the clearest Career Palace support for ACQUIRED_DISPOSITION:
- Qisha: acquired human-relations cultivation and skill training modify later expression;
- Pojun: specialized-skill acquisition can be required before later development.

No third memory type is required.

The literal source statement that Pojun can establish a base after “three or four consecutive favorable years” is preserved as source evidence only. It does not introduce a universal numeric threshold, a new independent time scale, a probability, a hazard rate, or decay.

## Schema closure
A product-side readiness audit correctly detected that CA04–CA08 had a serialization-position defect: the header declared `time_layer, condition` while 500 rows stored the two values in the reverse positions.

Knowledge-side canonical repair:
- repaired batches: CA04, CA05, CA06, CA07, CA08;
- repaired rows: 500;
- semantic values changed: 0;
- rule IDs changed: 0;
- provenance changed: 0;
- CASE_SUPPORT_ONLY flags changed: 0;
- history-feedback markers changed: 0.

Post-repair full-corpus validation on the closure branch:
- rows: 888
- unique IDs: 888
- source verified: 888
- invalid time_layer rows: 0
- time_layer/condition drift rows: 0

The repair is therefore schema-only and source-preserving.

## Architecture closure
Across the full P09 corpus, source extraction did **not** require:
- a new primitive qi;
- a new memory type;
- a new Human Gate;
- a new independent time scale;
- manually invented numerical weights;
- empirical probabilities;
- decay coefficients.

The existing projection schema, cross-palace constraints, SCENE_TRANSLATION, EVENT_CANDIDATE fail-closed policy, PATH_DEPENDENT_GATE and ACQUIRED_DISPOSITION remain sufficient.

## Chapter boundary
The canonical source starts **田宅宫** immediately after the final Chen-Xu Pojun paragraph on printed p155. P09 therefore closes without inferred continuation.

## Next work
Proceed to **P10 田宅宫 semantic-boundary audit**, then begin source-span extraction under the same source-first, schema-validated, no-invented-weight discipline.
