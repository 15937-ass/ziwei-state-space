# Canonical Chart Migration: v1.0 → v1.1

Status: **MIGRATION PLAN — Product Issue #981**

## 1. Change

- v1.0: `day_divide=forward`; late Zi (23:00–23:59) is attributed to the next day.
- v1.1: `day_divide=current`; late Zi remains on the supplied date, and the new date begins at 00:00.
- v1.1 additionally requires the input time basis to be explicitly recorded as `true_solar_time`; the chart engine must not apply a second birthplace/location correction.

The pinned production engine remains `iztro-js@2.6.1`; the Zhongzhou algorithm and all other v1.0 chart settings remain unchanged.

## 2. Historical data policy

- Keep v1.0 contract JSON/Markdown, old regression inputs, old B02-B manifest, historical P1 acceptance reports, and old Wang case materialization artifacts unchanged.
- A v1.0 snapshot is not a v1.1 production snapshot. The v1.1 validator must reject its old contract ID/config.
- Do not rewrite a historical chart by changing its contract ID or config metadata.
- A historical source case may be re-materialized only through a separately versioned process that rechecks the original source inputs and target anchors.

## 3. New regression inputs

- New canonical seed set: `validation/product_chart_regression/regression_inputs_v0.2.csv`.
- New late-Zi manifest: `validation/product_chart_regression/b02b_zi_day_boundary_v0.3.json`.
- Existing v0.1 CSV and v0.2 B02-B manifest remain historical.
- Run the 100-seed JS/Rust full differential and B02-A/B02-B/B02-C boundary workflows under the v1.1 input/config contract.

## 4. Input time policy

The v1.1 chart engine accepts an already supplied true-solar-time input. The chart layer does not infer birthplace, longitude, timezone or daylight-saving corrections. A future place-conversion component must be upstream, versioned, provenance-bearing, and applied exactly once.

## 5. Cutover

- Before PR acceptance: v1.0 remains the accepted main contract.
- After PR acceptance: v1.1 becomes the sole production contract for newly generated snapshots.
- Old v1.0 snapshots remain historical and fail the v1.1 production admission gate until regenerated and revalidated.
- No Knowledge/Core content, palace semantics, inference permission or predictive-validity claim changes.
