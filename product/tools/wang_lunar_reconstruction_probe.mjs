#!/usr/bin/env node
/**
 * HISTORICAL V1.0 RECONSTRUCTION PROBE — NOT A CURRENT PRODUCTION CHART GENERATOR.
 * This probe records the former day_divide=forward reconstruction evidence.
 * Keep its outputs historical; do not use them as v1.1 production snapshots.
 * New production charts must use product/CANONICAL_CHART_CONTRACT_v1.1.md.
 */
 * Source-bounded Wang full-chart reconstruction readiness probe.
 *
 * Usage:
 *   npm install --no-save iztro@2.6.1
 *   node product/tools/wang_lunar_reconstruction_probe.mjs \
 *     product/expert_cases/wang_tingzhi/SOURCE_BIRTH_SIGNATURES_V0_1.json \
 *     product/expert_cases/wang_tingzhi/BLIND_EVIDENCE_V0_1.json \
 *     /tmp/wang_reconstruction_readiness.json
 *
 * This probe never fills missing source birth data. It enumerates only the
 * source-bounded candidate days/times and compares each generated chart against
 * the independently source-reviewed target-palace major-star anchor.
 */
import fs from "node:fs";
import { astro } from "iztro";

const [signaturePath, blindEvidencePath, outputPath] = process.argv.slice(2);
if (!signaturePath || !blindEvidencePath || !outputPath) {
  throw new Error(
    "Usage: node product/tools/wang_lunar_reconstruction_probe.mjs " +
      "SOURCE_BIRTH_SIGNATURES.json BLIND_EVIDENCE.json OUTPUT.json"
  );
}

const signatures = JSON.parse(fs.readFileSync(signaturePath, "utf8"));
const blind = JSON.parse(fs.readFileSync(blindEvidencePath, "utf8"));
const blindById = new Map((blind.cases ?? []).map((row) => [row.case_id, row]));

const MAJOR_ORDER = [
  "紫微",
  "天机",
  "太阳",
  "武曲",
  "天同",
  "廉贞",
  "天府",
  "太阴",
  "贪狼",
  "巨门",
  "天相",
  "天梁",
  "七杀",
  "破军",
];

const DOMAIN_PALACE_ALIASES = {
  PARENTS: ["父母"],
  LIFE: ["命"],
  SIBLINGS: ["兄弟"],
  SPOUSE: ["夫妻"],
  CHILDREN: ["子女"],
  WEALTH: ["财帛"],
  HEALTH: ["疾厄"],
  TRAVEL: ["迁移"],
  FRIENDS: ["奴仆", "仆役", "交友"],
  CAREER: ["官禄", "事业"],
  PROPERTY: ["田宅"],
  FORTUNE_VIRTUE: ["福德"],
};

const OPPOSITE_BRANCH = {
  子: "午",
  丑: "未",
  寅: "申",
  卯: "酉",
  辰: "戌",
  巳: "亥",
  午: "子",
  未: "丑",
  申: "寅",
  酉: "卯",
  戌: "辰",
  亥: "巳",
};

// astro.byLunar reads the pinned chart configuration from the global defaults.
// Set it once before any chart is constructed so every candidate uses the same
// Zhongzhou/time-boundary contract.
astro.config({
  algorithm: "zhongzhou",
  dayDivide: "forward",
  yearDivide: "normal",
  horoscopeDivide: "normal",
});

function normalizePalaceName(value) {
  return String(value ?? "").trim().replace(/宫$/u, "");
}

function stableMajorNames(stars) {
  const order = new Map(MAJOR_ORDER.map((name, index) => [name, index]));
  return [...new Set((stars ?? []).map((star) => String(star.name ?? "").trim()).filter(Boolean))]
    .sort((a, b) => {
      const aa = order.has(a) ? order.get(a) : 999;
      const bb = order.has(b) ? order.get(b) : 999;
      if (aa !== bb) return aa - bb;
      return a < b ? -1 : a > b ? 1 : 0;
    });
}

function sameNames(left, right) {
  const a = stableMajorNames((left ?? []).map((name) => ({ name })));
  const b = stableMajorNames((right ?? []).map((name) => ({ name })));
  return JSON.stringify(a) === JSON.stringify(b);
}

function findTargetPalace(raw, domain) {
  const aliases = DOMAIN_PALACE_ALIASES[domain];
  if (!aliases) throw new Error(`unsupported target domain: ${domain}`);
  const palace = (raw.palaces ?? []).find((item) =>
    aliases.includes(normalizePalaceName(item.name))
  );
  if (!palace) {
    throw new Error(
      `target palace not found for domain ${domain}; observed=` +
        (raw.palaces ?? []).map((item) => item.name).join(",")
    );
  }
  return palace;
}

function oppositePalace(raw, target) {
  const branch = String(target.earthlyBranch ?? "").trim();
  const opposite = OPPOSITE_BRANCH[branch];
  if (!opposite) throw new Error(`unsupported target branch: ${branch}`);
  const palace = (raw.palaces ?? []).find(
    (item) => String(item.earthlyBranch ?? "").trim() === opposite
  );
  if (!palace) throw new Error(`opposite palace not found for branch ${branch}`);
  return palace;
}

function candidateInputs(row) {
  if (String(row.source_status ?? "").startsWith("BLOCKED_")) return [];
  const out = [];
  for (const day of row.lunar_day_candidates ?? []) {
    for (const timeIndex of row.time_index_candidates ?? []) {
      out.push({
        lunar_date: `${row.lunar_year}-${row.lunar_month}-${day}`,
        lunar_day: day,
        time_index: timeIndex,
        gender: row.gender,
        is_leap_month: Boolean(row.is_leap_month),
      });
    }
  }
  return out.sort((a, b) =>
    a.lunar_day - b.lunar_day || a.time_index - b.time_index
  );
}

function renderCandidate(row, anchor, candidate) {
  try {
    const chart = astro.byLunar(
      candidate.lunar_date,
      Number(candidate.time_index),
      candidate.gender,
      candidate.is_leap_month,
      true,
      "zh-CN"
    );
    const raw = typeof chart.toJSON === "function" ? chart.toJSON() : chart;
    const target = findTargetPalace(raw, anchor.target_domain);
    const targetPalaceAliases = DOMAIN_PALACE_ALIASES[anchor.target_domain] ?? [];
    const expectedTargetPalaceName = normalizePalaceName(anchor.target_palace);
    const observedTargetPalaceName = normalizePalaceName(target.name);
    const targetPalaceIdentityMatch =
      targetPalaceAliases.includes(expectedTargetPalaceName) &&
      targetPalaceAliases.includes(observedTargetPalaceName);
    const observedDirect = stableMajorNames(target.majorStars);
    let observedBorrowed = [];
    if (anchor.target_palace_empty_main_star) {
      observedBorrowed = stableMajorNames(oppositePalace(raw, target).majorStars);
    }
    const directMatch = sameNames(
      observedDirect,
      anchor.target_palace_main_stars ?? []
    );
    const borrowedMatch = sameNames(
      observedBorrowed,
      anchor.borrowed_from_opposite_main_stars ?? []
    );
    const emptyMatch =
      Boolean(anchor.target_palace_empty_main_star) === (observedDirect.length === 0);

    return {
      candidate_id:
        `${row.case_id}:D${String(candidate.lunar_day).padStart(2, "0")}:` +
        `T${String(candidate.time_index).padStart(2, "0")}`,
      lunar_date_input: candidate.lunar_date,
      time_index: candidate.time_index,
      gender: candidate.gender,
      solar_date_output: raw.solarDate ?? null,
      lunar_date_output: raw.lunarDate ?? null,
      chinese_date_output: raw.chineseDate ?? null,
      source_year_ganzhi_match: row.source_year_ganzhi
        ? String(raw.chineseDate ?? "").includes(row.source_year_ganzhi)
        : null,
      target_palace_name: target.name ?? null,
      target_palace_branch: target.earthlyBranch ?? null,
      expected_target_palace_name: anchor.target_palace ?? null,
      target_palace_identity_match: targetPalaceIdentityMatch,
      observed_target_main_stars: observedDirect,
      observed_borrowed_opposite_main_stars: observedBorrowed,
      expected_target_main_stars: anchor.target_palace_main_stars ?? [],
      expected_borrowed_opposite_main_stars:
        anchor.borrowed_from_opposite_main_stars ?? [],
      anchor_match:
        targetPalaceIdentityMatch && directMatch && borrowedMatch && emptyMatch,
      engine_error: null,
    };
  } catch (error) {
    return {
      candidate_id:
        `${row.case_id}:D${String(candidate.lunar_day).padStart(2, "0")}:` +
        `T${String(candidate.time_index).padStart(2, "0")}`,
      lunar_date_input: candidate.lunar_date,
      time_index: candidate.time_index,
      gender: candidate.gender,
      anchor_match: false,
      engine_error: String(error?.message ?? error),
    };
  }
}

function probeCase(row) {
  const anchor = blindById.get(row.case_id);
  if (!anchor) throw new Error(`${row.case_id}: blind anchor missing`);

  if (String(row.source_status ?? "").startsWith("BLOCKED_")) {
    return {
      case_id: row.case_id,
      source_status: row.source_status,
      target_domain: anchor.target_domain,
      source_candidate_count: 0,
      evaluated_candidate_count: 0,
      anchor_match_count: 0,
      status: "BLOCKED_SOURCE_INCOMPLETE",
      matched_candidate_ids: [],
      candidates: [],
      engine_errors: [],
      full_chart_materialization_ready: false,
    };
  }

  const inputs = candidateInputs(row);
  const candidates = inputs.map((candidate) =>
    renderCandidate(row, anchor, candidate)
  );
  const evaluated = candidates.filter((item) => !item.engine_error);
  const matched = evaluated.filter((item) => item.anchor_match);
  const engineErrors = candidates
    .filter((item) => item.engine_error)
    .map((item) => ({
      candidate_id: item.candidate_id,
      error: item.engine_error,
    }));

  let status;
  // A case is unique only when every source-bounded candidate was evaluated.
  // Any candidate-level engine/probe failure keeps the whole case unsupported.
  if (engineErrors.length > 0 || evaluated.length !== inputs.length) {
    status = "ENGINE_UNSUPPORTED";
  } else if (!evaluated.length) status = "ENGINE_UNSUPPORTED";
  else if (matched.length === 1) status = "UNIQUE_ANCHOR_MATCH";
  else if (matched.length > 1) status = "MULTIPLE_ANCHOR_MATCH";
  else status = "NO_ANCHOR_MATCH";

  return {
    case_id: row.case_id,
    source_status: row.source_status,
    target_domain: anchor.target_domain,
    source_candidate_count: inputs.length,
    evaluated_candidate_count: evaluated.length,
    anchor_match_count: matched.length,
    status,
    matched_candidate_ids: matched.map((item) => item.candidate_id),
    engine_errors: engineErrors,
    candidates,
    full_chart_materialization_ready: status === "UNIQUE_ANCHOR_MATCH",
  };
}

const cases = (signatures.cases ?? []).map(probeCase);
const statusCounts = {};
for (const row of cases) {
  statusCounts[row.status] = (statusCounts[row.status] ?? 0) + 1;
}
const output = {
  schema_version: "0.1",
  artifact_id: "WANG_FULL_CHART_RECONSTRUCTION_READINESS_V0_1",
  issue: 545,
  corpus_id: signatures.corpus_id,
  engine: {
    name: "iztro-js",
    version: signatures.reconstruction_policy.engine_version,
    entrypoint: "astro.byLunar",
    algorithm: "zhongzhou",
    astro_type: "heaven",
    input_calendar: "lunar",
    fix_leap: true,
    day_divide: "forward",
    year_divide: "normal",
    horoscope_divide: "normal",
  },
  anchor_artifact_id: blind.artifact_id,
  summary: {
    cases_total: cases.length,
    source_candidate_inputs: cases.reduce(
      (sum, row) => sum + row.source_candidate_count,
      0
    ),
    evaluated_candidate_inputs: cases.reduce(
      (sum, row) => sum + row.evaluated_candidate_count,
      0
    ),
    unique_anchor_match: statusCounts.UNIQUE_ANCHOR_MATCH ?? 0,
    multiple_anchor_match: statusCounts.MULTIPLE_ANCHOR_MATCH ?? 0,
    no_anchor_match: statusCounts.NO_ANCHOR_MATCH ?? 0,
    blocked_source_incomplete: statusCounts.BLOCKED_SOURCE_INCOMPLETE ?? 0,
    engine_unsupported: statusCounts.ENGINE_UNSUPPORTED ?? 0,
    full_chart_materialization_ready: cases.filter(
      (row) => row.full_chart_materialization_ready
    ).length,
  },
  cases,
  boundaries: {
    missing_source_inputs_backfilled: false,
    subject_identity_used: false,
    expert_reasoning_used: false,
    outcome_used: false,
    biography_used: false,
    method_scope_broadened: false,
    empirical_probability_used: false,
    full_chart_claim_requires_unique_anchor_match: true,
    target_palace_identity_checked: true,
    partial_engine_failure_blocks_promotion: true,
  },
};

fs.writeFileSync(outputPath, JSON.stringify(output, null, 2) + "\n", "utf8");
console.log(JSON.stringify(output.summary));
for (const row of cases) {
  console.log(
    [
      row.case_id,
      row.status,
      `candidates=${row.source_candidate_count}`,
      `evaluated=${row.evaluated_candidate_count}`,
      `matches=${row.anchor_match_count}`,
      row.matched_candidate_ids.join(",") || "-",
    ].join("\t")
  );
}
