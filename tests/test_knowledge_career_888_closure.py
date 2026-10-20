import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec

ROOT = Path(__file__).resolve().parents[1]
TAIL = json.loads((ROOT / "knowledge/wp07a/CAREER_FINAL36_CLOSURE_v0.1.json").read_text())
CLOSURE = json.loads((ROOT / "knowledge/wp07a/CAREER_888_CLOSURE_AUDIT_v0.1.json").read_text())
RECORDS = TAIL["mappings"]
BY_ID = {item["source_rule_id"]: item for item in RECORDS}


def canonical_rows():
    rows = []
    for filename in [
        "CA01_career_projection_review_001_100.csv",
        "CA02_career_projection_review_101_200.csv",
        "CA03_career_projection_review_201_300.csv",
        "CA04_career_projection_review_301_400.csv",
        "CA05_career_projection_review_401_500.csv",
        "CA06_career_projection_review_501_600.csv",
        "CA07_career_projection_review_601_700.csv",
        "CA08_career_projection_review_701_800.csv",
        "CA09_career_projection_review_801_888.csv",
    ]:
        with (ROOT / "validation/wp05" / filename).open(encoding="utf-8-sig", newline="") as handle:
            rows.extend(csv.DictReader(handle))
    return rows


def atoms(spec):
    out = list(spec.get("all_of", [])) + list(spec.get("none_of", []))
    for group in spec.get("any_of", []):
        out.extend(group)
    for group in spec.get("alternatives", []):
        out.extend(group)
    return out


def test_final36_is_exact_canonical_remainder_after_852_baseline():
    baseline = set()
    for rel in TAIL["baseline_mapping_paths"]:
        prior = json.loads((ROOT / rel).read_text())
        baseline.update(
            item["source_rule_id"]
            for item in prior.get("mappings", [])
            if item.get("source_rule_id")
        )
    assert len(baseline) == 852

    canonical = canonical_rows()
    canonical_ids = [row["projection_rule_id"] for row in canonical]
    expected = [rid for rid in canonical_ids if rid not in baseline]

    assert len(expected) == 36
    assert [item["source_rule_id"] for item in RECORDS] == expected
    assert expected[0] == "CA09-853"
    assert expected[-1] == "CA09-888"
    assert "CA09-852" in baseline
    assert len(baseline | set(expected)) == 888
    assert baseline | set(expected) == set(canonical_ids)


def test_full_888_union_has_no_missing_or_extra_ids():
    structured = set()
    for rel in TAIL["baseline_mapping_paths"] + ["knowledge/wp07a/CAREER_FINAL36_CLOSURE_v0.1.json"]:
        data = json.loads((ROOT / rel).read_text())
        structured.update(
            item["source_rule_id"]
            for item in data.get("mappings", [])
            if item.get("source_rule_id")
        )
    canonical_ids = {row["projection_rule_id"] for row in canonical_rows()}
    assert len(canonical_ids) == 888
    assert len(structured) == 888
    assert structured == canonical_ids


def test_tail_counts_close_exactly():
    counts = TAIL["progress_counts"]
    assert counts["source_rules_rechecked"] == 36
    assert counts["first_time_complete_condition_mappings"] == 7
    assert counts["methodology_or_context_only"] == 2
    assert counts["blocked_outcome_mappings"] == 27
    assert counts["new_production_executable_rules"] == 0
    assert counts["unique_structured_rule_records_before"] == 852
    assert counts["unique_structured_rule_records_after"] == 888
    assert 7 + 2 + 27 == 36


def test_closure_census_is_consistent():
    assert CLOSURE["canonical_source_rules"] == 888
    assert CLOSURE["structured_unique_ids_expected"] == 888
    assert CLOSURE["strict_review_disposition_rows"] == 836
    assert CLOSURE["pre_hundred_batch_specialized_structured_ids"] == 52
    assert CLOSURE["disposition_totals"] == {
        "COMPLETE_CONDITION_MAPPING": 216,
        "METHODOLOGY_OR_CONTEXT_ONLY": 107,
        "BLOCKED_OUTCOME_MAPPING": 513,
    }
    assert sum(CLOSURE["blocker_totals"].values()) == 513


def test_embedded_tail_rows_match_canonical():
    source = {row["projection_rule_id"]: row for row in canonical_rows()}
    for item in RECORDS:
        assert item["source_record"] == source[item["source_rule_id"]]
        assert item["source_condition_text"] == item["source_record"]["condition"]
        assert item["source_provenance"]["history_feedback"] == item["source_record"]["history_feedback"]


def test_complete_tail_conditions_use_only_existing_atoms():
    for item in RECORDS:
        if item["review_disposition"] == "COMPLETE_CONDITION_MAPPING":
            assert item["condition"] is not None
            aa = atoms(item["condition"])
            assert aa
            assert {atom["atom_type"] for atom in aa} <= ALLOWED_ATOM_TYPES
            compile_condition_spec(item["condition"])
        else:
            assert item["condition"] is None
            assert item["blocker_code"]


def test_path_temporal_gender_and_behavior_boundaries():
    assert BY_ID["CA09-853"]["source_provenance"]["history_feedback"] == "PATH_DEPENDENT_GATE"
    assert BY_ID["CA09-853"]["execution_readiness"] == "BLOCKED_PATH_DEPENDENT_TARGET"
    assert BY_ID["CA09-867"]["blocker_code"] == "TEMPORAL"
    assert BY_ID["CA09-867"]["source_provenance"]["time_layer"] == "YEAR"
    assert BY_ID["CA09-872"]["blocker_code"] == "UNMODELED_STATE"
    for rid in ["CA09-855", "CA09-868", "CA09-869", "CA09-881", "CA09-883", "CA09-888"]:
        assert BY_ID[rid]["blocker_code"] == "CONTEXT_STATE"
        assert BY_ID[rid]["condition"] is None


def test_ambiguous_meetings_and_groups_remain_blocked():
    for rid in ["CA09-859", "CA09-860", "CA09-861"]:
        assert BY_ID[rid]["blocker_code"] == "RELATION_AND_GROUP"
    for rid in ["CA09-863", "CA09-864", "CA09-865", "CA09-886", "CA09-887"]:
        assert BY_ID[rid]["blocker_code"] == "GROUP"
    for rid in ["CA09-875", "CA09-876"]:
        assert BY_ID[rid]["blocker_code"] == "RELATION"


def test_explicit_branch_structures_are_preserved():
    for rid, branches in [
        ("CA09-870", {"子", "午"}),
        ("CA09-873", {"寅", "申"}),
        ("CA09-878", {"寅", "申"}),
        ("CA09-880", {"寅", "申"}),
        ("CA09-882", {"辰", "戌"}),
    ]:
        spec = BY_ID[rid]["condition"]
        seen = {
            atom["args"]["branch"]
            for atom in atoms(spec)
            if atom["atom_type"] == "BRANCH_PRESENT"
        }
        assert seen == branches


def test_tail_source_spans_and_nonproduction_boundary():
    assert [span["printed_page"] for span in TAIL["source_spans"]] == [154, 155]
    assert all(span["visual_reviewed"] for span in TAIL["source_spans"])
    assert all(len(span["extracted_text_not_silently_corrected"]) > 500 for span in TAIL["source_spans"])
    assert all(item["executable_registry_entry"] is False for item in RECORDS)
    assert TAIL["guardrails"]["production_registry_modified"] is False
    assert TAIL["guardrails"]["new_atoms_or_semantic_defaults"] is False
    assert TAIL["guardrails"]["closure_means_review_coverage_not_executability"] is True
