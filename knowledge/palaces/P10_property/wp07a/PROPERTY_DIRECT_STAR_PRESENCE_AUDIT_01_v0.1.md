# Property Direct Star-Presence Mapping Audit 01

Status: **5/5 mapped with existing atom; not production**

Work unit: `KB-WP07A-PROPERTY-DIRECT-STAR-PRESENCE-MAP-01` / Issue #583  
Approved source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》, 田宅宫  
Canonical baseline: 358/358 source-rechecked

## Mapped source conditions

- **TP01-055 — 天机守田宅宫** (printed p157). The source describes property and residence movement as a general Tianji-in-Property tendency; it explicitly warns not to reduce it to one simple “ancestral property lost, then self-acquired” path.
- **TP02-195 — 天府守田宅宫** (printed pp161–162). The source supports ancestral/parental property or service in an institution with an established reputation. No extra auxiliary-star or treasury-state condition is added.
- **TP03-297 — 天相守田宅** (printed p164). The source says Tianxiang is quite fengshui-sensitive. Its separate “煞 / 武曲破军对拱” intensifiers are not added to this base mapping.
- **TP03-253 — 贪狼守田宅** (printed p163). The source says Tanlang in the Property palace is highly sensitive to fengshui. The annual Tanlang Hua Lu/Hua Ji clauses on the same page remain separate temporal projections and are not folded into this NATAL presence atom.
- **TP04-358 — 破军守田宅** (printed p165). The source directly states that Pojun in Property is not affected by fengshui; this is not generalized to other Pojun acquisition/movement outcomes.

Each mapped condition uses exactly one existing atom:

`PALACE_HAS_STAR(palace=P10, star=<source star>)`

The current resolver emits palace-bound `PALACE_HAS_STAR` facts for named stars in each palace. This mapping establishes condition representability only; it does not create a production rule.

## Scope correction in revision r2

The earlier prepared branch accidentally substituted TP04-319 for the live Issue #583 nomination TP03-253. This revision follows the exact five IDs in Issue #583 and the canonical TP03 source row/readjudication/time-scope artifacts. TP04-319 remains a canonical source rule but is outside this bounded work unit.

## Explicit non-mapped rows retained (including scope-only deferral)

| Rule | Disposition |
|---|---|
| TP01-018 | `独坐` requires exclusivity/absence semantics, not simple presence |
| TP02-139 | Outside this exact five-ID nomination. Its canonical condition is direct `天同守田宅宫`; it is not blocked by the presence atom. Do not conflate it with the separate TP02-163 Tianliang-opposition comparison, which belongs in later relation mapping. |
| TP02-170 | Preserve source glyph uncertainty around `破组`; do not normalize silently |
| TP03-261 | Preserve literal `中年后` and surrounding source scope; reserve for context/time mapping |
| TP03-275 | The projection includes a 化忌 strengthening clause |
| TP03-288 | A 天府 condition is required; reserve for cross-palace mapping |
| TP04-320 | Separate Tianliang-specific compound fengshui clause; not collapsed into any single-star presence atom |
| TP04-321 | `独坐` and 寅申 exception cannot be reduced to star presence |

## Boundary

- 5 nominated; 5 mapped; 0 blocked.
- Only `PALACE_HAS_STAR` is used.
- No source row, Product runtime, production registry, shared Core semantic, probability, numeric weight, or threshold is modified.
- Generic 吉曜/煞曜 groups, brightness, branch gates, transformations, relation geometry, and CASE_SUPPORT_ONLY events remain outside this unit.
