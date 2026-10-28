import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP05 = ROOT / "knowledge/palaces/P03_spouse/wp05"
FOLLOWUP = WP05 / "P03_SOURCE_ATOM_FOLLOWUP_ISSUE819_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"
REPORT = ROOT / "validation/knowledge/palaces/P03_spouse/issue_819/SOURCE_ATOM_FOLLOWUP_REVIEW.md"
LEDGER_PATHS = [
    *(WP05 / f"SPOUSE_SP{i:02d}_SOURCE_READJUDICATION_100_v0.1.json" for i in range(1, 9)),
    WP05 / "SPOUSE_SP09_SOURCE_READJUDICATION_36_v0.1.json",
]
APPROVED_SOURCE_SHA = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_three_source_atoms_match_exact_scan_literals_and_gap_ids():
    d = load(FOLLOWUP)
    assert d["issue"] == 819
    assert d["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert d["source_basis"]["approved_pdf_sha256"] == APPROVED_SOURCE_SHA
    assert d["source_basis"]["verification_method"] == "DIRECT_VISUAL_REVIEW_OF_ORIGINAL_SCAN_IMAGES"
    assert d["source_basis"]["printed_pages_reviewed"] == [33, 35, 36]
    assert d["source_basis"]["pdf_physical_pages_reviewed"] == [17, 18]

    records = d["source_atom_records"]
    assert len(records) == 3
    assert len({r["projection_rule_id"] for r in records}) == 3
    by_gap = {r["gap_id"]: r for r in records}
    assert set(by_gap) == {
        "P03-SP01-GAP-001",
        "P03-SP02-GAP-004",
        "P03-SP02-GAP-005",
    }
    assert by_gap["P03-SP01-GAP-001"]["source_literal_claim"] == (
        "寅申宫[紫府]同度，若无辅佐诸曜(或有，而所见者多[单星])，或府库[空露]，"
        "则防于贪狼、破军、巨门大运，婚姻发生变化。此等宫垣，见煞忌空劫即为生变之兆。"
    )
    assert "则更为生变之兆" not in by_gap["P03-SP01-GAP-001"]["source_literal_claim"]
    assert by_gap["P03-SP02-GAP-004"]["source_literal_claim"] == (
        "女命夫妻宫不宜「机巨」。古人说，「天机巨门为破荡」，虽指命宫，在夫妻宫者亦然。"
        "见火铃或陀罗与天同同躔，即非一婚之命。"
    )
    assert by_gap["P03-SP02-GAP-005"]["source_literal_claim"] == (
        "天机在夫妻宫者，基本上不利。唯与太阴相对或同度的情形下，见吉曜，然后始主谐美。"
    )
    for record in records:
        assert record["visual_status"] == "VERIFIED_VISUAL_SCAN"
        assert record["source_literal_preserved"] is True
        assert record["disposition"] == "SOURCE_GAP_SUPPLEMENTAL_RECORD"
        assert record["gap_disposition"] == "RESOLVED_BY_ISSUE819_SUPPLEMENTAL_SOURCE_RECORD"
        assert record["canonical_promotion"] is False
        assert record["canonical_projection_target"] is None
        assert record["canonical_condition"] is None


def test_supplemental_ids_do_not_collide_with_accepted_ledgers():
    d = load(FOLLOWUP)
    accepted_ids = set()
    for path in LEDGER_PATHS:
        ledger = load(path)
        accepted_ids.update(record["projection_rule_id"] for record in ledger["records"])
    new_ids = {record["projection_rule_id"] for record in d["source_atom_records"]}
    assert len(accepted_ids) == len(set(accepted_ids))
    assert new_ids.isdisjoint(accepted_ids)
    assert d["boundary"]["accepted_sp01_sp09_ledgers_read_only"] is True
    assert d["boundary"]["historical_candidate_csvs_read_only"] is True
    assert d["boundary"]["no_canonical_rule_rows_added"] is True
    assert d["summary"]["accepted_sp01_sp09_ledgers_modified"] == 0
    assert d["summary"]["historical_candidate_csvs_modified"] == 0
    assert d["summary"]["canonical_rule_rows_added"] == 0
    assert d["summary"]["canonical_promotion_count"] == 0


def test_p37_literal_and_time_scope_remain_fail_closed():
    d = load(FOLLOWUP)
    residuals = d["remaining_residuals"]
    assert len(residuals) == 1
    residual = residuals[0]
    assert residual["gap_id"] == "P03-SP02-GAP-001"
    assert residual["printed_page"] == 37
    assert residual["pdf_physical_page"] == 19
    assert residual["source_literal"] == "机录像"
    assert residual["status"] == "OPEN_SOURCE_LITERAL_AND_TIME_SCOPE_UNRESOLVED"
    assert "YEAR versus DECADE" in residual["reason"] or "YEAR / DECADE" in residual["reason"]
    boundary = d["execution_boundary"]
    assert boundary["history_feedback"] == 0
    assert boundary["conditions_compiled"] == 0
    assert boundary["execution_unlocked"] == 0
    assert boundary["product_runtime_authorized"] is False
    assert boundary["no_product_runtime_changes"] is True
    assert boundary["shared_core_semantics_changed"] is False
    assert boundary["no_shared_core_semantics"] is True
    assert boundary["other_palace_changed"] is False
    assert boundary["new_primitive_qi"] == 0
    assert boundary["new_memory_type"] == 0
    assert boundary["new_independent_time_scale"] == 0
    assert boundary["numeric_weight"] == 0
    assert boundary["probability"] == 0
    assert boundary["decay"] == 0


def test_active_p03_state_and_handoff_report_are_consistent():
    d = load(FOLLOWUP)
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in state
    assert "active_issue: 819" in state
    assert 'active_branch: "knowledge/p03-819-spouse-source-atoms"' in state
    assert "P03_SOURCE_COVERAGE_CENSUS_AND_TEMPORAL_HANDOFF_ACCEPTED" in state
    assert "P03-SP01-GAP-001" in state
    assert "P03-SP02-GAP-001" in state
    assert "P03-SP02-GAP-004" in state
    assert "P03-SP02-GAP-005" in state
    assert "conditions_compiled: 0" in state
    assert "execution_unlocked: 0" in state
    assert "history_feedback: 0" in state
    assert REPORT.exists()
    report = REPORT.read_text(encoding="utf-8")
    for gap_id in (
        "P03-SP01-GAP-001",
        "P03-SP02-GAP-001",
        "P03-SP02-GAP-004",
        "P03-SP02-GAP-005",
    ):
        assert gap_id in report
    assert "机录像" in report
    assert "canonical_promotion=0" in report
