import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "knowledge/palaces/P04_children/source_audit/CH02_101_200_SOURCE_AUDIT_v0.1.json"
STATE_PATH = ROOT / "knowledge/states/P04_CHILDREN_STATE.yaml"


def _audit():
    return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))


def test_ch02_candidate_ids_are_exactly_one_hundred_contiguous_rows():
    audit = _audit()
    ids = [item["legacy_candidate_id"] for item in audit["candidate_adjudications"]]

    assert ids == [f"CH02-{number:03d}" for number in range(101, 201)]
    assert ids[:50] == [f"CH02-{number:03d}" for number in range(101, 151)]
    assert ids[50:] == [f"CH02-{number:03d}" for number in range(151, 201)]
    assert audit["summary"]["candidate_rows"] == 100
    assert audit["summary"]["unique_candidate_ids"] == 100
    assert audit["status"] == "SOURCE_REVIEW_COMPLETE_PENDING_VALIDATION"


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
    assert audit["source"]["reviewed_printed_pages"] == [53, 54, 55]
    assert audit["source"]["reviewed_pdf_physical_pages"] == [27, 28]
    assert audit["boundary"]["candidate_batch_printed_pages"] == [53, 54, 55]
    assert audit["boundary"]["candidate_batch_pdf_physical_pages"] == [27, 28]
    assert audit["candidate_archive"]["reviewed_candidate_id_range"] == ["CH02-101", "CH02-200"]
    assert audit["candidate_archive"]["exact_candidate_id_set_verified"] is True


def test_time_scope_hubs_without_explicit_year_or_decade_are_held():
    audit = _audit()
    held = {
        item["legacy_candidate_id"]: item
        for item in audit["candidate_adjudications"]
        if item["disposition"] == "HELD_TIME_SCOPE_UNRESOLVED"
    }

    assert set(held) == {
        "CH02-102", "CH02-103", "CH02-146",
        "CH02-171", "CH02-172", "CH02-173",
        "CH02-186", "CH02-187", "CH02-188",
        "CH02-199", "CH02-200",
    }
    assert all(item["time_layer"] == "UNRESOLVED" for item in held.values())
    assert all(item["canonical_promotion"] is False for item in held.values())
    assert all(item["source_condition_supported"] is False for item in held.values())
    assert all(item["source_record_ids"] == [] for item in held.values())
    time_gaps = [gap for gap in audit["gap_register"] if "TIME" in gap["gap_id"]]
    assert len(time_gaps) == 5


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
        "CH02-152", "CH02-160", "CH02-161", "CH02-162", "CH02-163",
        "CH02-164", "CH02-165", "CH02-166", "CH02-174", "CH02-175",
        "CH02-189", "CH02-190",
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


def test_explicit_flow_year_and_decade_hubs_keep_both_layers_without_inventing_xing_trigger():
    audit = _audit()
    by_id = {item["legacy_candidate_id"]: item for item in audit["candidate_adjudications"]}
    for candidate_id in ("CH02-157", "CH02-158", "CH02-159"):
        item = by_id[candidate_id]
        assert item["disposition"] == "ACCEPTED_SOURCE_PROJECTION"
        assert item["time_layer"] == "DECADE_YEAR"
        assert item["source_time_layers"] == ["YEAR", "DECADE"]
        assert item["scope_status"] == "SOURCE_EXPLICIT_DECADE_AND_YEAR"
        assert item["legacy_trigger_phrase_supported"] is False
        assert item["adjudicated_projection_mode"] == "SOURCE_DESCRIPTIVE_RESPONSE_HUB"


def test_p04_later_generation_projections_exclude_ordinary_staff_and_general_networks():
    audit = _audit()
    by_id = {item["legacy_candidate_id"]: item for item in audit["candidate_adjudications"]}
    for candidate_id in ("CH02-151", "CH02-178", "CH02-179", "CH02-191", "CH02-195"):
        dependencies = by_id[candidate_id]["context_dependencies"]
        assert "P04_SCOPE_PERSONALLY_CULTIVATED_LATER_GENERATION_ONLY" in dependencies
        assert "P08_EXCLUDE_ORDINARY_STAFF_SUBORDINATES_AND_GENERAL_NETWORKS" in dependencies


def test_historical_ch02_batch_remains_accepted_after_p04_state_advances():
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    summary = audit["summary"]
    assert summary["candidate_rows"] == 100
    assert summary["accepted_reusable_candidate_rows"] == 54
    assert summary["case_support_only_candidate_rows"] == 33
    assert summary["held_time_scope_candidate_rows"] == 11
    assert summary["held_gap_groups"] == 5

    state = STATE_PATH.read_text(encoding="utf-8")
    # The historical CH02 acceptance is immutable, but the P04 recovery cache may advance.
    assert "CH02 (#953/#960) merged at " in state
    assert "76a34c14d73371a96b4144c396a491b23e098b48" in state
    assert any(
        f'status: "{status}"' in state
        for status in ("ACTIVE_BUILD", "READY_TO_INTEGRATE", "INTEGRATING", "ACTIVE_NO_ACTIVE_WORK")
    )
    assert 'active_candidate_batch: "CH02-101…200"' not in state
