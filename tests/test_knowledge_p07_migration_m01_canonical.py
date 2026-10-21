import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/M01_migration_projection_review_001_100.csv"
READJ = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_TIME_SCOPE_v0.1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def candidate_rows():
    with CANDIDATE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def test_candidate_census_is_exactly_100_and_read_only_basis():
    rows = candidate_rows()
    assert len(rows) == 100
    assert len({r["projection_rule_id"] for r in rows}) == 100
    assert rows[0]["projection_rule_id"] == "M01-001"
    assert rows[-1]["projection_rule_id"] == "M01-100"
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert all(r["palace_id"] == "P07" for r in rows)
    assert all(r["source_span_verified"] == "true" for r in rows)

def test_case_and_history_counts_are_reconfirmed():
    rows = candidate_rows()
    assert sum(r["case_support_only"] == "true" for r in rows) == 8
    history = {r["projection_rule_id"] for r in rows if r["history_feedback"]}
    assert history == {"M01-044", "M01-054", "M01-088", "M01-100"}

def test_readjudication_promotes_all_100_with_bounded_repairs():
    d = load(READJ)
    s = d["summary"]
    assert s["reviewed"] == 100
    assert s["canonical_promoted"] == 100
    assert s["reusable_projection_rules"] == 92
    assert s["case_support_only"] == 8
    assert s["history_feedback"] == 4
    assert s["source_resolution_changed_rows"] == ["M01-030", "M01-047", "M01-051", "M01-052", "M01-060", "M01-068"]
    assert s["source_text_uncertainty_preserved"] == ["M01-030"]
    assert s["source_scan_resolved_rows"] == ["M01-026", "M01-027", "M01-076"]
    assert len(d["records"]) == 100
    assert len({r["projection_rule_id"] for r in d["records"]}) == 100

def test_source_logic_repairs_do_not_strengthen_claims():
    d = load(READJ)
    m = {r["projection_rule_id"]: r for r in d["records"]}
    assert "羊陀裔冲" in m["M01-030"]["canonical_condition"]
    assert m["M01-047"]["canonical_projection_target"] == "decline_or_setback"
    assert m["M01-051"]["canonical_projection_target"] == "relocation_advantage_not_supported_in_this_context"
    assert m["M01-052"]["canonical_projection_target"] == "relocation_advantage_not_supported_in_this_context"
    assert m["M01-060"]["canonical_condition"] == "紫微在迁移宫再见天刑大耗天虚空劫等曜"
    assert "或" in m["M01-068"]["canonical_condition"]
    assert all(r["canonical_promotion"] is True for r in d["records"])

def test_temporal_contract_preserves_event_relative_boundary():
    d = load(TIME)
    assert d["chapter_scope"]["source_layers"] == ["NATAL", "DECADE", "YEAR", "MONTH"]
    overlay = d["event_relative_overlay"]
    assert overlay["overlay_id"] == "MIGRATION_FIRST_THREE_YEARS"
    assert overlay["human_gate"] == "HG-P07-TEMPORAL-01-A"
    assert overlay["active_year_index"] == [1, 2, 3]
    assert overlay["seventh_calendar_layer"] is False
    assert overlay["generic_event_timer"] is False
    assert d["default_star_system_records"]["runtime_eligibility_granted"] is False

def test_no_new_quantitative_or_shared_semantics():
    d = load(READJ)["summary"]
    for key in [
        "new_primitive_qi",
        "new_memory_type",
        "new_independent_time_scale",
        "new_shared_group_semantics",
        "numeric_weight",
        "probability",
        "decay",
    ]:
        assert d[key] == 0
