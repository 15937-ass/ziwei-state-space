#!/usr/bin/env node
/**
 * Export iztro charts into this project's Normalized Chart Snapshot v0.1.
 *
 * Usage:
 *   npm install --no-save iztro@2.6.1
 *   node tools/iztro_export.mjs input.jsonl output.jsonl
 */

import fs from "node:fs";
import { astro } from "iztro";

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) {
  throw new Error("Usage: node tools/iztro_export.mjs input.jsonl output.jsonl");
}

const iztroVersion = process.env.IZTRO_VERSION || "2.6.1";
const adapterVersion = "0.1";

function starRecord(star) {
  return {
    name: star.name,
    brightness: star.brightness ?? null,
    mutagen: star.mutagen ?? null,
    type: star.type ?? null,
    scope: star.scope ?? null,
  };
}

function normalize(caseInput) {
  const chart = astro.withOptions({
    type: "solar",
    dateStr: caseInput.solar_date,
    timeIndex: Number(caseInput.time_index),
    gender: caseInput.gender,
    fixLeap: caseInput.fix_leap ?? true,
    language: "zh-CN",
    config: {
      algorithm: caseInput.algorithm ?? "zhongzhou",
      dayDivide: caseInput.day_divide ?? "current",
      yearDivide: caseInput.year_divide ?? "normal",
      horoscopeDivide: caseInput.horoscope_divide ?? "normal",
    },
  });

  const raw = typeof chart.toJSON === "function" ? chart.toJSON() : chart;
  const palaces = {};
  for (const p of raw.palaces) {
    palaces[p.name] = {
      stem: p.heavenlyStem,
      branch: p.earthlyBranch,
      is_body_palace: Boolean(p.isBodyPalace),
      major_stars: (p.majorStars ?? []).map(starRecord),
      minor_stars: (p.minorStars ?? []).map(starRecord),
      adjective_stars: (p.adjectiveStars ?? []).map(starRecord),
      decadal: p.decadal
        ? {
            range: p.decadal.range,
            stem: p.decadal.heavenlyStem,
            branch: p.decadal.earthlyBranch,
          }
        : null,
    };
  }

  return {
    case_id: caseInput.case_id ?? null,
    schema_version: "0.1",
    engine: {
      name: "iztro",
      version: iztroVersion,
      source_revision: null,
      adapter_version: adapterVersion,
    },
    input: {
      solar_date: caseInput.solar_date,
      time_index: Number(caseInput.time_index),
      gender: caseInput.gender,
      fix_leap: caseInput.fix_leap ?? true,
      config: {
        algorithm: caseInput.algorithm ?? "zhongzhou",
        day_divide: caseInput.day_divide ?? "forward",
        year_divide: caseInput.year_divide ?? "normal",
        horoscope_divide: caseInput.horoscope_divide ?? "normal",
      },
    },
    chart: {
      solar_date: raw.solarDate,
      lunar_date: raw.lunarDate,
      chinese_date: raw.chineseDate,
      time: raw.time,
      time_range: raw.timeRange,
      soul_star: raw.soul,
      body_star: raw.body,
      five_elements_class: raw.fiveElementsClass,
      soul_palace_branch: raw.earthlyBranchOfSoulPalace,
      body_palace_branch: raw.earthlyBranchOfBodyPalace,
      palaces,
    },
  };
}

const lines = fs
  .readFileSync(inputPath, "utf8")
  .split(/\r?\n/)
  .map((x) => x.trim())
  .filter(Boolean);

const output = [];
for (const line of lines) {
  const caseInput = JSON.parse(line);
  output.push(JSON.stringify(normalize(caseInput)));
}

fs.writeFileSync(outputPath, output.join("\n") + "\n", "utf8");
console.log(`wrote ${output.length} normalized charts to ${outputPath}`);
