import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "knowledge/palaces/P04_children/source_audit/CH02_101_200_SOURCE_AUDIT_v0.1.json"
STATE_PATH = ROOT / "knowledge/states/P04_CHILDREN_STATE.yaml"


def _audit():
    return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))


def test_ch02_first_subbatch_has_exactly_fifty_contiguous_candidates():
    audit = _audit()
    ids = [item["legacy_candidate_id"] for item in audit["candidate_adjudications"]]

    assert ids == [f"CH02-{number:03d}" for number in range(101, 151)]
    assert audit["summary"]["candidate_rows"] == 50
    assert audit["summary"]["unique_candidate_ids"] == 50
    assert audit["status"] == "IN_PROGRESS_FIRST_50_REVIEWED_PENDING_CH02_151_200"


def test_original_source_and_frozen_candidate_archive_are_pinned():
    audit = _audit()

    assert audit["source"]["source_id"] == "SRC-ZZ-003"
    assert audit["source"]["pdf_sha256"] == (
        "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    )
    assert audit["candidate_archive"]["git_blob_sha"] == (
        "dc0f10c69906ab84cbb272089ec175bb57c1aefe"
    )
    assert audit["candidate_archive"]["legacy_labels_are_navigation_only"] is True
    assert audit["boundary"]["candidate_batch_printed_pages"] == [53, 54]
    assert audit["boundary"]["candidate_batch_pdf_physical_pages"] == [27]


def test_time_scope_hubs_without_explicit_year_or_decade_are_held():
    audit = _audit()
    held = {
        item["legacy_candidate_id"]: item
        for item in audit["candidate_adjudications"]
        if item["disposition"] == "HELD_TIME_SCOPE_UNRESOLVED"
    }

    assert set(held) == {"CH02-102", "CH02-103", "CH02-146"}
    assert all(item["time_layer"] == "UNRESOLVED" for item in held.values())
    assert all(item["canonical_promotion"] is False for item in held.values())
    assert all(item["source_condition_supported"] is False for item in held.values())
    assert all(item["source_record_ids"] == [] for item in held.values())
    assert len(audit["gap_register"]) == 2


def test_mixed_childbearing_and_later_generation_timing_is_split():
    audit = _audit()
    mixed = {
        item["legacy_candidate_id"]: item
        for item in audit["candidate_adjudications"]
        if item.get("disposition") == "SPLIT_DISPOSITION"
    }

    assert set(mixed) == {"CH02-117", "CH02-129"}
    for item in mixed.values():
        dispositions = {claim["disposition"] for claim in item["split_claims"]}
        assert dispositions == {"CASE_SUPPORT_ONLY", "ACCEPTED_SOURCE_PROJECTION"}
        assert item["executable"] is False
        assert item["canonical_mapping_approved"] is False


def test_child_count_obstetric_and_traditional_household_claims_remain_case_only():
    audit = _audit()
    by_id = {
        item["legacy_candidate_id"]: item
        for item in audit["candidate_adjudications"]
    }
    expected = {
        "CH02-104", "CH02-105", "CH02-106", "CH02-111",
        "CH02-121", "CH02-122", "CH02-123", "CH02-124", "CH02-125",
        "CH02-130", "CH02-131", "CH02-132", "CH02-133", "CH02-134",
        "CH02-135", "CH02-136", "CH02-139", "CH02-140",
        "CH02-147", "CH02-148", "CH02-149",
    }
    assert all(by_id[item]["disposition"] == "CASE_SUPPORT_ONLY" for item in expected)
    assert all(by_id[item]["case_support_only"] is True for item in expected)


def test_all_candidate_adjudications_are_non_executable_and_mapping_unapproved():
    audit = _audit()
    assert all(item["source_text_directly_reviewed"] for item in audit["candidate_adjudications"])
    assert all(item["source_location_revalidated"] for item in audit["candidate_adjudications"])
    assert all(item["executable"] is False for item in audit["candidate_adjudications"])
    assert all(item["canonical_mapping_approved"] is False for item in audit["candidate_adjudications"])
    assert all(item["history_feedback"] is False for item in audit["candidate_adjudications"])
    assert audit["execution_boundary"]["source_records_executable"] == 0
    assert audit["execution_boundary"]["conditions_compiled"] == 0
    assert audit["execution_boundary"]["execution_unlocked"] == 0
    assert audit["execution_boundary"]["product_or_kib_authorized"] is False


def test_first_subbatch_state_cache_matches_reviewed_progress():
    state = STATE_PATH.read_text(encoding="utf-8")
    assert 'active_issue: 953' in state
    assert 'active_candidate_batch: "CH02-101…200"' in state
    assert "active_candidate_rows_reviewed: 50" in state
    assert "proposed_reusable_source_records: 26" in state
    assert "proposed_case_support_only_source_records: 23" in state
    assert "proposed_held_candidates: 3" in state
    assert "proposed_gap_groups: 2" in state
