import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READJ = ROOT / "knowledge/palaces/P05_wealth/w03/WEALTH_W03_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P05_wealth/w03/WEALTH_W03_SOURCE_TIME_SCOPE_v0.1.json"
GAPS = ROOT / "knowledge/palaces/P05_wealth/w03/WEALTH_W03_SOURCE_GAPS_v0.1.json"

EXPECTED_IDS = {f"W03-{i:03d}" for i in range(201, 301)}
EXPECTED_PATH = {"W03-207", "W03-278"}
EXPECTED_VISUAL = {"W03-206", "W03-215", "W03-269", "W03-271", "W03-273"}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_w03_exact_100_and_unique():
    data = load(READJ)
    records = data["records"]
    ids = [r["projection_rule_id"] for r in records]
    assert len(records) == 100
    assert len(ids) == len(set(ids))
    assert set(ids) == EXPECTED_IDS
    assert data["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert data["source_basis"]["printed_pages"] == "74-76"

def test_w03_all_rows_source_rechecked_and_promoted():
    records = load(READJ)["records"]
    assert all(r["disposition"] in {"DIRECT_SOURCE_RECHECK_CONFIRMED", "DIRECT_SOURCE_RECHECK_REVISED"} for r in records)
    assert all(r["canonical_promotion"] is True for r in records)
    assert all(r["case_support_only"] is False for r in records)
    assert all(r["palace_id"] == "P05" for r in records)
    assert all(r["source_uncertainty"] is None for r in records)

def test_w03_visual_resolution_is_explicit_and_no_open_gap():
    records = load(READJ)["records"]
    visual = {r["projection_rule_id"] for r in records if r["visual_source_resolution"]}
    assert visual == EXPECTED_VISUAL
    gaps = load(GAPS)
    assert gaps["gap_count"] == 0
    assert gaps["core_gap_count"] == 0
    assert gaps["gaps"] == []
    assert {x["projection_rule_id"] for x in gaps["resolved_extraction_surfaces"]} == EXPECTED_VISUAL

def test_w03_time_and_path_scope():
    records = load(READJ)["records"]
    assert {r["projection_rule_id"] for r in records if r["time_layer"] != "NATAL"} == set()
    path = {r["projection_rule_id"] for r in records if r["history_feedback"] == "PATH_DEPENDENT_GATE"}
    assert path == EXPECTED_PATH
    sidecar = load(TIME)
    assert sidecar["exact_non_natal_ids"] == []
    assert set(sidecar["path_dependent_gate_ids"]) == EXPECTED_PATH
    assert all(r["no_numeric_generalization"] is True for r in sidecar["records"])

def test_w03_critical_source_repairs_are_frozen():
    r = {x["projection_rule_id"]: x for x in load(READJ)["records"]}
    assert "落陷" in r["W03-201"]["canonical_condition"]
    assert "落陷" in r["W03-202"]["canonical_condition"]
    assert "落陷" in r["W03-203"]["canonical_condition"]
    assert "can_support" in r["W03-207"]["canonical_target"]
    assert "high_" not in r["W03-208"]["canonical_target"]
    assert "空劫" in r["W03-212"]["canonical_condition"]
    assert "ancestral" in r["W03-234"]["canonical_target"]
    assert "concurrent_jobs" in r["W03-238"]["canonical_target"]
    assert r["W03-241"]["projection_domain"] == "career"
    assert "foreign_company_broker_or_agent" in r["W03-241"]["canonical_target"]
    assert "无太阴同度" in r["W03-255"]["canonical_condition"]
    assert all(x in r["W03-263"]["canonical_condition"] for x in ("禄存", "太阴化禄", "巨门化禄"))
    assert all(x in r["W03-281"]["canonical_condition"] for x in ("辅弼", "魁钺", "昌曲", "不见煞忌"))
    assert r["W03-290"]["projection_domain"] == "acquisition"
    assert "distant" not in r["W03-290"]["canonical_target"]
    assert "不见空劫及铃星" in r["W03-295"]["canonical_condition"]

def test_w03_cross_palace_boundaries_preserved():
    r = {x["projection_rule_id"]: x for x in load(READJ)["records"]}
    assert "命宫" in r["W03-223"]["canonical_condition"]
    assert "事业宫" in r["W03-224"]["canonical_condition"]
    assert "夫妻" in r["W03-265"]["canonical_condition"]
    assert "田宅" in r["W03-266"]["canonical_condition"]

def test_w03_no_numeric_model_parameters_introduced():
    data = load(READJ)
    forbidden = {"weight", "probability", "decay", "threshold", "half_life", "persistence_parameter", "frequency_parameter"}
    def walk(obj):
        if isinstance(obj, dict):
            assert not (forbidden & set(obj.keys()))
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
    walk(data["records"])
