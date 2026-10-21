import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READJ = ROOT / "knowledge/palaces/P05_wealth/w04/WEALTH_W04_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P05_wealth/w04/WEALTH_W04_SOURCE_TIME_SCOPE_v0.1.json"
GAPS = ROOT / "knowledge/palaces/P05_wealth/w04/WEALTH_W04_SOURCE_GAPS_v0.1.json"

EXPECTED_IDS = {f"W04-{i:03d}" for i in range(301, 401)}
EXPECTED_NON_NATAL = {"W04-306", "W04-307", "W04-336", "W04-354", "W04-355", "W04-364", "W04-365"}
EXPECTED_PATH = {"W04-318", "W04-319", "W04-388", "W04-394", "W04-400"}
EXPECTED_VISUAL = {"W04-338", "W04-340", "W04-353", "W04-354", "W04-355", "W04-358", "W04-359", "W04-360", "W04-389", "W04-397", "W04-398", "W04-400"}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_w04_exact_100_and_unique():
    data = load(READJ)
    records = data["records"]
    ids = [r["projection_rule_id"] for r in records]
    assert len(records) == 100
    assert len(ids) == len(set(ids))
    assert set(ids) == EXPECTED_IDS
    assert data["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert data["source_basis"]["printed_pages"] == "76-79"

def test_w04_all_rows_source_rechecked_and_promoted():
    records = load(READJ)["records"]
    assert all(r["disposition"] in {"DIRECT_SOURCE_RECHECK_CONFIRMED", "DIRECT_SOURCE_RECHECK_REVISED"} for r in records)
    assert all(r["canonical_promotion"] is True for r in records)
    assert all(r["case_support_only"] is False for r in records)
    assert all(r["palace_id"] == "P05" for r in records)
    assert all(r["source_uncertainty"] is None for r in records)

def test_w04_visual_resolution_is_explicit_and_no_open_gap():
    records = load(READJ)["records"]
    visual = {r["projection_rule_id"] for r in records if r["visual_source_resolution"]}
    assert visual == EXPECTED_VISUAL
    gaps = load(GAPS)
    assert gaps["gap_count"] == 0
    assert gaps["core_gap_count"] == 0
    assert gaps["gaps"] == []
    assert {x["projection_rule_id"] for x in gaps["resolved_extraction_surfaces"]} == EXPECTED_VISUAL

def test_w04_time_scope_and_path_gates():
    records = load(READJ)["records"]
    non_natal = {r["projection_rule_id"] for r in records if r["time_layer"] != "NATAL"}
    path = {r["projection_rule_id"] for r in records if r["history_feedback"] == "PATH_DEPENDENT_GATE"}
    assert non_natal == EXPECTED_NON_NATAL
    assert path == EXPECTED_PATH
    sidecar = load(TIME)
    assert set(sidecar["exact_non_natal_ids"]) == EXPECTED_NON_NATAL
    assert sidecar["counts"]["decade"] == 3
    assert sidecar["counts"]["year"] == 4
    assert set(sidecar["path_dependent_gate_ids"]) == EXPECTED_PATH
    assert all(r["no_numeric_generalization"] is True for r in sidecar["records"])

def test_w04_critical_source_dependencies_are_frozen():
    r = {x["projection_rule_id"]: x for x in load(READJ)["records"]}
    assert "太阳必同时化权" in r["W04-303"]["canonical_condition"]
    assert "流年" in r["W04-307"]["canonical_condition"]
    assert "太阳化忌" in r["W04-315"]["canonical_condition"]
    assert "太阳化忌" in r["W04-316"]["canonical_condition"]
    assert "日生人尤甚" in r["W04-323"]["canonical_condition"]
    assert "父荫" in r["W04-330"]["source_note"]
    assert "事业宫必见禄存" in r["W04-359"]["canonical_condition"]
    assert "事业宫廉贞叠禄" in r["W04-360"]["canonical_condition"]
    assert "天刑" in r["W04-343"]["canonical_condition"]
    assert "龙池凤阁" in r["W04-347"]["canonical_condition"]
    assert "无煞曜同宫" in r["W04-348"]["canonical_condition"]
    assert "流煞冲起" in r["W04-354"]["canonical_condition"]
    assert "流煞冲起" in r["W04-355"]["canonical_condition"]
    assert "偏财" not in r["W04-368"]["canonical_target"] or "side" in r["W04-368"]["canonical_target"]
    assert "文曲化忌" in r["W04-376"]["canonical_condition"]
    assert "破军化权" in r["W04-378"]["canonical_condition"]
    assert "兄弟或友人" in r["W04-381"]["source_note"]
    assert "化禄或禄存" in r["W04-389"]["canonical_condition"]
    assert "禄存在命宫" in r["W04-397"]["canonical_condition"]
    assert "至少有一次困境" in r["W04-400"]["source_note"]

def test_w04_no_numeric_model_parameters_introduced():
    data = load(READJ)
    forbidden = {"weight", "probability", "decay", "threshold", "half_life", "persistence_parameter", "frequency_parameter"}
    def walk(obj):
        if isinstance(obj, dict):
            assert not (forbidden & set(obj.keys()))
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)
    walk(data["records"])
