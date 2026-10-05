# WP05 P10 Property/Home Palace TP01 — Source Review 001–100

Status: **CHECKPOINT_CLOSED_SOURCE_SPAN_VERIFIED**

## Scope
- source: SRC-ZZ-003
- palace: P10 田宅宫
- source span: printed pp156–158
- reviewed records: TP01-001 … TP01-100
- coverage: chapter opening methodology + Ziwei full section + Tianji full section + Taiyang opening through Taiyang-Tianliang acquisition/trouble distinction

## Result
- reviewed: 100
- SOURCE_SPAN_VERIFIED: 100 / 100
- reusable projection rules: 91
- CASE_SUPPORT_ONLY: 9
- history-feedback items: 4
- invalid time_layer rows: 0
- new primitive qi: 0
- new history-memory type: 0
- new Human Gate: 0
- new independent time scale: 0
- new numeric weights / decay / probabilities: 0

## Modeling notes
- The chapter opening is preserved as a multi-scope palace boundary: home/property, elder bereavement events, service-institution condition, residence/company relocation and cross-palace family causation are separate targets.
- Property ownership, speculative profit and career/business performance are not collapsed. The source explicitly says speculative property-trading outcomes are generally not determined by P10 alone.
- Ziwei is normalized through self-acquisition, inherited/existing property preservation, residence quality, service-institution scale, movement, contract/document risk and fengshui sensitivity.
- Tianji is normalized through movement, property turnover, workplace-environment change, neighbor/environment pressure, dispute, actual-versus-planned relocation, and fengshui sensitivity.
- Taiyang begins with ancestral property preservation, self-acquisition, service-institution mobility, public/communal property and the distinction between property trouble and other palace meanings.
- Concrete pests, supernatural disturbance, fire, litigation and bereavement claims are kept as EVENT_CANDIDATE + CASE_SUPPORT_ONLY.

## CASE_SUPPORT_ONLY
Nine high-specificity event statements are retained without deterministic generalization:
- TP01-016: termite/insect infestation candidate under Feilian.
- TP01-017: source-specific supernatural-disturbance claim.
- TP01-024: property litigation candidate in an adverse Ziwei-Pojun structure.
- TP01-036: property fire candidate in the specified Ziwei adverse structure.
- TP01-048: elder bereavement candidate under the explicit temporal/family conditions.
- TP01-066: property/neighbor litigation candidate under Tianji + legal/adverse markers.
- TP01-076: property/relocation litigation candidate under Tianji-Jumen adverse structure.
- TP01-084: fire-scare candidate in the specified Tianji-Tianliang temporal structure.
- TP01-098: public-property litigation candidate in the specified Taiyang-Tianliang adverse structure.

## History feedback
Four explicit ordered/state-dependent relations are retained:
- Ziwei-Pojun: existing/inherited property can precede later decline.
- Ziwei-Tanlang: sudden property increase can reverse into sudden loss under added adverse conditions.
- Tianji neighbor/environment conflict: continued standoff can intensify later trouble.
- Tianji-Jumen: failing to move when movement is required can precede regret.

All fit the existing PATH_DEPENDENT_GATE. No new memory type is required.

## Source timing note
The Tianji-Tianliang source gives literal life-stage thresholds for property acquisition/increase. These are preserved as source timing language only; they do not create a new independent time scale or a universal deterministic threshold.

## Next anchor
Continue Taiyang remainder, then Wuqü and Tiantong.
