import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READJ = ROOT / "knowledge/palaces/P05_wealth/w02/WEALTH_W02_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P05_wealth/w02/WEALTH_W02_SOURCE_TIME_SCOPE_v0.1.json"
GAPS = ROOT / "knowledge/palaces/P05_wealth/w02/WEALTH_W02_SOURCE_GAPS_v0.1.json"

EXPECTED_IDS = {f"W02-{i:03d}" for i in range(101, 201)}
EXPECTED_NON_NATAL = {"W02-114", "W02-115", "W02-160"}
EXPECTED_PATH = {"W02-114", "W02-115", "W02-119", "W02-143"}
EXPECTED_UNCERTAIN = {"W02-138", "W02-139"}
ALLOWED_DISPOSITIONS = {
    "DIRECT_SOURCE_RECHECK_CONFIRMED",
    "DIRECT_SOURCE_RECHECK_REVISED",
    "DIRECT_SOURCE_RECHECK_SOURCE_UNCERTAINTY",
    "DIRECT_SOURCE_RECHECK_REVISED_WITH_UNCERTAINTY",
}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_w02_exact_100_and_unique():
    data = load(READJ)
    records = data["records"]
    ids = [r["projection_rule_id"] for r in records]
    assert len(records) == 100
    assert len(ids) == len(set(ids))
    assert set(ids) == EXPECTED_IDS
    assert data["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert data["source_basis"]["printed_pages"] == "72-74"

def test_w02_all_rows_are_direct_source_rechecked():
    records = load(READJ)["records"]
    assert all(r["disposition"] in ALLOWED_DISPOSITIONS for r in records)
    assert all(r["canonical_promotion"] is True for r in records)
    assert all(r["case_support_only"] is False for r in records)
    assert all(r["palace_id"] == "P05" for r in records)

def test_w02_uncertainty_is_fail_closed():
    records = load(READJ)["records"]
    uncertain = {r["projection_rule_id"] for r in records if r["source_uncertainty"]}
    assert uncertain == EXPECTED_UNCERTAIN
    gaps = load(GAPS)
    assert gaps["gap_count"] == len(EXPECTED_UNCERTAIN)
    assert {g["projection_rule_id"] for g in gaps["gaps"]} == EXPECTED_UNCERTAIN
    assert all(g["requires_core_semantics"] is False for g in gaps["gaps"])

def test_w02_temporal_and_history_scope():
    records = load(READJ)["records"]
    non_natal = {r["projection_rule_id"] for r in records if r["time_layer"] != "NATAL"}
    path = {r["projection_rule_id"] for r in records if r["history_feedback"] == "PATH_DEPENDENT_GATE"}
    assert non_natal == EXPECTED_NON_NATAL
    assert path == EXPECTED_PATH
    sidecar = load(TIME)
    assert set(sidecar["exact_non_natal_ids"]) == EXPECTED_NON_NATAL
    assert set(sidecar["path_dependent_gate_ids"]) == EXPECTED_PATH
    assert all(r["no_numeric_generalization"] is True for r in sidecar["records"])

def test_w02_critical_source_repairs_are_frozen():
    records = {r["projection_rule_id"]: r for r in load(READJ)["records"]}
    assert "左辅右弼同会" in records["W02-105"]["canonical_condition"]
    assert records["W02-115"]["time_layer"] == "YEAR"
    assert records["W02-115"]["history_feedback"] == "PATH_DEPENDENT_GATE"
    assert "enduring" in records["W02-129"]["canonical_target"]
    assert records["W02-159"]["canonical_target"] == "financial_state_is_variable"
    assert records["W02-166"]["canonical_target"].startswith("source_attributes_")
    assert "relatively_better" in records["W02-172"]["canonical_target"]
    assert "太阴入庙" in records["W02-192"]["canonical_condition"]
    assert records["W02-194"]["canonical_target"] == "open_mindedness_and_avoidance_of_scheming_as_remedial_guidance"

def test_w02_does_not_create_flank_semantics_from_ocr_surface():
    records = {r["projection_rule_id"]: r for r in load(READJ)["records"]}
    for rid in ("W02-138", "W02-139"):
        assert records[rid]["source_uncertainty"]
        assert "primitive" in records[rid]["source_note"]

def test_w02_no_numeric_model_parameters_introduced():
    data = load(READJ)
    forbidden = {
        "weight", "probability", "decay", "threshold", "half_life",
        "persistence_parameter", "frequency_parameter"
    }
    def walk(obj):
        if isinstance(obj, dict):
            assert not (forbidden & set(obj.keys()))
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
    walk(data["records"])
