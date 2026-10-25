# Comparison report — spatiotemporal probe v0.3

**Status:** TEST_ONLY engineering probe. This is not canonical rule acceptance and not a production-readiness decision.

## Fixture and coverage

- Pinned producer: Product P1 dual-engine workflow run `40161980768`, artifact `12586873751`, SHA-256 digest `730158ea500b26b458ca836091a23bf209363e8121437bf0296f374dc5936a8f`.
- Selected regression cases: CR-001 and CR-031.
- Selected targets: T1_LEAP_LATE_ZI and T3_DAYTIME.
- Coverage: 2 natal projections, 24 palace records, 4 target snapshots, 24 temporal scope instances, 204 temporal star objects.
- The fixture omits birth inputs and nonessential natal metadata. It is a reduced projection of engine-generated output, not source-transcribed ground truth.

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

## Contract-review finding

The pinned full exporter’s scope-level `mutagen` array contains star names such as 天梁、紫微、左辅、武曲. The earlier toy temporal fixture used glyph-like values such as 科. The current adapter preserves each raw entry as `TRANSFORMATION_PRESENT(mutagen=<raw value>)`.

This is a **representation-domain difference requiring contract review**, not an authorized production fix. v0.3 preserves the raw values and tests the derived facts without silently converting star names into glyphs.

## Engineering decision

**KEEP_INDEX_BASELINE.** No production migration benefit has been demonstrated. Continue the isolated TEST_ONLY guarded-temporal experiment, but do not promote canonical reaction semantics until the mutagen value-domain contract is resolved.

## Not evaluated

- Source-transcribed full-chart equivalence.
- Traditional semantic correctness.
- Eligibility of canonical temporal reaction rules.
- Runtime performance or migration benefit.
- Predictive validity or probability calibration.
