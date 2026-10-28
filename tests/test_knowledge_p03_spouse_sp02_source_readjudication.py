import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/SP02_spouse_projection_review_101_200.csv"
READJ = ROOT / "knowledge/palaces/P03_spouse/wp05/SPOUSE_SP02_SOURCE_READJUDICATION_100_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_rows():
    with CANDIDATE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def by_candidate():
    return {r["historical_candidate_id"]: r for r in load(READJ)["candidate_batch"]["candidate_dispositions"]}


def records_by_id():
    return {r["projection_rule_id"]: r for r in load(READJ)["records"]}


def test_exact_candidate_inventory_source_pin_and_page_mapping():
    d = load(READJ)
    rows = candidate_rows()
    inv = d["historical_candidate_inventory"]
    assert len(rows) == 100
    assert len({r["projection_rule_id"] for r in rows}) == 100
    assert rows[0]["projection_rule_id"] == "SP02-101"
    assert rows[-1]["projection_rule_id"] == "SP02-200"
    assert d["candidate_batch"]["rows"] == 100
    assert d["candidate_batch"]["sha"] == "0bc7a6f9c03790cf8b7c610a19ca55d78b3cf007"
    src = d["source_basis"]
    assert src["source_id"] == "SRC-ZZ-003"
    assert src["attachment_sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert src["candidate_batch_verified_printed_pages"] == [35, 36, 37]
    assert src["candidate_batch_verified_pdf_physical_pages"] == [18, 19]
    assert src["page_mapping"]["35"] == src["page_mapping"]["36"] == 18
    assert src["page_mapping"]["37"] == 19
    assert inv["total_rows"] == inv["unique_ids"] == 836
    assert inv["first_id"] == "SP01-001"
    assert inv["last_id"] == "SP09-836"


def test_all_candidates_have_dispositions_and_counts_reconcile():
    d = load(READJ)
    rows = candidate_rows()
    disp = d["candidate_batch"]["candidate_dispositions"]
    ids = [r["historical_candidate_id"] for r in disp]
    assert ids == [r["projection_rule_id"] for r in rows]
    assert len(disp) == 100
    assert all(r["reason"] for r in disp)
    s = d["summary"]
    records = d["records"]
    assert s["reviewed"] == 100
    assert s["canonical_promoted"] == 77
    assert s["canonical_record_count"] == len(records) == 77
    assert len({r["projection_rule_id"] for r in records}) == 77
    assert s["reusable_projection_rules"] == 60
    assert s["case_support_only"] == 17
    assert s["held"] == 23
    assert s["deduplicated"] == 0
    assert sum(r["case_support_only"] is True for r in records) == 17
    assert sum(r["case_support_only"] is False for r in records) == 60
    known = set(r["projection_rule_id"] for r in records)
    for row in disp:
        assert set(row["canonical_record_ids"]).issubset(known)
        if row["direct_scan_disposition"].startswith("HOLD_"):
            assert row["canonical_record_ids"] == []
        else:
            assert row["canonical_record_ids"]


def test_unsupported_temporal_layers_fail_closed():
    d = load(READJ)
    disp = by_candidate()
    expected = {
        "SP02-113", "SP02-114", "SP02-115", "SP02-116", "SP02-117",
        "SP02-122", "SP02-123", "SP02-124", "SP02-125",
        "SP02-128", "SP02-129", "SP02-135",
        "SP02-153", "SP02-154", "SP02-155",
        "SP02-169", "SP02-170", "SP02-175", "SP02-180", "SP02-181",
        "SP02-193", "SP02-194", "SP02-195",
    }
    actual = {k for k, v in disp.items() if v["direct_scan_disposition"] == "HOLD_TEMPORAL_GRANULARITY_UNRESOLVED"}
    assert actual == expected
    temporal_ids = {c for residual in d["temporal_scope_residuals"] for c in residual["candidate_ids"]}
    assert expected.issubset(temporal_ids)
    assert {"SP01-091", "SP01-092", "SP01-097", "SP01-098"}.issubset(temporal_ids)
    assert all(r["primary_time_layer"] != "YEAR" for r in d["records"] if r["projection_rule_id"] in {"P03S-140", "P03S-141"})


def test_gap_branches_and_source_qualifiers_are_preserved():
    d = load(READJ)
    disp = by_candidate()
    rec = records_by_id()
    assert disp["SP02-101"]["direct_scan_disposition"] == "PROMOTE_SOURCE_GROUNDED"
    assert disp["SP02-102"]["canonical_record_ids"] == ["P03S-102"]
    assert disp["SP02-103"]["canonical_record_ids"] == ["P03S-103"]
    assert "巨门化忌" in rec["P03S-103"]["canonical_condition"]
    assert "自我克制" in rec["P03S-103"]["source_literal_claim"]
    assert "对宫天梁" in rec["P03S-104"]["canonical_condition"]
    assert "OR" not in rec["P03S-104"]["canonical_condition"] or "或" in rec["P03S-104"]["canonical_condition"]
    assert "无煞" in rec["P03S-108"]["canonical_condition"]
    assert "尚可" in rec["P03S-108"]["source_literal_claim"]
    assert "未明确编码为全部 AND" in rec["P03S-121"]["source_condition_uncertainty"]
    assert "大限夫妻宫" in rec["P03S-140"]["canonical_condition"]
    assert "不重" in rec["P03S-199"]["canonical_condition"]
    assert rec["P03S-192"]["canonical_projection_target"] == "sun_moon_in_wei_relatively_more_favorable_for_female_chart_than_chou_branch"
    assert rec["P03S-118"]["canonical_projection_target"] == "wife_beauty_and_support"
    assert rec["P03S-136"]["canonical_projection_target"] == "late_marriage_or_premarital_turbulence_otherwise_separation"
    assert rec["P03S-150"]["canonical_projection_target"] == "spouse_refined_and_career_capable"
    assert rec["P03S-189"]["canonical_projection_target"] == "support_from_wifes_family_and_general_spousal_support"


def test_source_coverage_gaps_are_explicit_and_prior_gaps_reconciled():
    d = load(READJ)
    gaps = {g["gap_id"]: g for g in d["source_coverage_gaps"]}
    assert len(gaps) == 9
    assert gaps["P03-SP01-GAP-001"]["status"] == "CARRIED_FORWARD"
    assert gaps["P03-SP01-GAP-002"]["status"] == "RESOLVED_BY_SP02-101"
    assert gaps["P03-SP01-GAP-003"]["status"] == "RESOLVED_BY_SEPARATE_SP02-102_AND_SP02-103"
    assert gaps["P03-SP01-GAP-004"]["status"] == "RESOLVED_BY_SOURCE_NARROWED_SP02-104"
    for key in ["P03-SP02-GAP-001", "P03-SP02-GAP-002", "P03-SP02-GAP-003"]:
        assert gaps[key]["status"] == "CARRIED_FORWARD"
        assert gaps[key]["printed_page"] == 37
        assert gaps[key]["pdf_physical_page"] == 19
    all_gap_text = " ".join(g["source_literal_claim"] for g in gaps.values())
    assert "见煞忌亦主离异" in all_gap_text
    assert "禄权科会" in all_gap_text
    assert "福德宫" in all_gap_text
    assert "辅佐诸吉" in all_gap_text


def test_execution_boundary_and_cumulative_state_are_fail_closed():
    d = load(READJ)
    boundary = d["execution_boundary"]
    assert boundary["canonical_promotion_is_source_only"] is True
    assert boundary["conditions_compiled"] == 0
    assert boundary["execution_unlocked"] == 0
    assert boundary["product_runtime_authorized"] is False
    assert boundary["shared_core_semantics_changed"] is False
    assert boundary["other_palace_changed"] is False
    assert boundary["history_feedback"] == 0
    s = d["summary"]
    for key in ["new_primitive_qi", "new_memory_type", "new_independent_time_scale",
                "new_shared_group_semantics", "numeric_weight", "probability", "decay",
                "product_runtime_change"]:
        assert s[key] == 0
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in state or 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    if 'status: "ACTIVE"' in state:
        issue_match = re.search(r"(?m)^  active_issue: (\\d+)$", state)
        branch_match = re.search(r'(?m)^  active_branch: "([^"]+)"
    batches = [load(path) for path in sorted(READJ.parent.glob(
        "SPOUSE_SP*_SOURCE_READJUDICATION_*.json"
    ))]
    fields = {
        "historical_candidate_rows_reviewed": "reviewed",
        "candidate_rows_promoted": "canonical_promoted",
        "source_records_added": "canonical_record_count",
        "reusable_projection_method_records_added": "reusable_projection_rules",
        "case_support_only_records_added": "case_support_only",
        "candidates_held": "held",
        "candidates_deduplicated": "deduplicated",
    }
    state_lines = set(state.splitlines())
    for field, summary_key in fields.items():
        total = sum(batch["summary"][summary_key] for batch in batches)
        assert f"  {field}: {total}" in state_lines
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state


def test_duplicate_delivery_reconciliation_keeps_source_and_event_boundaries():
    d = load(READJ)
    records = records_by_id()
    expected = {"P03S-110", "P03S-132", "P03S-134", "P03S-138",
                "P03S-145", "P03S-146", "P03S-147", "P03S-151", "P03S-152",
                "P03S-162", "P03S-163", "P03S-183", "P03S-186", "P03S-188",
                "P03S-190", "P03S-191", "P03S-200"}
    assert set(d["summary"]["case_support_only_ids"]) == expected
    assert {key for key, row in records.items() if row["case_support_only"]} == expected
    for key in d["repair_reconciliation"]["case_only_boundary_ids"]:
        assert records[key]["projection_mode"] == "EVENT_CANDIDATE"
        assert records[key]["case_support_reason"]
    gaps = {g["gap_id"]: g for g in d["source_coverage_gaps"]}
    assert "机录像" in gaps["P03-SP02-GAP-001"]["source_literal_claim"]
    assert "机梁紫破" not in gaps["P03-SP02-GAP-001"]["source_literal_claim"]
    assert gaps["P03-SP02-GAP-004"]["printed_page"] == 35
    assert gaps["P03-SP02-GAP-005"]["printed_page"] == 36
    assert all(gaps[key]["status"] == "CARRIED_FORWARD" for key in
               ["P03-SP02-GAP-004", "P03-SP02-GAP-005"])
    assert d["summary"]["open_source_coverage_gap_count"] == 6
    assert len(d["temporal_scope_residuals"]) == 12
, state)
        assert issue_match and branch_match
        assert f"p03-{issue_match.group(1)}-" in branch_match.group(1)
    else:
        assert "active_issue: null" in state
        assert "active_branch: null" in state
        assert "active_pr: null" in state
    assert "SOURCE_FIRST_REVIEW_COMPLETE" in state
    batches = [load(path) for path in sorted(READJ.parent.glob(
        "SPOUSE_SP*_SOURCE_READJUDICATION_*.json"
    ))]
    fields = {
        "historical_candidate_rows_reviewed": "reviewed",
        "candidate_rows_promoted": "canonical_promoted",
        "source_records_added": "canonical_record_count",
        "reusable_projection_method_records_added": "reusable_projection_rules",
        "case_support_only_records_added": "case_support_only",
        "candidates_held": "held",
        "candidates_deduplicated": "deduplicated",
    }
    state_lines = set(state.splitlines())
    for field, summary_key in fields.items():
        total = sum(batch["summary"][summary_key] for batch in batches)
        assert f"  {field}: {total}" in state_lines
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state


def test_duplicate_delivery_reconciliation_keeps_source_and_event_boundaries():
    d = load(READJ)
    records = records_by_id()
    expected = {"P03S-110", "P03S-132", "P03S-134", "P03S-138",
                "P03S-145", "P03S-146", "P03S-147", "P03S-151", "P03S-152",
                "P03S-162", "P03S-163", "P03S-183", "P03S-186", "P03S-188",
                "P03S-190", "P03S-191", "P03S-200"}
    assert set(d["summary"]["case_support_only_ids"]) == expected
    assert {key for key, row in records.items() if row["case_support_only"]} == expected
    for key in d["repair_reconciliation"]["case_only_boundary_ids"]:
        assert records[key]["projection_mode"] == "EVENT_CANDIDATE"
        assert records[key]["case_support_reason"]
    gaps = {g["gap_id"]: g for g in d["source_coverage_gaps"]}
    assert "机录像" in gaps["P03-SP02-GAP-001"]["source_literal_claim"]
    assert "机梁紫破" not in gaps["P03-SP02-GAP-001"]["source_literal_claim"]
    assert gaps["P03-SP02-GAP-004"]["printed_page"] == 35
    assert gaps["P03-SP02-GAP-005"]["printed_page"] == 36
    assert all(gaps[key]["status"] == "CARRIED_FORWARD" for key in
               ["P03-SP02-GAP-004", "P03-SP02-GAP-005"])
    assert d["summary"]["open_source_coverage_gap_count"] == 6
    assert len(d["temporal_scope_residuals"]) == 12
