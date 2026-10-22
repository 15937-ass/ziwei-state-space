import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READJ = ROOT / "knowledge/palaces/P05_wealth/w05/WEALTH_W05_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P05_wealth/w05/WEALTH_W05_SOURCE_TIME_SCOPE_v0.1.json"
GAPS = ROOT / "knowledge/palaces/P05_wealth/w05/WEALTH_W05_SOURCE_GAPS_v0.1.json"

EXPECTED_IDS = {f"W05-{i:03d}" for i in range(401, 501)}
EXPECTED_PATH = ["W05-403","W05-410","W05-411","W05-412","W05-413","W05-414","W05-416","W05-417","W05-429","W05-434"]
EXPECTED_CHANGED = ["W05-408","W05-412","W05-413","W05-417","W05-431","W05-432","W05-437","W05-454","W05-460","W05-462","W05-463","W05-474","W05-477","W05-486","W05-487","W05-488","W05-489","W05-490","W05-497","W05-498"]
EXPECTED_VISUAL = ["W05-403","W05-407","W05-408","W05-410","W05-411","W05-416","W05-431","W05-432","W05-447","W05-454","W05-460","W05-462","W05-463","W05-470","W05-471","W05-474","W05-475","W05-477","W05-481","W05-482","W05-486","W05-487","W05-488","W05-489","W05-490","W05-497","W05-498","W05-499","W05-500"]

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_w05_exact_100_and_unique():
    data = load(READJ)
    records = data["records"]
    ids = [r["projection_rule_id"] for r in records]
    assert len(records) == 100
    assert len(ids) == len(set(ids))
    assert set(ids) == EXPECTED_IDS
    assert data["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert data["source_basis"]["printed_pages"] == "79-81"

def test_w05_all_rows_source_rechecked_and_promoted():
    records = load(READJ)["records"]
    assert all(r["disposition"] in {"DIRECT_SOURCE_RECHECK_CONFIRMED", "DIRECT_SOURCE_RECHECK_REVISED"} for r in records)
    assert all(r["canonical_promotion"] is True for r in records)
    assert all(r["case_support_only"] is False for r in records)
    assert all(r["palace_id"] == "P05" for r in records)
    assert all(r["source_uncertainty"] is None for r in records)
    assert {r["projection_rule_id"] for r in records if r["source_resolution_changed"]} == set(EXPECTED_CHANGED)

def test_w05_visual_resolution_and_coverage_gap_are_explicit():
    records = load(READJ)["records"]
    visual = {r["projection_rule_id"] for r in records if r["visual_source_resolution"]}
    assert visual == set(EXPECTED_VISUAL)
    gaps = load(GAPS)
    assert gaps["gap_count"] == 0
    assert gaps["core_gap_count"] == 0
    assert gaps["gaps"] == []
    assert {x["projection_rule_id"] for x in gaps["resolved_extraction_surfaces"]} == set(EXPECTED_VISUAL)
    assert gaps["source_coverage_gap_count"] == 1
    assert gaps["source_coverage_gaps"][0]["source_uncertainty"] is None
    assert "命宫必同时见巨门化忌" in gaps["source_coverage_gaps"][0]["source_text"]

def test_w05_time_scope_and_path_gates():
    records = load(READJ)["records"]
    assert all(r["time_layer"] == "NATAL" for r in records)
    path = {r["projection_rule_id"] for r in records if r["history_feedback"] == "PATH_DEPENDENT_GATE"}
    assert path == set(EXPECTED_PATH)
    sidecar = load(TIME)
    assert sidecar["counts"]["non_natal_rows"] == 0
    assert sidecar["counts"]["year"] == 0
    assert sidecar["counts"]["decade"] == 0
    assert sidecar["exact_non_natal_ids"] == []
    assert set(sidecar["path_dependent_gate_ids"]) == set(EXPECTED_PATH)
    assert all(r["no_numeric_generalization"] is True for r in sidecar["records"])

def test_w05_critical_antecedents_are_frozen():
    r = {x["projection_rule_id"]: x for x in load(READJ)["records"]}
    assert "贪狼化忌" in r["W05-403"]["canonical_condition"]
    assert "破军化禄" in r["W05-403"]["canonical_condition"]
    assert "命宫有火铃" in r["W05-408"]["canonical_condition"]
    assert "空劫同度" in r["W05-411"]["canonical_condition"]
    assert "五十岁后" in r["W05-420"]["source_note"]
    assert "唯太阴化禄者不是" in r["W05-431"]["source_note"]
    assert "唯太阴化禄者不是" in r["W05-432"]["source_note"]
    assert "事业宫见天马" in r["W05-433"]["canonical_condition"]
    assert "不主商业贸迁" in r["W05-454"]["source_note"]
    assert "事业宫巨门必同时化忌" in r["W05-460"]["canonical_condition"]
    assert "无桃花" in r["W05-463"]["canonical_condition"]
    assert "只宜服务他人" in r["W05-470"]["source_note"]
    assert "自行经营" in r["W05-471"]["canonical_condition"]
    assert "名大于利" in r["W05-474"]["source_note"]
    assert "文曲化忌" in r["W05-475"]["canonical_condition"]
    assert "不宜经商" in r["W05-477"]["source_note"]
    assert r["W05-477"]["canonical_target"] == "business_not_recommended_under_tiantong_huaquan"
    assert "禄存同度" in r["W05-486"]["canonical_condition"]
    assert "火星、擎羊" in r["W05-487"]["canonical_condition"]
    assert "空劫、大耗" in r["W05-497"]["canonical_condition"]
    assert "天姚、阴煞" in r["W05-498"]["canonical_condition"]
    assert "财荫夹印" in r["W05-500"]["canonical_condition"]

def test_w05_no_numeric_model_parameters():
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
