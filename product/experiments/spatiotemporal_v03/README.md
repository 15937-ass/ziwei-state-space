# Spatiotemporal guarded-temporal probe v0.3

Status: **TEST_ONLY / NOT CANONICAL / NOT PRODUCTION-CONSUMABLE**

## Why this phase exists

- v0.1 tested layer and guard plumbing on a tiny demo asset.
- v0.2 tested natal-only Z12 coordinate views on engine-materialized charts.
- v0.3 checks whether a full twelve-palace natal projection and six temporal scopes can coexist in one pinned engine-output projection while preserving target, layer, and provenance boundaries.

## Input

The reduced fixture is derived from the P1 dual-engine workflow artifact `40161980768` (artifact `12586873751`, SHA-256 digest recorded in the fixture). It selects CR-001 and CR-031, each at T1_LEAP_LATE_ZI and T3_DAYTIME: four target snapshots and 24 temporal scope instances. The input is engine-generated regression data, not source-transcribed ground truth.

The fixture uses compact positional encoding only to avoid duplicating the same twelve palace names. `probe.py` expands it before calling the existing PL3-T temporal adapter. `age.s=null` means the exporter represented `stars=[]`; other scope star maps preserve only non-empty palace groups.

## What is tested

- branch-indexed occupancy and permutation-matrix view equivalence;
- complete unique twelve-palace maps and input-order invariance;
- six-scope mapping and adapter provenance;
- natal projection invariance across two targets for the same case;
- explicit TEST_ONLY temporal guards, including a palace-bound YEAR star that changes palace between targets;
- raw scope-level `mutagen` values versus condition facts derived by the current adapter.

## Finding boundary: scope-level mutagen is not the glyph

The pinned upstream **iztro v2.6.1** type declares `HoroscopeItem.mutagen: StarName[]` ([source at the exact tag](https://github.com/SylarLong/iztro/blob/v2.6.1/src/data/types/astro.ts)); its separate `Mutagen` type represents the four transformation labels (禄、权、科、忌; [type definition](https://github.com/SylarLong/iztro/blob/v2.6.1/src/i18n/types/mutagen.ts)). In the selected projection, all 96 scope-level entries are star names and each is present in the corresponding natal star inventory.

This means the earlier toy fixture's glyph-like `mutagen` values are inconsistent with the pinned upstream scope type. The current adapter preserves those scope-level names but serializes them as `TRANSFORMATION_PRESENT(mutagen=<raw value>)`. That serialization must not be interpreted as specifying a particular glyph or a star-to-glyph binding. The normalized field does not carry an explicit (star, glyph) pair, and this probe does not infer a glyph from array position. Any such mapping requires separate version-pinned evidence and a reviewed contract. v0.3 records this semantic-mapping gap; it does not change the production adapter or invent the missing association.
## Non-goals

No source truth claim, canonical reaction-rule acceptance, inference-runtime change, KIB promotion, production migration, predictive-validity claim, performance claim, or universal temporal-layer priority.
