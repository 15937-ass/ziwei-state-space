# WP05 Disease Palace D01 — Source Review 001–100

Status: **CHECKPOINT_CLOSED_SOURCE_SPAN_VERIFIED**

## Scope
- source: SRC-ZZ-003
- chapter: Disease Palace
- source span: printed pp93–95
- reviewed records: D01-001 … D01-100
- coverage: chapter methodology + Ziwei complete + Tianji opening
- semantic boundary: `validation/wp05/DISEASE_PALACE_SEMANTIC_BOUNDARY.md`

## Result
- reviewed: 100
- SOURCE_SPAN_VERIFIED: 100 / 100
- reusable projection rules: 52
- CASE_SUPPORT_ONLY: 48
- history-feedback items: 0
- new primitive qi: 0
- new history-memory type: 0
- new Human Gate: 0
- numeric health probabilities / hazard rates / continuous decay introduced: 0

## Boundary decisions
- General constitution, body-system susceptibility, five-element mechanism, whole-chart requirements and temporal activation logic are reusable.
- Named diseases, surgery, disability, cancer, poisoning and other concrete medical outcomes are quarantined as EVENT_CANDIDATE + CASE_SUPPORT_ONLY.
- Natal susceptibility is not treated as diagnosis.
- The source's decade/year activation logic is handled by the existing temporal resolver and does not create a new history-memory class.
- The source explicitly rejects deterministic disease inevitability and explicitly acknowledges empirical limits; those limits are preserved in the corpus.

## Next anchor
Complete Tianji, then Solar and Wuqu.
