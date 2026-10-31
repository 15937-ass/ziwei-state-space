#!/usr/bin/env node
/**
 * P1 full exporter for iztro 2.6.1.
 *
 * Produces one normalized record per natal seed, including:
 * natal chart + decadal/age/yearly/monthly/daily/hourly for every target.
 *
 * Usage:
 *   npm install --no-save iztro@2.6.1
 *   node tools/iztro_full_export.mjs input.jsonl targets.json output.jsonl
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { astro } from "iztro";

const [inputPath, targetsPath, outputPath] = process.argv.slice(2);
if (!inputPath || !targetsPath || !outputPath) {
  throw new Error("Usage: node tools/iztro_full_export.mjs input.jsonl targets.json output.jsonl");
}

const adapterVersion = "0.2";
const engineVersion = "2.6.1";
function resolveInstalledIztroVersion() {
  let directory = path.dirname(fileURLToPath(import.meta.resolve("iztro")));
  while (true) {
    const packagePath = path.join(directory, "package.json");
    if (fs.existsSync(packagePath)) {
      const packageMetadata = JSON.parse(fs.readFileSync(packagePath, "utf8"));
      if (packageMetadata.name === "iztro") return packageMetadata.version;
    }
    const parent = path.dirname(directory);
    if (parent === directory) break;
    directory = parent;
  }
  throw new Error("unable to resolve installed iztro package metadata");
}

const installedIztroVersion = resolveInstalledIztroVersion();
if (installedIztroVersion !== engineVersion) {
  throw new Error(`installed iztro version must equal ${engineVersion}; got ${installedIztroVersion}`);
}
const chartContractId = "ZHONGZHOU_IZTRO_JS_2_6_1_V1";
const canonicalConfig = Object.freeze({
  algorithm: "zhongzhou",
  astroType: "heaven",
  fixLeap: true,
  dayDivide: "forward",
  yearDivide: "normal",
  horoscopeDivide: "normal",
  language: "zh-CN",
});

if (process.env.IZTRO_VERSION && process.env.IZTRO_VERSION !== engineVersion) {
  throw new Error(`IZTRO_VERSION must remain pinned to ${engineVersion}`);
}

function assertCanonicalInput(caseInput) {
  const expected = {
    algorithm: canonicalConfig.algorithm,
    day_divide: canonicalConfig.dayDivide,
    year_divide: canonicalConfig.yearDivide,
    horoscope_divide: canonicalConfig.horoscopeDivide,
    fix_leap: canonicalConfig.fixLeap,
  };
  for (const [field, value] of Object.entries(expected)) {
    if (caseInput[field] !== value) {
      throw new Error(`non-canonical production chart input: ${field} must equal ${value}`);
    }
  }
}

function stableStars(stars) {
  return (stars ?? [])
    .map((s) => ({
      name: s.name,
      type: s.type ?? null,
      brightness: s.brightness ?? null,
      mutagen: s.mutagen ?? null,
      scope: s.scope ?? null,
    }))
    .sort((a, b) => {
      const aa = JSON.stringify(a);
      const bb = JSON.stringify(b);
      return aa < bb ? -1 : aa > bb ? 1 : 0;
    });
}

function stableFlowStars(groups) {
  return (groups ?? []).map((group) =>
    (group ?? [])
      .map((s) => ({ name: s.name, type: s.type ?? null }))
      .sort((a, b) => {
        const aa = JSON.stringify(a);
        const bb = JSON.stringify(b);
        return aa < bb ? -1 : aa > bb ? 1 : 0;
      })
  );
}

function normalizeSolarDate(value) {
  const parts = String(value).split("-");
  if (parts.length !== 3) return String(value);
  return `${parts[0].padStart(4, "0")}-${parts[1].padStart(2, "0")}-${parts[2].padStart(2, "0")}`;
}

function normalizeNatal(raw) {
  const palaces = {};
  for (const p of raw.palaces ?? []) {
    palaces[p.earthlyBranch] = {
      name: p.name,
      stem: p.heavenlyStem,
      branch: p.earthlyBranch,
      is_body_palace: Boolean(p.isBodyPalace),
      major_stars: stableStars(p.majorStars),
      minor_stars: stableStars(p.minorStars),
      adjective_stars: stableStars(p.adjectiveStars),
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
    solar_date: normalizeSolarDate(raw.solarDate),
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
  };
}

function normalizeScope(scope) {
  return {
    index: scope.index,
    name: scope.name,
    stem: scope.heavenlyStem,
    branch: scope.earthlyBranch,
    palace_names: scope.palaceNames,
    mutagen: scope.mutagen,
    nominal_age: scope.nominalAge ?? null,
    stars: stableFlowStars(scope.stars),
  };
}

function normalizeHoroscope(raw, target) {
  const yearlyDec = raw.yearly?.yearlyDecStar ?? null;
  return {
    target: target,
    solar_date: normalizeSolarDate(raw.solarDate),
    lunar_date: raw.lunarDate,
    scopes: {
      decadal: normalizeScope(raw.decadal),
      age: normalizeScope(raw.age),
      yearly: normalizeScope(raw.yearly),
      monthly: normalizeScope(raw.monthly),
      daily: normalizeScope(raw.daily),
      hourly: normalizeScope(raw.hourly),
    },
    yearly_dec_stars: yearlyDec
      ? {
          suiqian12: yearlyDec.suiqian12,
          jiangqian12: yearlyDec.jiangqian12,
        }
      : null,
  };
}

function render(caseInput, targets) {
  assertCanonicalInput(caseInput);
  const config = {
    algorithm: canonicalConfig.algorithm,
    dayDivide: canonicalConfig.dayDivide,
    yearDivide: canonicalConfig.yearDivide,
    horoscopeDivide: canonicalConfig.horoscopeDivide,
  };
  const chart = astro.withOptions({
    type: "solar",
    dateStr: caseInput.solar_date,
    timeIndex: Number(caseInput.time_index),
    gender: caseInput.gender,
    fixLeap: canonicalConfig.fixLeap,
    language: canonicalConfig.language,
    astroType: canonicalConfig.astroType,
    config,
  });
  const natalRaw = typeof chart.toJSON === "function" ? chart.toJSON() : chart;
  const temporal = targets.map((target) => {
    const h = chart.horoscope(target.solar_date, Number(target.time_index));
    const raw = typeof h.toJSON === "function" ? h.toJSON() : h;
    return normalizeHoroscope(raw, target);
  });
  return {
    case_id: caseInput.case_id,
    schema_version: "0.2",
    chart_contract_id: chartContractId,
    engine: {
      name: "iztro-js",
      version: engineVersion,
      source_revision: "2c7ef9be669df7b19d1799f4dce335fed3794f78",
      adapter_version: adapterVersion,
    },
    input: {
      ...caseInput,
      school: "zhongzhou",
      astro_type: canonicalConfig.astroType,
      language: canonicalConfig.language,
      input_calendar: "solar",
      entrypoint: "astro.withOptions",
      chart_config: {
        algorithm: canonicalConfig.algorithm,
        astro_type: canonicalConfig.astroType,
        fix_leap: canonicalConfig.fixLeap,
        day_divide: canonicalConfig.dayDivide,
        year_divide: canonicalConfig.yearDivide,
        horoscope_divide: canonicalConfig.horoscopeDivide,
        language: canonicalConfig.language,
      },
    },
    natal: normalizeNatal(natalRaw),
    temporal,
  };
}

const inputLines = fs.readFileSync(inputPath, "utf8").split(/\r?\n/).map((x) => x.trim()).filter(Boolean);
const targetManifest = JSON.parse(fs.readFileSync(targetsPath, "utf8"));
const targetsList = targetManifest.targets ?? [];
if (!targetsList.length) throw new Error("target manifest contains no targets");

const rows = inputLines.map((line) => render(JSON.parse(line), targetsList));
fs.writeFileSync(outputPath, rows.map((x) => JSON.stringify(x)).join("\n") + "\n", "utf8");
console.log(`P1 iztro-js: wrote ${rows.length} natal records and ${rows.length * targetsList.length} horoscope snapshots`);
