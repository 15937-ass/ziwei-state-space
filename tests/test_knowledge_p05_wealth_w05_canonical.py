import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READJ = ROOT / "knowledge/palaces/P05_wealth/w05/WEALTH_W05_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P05_wealth/w05/WEALTH_W05_SOURCE_TIME_SCOPE_v0.1.json"
GAPS = ROOT / "knowledge/palaces/P05_wealth/w05/WEALTH_W05_SOURCE_GAPS_v0.1.json"

EXPECTED_IDS = {f"W05-{i:03d}" for i in range(401, 501)}
EXPECTED_PATH = {"W05-403", "W05-410", "W05-411", "W05-414", "W05-416", "W05-429", "W05-434"}
EXPECTED_VISUAL = {"W05-406", "W05-411", "W05-422", "W05-450", "W05-452", "W05-461", "W05-466", "W05-467", "W05-468", "W05-478", "W05-480", "W05-500"}
EXPECTED_GAPS = {"W05-SG-001", "W05-SG-002", "W05-SG-003"}
FORBIDDEN_KEYS = {"weight", "probability", "decay", "threshold", "half_life", "persistence_parameter", "frequency_parameter"}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_w05_exact_100_unique_and_source_basis():
    data = load(READJ)
    ids = [r["projection_rule_id"] for r in data["records"]]
    assert len(ids) == 100
    assert len(set(ids)) == 100
    assert set(ids) == EXPECTED_IDS
    assert data["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert data["source_basis"]["printed_pages"] == "79-81"
    assert data["source_basis"]["archived_candidate_status"] == "NONCANONICAL_ACCELERATION_INPUT_ONLY"

def test_w05_all_rows_directly_rechecked_and_promoted():
    records = load(READJ)["records"]
    assert all(r["disposition"] in {"DIRECT_SOURCE_RECHECK_CONFIRMED", "DIRECT_SOURCE_RECHECK_REVISED"} for r in records)
    assert all(r["canonical_promotion"] is True for r in records)
    assert all(r["case_support_only"] is False for r in records)
    assert all(r["palace_id"] == "P05" and r["source_id"] == "SRC-ZZ-003" for r in records)
    assert all(r["source_uncertainty"] is None for r in records)

def test_w05_change_ledger_matches_record_flags():
    data = load(READJ)
    actual = {r["projection_rule_id"] for r in data["records"] if r["source_resolution_changed"]}
    assert actual == set(data["summary"]["source_resolution_changed_rows"])
    assert len(actual) == data["summary"]["source_resolution_change_count"]

def test_w05_visual_resolution_is_explicit_and_coverage_gaps_are_local():
    data = load(READJ)
    visual = {r["projection_rule_id"] for r in data["records"] if r["visual_source_resolution"]}
    assert visual == EXPECTED_VISUAL
    gaps = load(GAPS)
    assert gaps["gap_count"] == 3
    assert gaps["core_gap_count"] == 0
    assert {g["gap_id"] for g in gaps["gaps"]} == EXPECTED_GAPS
    assert all(g["status"] == "OPEN" and g["core_gap"] is False for g in gaps["gaps"])
    assert {x["projection_rule_id"] for x in gaps["resolved_extraction_surfaces"]} == EXPECTED_VISUAL
    assert "是非词讼" in next(g for g in gaps["gaps"] if g["gap_id"] == "W05-SG-002")["image_resolution"]

def test_w05_time_scope_and_ordered_paths_are_preserved():
    data = load(READJ)
    assert all(r["time_layer"] == "NATAL" for r in data["records"])
    paths = {r["projection_rule_id"] for r in data["records"] if r["history_feedback"] == "PATH_DEPENDENT_GATE"}
    assert paths == EXPECTED_PATH
    sidecar = load(TIME)
    assert sidecar["counts"]["non_natal_rows"] == 0
    assert sidecar["counts"]["year"] == 0
    assert sidecar["counts"]["decade"] == 0
    assert sidecar["counts"]["path_dependent_gate_rows"] == 7
    assert set(sidecar["path_dependent_gate_ids"]) == EXPECTED_PATH
    assert sidecar["source_age_qualifier_ids"] == ["W05-420"]
    assert sidecar["dependent_outcome_ids"] == ["W05-412"]
    assert all(r["no_numeric_generalization"] is True for r in sidecar["path_records"])
    assert "五十岁后" in sidecar["source_age_qualifier_records"][0]["source_phrase"]

def test_w05_critical_cross_palace_and_temporal_antecedents():
    r = {x["projection_rule_id"]: x for x in load(READJ)["records"]}
    assert "不宜经商" in r["W05-401"]["source_note"]
    assert "更不宜投机" in r["W05-402"]["source_note"]
    assert "破军同时化禄" in r["W05-403"]["canonical_condition"]
    assert "命宫有火铃" in r["W05-408"]["canonical_condition"]
    assert "禄马" not in r["W05-408"]["canonical_condition"]
    assert "东山复起" in r["W05-412"]["source_note"] and r["W05-412"]["canonical_target"] == "eventual_wealth_after_comeback"
    assert "中年辛苦求财" in r["W05-414"]["source_note"]
    assert "至身无一文" in r["W05-416"]["source_note"]
    assert "五十岁后" in r["W05-420"]["source_note"]
    assert "太阴不化禄" in r["W05-431"]["canonical_condition"]
    assert "太阴不化禄" in r["W05-432"]["canonical_condition"]
    assert "天马" in r["W05-433"]["canonical_condition"] and "事业宫" in r["W05-433"]["source_note"]
    assert "少年飘流" in r["W05-434"]["source_note"]
    assert "天同化忌或太阴化忌" in r["W05-437"]["canonical_condition"]
    assert "或对面福德宫有禄马" in r["W05-454"]["canonical_condition"]
    assert "不主商业贸迁" in r["W05-454"]["canonical_condition"]
    assert "事业宫巨门必同时化忌" in r["W05-460"]["canonical_condition"]
    assert "羊陀夹" in r["W05-462"]["canonical_condition"] and "福德宫见桃花" in r["W05-462"]["canonical_condition"]
    assert "无桃花而昌曲化忌" in r["W05-463"]["canonical_condition"]
    assert "命宫机巨叠禄" in r["W05-473"]["canonical_condition"]
    assert "不关财帛宫星曜" in r["W05-473"]["source_note"]
    assert "命宫必同时见巨门化忌" in r["W05-477"]["canonical_condition"]
    assert "廉贞与禄存同度" in r["W05-483"]["canonical_condition"]
    assert "廉贞与禄存同度" in r["W05-484"]["canonical_condition"]
    assert "火星、擎羊同度" in r["W05-488"]["canonical_condition"]
    assert "大耗、阴煞" in r["W05-498"]["canonical_condition"]
    assert "天姚" not in r["W05-498"]["canonical_condition"]
    assert "厚报" in r["W05-500"]["visual_source_resolution"]

def test_w05_source_gaps_are_not_misrepresented_as_core_gaps():
    gaps = load(GAPS)
    assert gaps["core_gap_count"] == 0
    assert all(g["gap_type"] == "OPEN_LOCAL_SOURCE_COVERAGE_GAP" for g in gaps["gaps"])
    assert all("do not invent" in g["action"].lower() or "no new projection ID" in g["action"].lower() for g in gaps["gaps"])

def test_w05_no_numeric_model_parameters_introduced():
    data = load(READJ)
    def walk(obj):
        if isinstance(obj, dict):
            assert not (FORBIDDEN_KEYS & set(obj.keys()))
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)
    walk(data["records"])
