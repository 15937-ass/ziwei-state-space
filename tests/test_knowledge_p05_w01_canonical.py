from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge/palaces/P05_wealth"
CSV_PATH = BASE / "W01_CANONICAL_001_100_v0.1.csv"
READJ_PATH = BASE / "W01_SOURCE_READJUDICATION_100_v0.1.json"
TIME_PATH = BASE / "W01_SOURCE_TIME_SCOPE_v0.1.json"
GAP_PATH = BASE / "W01_GAPS_AND_UNCERTAINTIES_v0.1.json"


def _rows():
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_w01_exact_contiguous_100():
    rows = _rows()
    assert len(rows) == 100
    expected = [f"W01-{i:03d}" for i in range(1, 101)]
    assert [r["projection_rule_id"] for r in rows] == expected
    assert len({r["projection_rule_id"] for r in rows}) == 100
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert all(r["palace_id"] == "P05" for r in rows)
    assert all(r["source_span_verified"] == "true" for r in rows)
    assert all(r["review_status"] == "SOURCE_SPAN_VERIFIED" for r in rows)


def test_w01_source_revalidation_is_not_empirical():
    rows = _rows()
    forbidden = {"probability", "weight", "gain", "decay", "posterior"}
    assert not (forbidden & set(rows[0].keys()))
    assert all(r["case_support_only"] == "false" for r in rows)
    assert all(r["history_feedback"] == "" for r in rows)


def test_w01_base_and_strengthener_are_separated():
    rows = {r["projection_rule_id"]: r for r in _rows()}
    r = rows["W01-076"]
    assert "天同在财帛宫" in r["condition"]
    assert "孤辰同度仅作性质加强" in r["condition"]
    assert r["normalization_status"] == "BASE_PLUS_STRENGTHENER_SEPARATED"


def test_w01_contextual_exception_not_general_career_rule():
    rows = {r["projection_rule_id"]: r for r in _rows()}
    r = rows["W01-094"]
    assert r["projection_target"] == "sharp_tool_profession_is_contextual_exception_for_ziwei_huaquan_with_malefics"
    assert r["normalization_status"] == "CONTEXTUAL_EXCEPTION_NOT_GENERAL_CAREER_RULE"


def test_w01_uncertainty_and_gap_are_explicit():
    data = json.loads(GAP_PATH.read_text(encoding="utf-8"))
    assert data["core_gap_required"] is False
    assert data["human_gate"] == "NONE"
    assert [g["gap_id"] for g in data["local_gaps"]] == ["W01-GAP-001"]
    ids = {x["id"] for x in data["lexical_uncertainties"]}
    assert {"W01-056", "W01-069", "W01-071", "W01-073", "W01-074", "W01-075", "W01-077"} <= ids
    policies = {x["id"]: x["policy"] for x in data["lexical_uncertainties"]}
    assert policies["W01-071"] == "DO_NOT_BROADEN_TO_GENERIC_EMPTY_STAR_SET"


def test_w01_temporal_scope_preserves_natal_baseline_guard():
    data = json.loads(TIME_PATH.read_text(encoding="utf-8"))
    recs = {x["id"]: x for x in data["records"]}
    assert recs["W01-051"]["source_scope"] == ["NATAL", "DECADE"]
    assert recs["W01-052"]["source_scope"] == ["DECADE", "YEAR"]
    assert recs["W01-055"]["source_scope"] == ["NATAL", "DECADE", "YEAR"]
    assert recs["W01-089"]["source_scope"] == ["NATAL_BASELINE", "DECADE_INFERENCE", "YEAR_INFERENCE"]
    assert "no new independent time scale" in data["boundary"]


def test_w01_readjudication_census():
    data = json.loads(READJ_PATH.read_text(encoding="utf-8"))
    s = data["summary"]
    assert s["reviewed"] == 100
    assert s["reconfirmed"] == 87
    assert s["special_dispositions"] == 13
    assert s["corrected_normalization"] == 2
    assert s["source_uncertainty_preserved"] == 7
    assert s["scope_or_time_augmented"] == 3
    assert s["gap_discovered"] == 1
    assert s["case_support_only"] == 0
    assert s["new_history_feedback"] == 0
    assert s["human_gate"] == "NONE"
