import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/SP02_spouse_projection_review_101_200.csv"
READJ = ROOT / "knowledge/palaces/P03_spouse/wp05/SPOUSE_SP02_SOURCE_READJUDICATION_100_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"
SOURCE_SHA = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_rows():
    with CANDIDATE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def by_candidate():
    return {r["historical_candidate_id"]: r for r in load(READJ)["candidate_batch"]["candidate_dispositions"]}


def records_by_id():
    return {r["projection_rule_id"]: r for r in load(READJ)["records"]}


def test_p03_sp02_candidate_inventory_source_pin_and_page_mapping():
    d = load(READJ)
    rows = candidate_rows()
    inv = d["historical_candidate_inventory"]
    src = d["source_basis"]
    assert len(rows) == 100
    assert len({r["projection_rule_id"] for r in rows}) == 100
    assert rows[0]["projection_rule_id"] == "SP02-101"
    assert rows[-1]["projection_rule_id"] == "SP02-200"
    assert inv["total_rows"] == inv["unique_ids"] == 836
    assert inv["first_id"] == "SP01-001"
    assert inv["last_id"] == "SP09-836"
    assert inv["case_support_only_flagged_total"] == 136
    assert inv["path_dependent_gate_flagged_total"] == 6
    assert all(f["role"] == "READ_ONLY_ACCELERATION_INPUT_NOT_CANONICAL" for f in inv["files"])
    assert src["source_id"] == "SRC-ZZ-003"
    assert src["attachment_sha256"] == SOURCE_SHA
    assert src["candidate_batch_verified_printed_pages"] == [35, 36, 37]
    assert src["candidate_batch_verified_pdf_physical_pages"] == [18, 19]
    assert src["page_mapping"]["35"] == src["page_mapping"]["36"] == 18
    assert src["page_mapping"]["37"] == 19


def test_exact_candidate_dispositions_and_record_counts_reconcile():
    d = load(READJ)
    rows = candidate_rows()
    disp = d["candidate_batch"]["candidate_dispositions"]
    assert len(disp) == 100
    assert [x["historical_candidate_id"] for x in disp] == [r["projection_rule_id"] for r in rows]
    assert all(x["reason"] for x in disp)
    summary = d["summary"]
    records = d["records"]
    assert summary["reviewed"] == 100
    assert summary["canonical_promoted"] == 77
    assert summary["canonical_record_count"] == len(records) == 79
    assert len({r["projection_rule_id"] for r in records}) == 79
    assert summary["reusable_projection_rules"] == 60
    assert summary["case_support_only"] == 19
    assert summary["held"] == 23
    assert summary["deduplicated"] == 0
    assert all(r["canonical_promotion"] is True for r in records)
    assert sum(r["case_support_only"] is True for r in records) == 19
    assert sum(r["case_support_only"] is False for r in records) == 60
    known = {r["projection_rule_id"] for r in records}
    for row in disp:
        assert set(row["canonical_record_ids"]).issubset(known)
        if row["direct_scan_disposition"].startswith("HOLD_"):
            assert row["canonical_record_ids"] == []
    assert len({r["historical_candidate_id"] for r in disp}) == 100


def test_temporal_holds_are_fail_closed_and_explicit_big_limits_are_preserved():
    d = load(READJ)
    disp = by_candidate()
    expected_held = {
        "SP02-113", "SP02-114", "SP02-115", "SP02-116", "SP02-117",
        "SP02-122", "SP02-123", "SP02-124", "SP02-125",
        "SP02-128", "SP02-129", "SP02-135",
        "SP02-153", "SP02-154", "SP02-155",
        "SP02-169", "SP02-170", "SP02-175", "SP02-180", "SP02-181",
        "SP02-193", "SP02-194", "SP02-195",
    }
    assert {k for k, v in disp.items() if v["direct_scan_disposition"].startswith("HOLD_")} == expected_held
    assert len(d["temporal_scope_residuals"]) == 10
    assert sum(len(r["candidate_ids"]) for r in d["temporal_scope_residuals"]) == 23
    records = records_by_id()
    for rid in ["P03S-140", "P03S-141", "P03S-165", "P03S-176"]:
        assert records[rid]["primary_time_layer"] == "DECADE"
        assert "大限" in records[rid]["source_time_expression"]


def test_source_first_corrections_and_case_only_boundaries():
    d = load(READJ)
    disp = by_candidate()
    rec = records_by_id()
    assert disp["SP02-101"]["direct_scan_disposition"] == "PROMOTE_SOURCE_GROUNDED"
    assert "见煞忌亦主离异" in rec["P03S-101"]["source_literal_claim"]
    assert "禄权科会" in rec["P03S-102"]["source_literal_claim"]
    assert "同时见巨门化忌" in rec["P03S-103"]["source_literal_claim"]
    assert "对宫为天梁" in rec["P03S-104"]["source_literal_claim"]
    assert rec["P03S-104"]["canonical_projection_target"] == "early_marriage_divorce_or_repeated_premarital_setbacks"
    assert rec["P03S-108"]["canonical_projection_target"] == "conditionally_acceptable_marriage_not_guaranteed"
    assert "未明示须全备" in rec["P03S-121"]["source_condition_uncertainty"]
    assert rec["P03S-132"]["case_support_only"] is True
    assert rec["P03S-133"]["canonical_projection_target"] == "relationship_emotional_secret_or_reservation"
    assert "桃花诸曜" in rec["P03S-149"]["canonical_condition"]
    assert rec["P03S-151"]["case_support_only"] is True
    assert rec["P03S-151"]["canonical_projection_target"] == "self_extramarital_attachment_after_marriage"
    assert rec["P03S-152"]["case_support_only"] is True
    assert "女命" in rec["P03S-163"]["canonical_condition"]
    assert rec["P03S-183"]["case_support_only"] is True
    assert set(disp["SP02-190"]["canonical_record_ids"]) == {
        "P03S-190-HEALTH", "P03S-190-HEAVY_SHA", "P03S-190-SEPARATION"
    }
    assert "煞重" in rec["P03S-190-HEAVY_SHA"]["canonical_condition"]
    assert "不见重煞" in rec["P03S-190-SEPARATION"]["canonical_condition"]
    assert "但不重" in rec["P03S-199"]["canonical_condition"]
    assert rec["P03S-200"]["case_support_only"] is True


def test_prior_gaps_resolved_and_new_source_gaps_carried_forward():
    d = load(READJ)
    gaps = {g["gap_id"]: g for g in d["source_coverage_gaps"]}
    assert gaps["P03-SP01-GAP-001"]["status"] == "CARRIED_FORWARD"
    assert gaps["P03-SP01-GAP-002"]["status"] == "RESOLVED_BY_SP02-101"
    assert gaps["P03-SP01-GAP-003"]["status"] == "RESOLVED_BY_SP02-102_AND_SP02-103"
    assert gaps["P03-SP01-GAP-004"]["status"] == "RESOLVED_BY_SP02-104"
    open_gaps = [g for g in gaps.values() if g["status"] == "CARRIED_FORWARD"]
    assert len(open_gaps) == 7
    assert d["summary"]["source_coverage_gap_count"] == 7
    claim_text = " ".join(g["source_literal_claim"] for g in open_gaps)
    for phrase in ["机巨", "基本上不利", "机录像", "申宫又劣于寅宫", "福德宫", "辅佐诸吉", "此等宫垣"]:
        assert phrase in claim_text


def test_execution_boundary_and_post_merge_state_checkpoint():
    d = load(READJ)
    state = STATE.read_text(encoding="utf-8")
    boundary = d["execution_boundary"]
    assert boundary["conditions_compiled"] == 0
    assert boundary["execution_unlocked"] == 0
    assert boundary["product_runtime_authorized"] is False
    assert boundary["shared_core_semantics_changed"] is False
    assert boundary["other_palace_changed"] is False
    assert boundary["history_feedback"] == 0
    assert d["summary"]["history_feedback"] == 0
    for key in ["new_primitive_qi", "new_memory_type", "new_independent_time_scale",
                "new_shared_group_semantics", "numeric_weight", "probability", "decay",
                "product_runtime_change"]:
        assert d["summary"][key] == 0
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert "SP02_101_200_SOURCE_FIRST_MERGED" in state
    assert "historical_candidate_rows_reviewed: 200" in state
    assert "candidate_rows_promoted: 166" in state
    assert "source_records_added: 169" in state
    assert "reusable_projection_method_records_added: 135" in state
    assert "case_support_only_records_added: 34" in state
    assert "candidates_held: 32" in state
    assert "source_coverage_residuals_open: 7" in state
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state
    assert "SP03-201" in state
