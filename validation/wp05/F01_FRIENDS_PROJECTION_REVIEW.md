# WP05 Friends/Subordinates Palace F01 — Source Review 001–100

Status: **CHECKPOINT_CLOSED_SOURCE_SPAN_VERIFIED**

## Scope
- source: SRC-ZZ-003
- palace: P08 交友宫 / 奴仆宫
- source span: printed pp122–124
- reviewed records: F01-001 … F01-100
- coverage: chapter semantic boundary + Ziwei complete + Tianji complete + Solar opening

## Result
- reviewed: 100
- SOURCE_SPAN_VERIFIED: 100 / 100
- reusable projection rules: 98
- CASE_SUPPORT_ONLY: 2
- history-feedback items: 3
- new primitive qi: 0
- new history-memory type: 0
- new Human Gate: 0
- new numeric weights / decay / probabilities: 0

## Modeling notes
- The opening chapter boundary is encoded explicitly: same-generation peers remain primarily P02, personally cultivated protégés route to P04, and ordinary subordinates/lower-generation contacts remain P08.
- P08 is not scored by "stronger is better": the source explicitly requires balance against P01 Life Palace.
- Ziwei rules preserve the distinction between subordinate loyalty, subordinate authority, power transfer, native being sidelined, and later independent development by capable subordinates.
- Tianji rules separate network breadth, turnover, temporary support, trustworthiness and relational stability. These are not collapsed into one social score.
- Severe concrete romance-loss or appropriation claims remain EVENT_CANDIDATE + CASE_SUPPORT_ONLY.

## History feedback
Three source-explicit ordered relations are retained in a WP05 sidecar:
- capable Ziwei-Pojun subordinates can later leave for independent development, followed by recurring support shortage;
- subordinate independent development under the stated Ziwei-Pojun/Wuqu-Huaji structure can later damage the native's interest;
- Tianji-Jumen relationship is explicitly described as starting well and ending badly.

All fit the existing PATH_DEPENDENT_GATE. No persistence duration, transition probability or decay is inferred.

## Next anchor
Continue Solar, then Wuqu.
