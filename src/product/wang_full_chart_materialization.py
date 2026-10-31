"""Historical v1.0 validator for source-bounded Wang full-chart evidence v0.1B.

This artifact was materialized under the former day_divide=forward configuration and is not a v1.1 production snapshot.

The full-chart artifact is a Product reconstruction, not source-transcribed chart truth.
It remains separate from the original target-palace-only blind-evidence artifact.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
CASE_ROOT = ROOT / "product" / "expert_cases" / "wang_tingzhi"
FULL_CHART_PATH = CASE_ROOT / "FULL_CHART_MATERIALIZATION_V0_1B.json"
SIGNATURES_PATH = CASE_ROOT / "SOURCE_BIRTH_SIGNATURES_V0_1.json"
BLIND_PATH = CASE_ROOT / "BLIND_EVIDENCE_V0_1.json"
READINESS_PATH = CASE_ROOT / "FULL_CHART_RECONSTRUCTION_READINESS_V0_1.json"

EXPECTED_SOURCE_GIT_BLOB_SHAS = {
    "source_signatures": "83800555169c4225427dbc35ae50e4ec21cf2257",
    "blind_anchor": "c5744b4c5278394859e563cbf6a2537c7315546f",
    "reconstruction_readiness": "a0ec93c5a17859a64d02eb029837c787c7b12bdf",
}
EXPECTED_CASE_IDS = (
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
BRANCH_ORDER = ("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥")
MAJOR_ORDER = (
    "紫微", "天机", "太阳", "武曲", "天同", "廉贞", "天府",
    "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军",
)
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
    "子": "午", "丑": "未", "寅": "申", "卯": "酉", "辰": "戌", "巳": "亥",
    "午": "子", "未": "丑", "申": "寅", "酉": "卯", "戌": "辰", "亥": "巳",
}
FORBIDDEN_KEYS = frozenset({
    "source_subject_label",
    "source_subject_name",
    "person_name",
    "person_group_id",
    "expert_reasoning_graph",
    "expert_conclusion_refs",
    "outcome_refs",
    "reasoning_span_ref",
    "conclusion_span_ref",
    "outcome_span_ref",
    "expert_prose",
    "biography",
})
ENGINE_EXPECTED = {
    "name": "iztro-js",
    "version": "2.6.1",
    "source_revision": "2c7ef9be669df7b19d1799f4dce335fed3794f78",
    "entrypoint": "astro.byLunar",
    "algorithm": "zhongzhou",
    "astro_type": "heaven",
    "input_calendar": "lunar",
    "fix_leap": True,
    "day_divide": "forward",
    "year_divide": "normal",
    "horoscope_divide": "normal",
}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, Mapping):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(_walk_keys(nested))
    return keys


def _normalise_palace_name(value: Any) -> str:
    return str(value or "").strip().removesuffix("宫")


def _stable_major_names(stars: Any) -> list[str]:
    names: set[str] = set()
    for star in (stars or []):
        if isinstance(star, Mapping):
            name = str(star.get("name") or "").strip()
        else:
            name = str(star or "").strip()
        if name:
            names.add(name)
    rank = {name: index for index, name in enumerate(MAJOR_ORDER)}
    return sorted(names, key=lambda name: (rank.get(name, 999), name))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_digest(value: Any, label: str) -> str:
    digest = str(value or "")
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError(f"{label} must be a lowercase SHA-256 digest")
    return digest


def _candidate_id(case_id: str, day: int, time_index: int) -> str:
    return f"{case_id}:D{day:02d}:T{time_index:02d}"


def _validate_chart_shape(chart: Mapping[str, Any], case_id: str) -> list[Mapping[str, Any]]:
    required_chart_fields = {
        "solar_date", "lunar_date", "chinese_date", "time", "time_range",
        "soul_star", "body_star", "five_elements_class", "soul_palace_branch",
        "body_palace_branch", "palaces",
    }
    missing = sorted(required_chart_fields - set(chart))
    if missing:
        raise ValueError(f"{case_id}: chart fields missing: {missing}")
    palaces = chart.get("palaces")
    if not isinstance(palaces, list) or len(palaces) != 12:
        raise ValueError(f"{case_id}: chart must contain exactly 12 palaces")
    branches = [str(palace.get("branch") or "") for palace in palaces]
    if branches != list(BRANCH_ORDER):
        raise ValueError(f"{case_id}: palace branches must be unique and in canonical branch order")
    names = [_normalise_palace_name(palace.get("name")) for palace in palaces]
    if len(set(names)) != 12:
        raise ValueError(f"{case_id}: normalized palace names must be unique")
    required_palace_fields = {
        "name", "stem", "branch", "is_body_palace", "major_stars",
        "minor_stars", "adjective_stars", "decadal",
    }
    for palace in palaces:
        missing_palace = sorted(required_palace_fields - set(palace))
        if missing_palace:
            raise ValueError(f"{case_id}: palace fields missing: {missing_palace}")
        for star_field in ("major_stars", "minor_stars", "adjective_stars"):
            stars = palace.get(star_field)
            if not isinstance(stars, list):
                raise ValueError(f"{case_id}: {star_field} must be an array")
            for star in stars:
                if not isinstance(star, Mapping) or not str(star.get("name") or "").strip():
                    raise ValueError(f"{case_id}: malformed {star_field} entry")
    return palaces


def validate_wang_full_chart_evidence(
    payload: Mapping[str, Any],
    signatures: Mapping[str, Any],
    blind: Mapping[str, Any],
    readiness: Mapping[str, Any],
    *,
    source_hashes: Mapping[str, str] | None = None,
) -> None:
    """Validate the full-chart artifact against its three immutable source inputs."""
    if payload.get("schema_version") != "0.1B":
        raise ValueError("full-chart evidence schema_version must be 0.1B")
    if payload.get("artifact_id") != "WANG_FULL_CHART_MATERIALIZATION_V0_1B":
        raise ValueError("unexpected full-chart evidence artifact_id")
    if payload.get("issue") != 588:
        raise ValueError("full-chart materialization must be tracked by Product Issue #588")
    if payload.get("corpus_id") != signatures.get("corpus_id"):
        raise ValueError("full-chart corpus_id mismatch")
    if payload.get("materialization_level") != "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED":
        raise ValueError("unsupported full-chart materialization level")
    if payload.get("engine") != ENGINE_EXPECTED:
        raise ValueError("full-chart engine/configuration contract mismatch")
    if payload.get("adapter_version") != "0.1B":
        raise ValueError("unexpected full-chart adapter version")

    if signatures.get("artifact_id") != "WANG_SOURCE_BIRTH_SIGNATURES_V0_1":
        raise ValueError("unexpected source-signature input artifact")
    if blind.get("artifact_id") != "WANG_BLIND_EVIDENCE_V0_1":
        raise ValueError("unexpected blind-anchor input artifact")
    if readiness.get("artifact_id") != "WANG_FULL_CHART_RECONSTRUCTION_READINESS_V0_1":
        raise ValueError("unexpected readiness input artifact")

    source_artifacts = payload.get("source_artifacts")
    if not isinstance(source_artifacts, Mapping):
        raise ValueError("source_artifacts must be an object")
    expected_source_refs = {
        "source_signatures": signatures["artifact_id"],
        "blind_anchor": blind["artifact_id"],
        "reconstruction_readiness": readiness["artifact_id"],
    }
    for key, artifact_id in expected_source_refs.items():
        ref = source_artifacts.get(key)
        if not isinstance(ref, Mapping) or ref.get("artifact_id") != artifact_id:
            raise ValueError(f"source artifact reference mismatch: {key}")
        digest = _check_digest(ref.get("sha256"), f"source_artifacts.{key}.sha256")
        if ref.get("git_blob_sha") != EXPECTED_SOURCE_GIT_BLOB_SHAS[key]:
            raise ValueError(f"source artifact Git blob version changed: {key}")
        if source_hashes is not None and digest != source_hashes.get(key):
            raise ValueError(f"source artifact digest mismatch: {key}")

    expected_summary = {
        "source_cases_total": 24,
        "full_chart_materialized": 11,
        "not_materialized": 13,
        "remaining_multiple_match": 6,
        "remaining_no_anchor_match": 5,
        "remaining_source_blocked": 2,
    }
    if payload.get("summary") != expected_summary:
        raise ValueError("full-chart summary mismatch")

    boundaries = payload.get("boundaries")
    if not isinstance(boundaries, Mapping):
        raise ValueError("boundaries must be an object")
    required_false = (
        "source_subject_identity_used",
        "expert_reasoning_used",
        "expert_conclusion_used",
        "outcome_used",
        "external_biography_used",
        "missing_source_input_backfilled",
        "non_unique_candidate_promoted",
        "canonical_rule_promoted",
        "empirical_probability_used",
        "full_source_chart_equivalence_verified",
        "method_scope_broadened",
    )
    if any(boundaries.get(key) is not False for key in required_false):
        raise ValueError("full-chart artifact violates a non-interference boundary")

    leaked = sorted(FORBIDDEN_KEYS.intersection(_walk_keys(payload)))
    if leaked:
        raise ValueError(f"full-chart artifact contains forbidden leakage keys: {leaked}")

    signature_rows = signatures.get("cases")
    blind_rows = blind.get("cases")
    readiness_rows = readiness.get("cases")
    if not all(isinstance(rows, list) and len(rows) == 24 for rows in (signature_rows, blind_rows, readiness_rows)):
        raise ValueError("all source inputs must contain exactly 24 case rows")
    signatures_by_id = {str(row.get("case_id")): row for row in signature_rows}
    blind_by_id = {str(row.get("case_id")): row for row in blind_rows}
    readiness_by_id = {str(row.get("case_id")): row for row in readiness_rows}
    if len(signatures_by_id) != 24 or len(blind_by_id) != 24 or len(readiness_by_id) != 24:
        raise ValueError("duplicate or missing case IDs in source inputs")

    eligible = tuple(
        str(row.get("case_id"))
        for row in readiness_rows
        if row.get("status") == "UNIQUE_ANCHOR_MATCH"
        and row.get("full_chart_materialization_ready") is True
    )
    if eligible != EXPECTED_CASE_IDS:
        raise ValueError("readiness eligibility set/order changed; explicit re-review required")

    cases = payload.get("cases")
    if not isinstance(cases, list) or tuple(str(row.get("case_id")) for row in cases) != EXPECTED_CASE_IDS:
        raise ValueError("full-chart artifact must contain exactly the 11 approved case IDs in order")

    for row in cases:
        case_id = str(row.get("case_id") or "")
        source_row = signatures_by_id.get(case_id)
        anchor = blind_by_id.get(case_id)
        ready = readiness_by_id.get(case_id)
        if source_row is None or anchor is None or ready is None:
            raise ValueError(f"{case_id}: source, anchor, or readiness row missing")
        if source_row.get("source_chart_span_ref") != anchor.get("source_chart_span_ref"):
            raise ValueError(f"{case_id}: source chart span mismatch")
        if row.get("blind_alias") != anchor.get("blind_alias"):
            raise ValueError(f"{case_id}: blind alias mismatch")
        if row.get("target_domain") != anchor.get("target_domain") or row.get("target_palace") != anchor.get("target_palace"):
            raise ValueError(f"{case_id}: target scope mismatch")
        if row.get("source_status") != source_row.get("source_status"):
            raise ValueError(f"{case_id}: source status mismatch")
        if row.get("materialization_status") != "FULL_CHART_MATERIALIZED":
            raise ValueError(f"{case_id}: invalid materialization status")
        if row.get("materialization_claim") != "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED":
            raise ValueError(f"{case_id}: invalid maturity claim")
        if row.get("full_source_chart_equivalence_verified") is not False:
            raise ValueError(f"{case_id}: full-source-chart equivalence must remain unverified")

        candidate_id = ready.get("matched_candidate_ids", [None])[0]
        if (
            ready.get("status") != "UNIQUE_ANCHOR_MATCH"
            or ready.get("full_chart_materialization_ready") is not True
            or ready.get("anchor_match_count") != 1
            or ready.get("engine_errors") != []
            or ready.get("evaluated_candidate_count") != ready.get("source_candidate_count")
            or ready.get("matched_candidate_ids") != [candidate_id]
        ):
            raise ValueError(f"{case_id}: readiness row is not uniquely eligible")
        source_provenance = row.get("source_provenance")
        if not isinstance(source_provenance, Mapping):
            raise ValueError(f"{case_id}: source_provenance must be an object")
        if source_provenance.get("source_chart_span_ref") != source_row.get("source_chart_span_ref"):
            raise ValueError(f"{case_id}: source provenance span mismatch")
        if source_provenance.get("source_pages") != source_row.get("source_pages"):
            raise ValueError(f"{case_id}: source page provenance mismatch")
        if source_provenance.get("source_input_artifact_id") != signatures.get("artifact_id"):
            raise ValueError(f"{case_id}: source-input artifact lineage mismatch")
        if source_provenance.get("readiness_artifact_id") != readiness.get("artifact_id"):
            raise ValueError(f"{case_id}: readiness artifact lineage mismatch")
        if source_provenance.get("readiness_status") != ready.get("status"):
            raise ValueError(f"{case_id}: readiness status lineage mismatch")
        if source_provenance.get("source_input_candidate_id") != candidate_id:
            raise ValueError(f"{case_id}: candidate ID does not match readiness report")

        source_candidate_set = row.get("source_candidate_set")
        expected_candidate_set = {
            "source_day_notation": source_row.get("source_day_notation"),
            "lunar_day_candidates": source_row.get("lunar_day_candidates"),
            "source_time_label": source_row.get("source_time_label"),
            "time_index_candidates": source_row.get("time_index_candidates"),
            "source_candidate_count": ready.get("source_candidate_count"),
            "evaluated_candidate_count": ready.get("evaluated_candidate_count"),
            "anchor_match_count": ready.get("anchor_match_count"),
            "matched_candidate_ids": ready.get("matched_candidate_ids"),
            "source_time_ambiguity_preserved": source_row.get("source_status") == "SOURCE_EXACT_ZI_TIME_AMBIGUITY",
            "selection_basis": "EXACTLY_ONE_READINESS_ANCHOR_MATCH",
            "source_time_ambiguity_note": "The source gives unqualified 子时 only; both candidate time indices 0 and 12 remain preserved. The pinned readiness evaluation examined both candidates and found exactly one target-anchor match, T00. This does not erase or resolve the source's original time ambiguity." if case_id == "WANG-CASE-021" else None,
        }
        if source_candidate_set != expected_candidate_set:
            raise ValueError(f"{case_id}: source candidate-set provenance mismatch")
        if case_id == "WANG-CASE-021" and (
            source_row.get("source_time_label") != "子"
            or source_row.get("time_index_candidates") != [0, 12]
            or ready.get("source_candidate_count") != 2
            or ready.get("evaluated_candidate_count") != 2
            or ready.get("anchor_match_count") != 1
            or ready.get("matched_candidate_ids") != ["WANG-CASE-021:D01:T00"]
            or source_candidate_set.get("source_time_ambiguity_preserved") is not True
        ):
            raise ValueError(f"{case_id}: unqualified 子时 ambiguity must remain explicit")

        match = re.fullmatch(r"WANG-CASE-(\d{3}):D(\d{2}):T(\d{2})", str(candidate_id or ""))
        if not match or "WANG-CASE-" + match.group(1) != case_id:
            raise ValueError(f"{case_id}: malformed candidate ID")
        day = int(match.group(2))
        time_index = int(match.group(3))
        if day not in (source_row.get("lunar_day_candidates") or []):
            raise ValueError(f"{case_id}: candidate day is not source-bounded")
        if time_index not in (source_row.get("time_index_candidates") or []):
            raise ValueError(f"{case_id}: candidate time is not source-bounded")
        expected_lunar_date = f"{source_row['lunar_year']}-{source_row['lunar_month']}-{day}"
        input_row = row.get("input")
        if not isinstance(input_row, Mapping):
            raise ValueError(f"{case_id}: input must be an object")
        expected_input = {
            "calendar": "LUNAR",
            "lunar_year": source_row.get("lunar_year"),
            "lunar_month": source_row.get("lunar_month"),
            "lunar_day": day,
            "lunar_date": expected_lunar_date,
            "time_index": time_index,
            "gender": source_row.get("gender"),
            "is_leap_month": source_row.get("is_leap_month"),
            "astro_type": "heaven",
            "config": {
                "algorithm": "zhongzhou",
                "day_divide": "forward",
                "year_divide": "normal",
                "horoscope_divide": "normal",
                "fix_leap": True,
            },
        }
        if input_row != expected_input:
            raise ValueError(f"{case_id}: normalized input does not match the approved lunar candidate")

        chart = row.get("chart")
        if not isinstance(chart, Mapping):
            raise ValueError(f"{case_id}: chart must be an object")
        palaces = _validate_chart_shape(chart, case_id)
        aliases = DOMAIN_PALACE_ALIASES.get(str(anchor.get("target_domain")))
        if not aliases:
            raise ValueError(f"{case_id}: unsupported target domain")
        target = next(
            (palace for palace in palaces if _normalise_palace_name(palace.get("name")) in aliases),
            None,
        )
        if target is None:
            raise ValueError(f"{case_id}: reconstructed target palace not found")
        expected_target_name = _normalise_palace_name(anchor.get("target_palace"))
        target_identity_match = expected_target_name in aliases and _normalise_palace_name(target.get("name")) in aliases
        direct_names = _stable_major_names(target.get("major_stars"))
        empty = anchor.get("target_palace_empty_main_star") is True
        if empty != (len(direct_names) == 0):
            raise ValueError(f"{case_id}: reconstructed target-palace empty-star status disagrees with anchor")
        opposite = OPPOSITE_BRANCH.get(str(target.get("branch")))
        opposite_palace = next((palace for palace in palaces if palace.get("branch") == opposite), None)
        if opposite_palace is None:
            raise ValueError(f"{case_id}: opposite palace not found")
        borrowed_names = _stable_major_names(opposite_palace.get("major_stars")) if empty else []
        if direct_names != _stable_major_names(anchor.get("target_palace_main_stars")):
            raise ValueError(f"{case_id}: reconstructed direct major-star system disagrees with anchor")
        if borrowed_names != _stable_major_names(anchor.get("borrowed_from_opposite_main_stars")):
            raise ValueError(f"{case_id}: reconstructed borrowed major-star system disagrees with anchor")
        verification = row.get("target_anchor_verification")
        if not isinstance(verification, Mapping):
            raise ValueError(f"{case_id}: target_anchor_verification must be an object")
        if (
            verification.get("status") != "UNIQUE_ANCHOR_MATCH_RECONFIRMED"
            or verification.get("matched") is not True
            or verification.get("target_palace_identity_match") is not target_identity_match
            or verification.get("expected_target_palace") != anchor.get("target_palace")
            or verification.get("expected_target_main_stars") != anchor.get("target_palace_main_stars", [])
            or verification.get("expected_borrowed_opposite_main_stars") != anchor.get("borrowed_from_opposite_main_stars", [])
            or verification.get("target_palace_empty_main_star") is not empty
            or verification.get("observed_target_palace") != target.get("name")
            or verification.get("observed_target_branch") != target.get("branch")
            or verification.get("observed_target_main_stars") != direct_names
            or verification.get("observed_borrowed_opposite_main_stars") != borrowed_names
        ):
            raise ValueError(f"{case_id}: anchor verification record disagrees with normalized chart")


def load_wang_full_chart_evidence(root: Path = ROOT) -> Mapping[str, Any]:
    """Load and validate the committed artifact and its immutable inputs."""
    case_root = root / "product" / "expert_cases" / "wang_tingzhi"
    payload = _read_json(case_root / "FULL_CHART_MATERIALIZATION_V0_1B.json")
    signatures = _read_json(case_root / "SOURCE_BIRTH_SIGNATURES_V0_1.json")
    blind = _read_json(case_root / "BLIND_EVIDENCE_V0_1.json")
    readiness = _read_json(case_root / "FULL_CHART_RECONSTRUCTION_READINESS_V0_1.json")
    source_paths = {
        "source_signatures": case_root / "SOURCE_BIRTH_SIGNATURES_V0_1.json",
        "blind_anchor": case_root / "BLIND_EVIDENCE_V0_1.json",
        "reconstruction_readiness": case_root / "FULL_CHART_RECONSTRUCTION_READINESS_V0_1.json",
    }
    for key, path in source_paths.items():
        raw = path.read_bytes()
        git_blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
        if git_blob_sha != EXPECTED_SOURCE_GIT_BLOB_SHAS[key]:
            raise ValueError(f"source artifact Git blob version changed: {key}")
    source_hashes = {key: _sha256(path) for key, path in source_paths.items()}
    validate_wang_full_chart_evidence(
        payload, signatures, blind, readiness, source_hashes=source_hashes
    )
    return payload
