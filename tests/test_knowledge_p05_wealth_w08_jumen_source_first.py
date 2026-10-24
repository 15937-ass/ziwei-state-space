import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "palaces" / "P05_wealth" / "w08"
READJ = BASE / "WEALTH_W08_SOURCE_READJUDICATION_701_742_v0.1.json"
TIME = BASE / "WEALTH_W08_SOURCE_TIME_SCOPE_701_742_v0.1.json"
GAPS = BASE / "WEALTH_W08_SOURCE_GAPS_701_742_v0.1.json"
STATE = ROOT / "knowledge" / "states" / "P05_WEALTH_STATE.yaml"
SUMMARY = BASE / "WEALTH_W08_CANONICAL_SUMMARY_701_742_v0.1.md"
W05_GAP_LEDGER = ROOT / "knowledge" / "palaces" / "P05_wealth" / "w05" / "WEALTH_W05_SOURCE_GAP_CLOSURE_LEDGER_v0.1.json"

EXPECTED_IDS = {f"W08-{i}" for i in range(701, 743)}
EXPECTED_PATH_IDS = {"W08-720", "W08-721", "W08-723", "W08-725"}
EXPECTED_REVISED_IDS = {"W08-704", "W08-709", "W08-711", "W08-712", "W08-714", "W08-717", "W08-726", "W08-728", "W08-729", "W08-733", "W08-734", "W08-735", "W08-736", "W08-738", "W08-739", "W08-740"}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_w08_exact_candidate_census_and_source_boundary():
    data = load(READJ)
    rows = data["records"]
    ids = [r["projection_rule_id"] for r in rows]
    assert len(rows) == 42
    assert len(ids) == len(set(ids))
    assert set(ids) == EXPECTED_IDS
    assert data["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert data["source_basis"]["printed_pages"] == "86–87"
    assert data["source_basis"]["sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert "10 巨门" in data["source_basis"]["note"]
    assert "11 天相" in data["source_basis"]["note"]
    assert data["candidate_inputs"]["historical_candidates_reviewed"] == 42
    assert data["candidate_inputs"]["candidate_file"] == "validation/wp05/W08_wealth_projection_review_701_800.csv"
    assert all(r["source_span_verified"] is True for r in rows)
    assert all(r["canonical_promotion"] is True for r in rows)
    assert all(r["case_support_only"] is False for r in rows)
    assert all(r["time_layer"] == "NATAL" for r in rows)
    assert all("11 天相" not in r["source_digest"] for r in rows)

def test_w08_source_condition_corrections_are_explicit():
    data = load(READJ)
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    assert {r["projection_rule_id"] for r in data["records"] if r["source_resolution_changed"]} == EXPECTED_REVISED_IDS
    assert all(rows[r]["disposition"] == "DIRECT_SOURCE_RECHECK_REVISED" for r in EXPECTED_REVISED_IDS)
    assert "否则" in rows["W08-704"]["source_digest"]
    assert "否则" in rows["W08-704"]["canonical_condition"]
    assert "刑耗煞曜" in rows["W08-709"]["canonical_condition"]
    assert all(x in rows["W08-709"]["canonical_condition"] for x in ["阴煞", "大耗", "天虚", "破碎", "蜚廉"])
    assert "太阳化忌" in rows["W08-711"]["canonical_condition"]
    assert "会巨门" not in rows["W08-711"]["canonical_condition"]
    assert "太阳化忌" in rows["W08-712"]["canonical_condition"] and "天刑" in rows["W08-712"]["canonical_condition"]
    assert "（A）" in rows["W08-717"]["canonical_condition"] and "（B）" in rows["W08-717"]["canonical_condition"]
    assert "化禄、化忌皆然" in rows["W08-726"]["canonical_condition"]
    assert "不额外要求前句的煞曜同度" in rows["W08-728"]["canonical_condition"]
    assert "禄存同度" in rows["W08-729"]["canonical_condition"] and "刑耗" in rows["W08-729"]["canonical_condition"]
    assert "与煞曜同度" in rows["W08-733"]["canonical_condition"]
    assert "辰戌巨门与煞曜同度" in rows["W08-734"]["canonical_condition"]
    assert "辰戌宫巨门化忌" in rows["W08-735"]["canonical_condition"]
    assert "辰宫巨门化忌" not in rows["W08-735"]["canonical_condition"]
    assert "独坐" in rows["W08-736"]["canonical_condition"]
    assert "巳亥" not in rows["W08-738"]["canonical_condition"]
    assert "巳亥" not in rows["W08-739"]["canonical_condition"]
    assert "及" in rows["W08-740"]["canonical_condition"] and "或" not in rows["W08-740"]["canonical_condition"]

def test_w08_temporal_scope_preserves_only_source_ordered_paths():
    data = load(READJ)
    sidecar = load(TIME)
    assert sidecar["counts"] == {"non_natal_rows": 0, "year": 0, "decade": 0, "path_dependent_gate_rows": 4, "source_age_qualifier_rows": 2}
    assert sidecar["exact_non_natal_ids"] == []
    assert sidecar["decade_ids"] == []
    assert sidecar["year_ids"] == []
    assert set(sidecar["path_dependent_gate_ids"]) == EXPECTED_PATH_IDS
    assert {r["projection_rule_id"] for r in sidecar["path_records"]} == EXPECTED_PATH_IDS
    assert sidecar["source_age_qualifier_ids"] == ["W08-719", "W08-720"]
    assert [r["literal_qualifier"] for r in sidecar["source_age_qualifier_records"]] == ["中年后", "早年必受艰辛"]
    assert all(r["time_layer"] == "NATAL" and r["no_numeric_generalization"] is True for r in sidecar["path_records"])
    source_rows = {r["projection_rule_id"]: r for r in load(READJ)["records"]}
    assert all(p["canonical_condition"] == source_rows[p["projection_rule_id"]]["canonical_condition"] for p in sidecar["path_records"])
    assert all(p["canonical_target"] == source_rows[p["projection_rule_id"]]["canonical_target"] for p in sidecar["path_records"])

def test_w08_gap_census_and_prior_gaps_are_carried_forward():
    data = load(GAPS)
    assert data["gap_count"] == 0
    assert data["core_gap_count"] == 0
    assert data["gaps"] == []
    assert data["summary"]["new_local_source_ambiguities"] == 0
    expected_prior = {"W05-SG-002", "W06-SG-001", "W06-SG-002", "W06-SG-003", "W06-SG-004", "W06-SG-005"}
    assert set(data["summary"]["unresolved_prior_gap_ids"]) == expected_prior
    ledger = load(W05_GAP_LEDGER)
    prior = next(g for g in ledger["entries"] if g["gap_id"] == "W05-SG-002")
    assert prior["status"] == "PARTIALLY_RESOLVED"
    state = STATE.read_text(encoding="utf-8")
    assert "merged_rule_count: 642" in state
    assert "current_batch_rule_count: 42" in state
    assert "source_resolution_change_count_current_batch: 16" in state
    assert "source_uncertainty_count_current_batch: 0" in state
    assert "path_dependent_gate_count_current_batch: 4" in state
    assert "source_coverage_gap_count_current_batch: 0" in state
    assert "source_coverage_gaps_remaining: 6" in state
    assert "W05-SG-002" in state and "PARTIALLY_RESOLVED" in state
    assert all(f"W06-SG-00{i}" in state for i in range(1,6))
    assert "11 天相" in state
    summary = SUMMARY.read_text(encoding="utf-8")
    assert "Issue #738" in summary and "W08-701…W08-742" in summary
    assert "source_resolution_change_count_current_batch: 16" in summary
    assert "下一来源锚点" in summary and "11 天相" in summary

def test_w08_no_forbidden_model_parameters_or_product_authorization():
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
    state = STATE.read_text(encoding="utf-8")
    assert "No Product/runtime authorization is implied" in state
