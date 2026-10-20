import csv
import json
from collections import Counter
from pathlib import Path

import pytest

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec

ROOT = Path(__file__).resolve().parents[1]
DOC = json.loads((ROOT / "knowledge/wp07a/CAREER_100_REVIEW_04_v0.1.json").read_text())
RECORDS = DOC["mappings"]
BY_ID = {item["source_rule_id"]: item for item in RECORDS}


def _rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _source_rows():
    return (
        _rows(ROOT / "validation/wp05/CA04_career_projection_review_301_400.csv")
        + _rows(ROOT / "validation/wp05/CA05_career_projection_review_401_500.csv")
    )


def _atoms(spec):
    out = []
    for atom in spec.get("all_of", []):
        out.append(atom)
    for group in spec.get("any_of", []):
        out.extend(group)
    for atom in spec.get("none_of", []):
        out.append(atom)
    for branch in spec.get("alternatives", []):
        out.extend(branch)
    return out


def test_exact_fourth_hundred_selection_and_counts():
    source = _source_rows()
    excluded = {"CA04-347", "CA04-349", "CA05-403"}
    expected = [
        row["projection_rule_id"]
        for row in source
        if (
            row["projection_rule_id"].startswith("CA04-")
            and int(row["projection_rule_id"].split("-")[1]) >= 343
        )
        or (
            row["projection_rule_id"].startswith("CA05-")
            and int(row["projection_rule_id"].split("-")[1]) <= 445
        )
    ]
    expected = [rid for rid in expected if rid not in excluded]

    assert len(RECORDS) == 100
    assert [item["source_rule_id"] for item in RECORDS] == expected
    assert RECORDS[0]["source_rule_id"] == "CA04-343"
    assert RECORDS[-1]["source_rule_id"] == "CA05-445"
    assert DOC["scope"]["reasoning_sub_batches"] == [50, 50]

    counts = DOC["progress_counts"]
    assert counts["first_time_complete_condition_mappings"] == 31
    assert counts["methodology_or_context_only"] == 11
    assert counts["blocked_outcome_mappings"] == 58
    assert counts["new_production_executable_rules"] == 0
    assert counts["unique_structured_rule_records_before"] == 352
    assert counts["unique_structured_rule_records_after"] == 452
    assert counts["canonical_source_reviewed_before"] == 888
    assert counts["canonical_source_reviewed_after"] == 888


@pytest.mark.parametrize("item", RECORDS, ids=lambda x: x["source_rule_id"])
def test_each_embedded_source_record_matches_canonical_csv(item):
    source_by_id = {row["projection_rule_id"]: row for row in _source_rows()}
    assert item["source_record"] == source_by_id[item["source_rule_id"]]
    assert item["source_condition_text"] == item["source_record"]["condition"]
    assert item["expected_projection"] == {
        key: item["source_record"][key]
        for key in ("projection_domain", "projection_target", "projection_mode")
    }
    assert item["executable_registry_entry"] is False
    assert len(item["review_reason_zh"]) > 20


@pytest.mark.parametrize(
    "item",
    [x for x in RECORDS if x["review_disposition"] == "COMPLETE_CONDITION_MAPPING"],
    ids=lambda x: x["source_rule_id"],
)
def test_complete_conditions_compile_with_existing_atoms_only(item):
    assert item["condition"] is not None
    atoms = _atoms(item["condition"])
    assert atoms
    assert {atom["atom_type"] for atom in atoms} <= ALLOWED_ATOM_TYPES
    compile_condition_spec(item["condition"])


def test_non_complete_records_never_become_match_all():
    for item in RECORDS:
        if item["review_disposition"] != "COMPLETE_CONDITION_MAPPING":
            assert item["condition"] is None
            assert item["blocker_code"]
            assert item["execution_readiness"].startswith("BLOCKED_")
    assert DOC["guardrails"]["null_condition_must_not_be_coerced_to_empty"] is True


def test_disposition_closure_and_sub_batches():
    counts = Counter(item["review_disposition"] for item in RECORDS)
    assert counts == {
        "COMPLETE_CONDITION_MAPPING": 31,
        "METHODOLOGY_OR_CONTEXT_ONLY": 11,
        "BLOCKED_OUTCOME_MAPPING": 58,
    }
    assert Counter(item["review_sub_batch"] for item in RECORDS) == {1: 50, 2: 50}


def test_red_team_keeps_ambiguous_group_quantifiers_blocked():
    for rid in ["CA04-343", "CA04-391", "CA05-409", "CA05-416", "CA05-417", "CA05-433"]:
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] in {"GROUP", "RELATION_AND_GROUP"}


def test_temporal_and_real_world_conditions_stay_out_of_static_matching():
    for rid in ["CA04-346", "CA04-350", "CA05-402", "CA05-439"]:
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] == "TEMPORAL"
    for rid in ["CA04-348", "CA05-404", "CA05-445"]:
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] == "CONTEXT_STATE"


def test_named_or_unmodeled_structures_are_not_approximated():
    for rid in ["CA04-373", "CA04-374", "CA04-377", "CA04-385"]:
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] == "COMPOSITE"
    assert BY_ID["CA05-422"]["condition"] is None
    assert BY_ID["CA05-422"]["blocker_code"] == "UNMODELED_STATE"


def test_precise_transformation_carriers_are_preserved():
    wu_tan = BY_ID["CA04-369"]["condition"]["alternatives"]
    carriers = {
        (atom["args"]["star"], atom["args"]["mutagen"])
        for branch in wu_tan
        for atom in branch
        if atom["atom_type"] == "TRANSFORMATION_PRESENT"
    }
    assert carriers == {("武曲", "禄"), ("贪狼", "权")}

    tong_yin = BY_ID["CA05-426"]["condition"]["alternatives"]
    assert all(
        any(
            atom["atom_type"] == "TRANSFORMATION_PRESENT"
            and atom["args"]["star"] == "太阴"
            and atom["args"]["mutagen"] == "忌"
            for atom in branch
        )
        for branch in tong_yin
    )

    tong_ji = BY_ID["CA05-428"]["condition"]["alternatives"]
    assert all(
        any(
            atom["atom_type"] == "TRANSFORMATION_PRESENT"
            and atom["args"]["star"] == "天同"
            and atom["args"]["mutagen"] == "忌"
            for atom in branch
        )
        for branch in tong_ji
    )


def test_branch_specific_wuqu_qisha_firestar_difference_is_preserved():
    assert any(
        atom["atom_type"] == "BRANCH_PRESENT" and atom["args"]["branch"] == "酉"
        for atom in BY_ID["CA04-380"]["condition"]["all_of"]
    )
    assert any(
        atom["atom_type"] == "BRANCH_PRESENT" and atom["args"]["branch"] == "卯"
        for atom in BY_ID["CA04-381"]["condition"]["all_of"]
    )


def test_preg_inheritance_is_explicit_for_key_records():
    expected = {
        "CA04-346": ["CA04-345"],
        "CA04-353": ["CA04-352"],
        "CA04-396": ["CA04-395"],
        "CA04-399": ["CA04-398"],
        "CA05-402": ["CA05-401"],
        "CA05-427": ["CA05-426"],
        "CA05-431": ["CA05-430"],
        "CA05-443": ["CA05-442"],
    }
    for rid, inherited in expected.items():
        assert BY_ID[rid]["source_context"]["inherited_source_rule_ids"] == inherited


def test_source_spans_cover_printed_pages_140_to_143():
    assert [x["printed_page"] for x in DOC["source_spans"]] == [140, 141, 142, 143]
    assert all(x["visual_reviewed"] for x in DOC["source_spans"])
    assert all(len(x["extracted_text_not_silently_corrected"]) > 500 for x in DOC["source_spans"])


def test_guardrails_keep_review_non_production():
    g = DOC["guardrails"]
    assert g["source_rows_modified"] is False
    assert g["product_runtime_modified"] is False
    assert g["production_registry_modified"] is False
    assert g["new_atoms_or_semantic_defaults"] is False
    assert g["outcome_probability_or_empirical_validity_claimed"] is False
