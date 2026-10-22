# Property Relation / Cross-Palace Mapping Audit 01

Status: **3/3 mapped to existing atoms; not production**

Work unit: `KB-WP07A-PROPERTY-RELATION-CROSS-PALACE-MAP-01` / Issue #607  
Approved source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》, 田宅宫  
Canonical baseline: 358/358 source-rechecked on main

## Mapped source conditions

- **TP01-027 — 紫微七杀同度或对拱** (printed p156). Preserve two distinct geometry branches: Ziwei and Qisha both in P10, OR Ziwei in P10 with Qisha in its opposite P04. The source says the property outcome must then be refined by Tianfu's condition. The mapping does not decide whether Tianfu's treasury is full or empty.
- **TP02-129 — 武曲七杀与天府对拱** (printed p159). Require Wuqu and Qisha in P10, Tianfu in P04, and the explicit P10→P04 OPPOSITE fact. This identifies the Tianfu context to inspect; it does not encode 得禄 or 府库空露.
- **TP02-163 — 天同与天梁对拱相对同度比较** (printed p160). Require Tiantong in P10 and Tianliang in P04 with OPPOSITE relation. Keep the canonical target `opposition_variant_is_relatively_smoother_for_property_acquisition` and an explicit same-palace baseline in metadata. This is a source-relative structural claim, not an absolute promise of acquisition.

## Current atom and resolver boundary

Only existing atoms are used:

- `PALACE_HAS_STAR(palace=P10/P04, star=<source star>)`
- `PALACE_RELATION(source=P10, target=P04, relation=OPPOSITE)`

The resolver emits explicit OPPOSITE / TRIAD facts. Same-palace geometry is represented by binding both stars to P10; no `SELF` runtime fact is invented. Boolean `alternatives` preserve TP01-027's two branches.

## Unresolved semantic boundaries preserved

- **Tianfu treasury state:** current approved atoms do not define a general `府库充盈 / 府库空露` state. Missing `TRANSFORMATION_PRESENT` is not evidence of an empty treasury, and generic 得禄 is not silently equated with a single 化禄 fact.
- **Comparative statement:** TP02-163's relative direction remains in the exact canonical projection target and comparison metadata. No runtime comparator, score, probability, or numerical ranking is created.
- No relation/treasury semantics are added to Core, ontology, or Product.

## Non-scope

- TP02-139 remains a direct-star rule, not a relation rule.
- TP03-288 / TP03-289 retain the Tianfu cross-palace and treasury-state dependency for a later pass.
- TP02-195's property-home vs work-institution dual scene remains separate.
- Clamping (夹), generic 吉曜/煞曜 groups, brightness, branch gates, transformations beyond explicitly modeled facts, and CASE_SUPPORT_ONLY event candidates remain excluded.

## Boundary

- 3 nominated; 3 mapped; 0 blocked.
- All selected rows are source-span-verified, NATAL, and non-CASE_SUPPORT_ONLY on the activation base.
- Mapping proves representability only; all entries remain non-executable.
- No canonical source row, Product runtime, production registry, shared Core semantics, probability, numeric weight, or threshold is modified.
