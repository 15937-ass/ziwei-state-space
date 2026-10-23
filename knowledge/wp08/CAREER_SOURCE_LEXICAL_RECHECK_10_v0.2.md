# Career Source Lexical Recheck 10 v0.2

**Issue #472 — second-pass source adjudication; not new rule coverage.**

## Scope correction
The ten target IDs are exactly the same ten IDs already present in `CAREER_SOURCE_LEXICON_QUANTIFIER_10_v0.1.json` from Issue #469. The earlier Issue #472 description incorrectly called them remaining residuals. This recheck therefore compares prior decisions against current main closure and corrects only source-supported semantic drift.

## Results
- reviewed: **10/10**
- exact overlap with Issue #469: **10/10**
- blocker restorations: **1** (CA01-059)
- blocker reclassifications: **1** (CA06-502)
- pair-internal semantics confirmed: **3 source-local pairs**
- outer list quantifiers newly resolved: **0**
- newly blocker-free rows: **1** (CA05-433)
- compiled conditions / execution unlocks: **0 / 0**

## Per-rule adjudication
- **CA01-059** — retain the source-explicit carriers 廉贞化禄、贪狼化禄、武曲化禄. The inner quantifier of the three-name list remains unspecified; restore `SOURCE_LIST_QUANTIFIER_UNSPECIFIED` while retaining current closed-world absence and auxiliary-support blockers.
- **CA02-107** — `刑曜` remains an open/exampled category; no closed member table.
- **CA03-289** — upper-volume evidence explicitly confirms pair-internal semantics for 三台/八座 and 恩光/天贵. It does **not** establish outer `ANY_OF` or `ALL_OF` across the pair list. Keep both `SOURCE_LIST_QUANTIFIER_UNSPECIFIED` and `SOURCE_OPEN_TAIL_MEMBERSHIP_UNSPECIFIED`; do not adopt the earlier branch's blocker-free ANY expression.
- **CA04-345** — preserve the exact surface `多见属火的星曜`; elemental membership remains open and `多见` remains nonnumeric.
- **CA04-391** — five-item list, quantifier unspecified; no universal list rule.
- **CA05-433** — deeper same-source recheck resolves the local phrase as **pair co-presence**. The Career clause says `见天厨、火星同度者尤然`; the same volume later repeats `天厨、火星同度` for food-industry manifestation and explicitly contrasts `不见天厨` with sharp-tool occupations, while the 福德宫 section again uses `天厨、火星同躔` for food appreciation. This supports `PAIR_CO_PRESENT(天厨,火星)` for this source-local construction only; no global pair rule is created.
- **CA05-484** — existing main closure already captures ranked 武曲化禄/禄存 alternatives and the explicit outer OR to 天府化科; confirm only.
- **CA06-502** — refine generic `SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED` to existing `LU_SHORTHAND_CONTEXTUAL_UNRESOLVED`. The source requires 见禄 and locally attests two carriers but does not declare them exhaustive.
- **CA08-723** — preserve `刑忌来会` as a source pattern, not the distinct named pattern `刑忌夹印`; current compound and closed-category blockers remain.
- **CA09-864** — `吉辅` is retained only as a scoped qualified-support alias candidate; membership/activation remains open.

## Source-derived boundary
Cross-source pair evidence can resolve the internal structure of a named pair. Repeated same-source syntax can also resolve pair-internal co-presence when the source itself supplies a discriminating contrast, as with CA05-433. Neither route, by itself, licenses a global ANY/ALL rule or a universal pair dictionary.

## Guardrails
No global ANY/ALL/N_OF default, no numerical cardinality threshold, no closed-world expansion, no Product/runtime changes, no compiled condition, no execution unlock.
