#!/usr/bin/env node
import fs from "node:fs";
import crypto from "node:crypto";
import { astro } from "iztro";

const inputCsv = process.argv[2] || "validation/product_chart_regression/regression_inputs_v0.1.csv";
const outPath = process.argv[3] || "/tmp/p1_iztro_js.jsonl";

const TARGET_DATES = [
  "2025-01-01",
  "2025-01-28",
  "2025-01-29",
  "2025-02-03",
  "2025-02-04",
  "2025-06-21",
  // 2025 leap sixth month: day 15 / day 16 boundary.
  "2025-08-08",
  "2025-08-09",
  "2026-01-01",
  "2026-02-16",
  "2026-02-17",
  "2026-03-20",
  "2026-09-23",
  "2026-12-31",
];
const TARGET_TIME_INDICES = [0, 6, 12];

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const header = lines[0].split(",");
  return lines.slice(1).map((line) => {
    const values = line.split(",");
    return Object.fromEntries(header.map((h, i) => [h, values[i]]));
  });
}

function sha256(path) {
  return crypto.createHash("sha256").update(fs.readFileSync(path)).digest("hex");
}

const rows = parseCsv(fs.readFileSync(inputCsv, "utf8"));
const out = fs.createWriteStream(outPath, { encoding: "utf8" });
let natalCount = 0;
let horoscopeCount = 0;

for (const row of rows) {
  const config = {
    algorithm: row.algorithm,
    dayDivide: row.day_divide,
    yearDivide: row.year_divide,
    horoscopeDivide: row.horoscope_divide,
    ageDivide: "normal",
  };
  const chart = astro.withOptions({
    type: "solar",
    dateStr: row.solar_date,
    timeIndex: Number(row.time_index),
    gender: row.gender,
    fixLeap: row.fix_leap === "true",
    language: "zh-CN",
    config,
  });
  out.write(JSON.stringify({
    kind: "natal",
    case_id: row.case_id,
    input: row,
    payload: chart.toJSON(),
  }) + "\n");
  natalCount += 1;

  for (const targetDate of TARGET_DATES) {
    // 运限目标早于出生日期没有产品语义；不同实现对 pre-birth 童限的
    // fallback 处理也不同，因此不把它混入“有效运限一致性”指标。
    if (targetDate < row.solar_date) continue;
    for (const targetTimeIndex of TARGET_TIME_INDICES) {
      const h = chart.horoscope(targetDate, targetTimeIndex);
      out.write(JSON.stringify({
        kind: "horoscope",
        case_id: row.case_id,
        target_date: targetDate,
        target_time_index: targetTimeIndex,
        input: row,
        payload: h.toJSON(),
      }) + "\n");
      horoscopeCount += 1;
    }
  }
}
out.end();
await new Promise((resolve) => out.on("finish", resolve));

console.log(JSON.stringify({
  engine: "iztro-js",
  version: "2.6.1",
  cases: rows.length,
  natal_snapshots: natalCount,
  candidate_target_dates_per_case: TARGET_DATES.length,
  target_times_per_date: TARGET_TIME_INDICES.length,
  horoscope_snapshots: horoscopeCount,
  skipped_pre_birth_targets: rows.length * TARGET_DATES.length * TARGET_TIME_INDICES.length - horoscopeCount,
  horoscope_layers_each: ["decadal", "age", "yearly", "monthly", "daily", "hourly"],
  output: outPath,
  sha256: sha256(outPath),
}));
