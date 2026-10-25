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

## Finding boundary

The P1 exporter’s scope-level `mutagen` arrays contain transformed star names (e.g. 天梁 / 紫微 / 左辅 / 武曲), while the earlier tiny test fixture used glyph-like values (e.g. 科). The current adapter preserves the raw array values as `TRANSFORMATION_PRESENT(mutagen=<value>)`. v0.3 records this representation difference for contract review; it does not reinterpret or patch it.

## Non-goals

No source truth claim, canonical reaction-rule acceptance, inference-runtime change, KIB promotion, production migration, predictive-validity claim, performance claim, or universal temporal-layer priority.
