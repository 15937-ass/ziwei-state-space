# Comparison report — spatiotemporal probe v0.3

**Status:** TEST_ONLY engineering probe. This is not canonical rule acceptance and not a production-readiness decision.

## Fixture and coverage

- Pinned producer: Product P1 dual-engine workflow run `40161980768`, artifact `12586873751`, SHA-256 digest `730158ea500b26b458ca836091a23bf209363e8121437bf0296f374dc5936a8f`.
- Selected regression cases: CR-001 and CR-031.
- Selected targets: T1_LEAP_LATE_ZI and T3_DAYTIME.
- Coverage: 2 natal projections, 24 palace records, 4 target snapshots, 24 temporal scope instances, 204 temporal star objects.
- The fixture omits birth inputs and nonessential natal metadata. It is a reduced projection of engine-generated output, not source-transcribed ground truth.
- The source-row SHA-256 values for CR-001 and CR-031 are verified against the pinned regression CSV using exact UTF-8 row text excluding line terminators; the hashes and convention are recorded in the fixture manifest.

## Deterministic structural results

| Check | Count |
|---|---:|
| Index/matrix offset equivalence | 24 |
| Inverse checks | 24 |
| Cyclic composition checks | 288 |
| Input-order invariance | 2 |
| Target-isolation pairs | 2 |
| Raw scope-level mutagen entries | 96 |

The probe enforces twelve unique natal palace identities per chart, six distinct temporal scope labels per target, twelve unique palace-name positions per scope, and target-dependent temporal signatures without rebuilding the natal projection.

## Source-grounded scope-mutagen finding

The pinned upstream **iztro v2.6.1** type defines `HoroscopeItem.mutagen: StarName[]` ([exact-tag type](https://github.com/SylarLong/iztro/blob/v2.6.1/src/data/types/astro.ts), blob `2d692b84e9a28c6786c804078f06d34c4388125f`). The separate `Mutagen` type is the four transformation labels; the simplified-Chinese mapping is 禄、权、科、忌 ([exact-tag type](https://github.com/SylarLong/iztro/blob/v2.6.1/src/i18n/types/mutagen.ts), blob `268d2440e3ea024a07673942cbe313bfe752fca3`; [locale values](https://github.com/SylarLong/iztro/blob/v2.6.1/src/i18n/locales/zh-CN/mutagen.ts), blob `7bb0325767a33ffc0c2e9c5952e3ac43c1978e80`).

In the pinned projection, all 96 scope-level entries are star names, and all occur in the corresponding natal star inventory. Therefore, the earlier toy fixture's glyph-like scope values do not match the pinned upstream type. The current adapter preserves the names but emits `TRANSFORMATION_PRESENT(mutagen=<star name>)`. This is a **semantic-mapping gap**, not a reason to reinterpret the raw values. The normalized field does not carry an explicit (star, glyph) pair, and this probe does not infer a glyph from array position. Any such mapping requires separate version-pinned evidence and a reviewed contract. This probe records the issue and deliberately does not modify production code.
## Engineering decision

**KEEP_INDEX_BASELINE.** No production migration benefit has been demonstrated. Continue the isolated TEST_ONLY guarded-temporal experiment, but do not promote canonical reaction semantics until scope-level mutagen-to-glyph binding semantics are contractually resolved.

## Not evaluated

- Source-transcribed full-chart equivalence.
- Traditional semantic correctness.
- Eligibility of canonical temporal reaction rules.
- Runtime performance or migration benefit.
- Predictive validity or probability calibration.
