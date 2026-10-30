import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "knowledge/palaces/P04_children/source_audit/CH03_201_300_SOURCE_AUDIT_v0.1.json"
STATE_PATH = ROOT / "knowledge/states/P04_CHILDREN_STATE.yaml"


def _audit():
    return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))


def test_ch03_candidate_ids_are_exactly_one_hundred_contiguous_rows():
    audit = _audit()
    ids = [item["legacy_candidate_id"] for item in audit["candidate_adjudications"]]
    assert ids == [f"CH03-{number:03d}" for number in range(201, 301)]
    assert ids[:50] == [f"CH03-{number:03d}" for number in range(201, 251)]
    assert ids[50:] == [f"CH03-{number:03d}" for number in range(251, 301)]
    assert audit["summary"]["candidate_rows"] == 100
    assert audit["summary"]["unique_candidate_ids"] == 100


def test_original_pdf_csv_hashes_and_page_boundary_are_pinned():
    audit = _audit()
    assert audit["source"]["source_id"] == "SRC-ZZ-003"
    assert audit["source"]["pdf_sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert audit["candidate_archive"]["git_blob_sha"] == "0dd555154c6d73cfc0a44a335147001c5ef2c30a"
    assert audit["candidate_archive"]["legacy_labels_are_navigation_only"] is True
    assert audit["source"]["reviewed_printed_pages"] == [55, 56]
    assert audit["source"]["reviewed_pdf_physical_pages"] == [28]
    assert audit["boundary"]["visual_pages_inspected"] == [28]
    assert audit["boundary"]["negative_boundaries"][0]["excluded"].startswith("preceding CH02")


def test_temporal_hubs_without_explicit_time_layer_or_trigger_remain_held():
    audit = _audit()
    by_id = {item["legacy_candidate_id"]: item for item in audit["candidate_adjudications"]}
    held_ids = {"CH03-211", "CH03-212", "CH03-228", "CH03-229", "CH03-243", "CH03-270", "CH03-271", "CH03-293", "CH03-294", "CH03-295"}
    assert {k for k, v in by_id.items() if v["disposition"] == "HELD_TIME_SCOPE_UNRESOLVED"} == held_ids
    assert all(by_id[k]["canonical_promotion"] is False for k in held_ids)
    assert all(by_id[k]["time_layer"] == "UNRESOLVED" for k in held_ids)
    assert by_id["CH03-243"]["legacy_trigger_phrase_supported"] is True
    assert by_id["CH03-243"]["scope_status"] == "SOURCE_TRIGGER_EXPLICIT_TIME_LAYER_UNSPECIFIED"
    assert by_id["CH03-211"]["legacy_trigger_phrase_supported"] is False


def test_explicit_flow_year_decade_hubs_keep_both_layers_without_inventing_xing_trigger():
    audit = _audit()
    by_id = {item["legacy_candidate_id"]: item for item in audit["candidate_adjudications"]}
    for candidate_id in ("CH03-244", "CH03-245", "CH03-280", "CH03-281", "CH03-282"):
        item = by_id[candidate_id]
        assert item["disposition"] == "ACCEPTED_SOURCE_PROJECTION"
        assert item["time_layer"] == "DECADE_YEAR"
        assert item["source_time_layers"] == ["YEAR", "DECADE"]
        assert item["scope_status"] == "SOURCE_EXPLICIT_DECADE_AND_YEAR"
        assert item["legacy_trigger_phrase_supported"] is False
        assert item["adjudicated_projection_mode"] == "SOURCE_DESCRIPTIVE_RESPONSE_HUB"


def test_ambiguous_yunxian_nianxian_wording_is_preserved_not_normalized():
    audit = _audit()
    by_id = {item["legacy_candidate_id"]: item for item in audit["candidate_adjudications"]}
    for candidate_id in ("CH03-293", "CH03-294", "CH03-295"):
        assert by_id[candidate_id]["source_time_expression"] == "运限年限；原文用语未在当前共享语义中定型"
        assert by_id[candidate_id]["time_layer"] == "UNRESOLVED"


def test_child_count_and_concrete_family_claims_remain_case_only():
    audit = _audit()
    by_id = {item["legacy_candidate_id"]: item for item in audit["candidate_adjudications"]}
    expected = "\"CH03-202\", \"CH03-203\", \"CH03-204\", \"CH03-205\", \"CH03-206\", \"CH03-207\", \"CH03-208\", \"CH03-215\", \"CH03-216\", \"CH03-218\", \"CH03-219\", \"CH03-220\", \"CH03-221\", \"CH03-224\", \"CH03-230\", \"CH03-231\", \"CH03-232\", \"CH03-233\", \"CH03-234\", \"CH03-235\", \"CH03-246\", \"CH03-256\", \"CH03-259\", \"CH03-260\", \"CH03-272\", \"CH03-273\", \"CH03-287\", \"CH03-288\", \"CH03-296\", \"CH03-297\""
    assert all(by_id[item]["disposition"] == "CASE_SUPPORT_ONLY" for item in expected)
    assert all(by_id[item]["case_support_only"] is True for item in expected)
    assert by_id["CH03-204"]["disposition"] == "CASE_SUPPORT_ONLY"


def test_duplicate_candidate_213_is_not_promoted_twice():
    audit = _audit()
    item = next(x for x in audit["candidate_adjudications"] if x["legacy_candidate_id"] == "CH03-213")
    assert item["disposition"] == "DUPLICATE_PRIOR_SOURCE_SCOPE"
    assert item["source_record_ids"] == []
    assert item["duplicate_of_source_record_ids"] == ["P04S-126", "P04S-127", "P04S-128"]


def test_unindexed_general_solar_source_atoms_are_registered():
    audit = _audit()
    atoms = audit["unindexed_source_atoms"]
    assert {x["source_atom_id"] for x in atoms} == {"CH03-U01", "CH03-U02", "CH03-U03", "CH03-U04"}
    assert len({x["source_record_id"] for x in atoms}) == 4
    assert all(x["source_text_directly_reviewed"] and x["source_location_revalidated"] for x in atoms)
    assert all(x["executable"] is False and x["canonical_mapping_approved"] is False for x in atoms)


def test_later_generation_and_cross_palace_boundaries_are_explicit():
    audit = _audit()
    by_id = {item["legacy_candidate_id"]: item for item in audit["candidate_adjudications"]}
    for candidate_id in ("CH03-227", "CH03-238", "CH03-258", "CH03-266", "CH03-276", "CH03-298"):
        deps = by_id[candidate_id]["context_dependencies"]
        assert "P04_SCOPE_PERSONALLY_CULTIVATED_LATER_GENERATION_ONLY" in deps
        assert "P08_EXCLUDE_ORDINARY_STAFF_SUBORDINATES_AND_GENERAL_NETWORKS" in deps
    assert "CROSS_PALACE_JUMEN_POSITION_REQUIRED" in by_id["CH03-276"]["context_dependencies"]
    assert "P03_SPOUSE_PALACE_REQUIRED_FOR_PARENTAL_SEPARATION_CHECK" in by_id["CH03-300"]["context_dependencies"]
    assert {"CH03-U04"} <= {x["source_atom_id"] for x in audit["unindexed_source_atoms"]}


def test_every_proposed_record_remains_non_executable_and_mapping_unapproved():
    audit = _audit()
    all_records = audit["candidate_adjudications"] + audit["unindexed_source_atoms"]
    assert all(x["source_text_directly_reviewed"] and x["source_location_revalidated"] for x in all_records)
    assert all(x["executable"] is False for x in all_records)
    assert all(x["canonical_mapping_approved"] is False for x in all_records)
    assert all(x["history_feedback"] is False for x in all_records)
    assert audit["execution_boundary"]["source_records_executable"] == 0
    assert audit["execution_boundary"]["conditions_compiled"] == 0
    assert audit["execution_boundary"]["execution_unlocked"] == 0
    assert audit["execution_boundary"]["product_or_kib_authorized"] is False


def test_p04_state_cache_tracks_ch03_active_work():
    state = STATE_PATH.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_BUILD"' in state
    assert "active_issue: 967" in state
    assert 'active_candidate_batch: "CH03-201…300"' in state
    assert "proposed_reusable_source_records: 62" in state
    assert "proposed_case_support_only_source_records: 30" in state
    assert "proposed_held_candidates: 11" in state


def test_literal_fuli_term_is_preserved_and_held():
    audit = _audit()
    item = next(x for x in audit["candidate_adjudications"] if x["legacy_candidate_id"] == "CH03-217")
    assert item["disposition"] == "HELD_SOURCE_TERM_UNRESOLVED"
    assert item["adjudicated_source_condition"].endswith("“子女易抚离”")
    assert item["source_condition_supported"] is True
    assert item["canonical_promotion"] is False
    assert item["source_record_ids"] == []
    assert item["gap_id"] == "P04-CH03-GAP-TERM-01"
    gap = next(x for x in audit["gap_register"] if x["gap_id"] == "P04-CH03-GAP-TERM-01")
    assert gap["candidate_ids"] == ["CH03-217"]
