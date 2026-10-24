import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "palaces" / "P01_life" / "wp05"


def _csv(name):
    with (BASE / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _json(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def test_p01_candidate_census_and_p14_deduplication():
    rows = _csv("LIFE_P05_SOURCE_READJUDICATION_401_500_v0.1.csv")
    assert len(rows) == 100
    assert [r["projection_rule_id"] for r in rows] == [f"P01-{i:03d}" for i in range(401, 501)]
    assert sum(r["canonical_promotion"] == "true" for r in rows) == 82
    assert sum(r["canonical_promotion"] == "false" for r in rows) == 18
    assert sum(r["case_support_only"] == "true" for r in rows if r["canonical_promotion"] == "true") == 11
    by = {r["projection_rule_id"]: r for r in rows}
    for i in range(401, 419):
        r = by[f"P01-{i:03d}"]
        assert r["source_location"].endswith("p14")
        assert r["disposition"] == "DEDUPLICATED_TO_EXISTING_CANONICAL"
        assert r["canonical_promotion"] == "false"
    assert by["P01-419"]["source_location"].endswith("p15")
    assert by["P01-494"]["source_location"].endswith("p16")
    assert "p16–p17" in by["P01-500"]["source_location"]
    assert by["P01-452"]["opposite_palace_dependency"] == "武曲"
    assert by["P01-441"]["cross_palace_dependency"] == "身宫"
    assert by["P01-442"]["cross_palace_dependency"] == "身宫"
    assert "空曜、天刑" in by["P01-454"]["canonical_condition"]
    assert by["P01-454"]["projection_target"] == "upright_conduct"
    assert "寅午戌年生人" in by["P01-482"]["source_literal_claim"]


def test_p01_source_time_scope_is_not_narrowed():
    data = _json("LIFE_P05_SOURCE_TIME_SCOPE_401_500_v0.1.json")
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    assert len(rows) == 100
    for k in ("P01-424", "P01-425", "P01-426", "P01-427", "P01-487", "P01-488", "P01-489", "P01-490", "P01-491", "P01-492"):
        assert rows[k]["source_time_layers"] == ["DECADE", "YEAR"]
        assert rows[k]["scope_status"] == "SOURCE_EXPLICIT_DECADE_AND_YEAR"
    assert rows["P01-448"]["source_time_layers"] == []
    assert rows["P01-449"]["source_time_layers"] == []
    assert rows["P01-448"]["scope_status"] == "SOURCE_TEMPORAL_LAYER_UNSPECIFIED"
    assert rows["P01-494"]["source_time_layers"] == []
    assert rows["P01-494"]["scope_status"] == "SOURCE_GENERIC_YEAR_PERIOD_NOT_NARROWED"
    assert rows["P01-493"]["source_time_layers"] == ["YEAR"]
    assert rows["P01-467"]["scope_status"] == "SOURCE_LIFE_STAGE_SEQUENCE_NOT_NEW_TIME_PRIMITIVE"
    assert rows["P01-475"]["scope_status"] == "SOURCE_LIFE_STAGE_SEQUENCE_NOT_NEW_TIME_PRIMITIVE"


def test_p01_gap_supplements_and_temporal_scope():
    rows = _csv("LIFE_P05_SOURCE_GAP_SUPPLEMENT_PP15_16_v0.1.csv")
    assert len(rows) == 15
    assert [r["projection_rule_id"] for r in rows] == [f"P01-SG-{i:03d}" for i in range(153, 168)]
    assert set(r["source_gap_id"] for r in rows) == {"P01-SRC-GAP-025"}
    assert sum(r["case_support_only"] == "true" for r in rows) == 7
    ts = {r["projection_rule_id"]: r for r in _json("LIFE_P05_SOURCE_GAP_TIME_SCOPE_PP15_16_v0.1.json")["records"]}
    assert len(ts) == 15
    for k in ("P01-SG-154", "P01-SG-155", "P01-SG-156", "P01-SG-157"):
        assert ts[k]["source_time_layers"] == []
        assert ts[k]["scope_status"] == "SOURCE_TEMPORAL_LAYER_UNSPECIFIED"
    for k in ("P01-SG-162", "P01-SG-163", "P01-SG-164", "P01-SG-165"):
        assert ts[k]["source_time_layers"] == ["DECADE", "YEAR"]
    assert ts["P01-SG-167"]["source_time_layers"] == ["YEAR"]
    by = {r["projection_rule_id"]: r for r in rows}
    for k in ("P01-SG-158", "P01-SG-159", "P01-SG-160", "P01-SG-161", "P01-SG-162", "P01-SG-163", "P01-SG-164", "P01-SG-165"):
        assert "己亥太阴" in by[k]["source_text_uncertainty"] or "己亥太阴" in by[k]["canonical_condition"]


def test_p01_gap_ledger_and_cumulative_counts():
    ledger = _json("LIFE_P03_SOURCE_GAP_LEDGER_v0.1.json")
    entries = {g["gap_id"]: g for g in ledger["entries"]}
    assert entries["P01-SRC-GAP-025"]["status"] == "CLOSED_BY_SOURCE_RECHECK_AND_CANONICAL_RULES"
    assert len(entries["P01-SRC-GAP-025"]["rule_ids"]) == 91
    assert ledger["unresolved_gap_ids"] == []
    assert entries["P01-SRC-GAP-028"]["status"] == "CLOSED_BY_SOURCE_RECHECK_AND_CANONICAL_RULES"
    assert len(entries["P01-SRC-GAP-028"]["rule_ids"]) == 51
    assert ledger["next_checkpoint_gaps"] == []
    assert "P01 source audit complete through printed p24" in ledger["next_source_anchor"]
    s = _json("LIFE_P05_SOURCE_READJUDICATION_SUMMARY_v0.1.json")["summary"]
    assert s["historical_candidates_reviewed"] == 100
    assert s["canonical_promoted"] == 82
    assert s["deduplicated_scope_metadata_rows"] == 18
    assert s["new_source_gap_supplement_records"] == 15
    assert s["new_canonical_records"] == 97
    assert (s["reusable_projection_rules"], s["case_support_only"]) == (79, 18)
    assert (s["cumulative_canonical_records_after_merge"], s["cumulative_reusable_projection_rules_after_merge"], s["cumulative_case_support_only_after_merge"]) == (647, 530, 117)
    assert s["new_primitive_qi"] == s["new_memory_type"] == s["new_independent_time_scale"] == 0
    assert s["numeric_weight"] == s["probability"] == s["decay"] == 0


def test_p01_next_source_anchor_uses_canonical_p01_ids():
    review = (BASE / "LIFE_P06_SOURCE_READJUDICATION_501_600_v0.1.md").read_text(encoding="utf-8")
    state = (ROOT / "knowledge/states/P01_LIFE_STATE.yaml").read_text(encoding="utf-8")
    assert "Source-first readjudication P01-501…P01-600" in review
    assert "Canonical IDs assigned after source recheck: `P01-501…P01-600`" in review
    assert "Historical acceleration inputs: `validation/wp05/P06_life_palace_projection_review_part1_v0.1.csv`" in review
    assert "P01-701…P01-751" in state
