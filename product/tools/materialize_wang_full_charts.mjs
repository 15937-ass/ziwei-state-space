#!/usr/bin/env node
/**
 * HISTORICAL V1.0 MATERIALIZER — NOT A CURRENT PRODUCTION CHART GENERATOR.
 * This tool reproduces the already-versioned Wang v0.1B historical artifact
 * under the former day_divide=forward configuration. Do not use it for new
 * production charts or silently relabel its output as canonical v1.1. A new
 * v1.1 Wang reconstruction requires a separately approved, source-rechecked
 * migration and target-anchor verification.
 */
 * Source-bounded full natal-chart materializer for the 11 unique Wang cases.
 *
 * Usage:
 *   npm install --no-save iztro@2.6.1
 *   node product/tools/materialize_wang_full_charts.mjs \
 *     product/expert_cases/wang_tingzhi/SOURCE_BIRTH_SIGNATURES_V0_1.json \
 *     product/expert_cases/wang_tingzhi/BLIND_EVIDENCE_V0_1.json \
 *     product/expert_cases/wang_tingzhi/FULL_CHART_RECONSTRUCTION_READINESS_V0_1.json \
 *     product/expert_cases/wang_tingzhi/FULL_CHART_MATERIALIZATION_V0_1B.json
 *
 * This tool only materializes source-bounded lunar inputs whose already-versioned
 * readiness record has exactly one target-anchor match. It does not use biography,
 * expert reasoning, conclusions, outcomes, or any guessed birth input.
 */
import fs from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { astro } from "iztro";

const [signaturePath, blindPath, readinessPath, outputPath] = process.argv.slice(2);
if (!signaturePath || !blindPath || !readinessPath || !outputPath) {
  throw new Error(
    "Usage: node product/tools/materialize_wang_full_charts.mjs " +
      "SOURCE_BIRTH_SIGNATURES.json BLIND_EVIDENCE.json " +
      "FULL_CHART_RECONSTRUCTION_READINESS.json OUTPUT.json"
  );
}

const EXPECTED_CASE_IDS = [
  "WANG-CASE-001", "WANG-CASE-003", "WANG-CASE-006", "WANG-CASE-009",
  "WANG-CASE-010", "WANG-CASE-012", "WANG-CASE-013", "WANG-CASE-015",
  "WANG-CASE-019", "WANG-CASE-021", "WANG-CASE-023",
];
const MAJOR_ORDER = [
  "紫微", "天机", "太阳", "武曲", "天同", "廉贞", "天府",
  "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军",
];
const BRANCH_ORDER = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"];
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
  子: "午", 丑: "未", 寅: "申", 卯: "酉", 辰: "戌", 巳: "亥",
  午: "子", 未: "丑", 申: "寅", 酉: "卯", 戌: "辰", 亥: "巳",
};
const ENGINE = {
  name: "iztro-js",
  version: "2.6.1",
  source_revision: "2c7ef9be669df7b19d1799f4dce335fed3794f78",
  entrypoint: "astro.byLunar",
  algorithm: "zhongzhou",
  astro_type: "heaven",
  input_calendar: "lunar",
  fix_leap: true,
  day_divide: "forward",
  year_divide: "normal",
  horoscope_divide: "normal",
};
const ADAPTER_VERSION = "0.1B";
const EXPECTED_INPUT_GIT_BLOBS = {
  source_signatures: "83800555169c4225427dbc35ae50e4ec21cf2257",
  blind_anchor: "c5744b4c5278394859e563cbf6a2537c7315546f",
  reconstruction_readiness: "a0ec93c5a17859a64d02eb029837c787c7b12bdf",
};
const resolvedEngineEntry = fileURLToPath(import.meta.resolve("iztro"));
const installedEngineVersion = findPackageVersion(resolvedEngineEntry, "iztro");
if (installedEngineVersion !== ENGINE.version) {
  throw new Error(
    "pinned engine version mismatch: expected iztro " + ENGINE.version +
    ", observed " + String(installedEngineVersion ?? "unknown")
  );
}

const FORBIDDEN_KEYS = new Set([
  "source_subject_label", "source_subject_name", "person_name", "person_group_id",
  "expert_reasoning_graph", "expert_conclusion_refs", "outcome_refs",
  "reasoning_span_ref", "conclusion_span_ref", "outcome_span_ref",
  "expert_prose", "biography",
]);

function readJson(path) {
  return JSON.parse(fs.readFileSync(path, "utf8"));
}
function findPackageVersion(entryPath, packageName) {
  let current = dirname(entryPath);
  while (true) {
    const packagePath = join(current, "package.json");
    if (fs.existsSync(packagePath)) {
      try {
        const metadata = JSON.parse(fs.readFileSync(packagePath, "utf8"));
        if (metadata.name === packageName) return String(metadata.version ?? "");
      } catch {
        // Keep walking upward; only the package whose name matches is authoritative.
      }
    }
    const parent = dirname(current);
    if (parent === current) return null;
    current = parent;
  }
}
function sha256(path) {
  return createHash("sha256").update(fs.readFileSync(path)).digest("hex");
}
function gitBlobSha(path) {
  const content = fs.readFileSync(path);
  return createHash("sha1")
    .update("blob " + content.length + "\0")
    .update(content)
    .digest("hex");
}
function requireText(value, label) {
  const text = String(value ?? "").trim();
  if (!text) throw new Error(label + " is required");
  return text;
}
function normalizePalaceName(value) {
  return String(value ?? "").trim().replace(/宫$/u, "");
}
function stableStars(stars) {
  return (stars ?? []).map((star) => ({
    name: requireText(star.name, "star.name"),
    type: star.type ?? null,
    brightness: star.brightness ?? null,
    mutagen: star.mutagen ?? null,
    scope: star.scope ?? null,
  })).sort((a, b) => {
    const aa = JSON.stringify(a);
    const bb = JSON.stringify(b);
    return aa < bb ? -1 : aa > bb ? 1 : 0;
  });
}
function stableMajorNames(stars) {
  const rank = new Map(MAJOR_ORDER.map((name, index) => [name, index]));
  return [...new Set((stars ?? []).map((star) => String(star.name ?? "").trim()).filter(Boolean))]
    .sort((a, b) => {
      const aa = rank.has(a) ? rank.get(a) : 999;
      const bb = rank.has(b) ? rank.get(b) : 999;
      if (aa !== bb) return aa - bb;
      return a < b ? -1 : a > b ? 1 : 0;
    });
}
function sameNames(left, right) {
  return JSON.stringify(stableMajorNames((left ?? []).map((name) => ({ name })))) ===
    JSON.stringify(stableMajorNames((right ?? []).map((name) => ({ name }))));
}
function normalizeDate(value) {
  if (value == null) return null;
  const parts = String(value).split("-");
  if (parts.length !== 3) return String(value);
  return parts[0].padStart(4, "0") + "-" + parts[1].padStart(2, "0") + "-" + parts[2].padStart(2, "0");
}
function normalizeNatal(raw) {
  if (!Array.isArray(raw.palaces) || raw.palaces.length !== 12) {
    throw new Error("pinned engine must return exactly 12 natal palaces");
  }
  const palaces = raw.palaces.map((palace) => {
    const branch = requireText(palace.earthlyBranch, "palace.earthlyBranch");
    if (!BRANCH_ORDER.includes(branch)) throw new Error("unsupported palace branch: " + branch);
    return {
      name: requireText(palace.name, "palace.name"),
      stem: requireText(palace.heavenlyStem, "palace.heavenlyStem"),
      branch,
      is_body_palace: Boolean(palace.isBodyPalace),
      major_stars: stableStars(palace.majorStars),
      minor_stars: stableStars(palace.minorStars),
      adjective_stars: stableStars(palace.adjectiveStars),
      decadal: palace.decadal ? {
        range: palace.decadal.range ?? null,
        stem: palace.decadal.heavenlyStem ?? null,
        branch: palace.decadal.earthlyBranch ?? null,
      } : null,
    };
  }).sort((a, b) => BRANCH_ORDER.indexOf(a.branch) - BRANCH_ORDER.indexOf(b.branch));
  const branches = palaces.map((palace) => palace.branch);
  const names = palaces.map((palace) => normalizePalaceName(palace.name));
  if (new Set(branches).size !== 12 || BRANCH_ORDER.some((branch) => !branches.includes(branch))) {
    throw new Error("normalized natal chart must contain each earthly branch exactly once");
  }
  if (new Set(names).size !== 12) throw new Error("normalized natal chart palace names must be unique");
  return {
    solar_date: normalizeDate(raw.solarDate),
    lunar_date: raw.lunarDate ?? null,
    chinese_date: raw.chineseDate ?? null,
    time: raw.time ?? null,
    time_range: raw.timeRange ?? null,
    soul_star: raw.soul ?? null,
    body_star: raw.body ?? null,
    five_elements_class: raw.fiveElementsClass ?? null,
    soul_palace_branch: raw.earthlyBranchOfSoulPalace ?? null,
    body_palace_branch: raw.earthlyBranchOfBodyPalace ?? null,
    palaces,
  };
}
function findTargetPalace(chart, domain) {
  const aliases = DOMAIN_PALACE_ALIASES[domain];
  if (!aliases) throw new Error("unsupported target domain: " + domain);
  const palace = chart.palaces.find((item) => aliases.includes(normalizePalaceName(item.name)));
  if (!palace) throw new Error("target palace not found for domain " + domain);
  return palace;
}
function findOppositePalace(chart, target) {
  const opposite = OPPOSITE_BRANCH[target.branch];
  if (!opposite) throw new Error("unsupported target branch: " + target.branch);
  const palace = chart.palaces.find((item) => item.branch === opposite);
  if (!palace) throw new Error("opposite palace not found for target branch " + target.branch);
  return palace;
}
function verifyTargetAnchor(chart, anchor) {
  const target = findTargetPalace(chart, anchor.target_domain);
  const aliases = DOMAIN_PALACE_ALIASES[anchor.target_domain];
  const expectedName = normalizePalaceName(anchor.target_palace);
  const observedName = normalizePalaceName(target.name);
  const targetIdentityMatch = aliases.includes(expectedName) && aliases.includes(observedName);
  const observedDirect = stableMajorNames(target.major_stars);
  const observedBorrowed = anchor.target_palace_empty_main_star
    ? stableMajorNames(findOppositePalace(chart, target).major_stars)
    : [];
  const directMatch = sameNames(observedDirect, anchor.target_palace_main_stars ?? []);
  const borrowedMatch = sameNames(observedBorrowed, anchor.borrowed_from_opposite_main_stars ?? []);
  const emptyMatch = Boolean(anchor.target_palace_empty_main_star) === (observedDirect.length === 0);
  const matched = targetIdentityMatch && directMatch && borrowedMatch && emptyMatch;
  return {
    status: matched ? "UNIQUE_ANCHOR_MATCH_RECONFIRMED" : "ANCHOR_MISMATCH_BLOCKED",
    target_palace_identity_match: targetIdentityMatch,
    expected_target_palace: anchor.target_palace,
    observed_target_palace: target.name,
    observed_target_branch: target.branch,
    expected_target_main_stars: anchor.target_palace_main_stars ?? [],
    observed_target_main_stars: observedDirect,
    expected_borrowed_opposite_main_stars: anchor.borrowed_from_opposite_main_stars ?? [],
    observed_borrowed_opposite_main_stars: observedBorrowed,
    target_palace_empty_main_star: Boolean(anchor.target_palace_empty_main_star),
    matched,
  };
}
function candidateFor(row, readinessRow) {
  if (readinessRow.status !== "UNIQUE_ANCHOR_MATCH" ||
      readinessRow.full_chart_materialization_ready !== true ||
      readinessRow.anchor_match_count !== 1 ||
      readinessRow.engine_errors?.length !== 0 ||
      readinessRow.evaluated_candidate_count !== readinessRow.source_candidate_count ||
      !Array.isArray(readinessRow.matched_candidate_ids) ||
      readinessRow.matched_candidate_ids.length !== 1) {
    throw new Error(row.case_id + ": case is not uniquely eligible for full-chart materialization");
  }
  const match = String(readinessRow.matched_candidate_ids[0]);
  const parsed = /^WANG-CASE-(\d{3}):D(\d{2}):T(\d{2})$/u.exec(match);
  if (!parsed || "WANG-CASE-" + parsed[1] !== row.case_id) {
    throw new Error(row.case_id + ": invalid matched candidate ID");
  }
  const day = Number(parsed[2]);
  const timeIndex = Number(parsed[3]);
  if (!(row.lunar_day_candidates ?? []).includes(day)) {
    throw new Error(row.case_id + ": matched day is not source-bounded");
  }
  if (!(row.time_index_candidates ?? []).includes(timeIndex)) {
    throw new Error(row.case_id + ": matched time is not source-bounded");
  }
  if (String(row.source_status ?? "").startsWith("BLOCKED_")) {
    throw new Error(row.case_id + ": blocked source input cannot be materialized");
  }
  if (!Number.isInteger(row.lunar_year) || !Number.isInteger(row.lunar_month) ||
      !row.gender || typeof row.is_leap_month !== "boolean") {
    throw new Error(row.case_id + ": required lunar source fields are incomplete");
  }
  return {
    candidate_id: match,
    lunar_year: row.lunar_year,
    lunar_month: row.lunar_month,
    lunar_day: day,
    lunar_date: String(row.lunar_year) + "-" + String(row.lunar_month) + "-" + String(day),
    time_index: timeIndex,
    gender: row.gender,
    is_leap_month: row.is_leap_month,
  };
}
function walkKeys(value, out = new Set()) {
  if (Array.isArray(value)) {
    for (const item of value) walkKeys(item, out);
  } else if (value && typeof value === "object") {
    for (const [key, nested] of Object.entries(value)) {
      out.add(key);
      walkKeys(nested, out);
    }
  }
  return out;
}

const signatures = readJson(signaturePath);
const blind = readJson(blindPath);
const readiness = readJson(readinessPath);
const inputGitBlobs = {
  source_signatures: gitBlobSha(signaturePath),
  blind_anchor: gitBlobSha(blindPath),
  reconstruction_readiness: gitBlobSha(readinessPath),
};
for (const [key, expected] of Object.entries(EXPECTED_INPUT_GIT_BLOBS)) {
  if (inputGitBlobs[key] !== expected) {
    throw new Error(key + " artifact version changed; explicit re-review is required");
  }
}
if (signatures.artifact_id !== "WANG_SOURCE_BIRTH_SIGNATURES_V0_1") throw new Error("unexpected source-signature artifact");
if (blind.artifact_id !== "WANG_BLIND_EVIDENCE_V0_1") throw new Error("unexpected blind-anchor artifact");
if (readiness.artifact_id !== "WANG_FULL_CHART_RECONSTRUCTION_READINESS_V0_1") throw new Error("unexpected readiness artifact");
if (signatures.schema_version !== "0.1" || blind.schema_version !== "0.1" || readiness.schema_version !== "0.1") {
  throw new Error("unsupported source artifact schema version");
}
if (signatures.reconstruction_policy?.engine !== ENGINE.name ||
    signatures.reconstruction_policy?.engine_version !== ENGINE.version ||
    signatures.reconstruction_policy?.algorithm !== ENGINE.algorithm ||
    signatures.reconstruction_policy?.astro_type !== ENGINE.astro_type ||
    signatures.reconstruction_policy?.fix_leap !== ENGINE.fix_leap ||
    signatures.reconstruction_policy?.day_divide !== ENGINE.day_divide ||
    signatures.reconstruction_policy?.year_divide !== ENGINE.year_divide ||
    signatures.reconstruction_policy?.horoscope_divide !== ENGINE.horoscope_divide ||
    readiness.probe?.engine !== ENGINE.name ||
    readiness.probe?.engine_version !== ENGINE.version ||
    readiness.probe?.entrypoint !== ENGINE.entrypoint ||
    readiness.probe?.input_calendar !== ENGINE.input_calendar ||
    readiness.probe?.algorithm !== ENGINE.algorithm ||
    readiness.probe?.astro_type !== ENGINE.astro_type ||
    readiness.probe?.fix_leap !== ENGINE.fix_leap ||
    readiness.probe?.day_divide !== ENGINE.day_divide ||
    readiness.probe?.year_divide !== ENGINE.year_divide ||
    readiness.probe?.horoscope_divide !== ENGINE.horoscope_divide) {
  throw new Error("source/readiness engine contract does not match pinned materializer");
}
if (readiness.summary?.cases_total !== 24 ||
    readiness.summary?.unique_anchor_match !== EXPECTED_CASE_IDS.length ||
    readiness.summary?.full_chart_materialization_ready !== EXPECTED_CASE_IDS.length) {
  throw new Error("readiness summary changed; explicit re-review is required");
}
const signaturesById = new Map((signatures.cases ?? []).map((row) => [row.case_id, row]));
const blindById = new Map((blind.cases ?? []).map((row) => [row.case_id, row]));
const readinessById = new Map((readiness.cases ?? []).map((row) => [row.case_id, row]));
if (signaturesById.size !== 24 || blindById.size !== 24 || readinessById.size !== 24) {
  throw new Error("source, blind-anchor, and readiness artifacts must each cover 24 cases");
}
const actualEligible = readiness.cases
  .filter((row) => row.status === "UNIQUE_ANCHOR_MATCH" && row.full_chart_materialization_ready === true)
  .map((row) => row.case_id);
if (JSON.stringify(actualEligible) !== JSON.stringify(EXPECTED_CASE_IDS)) {
  throw new Error("eligible case set changed; explicit re-review is required");
}
astro.config({
  algorithm: ENGINE.algorithm,
  dayDivide: ENGINE.day_divide,
  yearDivide: ENGINE.year_divide,
  horoscopeDivide: ENGINE.horoscope_divide,
});

const outputCases = [];
for (const caseId of EXPECTED_CASE_IDS) {
  const sourceRow = signaturesById.get(caseId);
  const anchor = blindById.get(caseId);
  const readinessRow = readinessById.get(caseId);
  if (!sourceRow || !anchor || !readinessRow) throw new Error(caseId + ": required input row missing");
  if (sourceRow.source_chart_span_ref !== anchor.source_chart_span_ref) {
    throw new Error(caseId + ": source span mismatch across source/anchor artifacts");
  }
  const candidate = candidateFor(sourceRow, readinessRow);
  let raw;
  try {
    const chart = astro.byLunar(
      candidate.lunar_date,
      candidate.time_index,
      candidate.gender,
      candidate.is_leap_month,
      true,
      "zh-CN"
    );
    raw = typeof chart.toJSON === "function" ? chart.toJSON() : chart;
  } catch (error) {
    throw new Error(caseId + ": pinned lunar engine failed: " + String(error?.message ?? error));
  }
  const natal = normalizeNatal(raw);
  const anchorVerification = verifyTargetAnchor(natal, anchor);
  if (!anchorVerification.matched) {
    throw new Error(caseId + ": runtime target anchor no longer matches; refusing to write artifact");
  }
  outputCases.push({
    case_id: caseId,
    blind_alias: anchor.blind_alias,
    target_domain: anchor.target_domain,
    target_palace: anchor.target_palace,
    source_status: sourceRow.source_status,
    source_provenance: {
      source_chart_span_ref: sourceRow.source_chart_span_ref,
      source_pages: sourceRow.source_pages,
      source_input_artifact_id: signatures.artifact_id,
      source_input_candidate_id: candidate.candidate_id,
      readiness_artifact_id: readiness.artifact_id,
      readiness_status: readinessRow.status,
    },
    source_candidate_set: {
      source_day_notation: sourceRow.source_day_notation ?? null,
      lunar_day_candidates: sourceRow.lunar_day_candidates,
      source_time_label: sourceRow.source_time_label ?? null,
      time_index_candidates: sourceRow.time_index_candidates,
      source_candidate_count: readinessRow.source_candidate_count,
      evaluated_candidate_count: readinessRow.evaluated_candidate_count,
      anchor_match_count: readinessRow.anchor_match_count,
      matched_candidate_ids: readinessRow.matched_candidate_ids,
      source_time_ambiguity_preserved: sourceRow.source_status === "SOURCE_EXACT_ZI_TIME_AMBIGUITY",
      selection_basis: "EXACTLY_ONE_READINESS_ANCHOR_MATCH",
      source_time_ambiguity_note: caseId === "WANG-CASE-021"
        ? "The source gives unqualified 子时 only; both candidate time indices 0 and 12 remain preserved. The pinned readiness evaluation examined both candidates and found exactly one target-anchor match, T00. This does not erase or resolve the source's original time ambiguity."
        : null,
    },
    input: {
      calendar: "LUNAR",
      lunar_year: candidate.lunar_year,
      lunar_month: candidate.lunar_month,
      lunar_day: candidate.lunar_day,
      lunar_date: candidate.lunar_date,
      time_index: candidate.time_index,
      gender: candidate.gender,
      is_leap_month: candidate.is_leap_month,
      astro_type: ENGINE.astro_type,
      config: {
        algorithm: ENGINE.algorithm,
        day_divide: ENGINE.day_divide,
        year_divide: ENGINE.year_divide,
        horoscope_divide: ENGINE.horoscope_divide,
        fix_leap: ENGINE.fix_leap,
      },
    },
    materialization_status: "FULL_CHART_MATERIALIZED",
    materialization_claim: "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED",
    full_source_chart_equivalence_verified: false,
    target_anchor_verification: anchorVerification,
    chart: natal,
  });
}

const payload = {
  schema_version: "0.1B",
  artifact_id: "WANG_FULL_CHART_MATERIALIZATION_V0_1B",
  issue: 588,
  corpus_id: signatures.corpus_id,
  materialization_level: "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED",
  engine: ENGINE,
  adapter_version: ADAPTER_VERSION,
  source_artifacts: {
    source_signatures: {
      artifact_id: signatures.artifact_id,
      git_blob_sha: inputGitBlobs.source_signatures,
      sha256: sha256(signaturePath),
    },
    blind_anchor: {
      artifact_id: blind.artifact_id,
      git_blob_sha: inputGitBlobs.blind_anchor,
      sha256: sha256(blindPath),
    },
    reconstruction_readiness: {
      artifact_id: readiness.artifact_id,
      git_blob_sha: inputGitBlobs.reconstruction_readiness,
      sha256: sha256(readinessPath),
    },
  },
  summary: {
    source_cases_total: 24,
    full_chart_materialized: outputCases.length,
    not_materialized: 13,
    remaining_multiple_match: 6,
    remaining_no_anchor_match: 5,
    remaining_source_blocked: 2,
  },
  boundaries: {
    source_subject_identity_used: false,
    expert_reasoning_used: false,
    expert_conclusion_used: false,
    outcome_used: false,
    external_biography_used: false,
    missing_source_input_backfilled: false,
    non_unique_candidate_promoted: false,
    canonical_rule_promoted: false,
    empirical_probability_used: false,
    full_source_chart_equivalence_verified: false,
    method_scope_broadened: false,
  },
  cases: outputCases,
};
const leakedKeys = [...walkKeys(payload)].filter((key) => FORBIDDEN_KEYS.has(key)).sort();
if (leakedKeys.length) throw new Error("forbidden leakage keys present: " + leakedKeys.join(", "));
if (outputCases.length !== EXPECTED_CASE_IDS.length) throw new Error("materializer did not produce exactly 11 cases");
fs.writeFileSync(outputPath, JSON.stringify(payload, null, 2) + "\n", "utf8");
console.log(JSON.stringify(payload.summary));
