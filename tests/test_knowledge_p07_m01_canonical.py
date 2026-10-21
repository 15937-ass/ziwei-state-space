import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M01_CANONICAL_001_100.csv"
READJ = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_TIME_SCOPE_v0.1.json"
STATE = ROOT / "knowledge/states/P07_MIGRATION_STATE.yaml"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def rows():
    with CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def test_m01_exact_100_unique_and_source_bound():
    r = rows()
    assert len(r) == 100
    assert len({x["projection_rule_id"] for x in r}) == 100
    assert r[0]["projection_rule_id"] == "M01-001"
    assert r[-1]["projection_rule_id"] == "M01-100"
    assert all(x["source_id"] == "SRC-ZZ-003" for x in r)
    assert all(x["palace_id"] == "P07" for x in r)
    assert all(x["source_span_verified"] == "true" for x in r)

def test_case_and_path_counts():
    r = rows()
    assert {x["projection_rule_id"] for x in r if x["case_support_only"] == "true"} == {
        "M01-048", "M01-054", "M01-063", "M01-064",
        "M01-070", "M01-071", "M01-072", "M01-086",
    }
    assert {x["projection_rule_id"] for x in r if x["history_feedback"]} == {
        "M01-044", "M01-054", "M01-088", "M01-100",
    }

def test_page_image_resolution_water_guest_not_ocr_error():
    m = {x["projection_rule_id"]: x for x in rows()}
    assert "驿夫水客" in m["M01-076"]["condition"]
    assert "水窖" not in m["M01-076"]["condition"]
    d = load_json(READJ)
    assert d["summary"]["source_image_resolution_rows"] == ["M01-076"]

def test_temporal_contract_is_bounded():
    d = load_json(TIME)
    m = {x["projection_rule_id"]: x for x in d["records"]}
    assert m["M01-001"]["source_time_layers"] == ["DECADE"]
    assert m["M01-002"]["source_time_layers"] == ["YEAR"]
    assert m["M01-003"]["source_time_layers"] == ["MONTH"]
    assert m["M01-004"]["event_relative_overlay"] == "MIGRATION_FIRST_THREE_YEARS"
    assert m["M01-004"]["overlay_human_gate"] == "HG-P07-TEMPORAL-01-A"
    assert m["M01-004"]["no_new_calendar_layer"] is True
    assert m["M01-010"]["source_time_layers"] == ["NATAL", "DECADE", "YEAR", "MONTH"]
    assert d["summary"]["generalized_event_timer"] is False

def test_movement_signal_is_not_auto_wealth():
    m = {x["projection_rule_id"]: x for x in rows()}
    assert m["M01-014"]["projection_target"] == "movement_requires_mobility_signal"
    assert m["M01-023"]["projection_target"] == "movement_signal_not_automatic_wealth_signal"

def test_path_dependencies_are_explicit():
    d = load_json(TIME)
    m = {x["projection_rule_id"]: x for x in d["records"]}
    assert "MH-001" in m["M01-044"]["dependencies"]
    assert "M01-053" in m["M01-054"]["dependencies"]
    assert "M01-087" in m["M01-088"]["dependencies"]
    assert "MH-004" in m["M01-100"]["dependencies"]

def test_no_new_quantitative_or_time_primitive():
    d = load_json(READJ)["summary"]
    for key in [
        "new_primitive_qi", "new_memory_type", "new_independent_time_scale",
        "numeric_weight", "probability", "decay",
    ]:
        assert d[key] == 0

def test_readjudication_summary():
    d = load_json(READJ)
    assert d["summary"]["reviewed"] == 100
    assert d["summary"]["canonical_promoted"] == 100
    assert d["summary"]["reusable_projection_rules"] == 92
    assert d["summary"]["case_support_only"] == 8
    assert d["summary"]["history_feedback"] == 4

def test_state_cache_points_to_post_merge_checkpoint():
    s = STATE.read_text(encoding="utf-8")
    assert 'shard: "P07"' in s
    assert 'canonical_checkpoint: "MIGRATION_M01_CANONICAL_100_OF_100_ON_MAIN_AFTER_MERGE"' in s
