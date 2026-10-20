import csv
import json
from collections import Counter
from pathlib import Path

import pytest

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec

ROOT = Path(__file__).resolve().parents[1]
DOC = json.loads((ROOT / "knowledge/wp07a/CAREER_100_REVIEW_06_v0.1.json").read_text())
RECORDS = DOC["mappings"]
BY_ID = {item["source_rule_id"]: item for item in RECORDS}


def _rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _canonical_rows():
    rows = []
    for path in [
        ROOT / "validation/wp05/CA01_career_projection_review_001_100.csv",
        ROOT / "validation/wp05/CA02_career_projection_review_101_200.csv",
        ROOT / "validation/wp05/CA03_career_projection_review_201_300.csv",
        ROOT / "validation/wp05/CA04_career_projection_review_301_400.csv",
        ROOT / "validation/wp05/CA05_career_projection_review_401_500.csv",
        ROOT / "validation/wp05/CA06_career_projection_review_501_600.csv",
        ROOT / "validation/wp05/CA07_career_projection_review_601_700.csv",
        ROOT / "validation/wp05/CA08_career_projection_review_701_800.csv",
        ROOT / "validation/wp05/CA09_career_projection_review_801_888.csv",
    ]:
        rows.extend(_rows(path))
    return rows


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


def test_exact_sixth_hundred_after_552_id_baseline():
    baseline = set()
    for rel in DOC["baseline_mapping_paths"]:
        prior = json.loads((ROOT / rel).read_text())
        baseline.update(
            item["source_rule_id"]
            for item in prior.get("mappings", [])
            if item.get("source_rule_id")
        )
    assert len(baseline) == 552

    expected = [
        row["projection_rule_id"]
        for row in _canonical_rows()
        if row["projection_rule_id"] not in baseline
    ][:100]

    assert len(RECORDS) == 100
    assert [item["source_rule_id"] for item in RECORDS] == expected
    assert RECORDS[0]["source_rule_id"] == "CA06-547"
    assert RECORDS[-1]["source_rule_id"] == "CA07-646"
    assert len(baseline | set(expected)) == 652
    assert DOC["scope"]["reasoning_sub_batches"] == [50, 50]


def test_counts_close_exactly():
    counts = DOC["progress_counts"]
    assert counts["first_time_complete_condition_mappings"] == 20
    assert counts["methodology_or_context_only"] == 10
    assert counts["blocked_outcome_mappings"] == 70
    assert counts["new_production_executable_rules"] == 0
    assert counts["unique_structured_rule_records_before"] == 552
    assert counts["unique_structured_rule_records_after"] == 652
    assert counts["canonical_source_reviewed_before"] == 888
    assert counts["canonical_source_reviewed_after"] == 888
    assert sum([
        counts["first_time_complete_condition_mappings"],
        counts["methodology_or_context_only"],
        counts["blocked_outcome_mappings"],
    ]) == 100


@pytest.mark.parametrize("item", RECORDS, ids=lambda x: x["source_rule_id"])
def test_embedded_source_record_is_canonical(item):
    source_by_id = {row["projection_rule_id"]: row for row in _canonical_rows()}
    source = source_by_id[item["source_rule_id"]]
    assert item["source_record"] == source
    assert item["source_condition_text"] == source["condition"]
    assert item["expected_projection"] == {
        key: source[key]
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


def test_noncomplete_never_becomes_match_all():
    for item in RECORDS:
        if item["review_disposition"] != "COMPLETE_CONDITION_MAPPING":
            assert item["condition"] is None
            assert item["blocker_code"]
            assert item["execution_readiness"].startswith("BLOCKED_")
    assert DOC["guardrails"]["null_condition_must_not_be_coerced_to_empty"] is True


def test_disposition_and_subbatch_closure():
    assert Counter(item["review_disposition"] for item in RECORDS) == {
        "COMPLETE_CONDITION_MAPPING": 20,
        "METHODOLOGY_OR_CONTEXT_ONLY": 10,
        "BLOCKED_OUTCOME_MAPPING": 70,
    }
    assert Counter(item["review_sub_batch"] for item in RECORDS) == {1: 50, 2: 50}


def test_tianfu_composites_and_relations_remain_blocked():
    expected = {
        "CA06-547": "COMPOSITE",
        "CA06-549": "RELATION_AND_GROUP",
        "CA06-554": "RELATION_AND_GROUP",
        "CA06-556": "COMPOSITE",
        "CA06-565": "COMPOSITE",
        "CA06-569": "RELATION",
        "CA06-577": "RELATION",
    }
    for rid, blocker in expected.items():
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] == blocker


def test_dignity_absence_and_temporal_semantics_stay_blocked():
    expected = {
        "CA06-558": "DIGNITY",
        "CA06-574": "ABSENCE_AND_GROUP",
        "CA06-580": "TEMPORAL",
        "CA06-590": "DIGNITY",
        "CA06-600": "TEMPORAL",
        "CA07-616": "ABSENCE",
    }
    for rid, blocker in expected.items():
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] == blocker


def test_taiyin_tianji_dual_geometry_preserves_transformation_carriers():
    spec = BY_ID["CA07-605"]["condition"]
    assert len(spec["alternatives"]) == 2
    same_palace, opposite = spec["alternatives"]

    assert any(
        atom["atom_type"] == "TRANSFORMATION_PRESENT"
        and atom["args"] == {"palace": "P09", "star": "天机", "mutagen": "禄"}
        for atom in same_palace
    )
    assert any(
        atom["atom_type"] == "TRANSFORMATION_PRESENT"
        and atom["args"] == {"palace": "P03", "star": "天机", "mutagen": "禄"}
        for atom in opposite
    )
    assert any(
        atom["atom_type"] == "PALACE_RELATION"
        and atom["args"]["relation"] == "OPPOSITE"
        for atom in opposite
    )


def test_maoyou_taiyin_keeps_tiantong_opposition():
    for rid, branch in [("CA07-612", "酉"), ("CA07-613", "卯")]:
        atoms = _atoms(BY_ID[rid]["condition"])
        assert any(
            atom["atom_type"] == "BRANCH_PRESENT" and atom["args"]["branch"] == branch
            for atom in atoms
        )
        assert any(
            atom["atom_type"] == "PALACE_HAS_STAR"
            and atom["args"] == {"palace": "P03", "star": "天同"}
            for atom in atoms
        )
        assert any(
            atom["atom_type"] == "PALACE_RELATION"
            and atom["args"]["relation"] == "OPPOSITE"
            for atom in atoms
        )


def test_chenxu_taiyin_solar_transformations_are_bound_to_opposite_palace():
    cases = {
        "CA07-614": "忌",
        "CA07-615": "禄",
    }
    for rid, mutagen in cases.items():
        atoms = _atoms(BY_ID[rid]["condition"])
        assert any(
            atom["atom_type"] == "TRANSFORMATION_PRESENT"
            and atom["args"] == {"palace": "P03", "star": "太阳", "mutagen": mutagen}
            for atom in atoms
        )


def test_tanlang_lu_quan_is_alternative_not_impossible_conjunction():
    spec = BY_ID["CA07-624"]["condition"]
    assert "alternatives" in spec
    carriers = []
    for branch in spec["alternatives"]:
        transforms = [
            (atom["args"]["star"], atom["args"]["mutagen"])
            for atom in branch
            if atom["atom_type"] == "TRANSFORMATION_PRESENT"
        ]
        assert len(transforms) == 1
        carriers.extend(transforms)
    assert set(carriers) == {("贪狼", "禄"), ("贪狼", "权")}


def test_food_symbolism_is_not_promoted_to_food_job_rule():
    item = BY_ID["CA07-640"]
    assert item["review_disposition"] == "METHODOLOGY_OR_CONTEXT_ONLY"
    assert item["condition"] is None
    assert item["blocker_code"] == "NOT_AN_EXECUTABLE_OUTCOME_CONDITION"
    assert BY_ID["CA07-641"]["condition"] is None
    assert BY_ID["CA07-641"]["blocker_code"] == "RELATION"


def test_group_terms_remain_conservative():
    for rid in ["CA06-551", "CA07-625", "CA07-626", "CA07-628", "CA07-636", "CA07-638", "CA07-644"]:
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] in {"GROUP", "ABSENCE_AND_GROUP"}


def test_methodology_and_external_context_are_not_direct_rules():
    for rid in ["CA06-571", "CA06-581", "CA06-586", "CA06-587", "CA06-589", "CA07-611", "CA07-618", "CA07-627", "CA07-630", "CA07-640"]:
        assert BY_ID[rid]["review_disposition"] == "METHODOLOGY_OR_CONTEXT_ONLY"
        assert BY_ID[rid]["condition"] is None


def test_preg_inheritance_is_explicit():
    expected = {
        "CA06-550": ["CA06-549"],
        "CA06-552": ["CA06-551"],
        "CA06-557": ["CA06-556"],
        "CA06-566": ["CA06-565"],
        "CA06-573": ["CA06-572"],
        "CA06-580": ["CA06-579"],
        "CA06-591": ["CA06-590"],
        "CA07-603": ["CA07-602"],
        "CA07-634": ["CA07-633"],
        "CA07-639": ["CA07-638"],
    }
    for rid, inherited in expected.items():
        assert BY_ID[rid]["source_context"]["inherited_source_rule_ids"] == inherited


def test_source_spans_cover_printed_pages_146_to_149():
    assert [x["printed_page"] for x in DOC["source_spans"]] == [146, 147, 148, 149]
    assert all(x["visual_reviewed"] for x in DOC["source_spans"])
    assert all(len(x["extracted_text_not_silently_corrected"]) > 500 for x in DOC["source_spans"])


def test_review_remains_nonproduction():
    g = DOC["guardrails"]
    assert g["source_rows_modified"] is False
    assert g["product_runtime_modified"] is False
    assert g["production_registry_modified"] is False
    assert g["new_atoms_or_semantic_defaults"] is False
    assert g["outcome_probability_or_empirical_validity_claimed"] is False
