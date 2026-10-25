# P09 Relation-Scope Gap Disposition — 3 rows (v0.1)

Status: **source rechecked; three relation-scope gaps retained unresolved**

- Issue: #785
- Lane / shard: `KNOWLEDGE_ONLY / P09 事业宫`
- Source: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》
- Source SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`
- Visual scan pages inspected: PDF physical pp73–75, corresponding to printed pp145, 147 and 150 for the three target spans.
- Scope: `CA05-484`, `CA06-582`, `CA07-699` only. The accepted 888-rule Career corpus was not re-extracted.

## Result

| Gap | Rule | Source span | Disposition |
|---|---|---|---|
| `P09-REL-SCOPE-GAP-001` | `CA05-484` | Printed p145 / PDF p73 | `RETAINED_UNRESOLVED` |
| `P09-REL-SCOPE-GAP-002` | `CA06-582` | Printed p147 / PDF p74 | `RETAINED_UNRESOLVED` |
| `P09-REL-SCOPE-GAP-003` | `CA07-699` | Printed p150 / PDF p75 | `RETAINED_UNRESOLVED` |

All three scan spans were visually rechecked. The source supports the relation words but does not directly define deterministic palace geometry for generic `会/同会`. For `CA06-582`, it also does not resolve the composition of `见 + 同会`. Therefore no row gains a new executable condition representation in this batch.

### Per-row source findings

1. **CA05-484 — printed p145.** The source says `[廉相]会禄（武曲化禄为上，禄存次之），或会天府化科，宜握财权。` The `或` alternative is preserved as source-local OR. The geometry of `会` remains unspecified.
2. **CA06-582 — printed p147.** The source says `太阴主富不主贵，故守事业宫时，必以见文昌文曲同会，然后始主其人有社会地位。` The named `文昌、文曲` pair is retained as source-clause-local BOTH; neither `见` nor `同会` is assigned a guessed binding, and their composition remains unresolved.
3. **CA07-699 — printed p150.** The source says `巳亥宫巨门，亦主先有社会地位，然后财富始随名誉而来。故以同会文昌、文曲为贵。唯不喜昌曲化忌，则其社会地位终有限度。` The named pair remains local to this clause; generic `同会` geometry remains unspecified.

## Explicit non-changes

- No canonical rule was changed and no new source meaning was promoted.
- `conditions_compiled=0`; `execution_unlocked=0`.
- No Product/runtime permission, probability, numeric weight, or generic meeting default is introduced.
- The 11 dependency-effective-underdetermined rows remain outside this batch and fail-closed.
- This batch does not close the P09 stage. Continue only through separately bounded, gap-driven work; do not re-extract the accepted 888 source rules.

Machine-readable counterpart: `P09_RELATION_SCOPE_GAP_DISPOSITION_3_v0.1.json`.
