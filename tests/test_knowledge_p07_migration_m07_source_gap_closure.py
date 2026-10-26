import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M07_RESIDUAL_SOURCE_GAP_CLOSURE_6_v0.1.json"
STATE = ROOT / "knowledge/states/P07_MIGRATION_STATE.yaml"
M03 = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M03_SOURCE_READJUDICATION_100_v0.1.json"
M05 = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M05_SOURCE_READJUDICATION_100_v0.1.json"
M06 = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M06_SOURCE_READJUDICATION_090_v0.1.json"

EXPECTED_GAPS = {
    "P07-M03-GAP-012", "P07-M03-GAP-001",
    "P07-M05-GAP-001", "P07-M05-GAP-002",
    "P07-M05-GAP-003", "P07-M05-GAP-004",
}
EXPECTED_RECORD_IDS = {f"M07-{i}" for i in range(591, 608)}
EXPECTED_UNRESOLVED = {"P07-M03-GAP-012"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_m07_rechecks_exact_six_gap_ids_against_original_scan():
    d = load(ARTIFACT)
    m03 = load(M03)
    m05 = load(M05)
    m06 = load(M06)

    assert d["artifact_id"] == "KB-P07-M07-RESIDUAL-SOURCE-GAP-CLOSURE-6-v0.1"
    assert d["issue"] == 669
    assert d["status"] == "SOURCE_RECHECKED_FIVE_COVERAGE_GAPS_CLOSED_ONE_RETAINED"
    assert d["source_basis"]["attachment_sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert d["source_basis"]["verification_method"] == "DIRECT_PDF_VISUAL_REVIEW"
    assert d["source_basis"]["verified_pdf_physical_pages"] == [57, 58, 59]
    assert d["source_basis"]["verified_printed_pages"] == [114, 115, 118]

    dispositions = d["gap_dispositions"]
    assert {row["gap_id"] for row in dispositions} == EXPECTED_GAPS
    assert len(dispositions) == 6
    assert {row["gap_id"] for row in dispositions if row["source_coverage_gap_closed"]} == EXPECTED_GAPS - EXPECTED_UNRESOLVED
    assert {row["gap_id"] for row in dispositions if not row["source_coverage_gap_closed"]} == EXPECTED_UNRESOLVED
    assert all(row["direct_scan_finding"] and row["reason"] for row in dispositions)

    assert {row["gap_id"] for row in m03["source_coverage_gaps"] if row["gap_id"] in EXPECTED_GAPS} >= {
        "P07-M03-GAP-012", "P07-M03-GAP-001"
    }
    assert {row["gap_id"] for row in m05["source_coverage_gaps"]} >= {
        "P07-M05-GAP-001", "P07-M05-GAP-002", "P07-M05-GAP-003", "P07-M05-GAP-004"
    }
    assert {row["gap_id"] for row in m06["source_coverage_gaps"]} == EXPECTED_GAPS


def test_m07_new_records_are_source_bounded_and_count_reconciles():
    d = load(ARTIFACT)
    records = d["records"]
    assert len(records) == 17
    assert {row["projection_rule_id"] for row in records} == EXPECTED_RECORD_IDS
    assert len({row["projection_rule_id"] for row in records}) == 17
    assert all(row["canonical_promotion"] is True for row in records)
    assert all(row["source_resolution_changed"] is True for row in records)
    assert all(row["source_location"] and row["source_span_id"] and row["source_literal_claim"] for row in records)
    expected_pages = {
        "M07-591": (115, 58),
        "M07-592": (118, 59), "M07-593": (118, 59),
        "M07-594": (118, 59), "M07-595": (118, 59),
        "M07-596": (118, 59), "M07-597": (118, 59),
        "M07-598": (118, 59), "M07-599": (118, 59),
        "M07-600": (118, 59), "M07-601": (118, 59),
        "M07-602": (118, 59), "M07-603": (118, 59),
        "M07-604": (118, 59), "M07-605": (118, 59),
        "M07-606": (118, 59), "M07-607": (118, 59),
    }
    for row in records:
        page, physical = expected_pages[row["projection_rule_id"]]
        assert row["source_location"] == f"SRC-ZZ-003 printed p{page} / PDF physical p{physical}"
        assert row["source_span_id"] == f"ZZ003-P{page}"
    assert all(row["primary_time_layer"] == "NATAL" for row in records)
    assert sum(row["case_support_only"] is True for row in records) == 1
    assert sum(row["case_support_only"] is False for row in records) == 16

    by_id = {row["projection_rule_id"]: row for row in records}
    assert by_id["M07-591"]["source_literal_claim"] == "太阴与辅弼同度，不外得人助。"
    assert by_id["M07-593"]["case_support_only"] is True
    assert "ALL/ANY/N_OF" in by_id["M07-593"]["source_condition_uncertainty"]
    assert "六吉夹" in by_id["M07-596"]["source_literal_claim"]
    assert "魁钺夹、辅弼夹、昌曲夹、禄权科夹、紫府夹、日月夹" in by_id["M07-596"]["source_literal_claim"]
    assert by_id["M07-604"]["source_condition_membership_status"] == "OPEN_SOURCE_NATIVE_CATEGORY"
    assert by_id["M07-605"]["source_condition_membership_status"] == "OPEN_SOURCE_NATIVE_CATEGORY"
    assert "仅主人小妒忌，或小人包围" in by_id["M07-607"]["source_literal_claim"]

    s = d["summary"]
    assert s["original_gaps_reviewed"] == 6
    assert s["source_coverage_gaps_closed"] == 5
    assert s["gaps_partially_resolved_and_retained"] == 1
    assert s["remaining_unresolved_gap_ids"] == ["P07-M03-GAP-012"]
    assert s["new_source_records"] == 17
    assert s["new_reusable_projection_records"] == 16
    assert s["new_case_support_only_records"] == 1
    assert s["cumulative_candidates_reviewed_after"] == 607
    assert s["cumulative_reusable_projection_method_records_after"] == 536
    assert s["cumulative_case_support_only_after"] == 71


def test_m03_p114_fragment_remains_unresolved_and_execution_stays_locked():
    d = load(ARTIFACT)
    unresolved = next(row for row in d["gap_dispositions"] if row["gap_id"] == "P07-M03-GAP-012")
    assert unresolved["disposition"] == "PARTIALLY_RESOLVED_RETAINED_UNRESOLVED"
    assert unresolved["added_record_ids"] == []
    assert "贞归三" in unresolved["direct_scan_finding"]
    assert "no explicit consequence" in unresolved["reason"].lower() or "does not state its consequence" in unresolved["reason"].lower()

    guard = d["guardrails"]
    assert guard["unresolved_p114_glyph_sequence_not_repaired"] is True
    assert guard["unresolved_p118_glyph_before_wei_not_silently_corrected"] is True
    assert guard["no_universal_all_any_n_of_default"] is True
    assert guard["no_global_jia_clamp_or_xiong_clamp_membership_invented"] is True
    assert guard["product_runtime_not_authorized"] is True
    assert d["execution_boundary"]["conditions_compiled"] == 0
    assert d["execution_boundary"]["execution_unlocked"] == 0
    assert d["execution_boundary"]["product_runtime_authorized"] is False
    assert d["execution_boundary"]["shared_core_semantics_changed"] is False

    state = STATE.read_text(encoding="utf-8")
    assert "M07_591_607_RESIDUAL_SOURCE_GAP_CLOSURE" in state
    assert "Five coverage gaps closed; P07-M03-GAP-012 retained unresolved" in state
    assert "607 cumulative candidates reviewed" in state
    assert "536 reusable projection/method records" in state
    assert "71 CASE_SUPPORT_ONLY" in state
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state
