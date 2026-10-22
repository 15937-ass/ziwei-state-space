"""Validation for the source-input-reconstructed Wang full-chart artifact.

Only the 11 cases with a complete, unique, source-anchor match are accepted.
The generated chart is engine output; target-palace verification must not be
misrepresented as full-source-chart equivalence or predictive validity.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from src.product.wang_source_reconstruction import (
    BLIND_EVIDENCE_PATH,
    READINESS_PATH,
    SIGNATURES_PATH,
    load_wang_reconstruction_readiness,
    load_wang_source_birth_signatures,
    wang_source_candidates,
)

ROOT = Path(__file__).resolve().parents[2]
MATERIALIZATION_PATH = (
    ROOT
    / "product"
    / "expert_cases"
    / "wang_tingzhi"
    / "FULL_CHART_MATERIALIZATION_V0_1B.json"
)

ELIGIBLE_CASES = (
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
)

MAJOR_ORDER = (
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
)
MAJOR_INDEX = {name: index for index, name in enumerate(MAJOR_ORDER)}

DOMAIN_PALACE_ALIASES = {
    "PARENTS": ("父母",),
    "LIFE": ("命",),
    "SIBLINGS": ("兄弟",),
    "SPOUSE": ("夫妻",),
    "CHILDREN": ("子女",),
    "WEALTH": ("财帛",),
    "HEALTH": ("疾厄",),
    "TRAVEL": ("迁移",),
    "FRIENDS": ("奴仆", "仆役", "交友"),
    "CAREER": ("官禄", "事业"),
    "PROPERTY": ("田宅",),
    "FORTUNE_VIRTUE": ("福德",),
}
OPPOSITE_BRANCH = {
    "子": "午",
    "丑": "未",
    "寅": "申",
    "卯": "酉",
    "辰": "戌",
    "巳": "亥",
    "午": "子",
    "未": "丑",
    "申": "寅",
    "酉": "卯",
    "戌": "辰",
    "亥": "巳",
}
FORBIDDEN_CASE_KEYS = frozenset(
    {
        "source_subject_label",
        "source_subject_name",
        "person_group_id",
        "expert_reasoning_graph",
        "expert_conclusion_refs",
        "outcome_refs",
        "reasoning_span_ref",
        "conclusion_span_ref",
        "outcome_span_ref",
        "expert_prose",
        "biography",
    }
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(_walk_keys(nested))
    return keys


def _normalize_palace_name(value: Any) -> str:
    return str(value or "").strip().removesuffix("宫")


def _major_names(stars: Any) -> list[str]:
    if not isinstance(stars, list):
        return []
    names = {
        str(item.get("name") or "").strip()
        for item in stars
        if isinstance(item, Mapping) and str(item.get("name") or "").strip()
    }
    return sorted(names, key=lambda name: (MAJOR_INDEX.get(name, 999), name))


def _source_candidate_id(candidate: Any) -> str:
    return (
        f"{candidate.case_id}:D{candidate.lunar_day:02d}:"
        f"T{candidate.time_index:02d}"
    )


def _canonical_hash(value: Any) -> str:
    canonical = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _find_target_palace(chart: Mapping[str, Any], domain: str) -> Mapping[str, Any]:
    aliases = DOMAIN_PALACE_ALIASES.get(domain)
    if aliases is None:
        raise ValueError(f"unsupported target domain: {domain}")
    palaces = chart.get("palaces")
    if not isinstance(palaces, list):
        raise ValueError("chart_snapshot.palaces must be an array")
    found = [
        palace
        for palace in palaces
        if isinstance(palace, Mapping)
        and _normalize_palace_name(palace.get("name")) in aliases
    ]
    if len(found) != 1:
        raise ValueError(f"expected one target palace for domain {domain}")
    return found[0]


def _find_opposite_palace(
    chart: Mapping[str, Any], target: Mapping[str, Any]
) -> Mapping[str, Any]:
    branch = str(target.get("earthlyBranch") or "").strip()
    opposite = OPPOSITE_BRANCH.get(branch)
    if opposite is None:
        raise ValueError(f"unsupported target palace branch: {branch}")
    found = [
        palace
        for palace in chart.get("palaces", [])
        if isinstance(palace, Mapping)
        and str(palace.get("earthlyBranch") or "").strip() == opposite
    ]
    if len(found) != 1:
        raise ValueError(f"expected one opposite palace for branch {branch}")
    return found[0]


def validate_wang_full_chart_materialization(payload: Mapping[str, Any]) -> None:
    if payload.get("schema_version") != "0.1B":
        raise ValueError("Wang full-chart materialization schema_version must be 0.1B")
    if payload.get("artifact_id") != "WANG_FULL_CHART_MATERIALIZATION_V0_1B":
        raise ValueError("unexpected Wang full-chart materialization artifact_id")
    if payload.get("source_artifact_id") != "WANG_SOURCE_BIRTH_SIGNATURES_V0_1":
        raise ValueError("unexpected source-input artifact id")
    if payload.get("readiness_artifact_id") != "WANG_FULL_CHART_RECONSTRUCTION_READINESS_V0_1":
        raise ValueError("unexpected reconstruction-readiness artifact id")
    if payload.get("anchor_artifact_id") != "WANG_BLIND_EVIDENCE_V0_1":
        raise ValueError("unexpected target-anchor artifact id")

    expected_engine = {
        "name": "iztro-js",
        "version": "2.6.1",
        "entrypoint": "astro.byLunar",
        "algorithm": "zhongzhou",
        "input_calendar": "lunar",
        "astro_type": "heaven",
        "fix_leap": True,
        "day_divide": "forward",
        "year_divide": "normal",
        "horoscope_divide": "normal",
    }
    if payload.get("engine") != expected_engine:
        raise ValueError("Wang full-chart engine/configuration contract drift")

    source = load_wang_source_birth_signatures()
    readiness = load_wang_reconstruction_readiness()
    blind = _read_json(BLIND_EVIDENCE_PATH)
    source_by_id = {row["case_id"]: row for row in source["cases"]}
    readiness_by_id = {row["case_id"]: row for row in readiness["cases"]}
    blind_by_id = {row["case_id"]: row for row in blind["cases"]}

    scope = payload.get("scope")
    if not isinstance(scope, Mapping):
        raise ValueError("scope must be an object")
    expected_scope = {
        "corpus_case_count": 24,
        "eligible_case_count": 11,
        "materialized_case_count": 11,
        "case_ids": list(ELIGIBLE_CASES),
        "materialization_level": "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED_FULL_CHART",
        "target_anchor_verified": True,
        "target_anchor_verification_scope": "TARGET_PALACE_IDENTITY_AND_FOURTEEN_MAJOR_STAR_SYSTEM_ONLY",
        "non_target_chart_fields_independently_source_verified": False,
        "full_source_chart_equivalence_claimed": False,
        "method_fidelity": "NOT_VALIDATED",
        "predictive_validity": "NOT_VALIDATED",
        "empirical_probability": "NOT_USED",
    }
    if dict(scope) != expected_scope:
        raise ValueError("Wang full-chart materialization scope drift")

    boundaries = payload.get("boundaries")
    if not isinstance(boundaries, Mapping):
        raise ValueError("boundaries must be an object")
    expected_boundaries = {
        "subject_identity_used": False,
        "person_group_id_used": False,
        "expert_reasoning_used": False,
        "expert_conclusion_used": False,
        "outcome_used": False,
        "biography_used": False,
        "missing_source_inputs_backfilled": False,
        "candidate_set_collapsed_without_anchor": False,
        "method_scope_broadened": False,
        "canonical_knowledge_modified": False,
        "empirical_probability_used": False,
        "full_source_chart_equivalence_claimed": False,
    }
    if dict(boundaries) != expected_boundaries:
        raise ValueError("Wang full-chart materialization boundary drift")

    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != len(ELIGIBLE_CASES):
        raise ValueError("exactly 11 full-chart cases are required")
    if [str(row.get("case_id") or "") for row in cases] != list(ELIGIBLE_CASES):
        raise ValueError("Wang full-chart case IDs/order mismatch")

    expected_candidate_inputs = 0
    for case in cases:
        leaked = sorted(FORBIDDEN_CASE_KEYS.intersection(_walk_keys(case)))
        if leaked:
            raise ValueError(f"blind materialization contains forbidden leakage keys: {leaked}")

        case_id = str(case["case_id"])
        source_row = source_by_id[case_id]
        ready_row = readiness_by_id[case_id]
        anchor = blind_by_id[case_id]
        candidates = wang_source_candidates(source_row)
        candidate_ids = [_source_candidate_id(item) for item in candidates]
        expected_candidate_inputs += len(candidate_ids)

        if (
            ready_row.get("status") != "UNIQUE_ANCHOR_MATCH"
            or ready_row.get("full_chart_materialization_ready") is not True
            or ready_row.get("source_candidate_count") != len(candidates)
            or ready_row.get("evaluated_candidate_count") != len(candidates)
            or ready_row.get("anchor_match_count") != 1
            or ready_row.get("engine_errors") != []
            or len(ready_row.get("matched_candidate_ids", [])) != 1
        ):
            raise ValueError(f"{case_id}: accepted readiness is not uniquely evaluated")

        selection = case.get("candidate_selection")
        if not isinstance(selection, Mapping):
            raise ValueError(f"{case_id}: candidate_selection must be an object")
        selected_id = str(ready_row["matched_candidate_ids"][0])
        if selection.get("source_candidate_count") != len(candidate_ids):
            raise ValueError(f"{case_id}: source candidate count drift")
        if selection.get("evaluated_candidate_count") != len(candidate_ids):
            raise ValueError(f"{case_id}: not every source candidate was evaluated")
        if selection.get("anchor_match_count") != 1:
            raise ValueError(f"{case_id}: exactly one anchor match is required")
        if selection.get("candidate_ids_evaluated") != candidate_ids:
            raise ValueError(f"{case_id}: candidate evaluation set/order drift")
        if selection.get("matched_candidate_id") != selected_id:
            raise ValueError(f"{case_id}: selected candidate differs from readiness")
        expected_nonmatching = [item for item in candidate_ids if item != selected_id]
        if selection.get("nonmatching_candidate_ids") != expected_nonmatching:
            raise ValueError(f"{case_id}: nonmatching candidate provenance drift")
        if selection.get("policy") != "SELECT_ONLY_AFTER_COMPLETE_EVALUATION_AND_EXACTLY_ONE_SOURCE_ANCHOR_MATCH":
            raise ValueError(f"{case_id}: candidate-selection policy drift")

        evaluations = selection.get("evaluations")
        if not isinstance(evaluations, list) or len(evaluations) != len(candidate_ids):
            raise ValueError(f"{case_id}: candidate evaluation records missing")
        if [item.get("candidate_id") for item in evaluations] != candidate_ids:
            raise ValueError(f"{case_id}: candidate evaluation order drift")
        matching_ids = [
            item["candidate_id"] for item in evaluations if item.get("anchor_match") is True
        ]
        if matching_ids != [selected_id]:
            raise ValueError(f"{case_id}: evaluation records do not show one unique match")
        if any(
            not isinstance(item.get(field), bool)
            for item in evaluations
            for field in (
                "anchor_match",
                "target_palace_identity_match",
                "direct_major_star_system_match",
                "borrowed_opposite_major_star_system_match",
                "target_palace_empty_state_match",
            )
        ):
            raise ValueError(f"{case_id}: candidate evaluation flags must be booleans")

        selected = next(item for item in candidates if _source_candidate_id(item) == selected_id)
        source_input = case.get("source_input")
        if not isinstance(source_input, Mapping):
            raise ValueError(f"{case_id}: source_input must be an object")
        expected_input = {
            "calendar_type": "LUNAR",
            "lunar_date_input": selected.lunar_date,
            "lunar_year": selected.lunar_year,
            "lunar_month": selected.lunar_month,
            "lunar_day": selected.lunar_day,
            "time_index": selected.time_index,
            "source_time_label": source_row["source_time_label"],
            "source_day_notation": source_row["source_day_notation"],
            "gender": selected.gender,
            "is_leap_month": selected.is_leap_month,
        }
        if dict(source_input) != expected_input:
            raise ValueError(f"{case_id}: selected source input does not match the census")

        if case.get("source_chart_span_ref") != source_row["source_chart_span_ref"]:
            raise ValueError(f"{case_id}: source chart span reference drift")
        if case.get("source_pages") != source_row["source_pages"]:
            raise ValueError(f"{case_id}: source page provenance drift")
        if case.get("source_status") != source_row["source_status"]:
            raise ValueError(f"{case_id}: source status drift")

        chart = case.get("chart_snapshot")
        if not isinstance(chart, Mapping):
            raise ValueError(f"{case_id}: chart_snapshot must be an object")
        palaces = chart.get("palaces")
        if not isinstance(palaces, list) or len(palaces) != 12:
            raise ValueError(f"{case_id}: full chart must contain 12 palace records")
        palace_names = [_normalize_palace_name(item.get("name")) for item in palaces]
        if any(not name for name in palace_names) or len(set(palace_names)) != 12:
            raise ValueError(f"{case_id}: palace names must be 12 distinct values")

        target = _find_target_palace(chart, anchor["target_domain"])
        observed_direct = _major_names(target.get("majorStars"))
        identity_aliases = DOMAIN_PALACE_ALIASES[anchor["target_domain"]]
        identity_match = (
            _normalize_palace_name(anchor["target_palace"]) in identity_aliases
            and _normalize_palace_name(target.get("name")) in identity_aliases
        )
        if anchor.get("target_palace_empty_main_star"):
            observed_borrowed = _major_names(
                _find_opposite_palace(chart, target).get("majorStars")
            )
        else:
            observed_borrowed = []
        expected_direct = _major_names(
            [{"name": item} for item in anchor.get("target_palace_main_stars", [])]
        )
        expected_borrowed = _major_names(
            [{"name": item} for item in anchor.get("borrowed_from_opposite_main_stars", [])]
        )
        empty_match = bool(anchor.get("target_palace_empty_main_star")) == (
            len(observed_direct) == 0
        )
        direct_match = observed_direct == expected_direct
        borrowed_match = observed_borrowed == expected_borrowed

        verification = case.get("anchor_verification")
        if not isinstance(verification, Mapping):
            raise ValueError(f"{case_id}: anchor_verification must be an object")
        expected_verification = {
            "status": "UNIQUE_ANCHOR_MATCH",
            "target_domain": anchor["target_domain"],
            "expected_target_palace": anchor["target_palace"],
            "observed_target_palace": target.get("name"),
            "target_palace_identity_match": identity_match,
            "expected_target_main_stars": anchor["target_palace_main_stars"],
            "observed_target_main_stars": observed_direct,
            "direct_major_star_system_match": direct_match,
            "expected_borrowed_opposite_main_stars": anchor["borrowed_from_opposite_main_stars"],
            "observed_borrowed_opposite_main_stars": observed_borrowed,
            "borrowed_opposite_major_star_system_match": borrowed_match,
            "target_palace_empty_state_match": empty_match,
            "source_anchor_fact_refs": anchor["fact_refs"],
            "source_chart_span_ref": anchor["source_chart_span_ref"],
            "source_pages": anchor["source_pages"],
            "verification_scope": "TARGET_PALACE_IDENTITY_AND_FOURTEEN_MAJOR_STAR_SYSTEM_ONLY",
            "full_source_chart_equivalence": False,
        }
        if dict(verification) != expected_verification:
            raise ValueError(f"{case_id}: stored anchor verification differs from recomputed chart")
        if not all((identity_match, direct_match, borrowed_match, empty_match)):
            raise ValueError(f"{case_id}: target anchor verification failed")

        digest = case.get("chart_snapshot_sha256")
        if not isinstance(digest, str) or digest != _canonical_hash(chart):
            raise ValueError(f"{case_id}: chart snapshot SHA-256 mismatch")

    summary = payload.get("summary")
    if not isinstance(summary, Mapping):
        raise ValueError("summary must be an object")
    expected_summary = {
        "cases_total_in_source_corpus": 24,
        "unique_anchor_match_cases_materialized": 11,
        "candidate_inputs_re_evaluated": expected_candidate_inputs,
        "target_anchor_verifications_passed": 11,
        "full_source_chart_equivalence_verified": 0,
        "method_fidelity": "NOT_VALIDATED",
        "predictive_validity": "NOT_VALIDATED",
    }
    if dict(summary) != expected_summary:
        raise ValueError("Wang full-chart materialization summary drift")


def load_wang_full_chart_materialization(
    path: Path = MATERIALIZATION_PATH,
) -> dict[str, Any]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError("Wang full-chart materialization must be a JSON object")
    validate_wang_full_chart_materialization(payload)
    return payload
