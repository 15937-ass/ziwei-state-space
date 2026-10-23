import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "knowledge/core/wp07b/TEMPORAL_REACTION_SOURCE_HANDOFF_v0.1.json"


def data():
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_wp07b_source_census_and_source_record_join_are_exact():
    d = data()
    rows = d["candidate_dispositions"]
    assert d["schema_version"] == "0.1"
    assert d["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert len(rows) == 44
    assert len({row["rule_id"] for row in rows}) == 44
    assert d["counts"]["career"] == {
        "candidates": 9,
        "eligible_current_contract": 0,
        "case_support_only": 1,
        "blocked_reusable": 8,
    }
    assert d["counts"]["property"] == {
        "candidates": 35,
        "eligible_current_contract": 0,
        "case_support_only": 16,
        "blocked_reusable": 19,
        "declared_year": 32,
        "declared_decade": 3,
    }
    assert d["counts"]["total"] == {
        "candidates": 44,
        "eligible_current_contract": 0,
        "case_support_only": 17,
        "blocked_reusable": 27,
    }
    for row in rows:
        span = row["source_span"]
        assert span["source_id"] == "SRC-ZZ-003"
        assert span["source_location"]
        assert span["source_condition_anchor"]
        assert span["source_span_verified"] is True
        assert span["source_record_path"]
        printed_page = int(span["source_location"].split("printed_p", 1)[1])
        assert span["scan_pdf_page_1based"] == (printed_page + 1) // 2
        assert span["scan_visual_reviewed"] is True
        assert row["blocker_codes"]
        assert row["current_contract_eligible"] is False
        assert row["production_authorization"] == "NONE"


def test_case_support_and_event_candidates_never_become_runtime_reactions():
    d = data()
    case_rows = [r for r in d["candidate_dispositions"] if r["case_support_only"]]
    assert len(case_rows) == 17
    assert all(not r["current_contract_eligible"] for r in case_rows)
    assert all(r["normalization_status"] == "EXCLUDED_FROM_EXECUTABLE_NORMALIZATION" for r in case_rows)
    assert all("WP07B-GAP-013-CASE-SUPPORT-EXCLUSION" in r["gap_ids"] for r in case_rows)


def test_near_ready_rows_remain_blocked_for_source_fidelity_reasons():
    by_id = {r["rule_id"]: r for r in data()["candidate_dispositions"]}

    for rule_id in ("TP03-245", "TP03-246"):
        row = by_id[rule_id]
        assert row["eligibility_status"] == "BLOCKED_COMPILER_NATAL_ANTECEDENT"
        assert "REQUIRED_NATAL_ANTECEDENT_ABSENT_IN_SOURCE" in row["blocker_codes"]
        assert row["current_contract_eligible"] is False
        assert "WP07B-GAP-010-PURE-TEMPORAL-TRIGGER" in row["gap_ids"]

    for rule_id in ("TP04-307", "TP04-308"):
        row = by_id[rule_id]
        assert row["eligibility_status"] == "BLOCKED_TEMPORAL_STAR_TRANSFORMATION_BINDING"
        assert "SCOPE_LEVEL_MUTAGEN_MUST_NOT_BE_JOINED_TO_STAR" in row["blocker_codes"]
        assert row["current_contract_eligible"] is False
        assert "SOURCE_NATAL_CONTEXT_READY" not in row["blocker_codes"]
        assert "SOURCE_NATAL_CONTEXT_READY" in row["source_status_codes"]
        assert "WP07B-GAP-004-STAR-MUTAGEN-BINDING" in row["gap_ids"]

    multi_year = by_id["CA09-851"]
    assert multi_year["current_contract_eligible"] is False
    assert "MULTIYEAR_SEQUENCE_NOT_SUPPORTED" in multi_year["blocker_codes"]
    assert "DURATION_IS_EVIDENCE_NOT_THRESHOLD" in multi_year["blocker_codes"]
    assert "WP07B-GAP-007-PERSISTENCE-AND-PATH" in multi_year["gap_ids"]


def test_source_scope_and_uncertainty_are_preserved_not_silently_normalized():
    by_id = {r["rule_id"]: r for r in data()["candidate_dispositions"]}
    for rule_id in ("CA04-346", "CA04-350", "CA05-496"):
        span = by_id[rule_id]["source_span"]
        assert set(span["source_scope_layers"]) == {"DECADE", "YEAR"}
        assert span["declared_time_layer"] == "DECADE"

    tp044 = by_id["TP01-044"]["source_span"]
    assert set(tp044["source_scope_layers"]) == {"DECADE", "YEAR"}
    assert "SOURCE_TEXT_UNCERTAIN" in by_id["TP01-037"]["blocker_codes"]
    assert "SOURCE_TEXT_UNCERTAIN_OR_OCR_UNCERTAIN" in by_id["TP01-037"]["uncertainty_flags"]


def test_no_new_semantics_or_product_runtime_authorization_is_created():
    d = data()
    decision = d["decision"]
    assert decision["executable_pilot_emitted"] is False
    assert decision["production_temporal_reaction_registry_mutated"] is False
    assert decision["product_knowledge_lock_mutated"] is False
    assert decision["new_shared_semantics_created"] is False
    assert decision["new_runtime_atom_created"] is False
    assert decision["new_time_scale_created"] is False
    assert decision["numeric_weight_added"] == 0
    assert decision["probability_added"] == 0
    assert decision["duration_threshold_added"] == 0
    assert decision["source_truth_changed"] is False


def test_gap_and_future_gate_ids_have_traceable_impacted_rule_ids():
    d = data()
    rule_ids = {r["rule_id"] for r in d["candidate_dispositions"]}
    assert d["gap_register"]
    for gap in d["gap_register"]:
        assert gap["gap_id"].startswith("WP07B-GAP-")
        assert gap["runtime_semantics_added"] is False
        assert set(gap["impacted_rule_ids"]) <= rule_ids
    for gate in d["human_gate_candidates"]:
        assert gate["gate_candidate_id"].startswith("HG-WP07B-")
        assert gate["status"] == "FUTURE_NOT_PENDING"
        assert gate["no_decision_made"] is True
        assert set(gate["impacted_rule_ids"]) <= rule_ids



def test_ca04_350_reaudit_retires_stale_star_binding_blocker_only():
    d = data()
    by_id = {r["rule_id"]: r for r in d["candidate_dispositions"]}
    row = by_id["CA04-350"]

    assert row["current_contract_eligible"] is False
    assert row["original_eligibility_status"] == "BLOCKED_TEMPORAL_FACT_BINDING_AND_SCOPE"
    assert "STAR_MUTAGEN_BINDING_GAP" in row["original_blocker_codes"]
    assert row["eligibility_status"] == "BLOCKED_COMMERCE_CONTEXT_AND_SCOPE"
    assert "STAR_MUTAGEN_BINDING_GAP" not in row["blocker_codes"]
    assert "REAL_WORLD_COMMERCE_CONTEXT_UNTYPED" in row["blocker_codes"]
    assert "LAYER_SCOPE_MISMATCH" in row["blocker_codes"]
    assert "WP07B-GAP-014-COMMERCE-CONTEXT" in row["gap_ids"]
    assert "WP07B-GAP-004-STAR-MUTAGEN-BINDING" not in row["gap_ids"]
    assert "CONTEXT_DEPENDENT_COMMERCE_GATE" in row["current_contract_gap"]
    assert "CA04-349" in row["current_contract_gap"]

    gap_by_id = {g["gap_id"]: g for g in d["gap_register"]}
    assert "CA04-350" not in gap_by_id["WP07B-GAP-004-STAR-MUTAGEN-BINDING"]["impacted_rule_ids"]
    assert set(gap_by_id["WP07B-GAP-004-STAR-MUTAGEN-BINDING"]["impacted_rule_ids"]) >= {
        "TP01-061", "TP04-307", "TP04-308"
    }
    assert gap_by_id["WP07B-GAP-014-COMMERCE-CONTEXT"]["impacted_rule_ids"] == ["CA04-350"]
    assert gap_by_id["WP07B-GAP-014-COMMERCE-CONTEXT"]["runtime_semantics_added"] is False


def test_source_scan_review_covers_all_printed_page_anchors():
    d = data()
    scan = d["snapshot"]["source_scan_review"]
    assert scan["status"] == "VISUALLY_REVIEWED"
    assert scan["source_id"] == "SRC-ZZ-003"
    assert scan["scan_pdf_pages_1based"] == [70, 71, 73, 74, 77, 78, 79, 80, 81, 82, 83]
    assert all(
        row["source_span"]["scan_visual_reviewed"] is True
        for row in d["candidate_dispositions"]
    )


def test_blocker_code_counts_match_current_reaudit_dispositions():
    d = data()
    expected = {}
    for row in d["candidate_dispositions"]:
        for code in row["blocker_codes"]:
            expected[code] = expected.get(code, 0) + 1
    assert d["blocker_code_counts"] == expected
    assert "STAR_MUTAGEN_BINDING_GAP" not in d["blocker_code_counts"]
    assert d["blocker_code_counts"]["REAL_WORLD_COMMERCE_CONTEXT_UNTYPED"] == 1


def test_blocker_code_aggregate_matches_current_candidate_dispositions():
    d = data()
    counts = Counter(
        code
        for row in d["candidate_dispositions"]
        for code in row["blocker_codes"]
    )
    assert d["blocker_code_counts"] == dict(sorted(counts.items()))


def test_original_eligibility_status_and_blockers_are_preserved_for_all_candidates():
    d = data()
    by_id = {r["rule_id"]: r for r in d["candidate_dispositions"]}
    inputs = (
        ROOT / "knowledge/wp07b/CAREER_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv",
        ROOT / "knowledge/palaces/P10_property/wp07b/PROPERTY_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv",
    )
    source_rows = []
    for path in inputs:
        with path.open(encoding="utf-8", newline="") as handle:
            source_rows.extend(csv.DictReader(handle))

    assert len(source_rows) == 44
    for source in source_rows:
        row = by_id[source["candidate_id"]]
        assert row["original_eligibility_status"] == source["eligibility_status"]
        assert row["original_blocker_codes"] == [
            code for code in source["blocking_reasons"].split("|") if code
        ]
