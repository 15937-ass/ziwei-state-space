"""Wang 24-case source-input census and reconstruction readiness.

This module validates only source-visible lunar birth signatures extracted from
Wang Tingzhi's case charts. It does not reconstruct charts itself and never
fills missing source inputs from biography, expert conclusions, or later
historical knowledge.

The corresponding JS probe uses the validated candidate inputs with the pinned
Product Zhongzhou chart configuration and compares them against the independent
target-palace anchor already materialized in BLIND_EVIDENCE_V0_1.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[2]
SIGNATURES_PATH = (
    ROOT
    / "product"
    / "expert_cases"
    / "wang_tingzhi"
    / "SOURCE_BIRTH_SIGNATURES_V0_1.json"
)
BLIND_EVIDENCE_PATH = (
    ROOT
    / "product"
    / "expert_cases"
    / "wang_tingzhi"
    / "BLIND_EVIDENCE_V0_1.json"
)

SOURCE_STATUSES = frozenset(
    {
        "SOURCE_EXACT",
        "SOURCE_EXPLICIT_DAY_ALTERNATIVES",
        "SOURCE_EXACT_ZI_TIME_AMBIGUITY",
        "BLOCKED_SOURCE_DAY_UNKNOWN",
        "BLOCKED_SOURCE_CENTER_INCOMPLETE",
    }
)

TIME_LABEL_TO_INDEX = {
    "子": (0, 12),
    "丑": (1,),
    "寅": (2,),
    "卯": (3,),
    "辰": (4,),
    "巳": (5,),
    "午": (6,),
    "未": (7,),
    "申": (8,),
    "酉": (9,),
    "戌": (10,),
    "亥": (11,),
}

FORBIDDEN_SOURCE_INPUT_KEYS = frozenset(
    {
        "source_subject_label",
        "person_group_id",
        "expert_reasoning_graph",
        "expert_conclusion_refs",
        "outcome_refs",
        "biography",
        "expert_prose",
    }
)


@dataclass(frozen=True)
class WangSourceCandidate:
    case_id: str
    lunar_date: str
    lunar_year: int
    lunar_month: int
    lunar_day: int
    time_index: int
    gender: str
    is_leap_month: bool


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


def _expected_page_map() -> dict[str, tuple[int, ...]]:
    payload = _read_json(BLIND_EVIDENCE_PATH)
    return {
        str(row["case_id"]): tuple(int(page) for page in row["source_pages"])
        for row in payload["cases"]
    }


def _expected_span_map() -> dict[str, str]:
    payload = _read_json(BLIND_EVIDENCE_PATH)
    return {
        str(row["case_id"]): str(row["source_chart_span_ref"])
        for row in payload["cases"]
    }


def _validate_int_list(
    value: Any,
    *,
    field: str,
    lower: int,
    upper: int,
    allow_empty: bool,
) -> tuple[int, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    if not allow_empty and not value:
        raise ValueError(f"{field} cannot be empty")
    out: list[int] = []
    for item in value:
        if isinstance(item, bool) or not isinstance(item, int):
            raise ValueError(f"{field} entries must be integers")
        if not lower <= item <= upper:
            raise ValueError(f"{field} entry out of range: {item}")
        out.append(item)
    if len(out) != len(set(out)):
        raise ValueError(f"{field} cannot contain duplicates")
    if out != sorted(out):
        raise ValueError(f"{field} must be sorted")
    return tuple(out)


def validate_wang_source_birth_signatures(payload: Mapping[str, Any]) -> None:
    if payload.get("schema_version") != "0.1":
        raise ValueError("Wang source signatures schema_version must be 0.1")
    if payload.get("artifact_id") != "WANG_SOURCE_BIRTH_SIGNATURES_V0_1":
        raise ValueError("unexpected Wang source-signature artifact_id")
    if payload.get("corpus_id") != "WANG_TINGZHI_ANXING_TUIDUAN_24_V0_1":
        raise ValueError("unexpected Wang corpus_id")

    leaked = sorted(FORBIDDEN_SOURCE_INPUT_KEYS.intersection(_walk_keys(payload)))
    if leaked:
        raise ValueError(
            "Wang source-input census contains forbidden leakage keys: "
            + ", ".join(leaked)
        )

    source = payload.get("source")
    if not isinstance(source, Mapping):
        raise ValueError("source must be an object")
    if source.get("artifact_ref") != "PROJECT_SOURCE:王亭之-安星法与推断实例.pdf":
        raise ValueError("unexpected Wang source artifact")
    if source.get("review_mode") != "VISUAL_SOURCE_CHART_INPUT_REVIEW_NO_OCR_GUESS":
        raise ValueError("Wang source-input review mode drift")

    policy = payload.get("reconstruction_policy")
    if not isinstance(policy, Mapping):
        raise ValueError("reconstruction_policy must be an object")
    expected_policy = {
        "engine": "iztro-js",
        "engine_version": "2.6.1",
        "algorithm": "zhongzhou",
        "astro_type": "heaven",
        "day_divide": "forward",
        "year_divide": "normal",
        "horoscope_divide": "normal",
        "fix_leap": True,
        "candidate_expansion": "SOURCE_BOUNDED_CARTESIAN_PRODUCT_ONLY",
        "zi_time_policy": "UNQUALIFIED_ZI_EXPANDS_TO_TIME_INDEX_0_AND_12",
        "missing_field_policy": "FAIL_CLOSED_NO_BIOGRAPHY_BACKFILL",
        "promotion_gate": "FULL_CHART_ONLY_AFTER_UNIQUE_TARGET_ANCHOR_MATCH",
    }
    for key, expected in expected_policy.items():
        if policy.get(key) != expected:
            raise ValueError(f"reconstruction_policy.{key} drift")

    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != 24:
        raise ValueError("Wang source-input census must contain exactly 24 cases")

    expected_ids = [f"WANG-CASE-{index:03d}" for index in range(1, 25)]
    actual_ids = [str(row.get("case_id") or "") for row in cases]
    if actual_ids != expected_ids:
        raise ValueError("Wang source-input case IDs/order mismatch")

    page_map = _expected_page_map()
    span_map = _expected_span_map()

    blocked = 0
    alternative = 0
    zi_ambiguous = 0

    for row in cases:
        if not isinstance(row, Mapping):
            raise ValueError("Wang source-input case row must be an object")

        case_id = str(row["case_id"])
        status = str(row.get("source_status") or "")
        if status not in SOURCE_STATUSES:
            raise ValueError(f"{case_id}: unsupported source_status {status}")

        pages = row.get("source_pages")
        if not isinstance(pages, list) or tuple(pages) != page_map[case_id]:
            raise ValueError(f"{case_id}: source_pages disagree with blind anchor")
        if row.get("source_chart_span_ref") != span_map[case_id]:
            raise ValueError(f"{case_id}: chart span disagrees with blind anchor")
        if row.get("calendar_type") != "LUNAR":
            raise ValueError(f"{case_id}: only source lunar input is accepted")

        year = row.get("lunar_year")
        if isinstance(year, bool) or not isinstance(year, int) or not 1 <= year <= 9999:
            raise ValueError(f"{case_id}: lunar_year must be 1..9999")

        month = row.get("lunar_month")
        day_candidates = _validate_int_list(
            row.get("lunar_day_candidates"),
            field=f"{case_id}.lunar_day_candidates",
            lower=1,
            upper=30,
            allow_empty=True,
        )
        time_candidates = _validate_int_list(
            row.get("time_index_candidates"),
            field=f"{case_id}.time_index_candidates",
            lower=0,
            upper=12,
            allow_empty=True,
        )
        gender = row.get("gender")
        time_label = row.get("source_time_label")

        is_blocked = status.startswith("BLOCKED_")
        if is_blocked:
            blocked += 1
            if status == "BLOCKED_SOURCE_DAY_UNKNOWN":
                if month is None or not 1 <= int(month) <= 12:
                    raise ValueError(f"{case_id}: known month required for day-unknown row")
                if day_candidates:
                    raise ValueError(f"{case_id}: blocked unknown day cannot have candidates")
                if gender not in {"male", "female"}:
                    raise ValueError(f"{case_id}: gender must remain source-visible")
                if time_label not in TIME_LABEL_TO_INDEX:
                    raise ValueError(f"{case_id}: time label must remain source-visible")
            elif status == "BLOCKED_SOURCE_CENTER_INCOMPLETE":
                if any((month is not None, day_candidates, time_candidates)):
                    raise ValueError(
                        f"{case_id}: incomplete page-broken center must not be backfilled"
                    )
            continue

        if isinstance(month, bool) or not isinstance(month, int) or not 1 <= month <= 12:
            raise ValueError(f"{case_id}: lunar_month must be 1..12")
        if not day_candidates:
            raise ValueError(f"{case_id}: usable row requires day candidates")
        if gender not in {"male", "female"}:
            raise ValueError(f"{case_id}: gender must be male/female")
        if time_label not in TIME_LABEL_TO_INDEX:
            raise ValueError(f"{case_id}: unsupported source_time_label")
        if tuple(time_candidates) != TIME_LABEL_TO_INDEX[str(time_label)]:
            raise ValueError(f"{case_id}: time candidates do not match source time label")
        if row.get("is_leap_month") is not False:
            raise ValueError(f"{case_id}: source does not mark a leap month")

        if status == "SOURCE_EXACT":
            if len(day_candidates) != 1 or len(time_candidates) != 1:
                raise ValueError(f"{case_id}: SOURCE_EXACT must be singleton input")
        elif status == "SOURCE_EXPLICIT_DAY_ALTERNATIVES":
            alternative += 1
            if len(day_candidates) < 2 or len(time_candidates) != 1:
                raise ValueError(
                    f"{case_id}: explicit day alternatives require >1 days and one time"
                )
        elif status == "SOURCE_EXACT_ZI_TIME_AMBIGUITY":
            zi_ambiguous += 1
            if len(day_candidates) != 1 or time_label != "子":
                raise ValueError(
                    f"{case_id}: zi-time ambiguity requires one day and source 子时"
                )
            if time_candidates != (0, 12):
                raise ValueError(f"{case_id}: 子时 must expand to 0 and 12")

    if blocked != 2:
        raise ValueError(f"Wang source-input blocked census drift: {blocked} != 2")
    if alternative != 7:
        raise ValueError(
            f"Wang explicit day-alternative census drift: {alternative} != 7"
        )
    if zi_ambiguous != 3:
        raise ValueError(
            f"Wang 子时 ambiguity census drift: {zi_ambiguous} != 3"
        )


def load_wang_source_birth_signatures(
    path: Path = SIGNATURES_PATH,
) -> dict[str, Any]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError("Wang source-input census must be a JSON object")
    validate_wang_source_birth_signatures(payload)
    return payload


def wang_source_candidates(
    row: Mapping[str, Any],
) -> tuple[WangSourceCandidate, ...]:
    status = str(row.get("source_status") or "")
    if status.startswith("BLOCKED_"):
        return ()

    year = int(row["lunar_year"])
    month = int(row["lunar_month"])
    gender = str(row["gender"])
    is_leap = bool(row["is_leap_month"])
    case_id = str(row["case_id"])

    candidates = [
        WangSourceCandidate(
            case_id=case_id,
            lunar_date=f"{year}-{month}-{day}",
            lunar_year=year,
            lunar_month=month,
            lunar_day=day,
            time_index=time_index,
            gender=gender,
            is_leap_month=is_leap,
        )
        for day in row["lunar_day_candidates"]
        for time_index in row["time_index_candidates"]
    ]
    return tuple(
        sorted(
            candidates,
            key=lambda item: (item.lunar_day, item.time_index),
        )
    )


def wang_source_candidate_census(
    path: Path = SIGNATURES_PATH,
) -> dict[str, int]:
    payload = load_wang_source_birth_signatures(path)
    rows = payload["cases"]
    usable = [row for row in rows if not str(row["source_status"]).startswith("BLOCKED_")]
    candidate_count = sum(len(wang_source_candidates(row)) for row in rows)
    return {
        "cases_total": len(rows),
        "cases_source_usable": len(usable),
        "cases_source_blocked": len(rows) - len(usable),
        "cases_exact": sum(row["source_status"] == "SOURCE_EXACT" for row in rows),
        "cases_day_alternatives": sum(
            row["source_status"] == "SOURCE_EXPLICIT_DAY_ALTERNATIVES"
            for row in rows
        ),
        "cases_zi_time_ambiguous": sum(
            row["source_status"] == "SOURCE_EXACT_ZI_TIME_AMBIGUITY"
            for row in rows
        ),
        "bounded_candidate_inputs": candidate_count,
    }
