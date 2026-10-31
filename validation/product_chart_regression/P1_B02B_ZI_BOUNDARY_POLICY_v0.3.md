# P1 B02-B — Zhongzhou canonical Zi/day boundary v0.3

Status: **V1.1 CANONICAL POLICY — REGRESSION PENDING**

Supersedes for new production work: `P1_B02B_ZI_BOUNDARY_POLICY.md` v0.2.  
Historical v0.2 results remain immutable and continue to describe the former `day_divide=forward` test configuration.

## 1. Source and PI decision

Wang Tingzhi, 《中州派紫微斗数初级讲义》, “出生时换算法” (PDF p.4 / printed pp.7–8), explicitly discusses the dispute over treating 23:00–01:00 as one Zi hour and selects the table split in which **00:00 begins the new day**.

The PI has selected Zhongzhou as the project's sole production school and approved this rule for production.

## 2. Canonical Zhongzhou rule

- 23:00–23:59: late Zi, `time_index=12`, remains on the supplied date.
- 00:00–00:59: early Zi, `time_index=0`, belongs to the new date.
- Engine setting: `day_divide=current`.
- `day_divide=forward` is not permitted for v1.1 production snapshots.

The supplied date/time has already been normalized to the current input contract's true-solar-time basis. The chart engine does not apply an additional birthplace, longitude or timezone correction.

## 3. Regression layers

### 3.1 Same-contract implementation hard gate

- iztro JS 2.6.1 and x-iztro 0.6.1 use the same `zhongzhou + day_divide=current` configuration.
- Full normalized diff must be zero.
- The 100-seed input set is `regression_inputs_v0.2.csv`.

### 3.2 Calendar marker validation

The late-Zi targets at the lunar year/month boundary must retain the lunar marker belonging to the supplied date. The next-day early-Zi targets must carry the new date's marker.

### 3.3 Independent Go core

The pinned Go core is not configured as the canonical Zhongzhou `day_divide=current` implementation. Late-Zi targets remain excluded from its hard equality gate and are retained as cross-school/independent diagnostics only. This exclusion does not create a second production candidate.

## 4. Product semantics

Within the selected Zhongzhou production contract:

```text
late Zi -> same supplied date
00:00   -> new date
```

Do not preserve same-day / next-day / dual-chart candidates as production ambiguity for this explicitly selected Zhongzhou contract. Other-school comparisons may be stored as diagnostic evidence, but cannot alter the canonical chart.

## 5. Historical evidence

- The former B02-B v0.2 manifest and acceptance record remain historical.
- v1.0 snapshots produced with `day_divide=forward` are not v1.1 production snapshots.
- Do not rewrite historical source charts or silently relabel their contract IDs.
- New production snapshots must carry contract ID `ZHONGZHOU_IZTRO_JS_2_6_1_V1_1`.

## 6. Acceptance

Acceptance requires:
1. 100-seed JS/Rust full normalized diff = 0;
2. civil/lunar marker errors = 0;
3. late-Zi same-date behavior explicitly exercised;
4. pinned Go core differences remain diagnostic only for late-Zi targets;
5. full repository quality gate passes on the exact integration head.
