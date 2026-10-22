#!/usr/bin/env node
/**
 * Materialize only the 11 Wang cases with a unique, fully evaluated source-anchor match.
 *
 * Usage:
 *   npm install --no-save iztro@2.6.1
 *   node product/tools/materialize_wang_full_charts.mjs \
 *     product/expert_cases/wang_tingzhi/SOURCE_BIRTH_SIGNATURES_V0_1.json \
 *     product/expert_cases/wang_tingzhi/FULL_CHART_RECONSTRUCTION_READINESS_V0_1.json \
 *     product/expert_cases/wang_tingzhi/BLIND_EVIDENCE_V0_1.json \
 *     /tmp/FULL_CHART_MATERIALIZATION_V0_1B.json
 *
 * The complete generated chart is retained as engine output. Only the target
 * palace identity and fourteen-major-star anchor are independently verified.
 */
import fs from "node:fs";
import crypto from "node:crypto";
import { astro } from "iztro";

const [signaturePath, readinessPath, blindEvidencePath, outputPath] =
  process.argv.slice(2);
if (!signaturePath || !readinessPath || !blindEvidencePath || !outputPath) {
  throw new Error("Usage: materialize_wang_full_charts.mjs SOURCE.json READINESS.json BLIND.json OUTPUT.json");
}

const readJson = (path) => JSON.parse(fs.readFileSync(path, "utf8"));
const signatures = readJson(signaturePath);
const readiness = readJson(readinessPath);
const blind = readJson(blindEvidencePath);

const ELIGIBLE_CASES = [
  "WANG-CASE-001",
  "WANG-CASE-003",
  "WANG-CASE-006",
  "WANG-CASE-009",
  "WANG-CASE-010",
  "WANG-CASE-012",
  "WANG-CASE-013",
  "WANG-CASE-015",
  "WANG-CASE-019",
  "WANG-CASE-021",
  "WANG-CASE-023",
];

const MAJOR_ORDER = [
  "紫微", "天机", "太阳", "武曲", "天同", "廉贞", "天府",
  "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军",
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
  子: "午", 丑: "未", 寅: "申", 卯: "酉", 辰: "戌", 巳: "亥",
  午: "子", 未: "丑", 申: "寅", 酉: "卯", 戌: "辰", 亥: "巳",
};

function stableValue(value) {
  if (Array.isArray(value)) return value.map(stableValue);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value).sort().map((key) => [key, stableValue(value[key])])
    );
  }
  return value;
}

function normalizePalaceName(value) {
  return String(value ?? "").trim().replace(/宫$/u, "");
}

function stableMajorNames(stars) {
  const order = new Map(MAJOR_ORDER.map((name, index) => [name, index]));
  return [...new Set((stars ?? [])
    .map((star) => String(star.name ?? "").trim())
    .filter(Boolean))]
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
  if (!aliases) throw new Error("unsupported target domain: " + domain);
  const palace = (raw.palaces ?? []).find((item) =>
    aliases.includes(normalizePalaceName(item.name))
  );
  if (!palace) {
    throw new Error("target palace not found for domain " + domain);
  }
  return palace;
}

function oppositePalace(raw, target) {
  const branch = String(target.earthlyBranch ?? "").trim();
  const opposite = OPPOSITE_BRANCH[branch];
  if (!opposite) throw new Error("unsupported target branch: " + branch);
  const palace = (raw.palaces ?? []).find(
    (item) => String(item.earthlyBranch ?? "").trim() === opposite
  );
  if (!palace) throw new Error("opposite palace not found for branch " + branch);
  return palace;
}

function candidateId(caseId, day, timeIndex) {
  return caseId + ":D" + String(day).padStart(2, "0") +
    ":T" + String(timeIndex).padStart(2, "0");
}

function sourceCandidates(row) {
  if (String(row.source_status ?? "").startsWith("BLOCKED_")) return [];
  const out = [];
  for (const day of row.lunar_day_candidates ?? []) {
    for (const timeIndex of row.time_index_candidates ?? []) {
      out.push({
        candidate_id: candidateId(row.case_id, day, timeIndex),
        lunar_date_input: String(row.lunar_year) + "-" +
          String(row.lunar_month) + "-" + String(day),
        lunar_year: Number(row.lunar_year),
        lunar_month: Number(row.lunar_month),
        lunar_day: Number(day),
        time_index: Number(timeIndex),
        gender: row.gender,
        is_leap_month: Boolean(row.is_leap_month),
      });
    }
  }
  return out.sort((a, b) =>
    a.lunar_day - b.lunar_day || a.time_index - b.time_index
  );
}

function evaluateCandidate(sourceRow, anchor, candidate) {
  const chart = astro.byLunar(
    candidate.lunar_date_input,
    candidate.time_index,
    candidate.gender,
    candidate.is_leap_month,
    true,
    "zh-CN"
  );
  const raw = typeof chart.toJSON === "function" ? chart.toJSON() : chart;
  const target = findTargetPalace(raw, anchor.target_domain);
  const aliases = DOMAIN_PALACE_ALIASES[anchor.target_domain] ?? [];
  const expectedName = normalizePalaceName(anchor.target_palace);
  const observedName = normalizePalaceName(target.name);
  const identityMatch =
    aliases.includes(expectedName) && aliases.includes(observedName);
  const observedDirect = stableMajorNames(target.majorStars);
  const observedBorrowed = anchor.target_palace_empty_main_star
    ? stableMajorNames(oppositePalace(raw, target).majorStars)
    : [];
  const directMatch = sameNames(observedDirect, anchor.target_palace_main_stars ?? []);
  const borrowedMatch = sameNames(
    observedBorrowed,
    anchor.borrowed_from_opposite_main_stars ?? []
  );
  const emptyMatch =
    Boolean(anchor.target_palace_empty_main_star) === (observedDirect.length === 0);
  const anchorMatch = identityMatch && directMatch && borrowedMatch && emptyMatch;

  return {
    candidate_id: candidate.candidate_id,
    anchor_match: anchorMatch,
    target_palace_identity_match: identityMatch,
    direct_major_star_system_match: directMatch,
    borrowed_opposite_major_star_system_match: borrowedMatch,
    target_palace_empty_state_match: emptyMatch,
    raw,
    observed: {
      target_palace_name: target.name ?? null,
      target_palace_branch: target.earthlyBranch ?? null,
      target_main_stars: observedDirect,
      borrowed_opposite_main_stars: observedBorrowed,
    },
  };
}

// Match the exact engine/configuration used by Product #545.
if (signatures.artifact_id !== "WANG_SOURCE_BIRTH_SIGNATURES_V0_1") {
  throw new Error("unexpected source-signature artifact");
}
if (readiness.artifact_id !== "WANG_FULL_CHART_RECONSTRUCTION_READINESS_V0_1") {
  throw new Error("unexpected reconstruction-readiness artifact");
}
if (blind.artifact_id !== "WANG_BLIND_EVIDENCE_V0_1") {
  throw new Error("unexpected blind-evidence anchor artifact");
}
const policy = signatures.reconstruction_policy ?? {};
const expectedPolicy = {
  engine: "iztro-js",
  engine_version: "2.6.1",
  algorithm: "zhongzhou",
  astro_type: "heaven",
  day_divide: "forward",
  year_divide: "normal",
  horoscope_divide: "normal",
  fix_leap: true,
};
for (const [key, expected] of Object.entries(expectedPolicy)) {
  if (policy[key] !== expected) {
    throw new Error("source reconstruction policy drift at " + key);
  }
}
if (readiness.summary?.unique_anchor_match !== 11 ||
    readiness.summary?.multiple_anchor_match !== 6 ||
    readiness.summary?.no_anchor_match !== 5 ||
    readiness.summary?.blocked_source_incomplete !== 2 ||
    readiness.summary?.engine_unsupported !== 0) {
  throw new Error("accepted readiness census drift");
}

astro.config({
  algorithm: "zhongzhou",
  dayDivide: "forward",
  yearDivide: "normal",
  horoscopeDivide: "normal",
});

const sourceById = new Map(signatures.cases.map((row) => [row.case_id, row]));
const readinessById = new Map(readiness.cases.map((row) => [row.case_id, row]));
const blindById = new Map(blind.cases.map((row) => [row.case_id, row]));

const materializedCases = ELIGIBLE_CASES.map((caseId) => {
  const sourceRow = sourceById.get(caseId);
  const readinessRow = readinessById.get(caseId);
  const anchor = blindById.get(caseId);
  if (!sourceRow || !readinessRow || !anchor) {
    throw new Error(caseId + ": required source/readiness/anchor row missing");
  }
  if (readinessRow.status !== "UNIQUE_ANCHOR_MATCH" ||
      readinessRow.full_chart_materialization_ready !== true ||
      readinessRow.engine_errors?.length !== 0 ||
      readinessRow.source_candidate_count !== readinessRow.evaluated_candidate_count ||
      readinessRow.anchor_match_count !== 1 ||
      readinessRow.matched_candidate_ids?.length !== 1) {
    throw new Error(caseId + ": readiness is not uniquely and completely evaluated");
  }

  const candidates = sourceCandidates(sourceRow);
  if (candidates.length !== readinessRow.source_candidate_count) {
    throw new Error(caseId + ": source candidate count disagrees with readiness");
  }

  const evaluations = candidates.map((candidate) => {
    const evaluated = evaluateCandidate(sourceRow, anchor, candidate);
    return { candidate, ...evaluated };
  });
  const matches = evaluations.filter((item) => item.anchor_match);
  if (evaluations.some((item) => !item.raw)) {
    throw new Error(caseId + ": a source-bounded candidate did not produce a chart");
  }
  if (matches.length !== 1) {
    throw new Error(caseId + ": rerun did not produce exactly one target-anchor match");
  }
  if (matches[0].candidate.candidate_id !== readinessRow.matched_candidate_ids[0]) {
    throw new Error(caseId + ": selected candidate differs from accepted readiness");
  }

  const selected = matches[0];
  const chartSnapshot = stableValue(selected.raw);
  const snapshotCanonical = JSON.stringify(chartSnapshot);
  const chartHash = crypto.createHash("sha256").update(snapshotCanonical, "utf8").digest("hex");
  const candidateEvaluationRecords = evaluations.map((item) => ({
    candidate_id: item.candidate.candidate_id,
    anchor_match: item.anchor_match,
    target_palace_identity_match: item.target_palace_identity_match,
    direct_major_star_system_match: item.direct_major_star_system_match,
    borrowed_opposite_major_star_system_match:
      item.borrowed_opposite_major_star_system_match,
    target_palace_empty_state_match: item.target_palace_empty_state_match,
  }));

  return {
    case_id: caseId,
    source_chart_span_ref: sourceRow.source_chart_span_ref,
    source_pages: sourceRow.source_pages,
    source_status: sourceRow.source_status,
    candidate_selection: {
      source_candidate_count: candidates.length,
      evaluated_candidate_count: evaluations.length,
      anchor_match_count: matches.length,
      candidate_ids_evaluated: candidates.map((item) => item.candidate_id),
      matched_candidate_id: selected.candidate.candidate_id,
      nonmatching_candidate_ids: evaluations
        .filter((item) => !item.anchor_match)
        .map((item) => item.candidate.candidate_id),
      policy: "SELECT_ONLY_AFTER_COMPLETE_EVALUATION_AND_EXACTLY_ONE_SOURCE_ANCHOR_MATCH",
      evaluations: candidateEvaluationRecords,
    },
    source_input: {
      calendar_type: "LUNAR",
      lunar_date_input: selected.candidate.lunar_date_input,
      lunar_year: selected.candidate.lunar_year,
      lunar_month: selected.candidate.lunar_month,
      lunar_day: selected.candidate.lunar_day,
      time_index: selected.candidate.time_index,
      source_time_label: sourceRow.source_time_label,
      source_day_notation: sourceRow.source_day_notation,
      gender: selected.candidate.gender,
      is_leap_month: selected.candidate.is_leap_month,
    },
    anchor_verification: {
      status: "UNIQUE_ANCHOR_MATCH",
      target_domain: anchor.target_domain,
      expected_target_palace: anchor.target_palace,
      observed_target_palace: selected.observed.target_palace_name,
      target_palace_identity_match: selected.target_palace_identity_match,
      expected_target_main_stars: anchor.target_palace_main_stars,
      observed_target_main_stars: selected.observed.target_main_stars,
      direct_major_star_system_match: selected.direct_major_star_system_match,
      expected_borrowed_opposite_main_stars: anchor.borrowed_from_opposite_main_stars,
      observed_borrowed_opposite_main_stars: selected.observed.borrowed_opposite_main_stars,
      borrowed_opposite_major_star_system_match:
        selected.borrowed_opposite_major_star_system_match,
      target_palace_empty_state_match: selected.target_palace_empty_state_match,
      source_anchor_fact_refs: anchor.fact_refs,
      source_chart_span_ref: anchor.source_chart_span_ref,
      source_pages: anchor.source_pages,
      verification_scope: "TARGET_PALACE_IDENTITY_AND_FOURTEEN_MAJOR_STAR_SYSTEM_ONLY",
      full_source_chart_equivalence: false,
    },
    chart_snapshot_sha256: chartHash,
    chart_snapshot: chartSnapshot,
  };
});

const metadata = {
  schema_version: "0.1B",
  artifact_id: "WANG_FULL_CHART_MATERIALIZATION_V0_1B",
  created_from_issue: 588,
  corpus_id: signatures.corpus_id,
  source_artifact_id: signatures.artifact_id,
  readiness_artifact_id: readiness.artifact_id,
  anchor_artifact_id: blind.artifact_id,
  engine: {
    name: "iztro-js",
    version: "2.6.1",
    entrypoint: "astro.byLunar",
    algorithm: "zhongzhou",
    input_calendar: "lunar",
    astro_type: "heaven",
    fix_leap: true,
    day_divide: "forward",
    year_divide: "normal",
    horoscope_divide: "normal",
  },
  scope: {
    corpus_case_count: 24,
    eligible_case_count: 11,
    materialized_case_count: materializedCases.length,
    case_ids: ELIGIBLE_CASES,
    materialization_level: "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED_FULL_CHART",
    target_anchor_verified: true,
    target_anchor_verification_scope: "TARGET_PALACE_IDENTITY_AND_FOURTEEN_MAJOR_STAR_SYSTEM_ONLY",
    non_target_chart_fields_independently_source_verified: false,
    full_source_chart_equivalence_claimed: false,
    method_fidelity: "NOT_VALIDATED",
    predictive_validity: "NOT_VALIDATED",
    empirical_probability: "NOT_USED",
  },
  boundaries: {
    subject_identity_used: false,
    person_group_id_used: false,
    expert_reasoning_used: false,
    expert_conclusion_used: false,
    outcome_used: false,
    biography_used: false,
    missing_source_inputs_backfilled: false,
    candidate_set_collapsed_without_anchor: false,
    method_scope_broadened: false,
    canonical_knowledge_modified: false,
    empirical_probability_used: false,
    full_source_chart_equivalence_claimed: false,
  },
  summary: {
    cases_total_in_source_corpus: 24,
    unique_anchor_match_cases_materialized: materializedCases.length,
    candidate_inputs_re_evaluated: materializedCases.reduce(
      (sum, item) => sum + item.candidate_selection.evaluated_candidate_count, 0
    ),
    target_anchor_verifications_passed: materializedCases.filter(
      (item) => item.anchor_verification.status === "UNIQUE_ANCHOR_MATCH"
    ).length,
    full_source_chart_equivalence_verified: 0,
    method_fidelity: "NOT_VALIDATED",
    predictive_validity: "NOT_VALIDATED",
  },
  cases: materializedCases,
};

const output = stableValue(metadata);
fs.writeFileSync(outputPath, JSON.stringify(output, null, 2) + "\n", "utf8");

// Machine-readable log records let the approved CI runner provide the exact
// engine output for versioned materialization without adding a workflow to the
// final Product diff.
console.log("WANG_FULL_CHART_METADATA_JSON:" + JSON.stringify({
  ...metadata,
  cases: undefined,
}));
for (const item of materializedCases) {
  console.log("WANG_FULL_CHART_CASE_JSON:" + JSON.stringify(stableValue(item)));
}
console.log("WANG_FULL_CHART_SUMMARY_JSON:" + JSON.stringify(metadata.summary));
