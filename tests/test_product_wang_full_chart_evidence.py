import copy
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from src.product.wang_full_chart_evidence import (
    BRANCH_ORDER,
    EXPECTED_CASE_IDS,
    ENGINE_EXPECTED,
    validate_wang_full_chart_evidence,
)


ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "product" / "expert_cases" / "wang_tingzhi"
SIGNATURES_PATH = CASE_ROOT / "SOURCE_BIRTH_SIGNATURES_V0_1.json"
BLIND_PATH = CASE_ROOT / "BLIND_EVIDENCE_V0_1.json"
READINESS_PATH = CASE_ROOT / "FULL_CHART_RECONSTRUCTION_READINESS_V0_1.json"


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _star(name):
    return {
        "name": name,
        "type": "major",
        "brightness": None,
        "mutagen": None,
        "scope": None,
    }


def _synthetic_payload():
    """Build validator-only synthetic charts; never written as product evidence."""
    signatures = _read(SIGNATURES_PATH)
    blind = _read(BLIND_PATH)
    readiness = _read(READINESS_PATH)
    signatures_by_id = {row["case_id"]: row for row in signatures["cases"]}
    blind_by_id = {row["case_id"]: row for row in blind["cases"]}
    readiness_by_id = {row["case_id"]: row for row in readiness["cases"]}

    standard_names = [
        "命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫",
        "迁移宫", "奴仆宫", "官禄宫", "田宅宫", "福德宫", "父母宫",
    ]
    opposite = {
        "子": "午", "丑": "未", "寅": "申", "卯": "酉", "辰": "戌", "巳": "亥",
        "午": "子", "未": "丑", "申": "寅", "酉": "卯", "戌": "辰", "亥": "巳",
    }
    cases = []
    for case_id in EXPECTED_CASE_IDS:
        source = signatures_by_id[case_id]
        anchor = blind_by_id[case_id]
        ready = readiness_by_id[case_id]
        candidate_id = ready["matched_candidate_ids"][0]
        day = int(candidate_id.split(":D")[1].split(":")[0])
        time_index = int(candidate_id.split(":T")[1])
        target_name = anchor["target_palace"]
        names = [target_name] + [name for name in standard_names if name.rstrip("宫") != target_name.rstrip("宫")]
        names = names[:12]
        palaces = []
        for branch, name in zip(BRANCH_ORDER, names):
            palaces.append({
                "name": name,
                "stem": "甲",
                "branch": branch,
                "is_body_palace": False,
                "major_stars": [],
                "minor_stars": [],
                "adjective_stars": [],
                "decadal": None,
            })
        target = palaces[0]
        if anchor["target_palace_empty_main_star"]:
            borrowed = next(p for p in palaces if p["branch"] == opposite[target["branch"]])
            borrowed["major_stars"] = [_star(name) for name in anchor["borrowed_from_opposite_main_stars"]]
        else:
            target["major_stars"] = [_star(name) for name in anchor["target_palace_main_stars"]]

        direct_names = list(anchor["target_palace_main_stars"])
        borrowed_names = list(anchor["borrowed_from_opposite_main_stars"])
        cases.append({
            "case_id": case_id,
            "blind_alias": anchor["blind_alias"],
            "target_domain": anchor["target_domain"],
            "target_palace": anchor["target_palace"],
            "source_status": source["source_status"],
            "source_provenance": {
                "source_chart_span_ref": source["source_chart_span_ref"],
                "source_pages": source["source_pages"],
                "source_input_artifact_id": signatures["artifact_id"],
                "source_input_candidate_id": candidate_id,
                "readiness_artifact_id": readiness["artifact_id"],
                "readiness_status": ready["status"],
            },
            "input": {
                "calendar": "LUNAR",
                "lunar_year": source["lunar_year"],
                "lunar_month": source["lunar_month"],
                "lunar_day": day,
                "lunar_date": f'{source["lunar_year"]}-{source["lunar_month"]}-{day}',
                "time_index": time_index,
                "gender": source["gender"],
                "is_leap_month": source["is_leap_month"],
                "astro_type": "heaven",
                "config": {
                    "algorithm": "zhongzhou",
                    "day_divide": "forward",
                    "year_divide": "normal",
                    "horoscope_divide": "normal",
                    "fix_leap": True,
                },
            },
            "materialization_status": "FULL_CHART_MATERIALIZED",
            "materialization_claim": "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED",
            "full_source_chart_equivalence_verified": False,
            "target_anchor_verification": {
                "status": "UNIQUE_ANCHOR_MATCH_RECONFIRMED",
                "target_palace_identity_match": True,
                "expected_target_palace": anchor["target_palace"],
                "observed_target_palace": target_name,
                "observed_target_branch": target["branch"],
                "expected_target_main_stars": anchor["target_palace_main_stars"],
                "observed_target_main_stars": direct_names,
                "expected_borrowed_opposite_main_stars": anchor["borrowed_from_opposite_main_stars"],
                "observed_borrowed_opposite_main_stars": borrowed_names,
                "target_palace_empty_main_star": anchor["target_palace_empty_main_star"],
                "matched": True,
            },
            "chart": {
                "solar_date": "1900-01-01",
                "lunar_date": "1900-01-01",
                "chinese_date": "甲子年",
                "time": "子",
                "time_range": "23:00-00:59",
                "soul_star": "示例",
                "body_star": "示例",
                "five_elements_class": "示例",
                "soul_palace_branch": "子",
                "body_palace_branch": "午",
                "palaces": palaces,
            },
        })

    source_hashes = {
        "source_signatures": hashlib.sha256(SIGNATURES_PATH.read_bytes()).hexdigest(),
        "blind_anchor": hashlib.sha256(BLIND_PATH.read_bytes()).hexdigest(),
        "reconstruction_readiness": hashlib.sha256(READINESS_PATH.read_bytes()).hexdigest(),
    }
    payload = {
        "schema_version": "0.1B",
        "artifact_id": "WANG_FULL_CHART_BLIND_EVIDENCE_V0_1B",
        "issue": 586,
        "corpus_id": signatures["corpus_id"],
        "materialization_level": "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED",
        "engine": ENGINE_EXPECTED,
        "adapter_version": "0.1B",
        "source_artifacts": {
            "source_signatures": {
                "artifact_id": signatures["artifact_id"],
                "sha256": source_hashes["source_signatures"],
            },
            "blind_anchor": {
                "artifact_id": blind["artifact_id"],
                "sha256": source_hashes["blind_anchor"],
            },
            "reconstruction_readiness": {
                "artifact_id": readiness["artifact_id"],
                "sha256": source_hashes["reconstruction_readiness"],
            },
        },
        "summary": {
            "source_cases_total": 24,
            "full_chart_materialized": 11,
            "not_materialized": 13,
            "remaining_multiple_match": 6,
            "remaining_no_anchor_match": 5,
            "remaining_source_blocked": 2,
        },
        "boundaries": {
            "source_subject_identity_used": False,
            "expert_reasoning_used": False,
            "expert_conclusion_used": False,
            "outcome_used": False,
            "external_biography_used": False,
            "missing_source_input_backfilled": False,
            "non_unique_candidate_promoted": False,
            "canonical_rule_promoted": False,
            "empirical_probability_used": False,
            "full_source_chart_equivalence_verified": False,
            "method_scope_broadened": False,
        },
        "cases": cases,
    }
    return payload, signatures, blind, readiness, source_hashes


def _validate(payload, signatures, blind, readiness, source_hashes):
    validate_wang_full_chart_evidence(
        payload, signatures, blind, readiness, source_hashes=source_hashes
    )


def test_full_chart_validator_accepts_only_synthetic_validator_fixture():
    payload, signatures, blind, readiness, source_hashes = _synthetic_payload()
    _validate(payload, signatures, blind, readiness, source_hashes)
    assert tuple(row["case_id"] for row in payload["cases"]) == EXPECTED_CASE_IDS
    assert all(len(row["chart"]["palaces"]) == 12 for row in payload["cases"])


def test_full_chart_validator_rejects_any_leakage_key():
    payload, signatures, blind, readiness, source_hashes = _synthetic_payload()
    mutated = copy.deepcopy(payload)
    mutated["cases"][0]["source_subject_label"] = "FORBIDDEN"
    with pytest.raises(ValueError, match="forbidden leakage"):
        _validate(mutated, signatures, blind, readiness, source_hashes)


def test_full_chart_validator_rejects_non_unique_candidate_or_wrong_candidate_id():
    payload, signatures, blind, readiness, source_hashes = _synthetic_payload()
    mutated = copy.deepcopy(payload)
    mutated["cases"][0]["source_provenance"]["source_input_candidate_id"] = "WANG-CASE-001:D14:T06"
    with pytest.raises(ValueError, match="candidate ID"):
        _validate(mutated, signatures, blind, readiness, source_hashes)


def test_full_chart_validator_rejects_missing_or_duplicate_palace_branch():
    payload, signatures, blind, readiness, source_hashes = _synthetic_payload()
    mutated = copy.deepcopy(payload)
    mutated["cases"][0]["chart"]["palaces"][0]["branch"] = "午"
    with pytest.raises(ValueError, match="canonical branch order"):
        _validate(mutated, signatures, blind, readiness, source_hashes)


def test_full_chart_validator_rejects_anchor_star_mismatch():
    payload, signatures, blind, readiness, source_hashes = _synthetic_payload()
    mutated = copy.deepcopy(payload)
    mutated["cases"][0]["chart"]["palaces"][0]["major_stars"] = [_star("天梁")]
    with pytest.raises(ValueError, match="disagrees with anchor"):
        _validate(mutated, signatures, blind, readiness, source_hashes)


def test_full_chart_validator_rejects_source_digest_mismatch():
    payload, signatures, blind, readiness, source_hashes = _synthetic_payload()
    mutated = copy.deepcopy(source_hashes)
    mutated["blind_anchor"] = "0" * 64
    with pytest.raises(ValueError, match="digest mismatch"):
        _validate(payload, signatures, blind, readiness, mutated)


def test_full_chart_validator_rejects_changed_engine_contract():
    payload, signatures, blind, readiness, source_hashes = _synthetic_payload()
    mutated = copy.deepcopy(payload)
    mutated["engine"]["version"] = "2.6.0"
    with pytest.raises(ValueError, match="engine/configuration"):
        _validate(mutated, signatures, blind, readiness, source_hashes)


def test_materializer_javascript_syntax_when_node_is_available():
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is not available in this test runtime")
    script = ROOT / "product" / "tools" / "wang_full_chart_materializer.mjs"
    result = subprocess.run(
        [node, "--check", str(script)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
