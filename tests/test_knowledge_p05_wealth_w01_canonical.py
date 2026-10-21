import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READJ = ROOT / "knowledge/palaces/P05_wealth/w01/WEALTH_W01_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P05_wealth/w01/WEALTH_W01_SOURCE_TIME_SCOPE_v0.1.json"
GAPS = ROOT / "knowledge/palaces/P05_wealth/w01/WEALTH_W01_SOURCE_GAPS_v0.1.json"

EXPECTED_IDS = {f"W01-{i:03d}" for i in range(1, 101)}
EXPECTED_NON_NATAL = {
    "W01-011","W01-012","W01-051","W01-052","W01-053","W01-054","W01-055",
    "W01-063","W01-084","W01-085","W01-086","W01-087","W01-088",
}
EXPECTED_UNCERTAIN = {"W01-047","W01-056","W01-069","W01-074","W01-076","W01-077"}
ALLOWED_DISPOSITIONS = {
    "DIRECT_SOURCE_RECHECK_CONFIRMED",
    "DIRECT_SOURCE_RECHECK_REVISED",
    "DIRECT_SOURCE_RECHECK_SOURCE_UNCERTAINTY",
    "DIRECT_SOURCE_RECHECK_REVISED_WITH_UNCERTAINTY",
}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_w01_exact_100_and_unique():
    data = load(READJ)
    records = data["records"]
    ids = [r["projection_rule_id"] for r in records]
    assert len(records) == 100
    assert len(ids) == len(set(ids))
    assert set(ids) == EXPECTED_IDS
    assert data["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert data["source_basis"]["chapter"] == "财帛宫"
    assert data["source_basis"]["printed_pages"] == "69-72"

def test_w01_all_rows_source_rechecked_and_promoted_without_case_leak():
    records = load(READJ)["records"]
    assert all(r["disposition"] in ALLOWED_DISPOSITIONS for r in records)
    assert all(r["canonical_promotion"] is True for r in records)
    assert all(r["case_support_only"] is False for r in records)
    assert all(r["palace_id"] == "P05" for r in records)

def test_w01_source_uncertainty_is_explicit():
    records = load(READJ)["records"]
    uncertain = {r["projection_rule_id"] for r in records if r["source_uncertainty"]}
    assert uncertain == EXPECTED_UNCERTAIN
    gaps = load(GAPS)
    assert gaps["gap_count"] == len(EXPECTED_UNCERTAIN)
    assert {g["projection_rule_id"] for g in gaps["gaps"]} == EXPECTED_UNCERTAIN
    assert all(g["requires_core_semantics"] is False for g in gaps["gaps"])

def test_w01_temporal_scope_is_not_flattened():
    data = load(READJ)
    non_natal = {r["projection_rule_id"] for r in data["records"] if r["time_layer"] != "NATAL"}
    assert non_natal == EXPECTED_NON_NATAL
    sidecar = load(TIME)
    assert set(sidecar["exact_non_natal_ids"]) == EXPECTED_NON_NATAL
    assert sidecar["temporal_guard_ids"] == ["W01-089"]
    assert sidecar["counts"]["non_natal_rows"] == len(EXPECTED_NON_NATAL)
    assert all(r["no_numeric_generalization"] is True for r in sidecar["records"])

def test_w01_critical_repairs_are_frozen():
    records = {r["projection_rule_id"]: r for r in load(READJ)["records"]}
    assert records["W01-043"]["canonical_target"] == "public_service_management_can_gain_reputation_despite_wenqu_ji"
    assert "分别见" in records["W01-050"]["canonical_condition"]
    assert "命宫或财帛宫" in records["W01-054"]["canonical_condition"]
    assert "OCR" in records["W01-056"]["canonical_condition"]
    assert "later_five_years" in records["W01-063"]["canonical_target"]
    assert records["W01-071"]["canonical_target"] == "financial_collapse_risk"
    assert "or_collapse" in records["W01-085"]["canonical_target"]

def test_w01_no_numeric_model_parameters_introduced():
    data = load(READJ)
    forbidden = {"weight","probability","decay","threshold","half_life","persistence_parameter"}
    def walk(obj):
        if isinstance(obj, dict):
            assert not (forbidden & set(obj.keys()))
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
    walk(data["records"])
