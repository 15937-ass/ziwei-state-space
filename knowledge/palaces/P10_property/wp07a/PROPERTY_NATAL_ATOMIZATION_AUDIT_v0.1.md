# Property NATAL Atomization Pilot v0.1

Status: **COMPLETE — 3/3 mapped with existing atom, not production**

This is the P10 analogue of the first Career WP07A atomization pilot.

## Mapped rules
- **TP02-141** — 天同化忌 → property-related worry/effort can coexist with self-acquired property.
- **TP03-262** — 巨门化禄 → the source strengthens the mid/later-life self-acquisition tendency. `中年后` remains literal source language and is not assigned an age.
- **TP04-314** — 天梁在田宅宫化禄 → interpersonal/social friction strengthens.

Each condition maps to exactly one existing natal fact:
`TRANSFORMATION_PRESENT(palace=P10, star=<star>, mutagen=<禄/忌>)`.

## Why these three
They are canonical NATAL rows, source-span verified, non-case-only, and their trigger does not require a generic 吉煞 group, an unresolved relation geometry, a 前格 dependency, or a temporal fact.

## Nearby rows deliberately excluded
Compound rows such as TP02-142/143/144 and TP04-315/316 are not simplified into the direct transformation rule. TP03-263 remains CASE_SUPPORT_ONLY. Shared group semantics such as 四煞 are not defined by this P10 worker.

## Runtime fact-shape check
`ResolvedPalaceStructure.runtime_facts` already emits a palace/star/mutagen `TRANSFORMATION_PRESENT` fact when the P10 star object itself carries the mutagen. Dedicated tests build synthetic 12-palace snapshots and verify that the three expected atoms are actually emitted.

No source row, Product runtime, production registry, shared ontology, weight, probability or threshold is modified.
