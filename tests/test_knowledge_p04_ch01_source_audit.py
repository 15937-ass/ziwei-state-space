"""P04 CH01 source-first revalidation: preserve the original scan and fail closed."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "knowledge/palaces/P04_children/source_audit/CH01_001_100_SOURCE_AUDIT_v0.1.json"
CSV = ROOT / "validation/wp05/CH01_children_projection_review_001_100.csv"
STATE = ROOT / "knowledge/states/P04_CHILDREN_STATE.yaml"


def read():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def git_blob_sha1(path):
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def test_candidate_inventory_and_new_dispositions_reconcile():
    data = read()
    with CSV.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 100
    assert [row["projection_rule_id"] for row in rows] == [f"CH01-{n:03d}" for n in range(1, 101)]
    assert git_blob_sha1(CSV) == data["candidate_archive"]["git_blob_sha"]
    assert data["summary"]["candidate_rows"] == 100
    assert data["summary"]["unique_candidate_ids"] == 100
    assert data["summary"]["distinct_condition_strings"] == 87
    assert data["summary"]["multi_output_condition_groups"] == 13

    dispositions = data["candidate_adjudications"]
    assert len(dispositions) == 100
    assert [item["legacy_candidate_id"] for item in dispositions] == [row["projection_rule_id"] for row in rows]
    assert len({item["legacy_candidate_id"] for item in dispositions}) == 100
    assert sum(item["reusable_projection_method"] for item in dispositions) == 61
    assert sum(item["case_support_only"] for item in dispositions) == 33
    assert sum(item["disposition"] == "HELD_TIME_SCOPE_UNRESOLVED" for item in dispositions) == 6
    assert data["summary"]["proposed_source_records"] == 95
    assert data["summary"]["proposed_case_support_only_records"] == 34
    record_ids = sorted({rid for item in dispositions for rid in item["source_record_ids"]})
    assert record_ids == [f"P04S-{n:03d}" for n in range(1, 96)]
    assert len({rid for item in dispositions for rid in item["source_record_ids"]}) == 95
    split = next(item for item in dispositions if item["legacy_candidate_id"] == "CH01-022")
    assert len(split["source_record_ids"]) == 2
    assert split["case_support_only"]
    assert all(item["source_text_directly_reviewed"] and item["source_condition_supported"] and item["source_location_revalidated"] for item in dispositions)
    row19 = next(item for item in dispositions if item["legacy_candidate_id"] == "CH01-019")
    assert row19["adjudicated_target"] == "child_quality_assessment_only_not_automatic_affliction"


def test_time_scope_holds_and_explicit_decade_year_alternative_are_preserved():
    data = read()
    by_id = {item["legacy_candidate_id"]: item for item in data["candidate_adjudications"]}
    for candidate in ("CH01-047", "CH01-048", "CH01-060", "CH01-061", "CH01-062", "CH01-063"):
        assert by_id[candidate]["disposition"] == "HELD_TIME_SCOPE_UNRESOLVED"
        assert by_id[candidate]["time_layer"] == "UNRESOLVED"
        assert not by_id[candidate]["canonical_promotion"]
    assert by_id["CH01-079"]["time_layer"] == "DECADE"
    assert by_id["CH01-080"]["time_layer"] == "YEAR"
    assert by_id["CH01-079"]["time_alternative_group"] == by_id["CH01-080"]["time_alternative_group"]
    assert by_id["CH01-063"]["legacy_time_layer"] == "NATAL"
    assert by_id["CH01-047"]["gap_id"] == "P04-CH01-GAP-TIME-01"
    assert by_id["CH01-060"]["gap_id"] == "P04-CH01-GAP-TIME-02"
    assert by_id["CH01-063"]["gap_id"] == "P04-CH01-GAP-TIME-03"


def test_source_boundary_and_cross_palace_rules_are_fail_closed():
    data = read()
    boundary = data["boundary"]
    assert boundary["full_p04_body_printed_pages"] == [51, 68]
    assert boundary["full_p04_body_pdf_physical_pages"] == [26, 34]
    assert boundary["p04_start"]["position"].startswith("mid-page after")
    assert boundary["p04_end"]["printed_page"] == 68
    assert boundary["next_palace"]["printed_page"] == 69
    assert "table of contents" in boundary["toc_body_discrepancy"].lower()
    batch_end = boundary["candidate_batch_ends_mid_page_53_after"].lower()
    assert "first positive clause" in batch_end
    assert "ch02-101…103" in batch_end
    assert "unreviewed" in batch_end
    a15 = next(anchor for anchor in data["source_anchors"] if anchor["id"] == "P04-CH01-A15")
    assert "first positive clause" in a15["description"]
    assert "adverse-condition continuation" in a15["description"]
    assert "CH02-101…103" in a15["description"]
    by_id = {item["legacy_candidate_id"]: item for item in data["candidate_adjudications"]}
    assert by_id["CH01-008"]["routing_target_palace"] == "P08"
    assert by_id["CH01-009"]["routing_target_palace"] == "P04"
    assert by_id["CH01-067"]["cross_palace_refs"] == ["P03"]
    row99 = by_id["CH01-099"]
    assert row99["disposition"] == "CASE_SUPPORT_ONLY"
    assert "moralized behavioral-risk" in row99["adjudication_note"]
    assert "reusable modern" in row99["adjudication_note"]


def test_no_execution_mapping_or_history_feedback_is_authorized():
    data = read()
    assert data["execution_boundary"]["source_records_executable"] == 0
    assert data["execution_boundary"]["canonical_mapping_approved"] == 0
    assert data["execution_boundary"]["history_feedback"] == 0
    assert data["execution_boundary"]["conditions_compiled"] == 0
    assert data["execution_boundary"]["execution_unlocked"] == 0
    assert data["execution_boundary"]["product_or_kib_authorized"] is False
    assert all(not item["executable"] and not item["canonical_mapping_approved"] and not item["history_feedback"] for item in data["candidate_adjudications"])
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_BUILD"' in state
    assert 'active_issue: 943' in state
    assert 'active_pr: 944' in state
    assert 'active_branch: "knowledge/p04-943-children-ch01-001-100-source-audit"' in state
    assert 'canonical_checkpoint: "P04_CH01_001_100_SOURCE_FIRST_REVALIDATION_PROPOSED"' in state
