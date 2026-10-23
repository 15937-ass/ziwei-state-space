# TP03 Property Projection Review — canonical source pass

Issue #525 re-adjudicates **TP03-201..300** directly against SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》田宅宫 printed pp162–164.

## Census
- 100 / 100 rows directly source-rechecked
- 82 reusable projection rules
- 18 CASE_SUPPORT_ONLY
- 2 PATH_DEPENDENT_GATE: TP03-238, TP03-248
- 9 legacy YEAR rows
- 1 legacy DECADE row (TP03-273)

## Source-preserving repairs
Nine rows required a canonical condition/target/scope repair:
- TP03-206: Archived `天府受夹结构` was too broad. Canonical condition preserves the source instruction to examine the connected 天相 and, when 天府与禄存同度, still check whether other malefics are added.
- TP03-208: Printed source says `唯遇上述情形，则主被逼变动`. Canonical surface preserves antecedent dependence on the preceding 天府受夹 context rather than inventing a global pressure-category operator.
- TP03-252: Printed/extracted source reads `若见惊喜则主添人口`. Archived `喜庆相关曜` broadened the source; canonical surface restores the source wording and preserves the nonstandard glyph/phrase.
- TP03-266: Extracted source reads `巨天太阳同拱者`; archived candidate silently regularized to 巨门. Canonical condition preserves the source wording as uncertain rather than asserting a correction.
- TP03-273: Source explicitly says `巨门吉化，而大运流年却化为忌星者`. Legacy primary DECADE is retained for compatibility while the time-scope sidecar records both DECADE and YEAR.
- TP03-278: Extracted source reads `天相与须见禄`. Canonical surface expresses the safely supported requirement while preserving the damaged source wording in-line.
- TP03-287: Extracted source reads `魁铖夹`; archived candidate used 魁钺夹. Canonical surface preserves the source glyph uncertainty.
- TP03-290: Extracted source reads `若武曲化忌则主倾效`. Because the final glyph sequence is uncertain, the target is narrowed from `severe_property_decline_or_loss` to the safely supported adverse property decline/loss direction.
- TP03-292: Extracted source reads `必因事事而置业`. The archived target expanded this to `life_or_career_events`. Canonical target removes that unsupported causal gloss and retains only property acquisition / household celebration.

## Explicit uncertainty
The following source strings remain uncertain/nonstandard and are not silently normalized:
- TP03-252: Printed/extracted source reads `若见惊喜则主添人口`. Archived `喜庆相关曜` broadened the source; canonical surface restores the source wording and preserves the nonstandard glyph/phrase.
- TP03-256: Extracted source reads `若见煞忌，则片全无`. The damaged/nonstandard wording is preserved as lexical uncertainty; no stronger normalized claim is introduced.
- TP03-257: Extracted source includes `或为兵灾火独`. The damaged glyph sequence is preserved as uncertainty. The event target remains a bounded source-specific candidate, not a precise guaranteed fire claim.
- TP03-266: Extracted source reads `巨天太阳同拱者`; archived candidate silently regularized to 巨门. Canonical condition preserves the source wording as uncertain rather than asserting a correction.
- TP03-278: Extracted source reads `天相与须见禄`. Canonical surface expresses the safely supported requirement while preserving the damaged source wording in-line.
- TP03-287: Extracted source reads `魁铖夹`; archived candidate used 魁钺夹. Canonical surface preserves the source glyph uncertainty.
- TP03-290: Extracted source reads `若武曲化忌则主倾效`. Because the final glyph sequence is uncertain, the target is narrowed from `severe_property_decline_or_loss` to the safely supported adverse property decline/loss direction.
- TP03-292: Extracted source reads `必因事事而置业`. The archived target expanded this to `life_or_career_events`. Canonical target removes that unsupported causal gloss and retains only property acquisition / household celebration.

## Gap lineage
TP02-GAP-001 (`空劫夹亦主破败`) is now closed by direct source review of TP03-205. It remains a separate property-decline/loss branch and is not folded into the relocation/sale branch.

## Time semantics
TP03-273 explicitly contains both 大运 and 流年 in the source. The legacy primary field remains DECADE, while the sidecar preserves `[DECADE, YEAR]`. TP03-261/262 preserve `中年后` literally and do not numericize it.

No Product file, primitive qi, memory type, runtime time primitive, weight, probability, or decay is introduced.
