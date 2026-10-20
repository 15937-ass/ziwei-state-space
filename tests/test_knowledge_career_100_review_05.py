import csv
import json
from collections import Counter
from pathlib import Path

import pytest

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec

ROOT = Path(__file__).resolve().parents[1]
DOC = json.loads((ROOT / "knowledge/wp07a/CAREER_100_REVIEW_05_v0.1.json").read_text())
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


def test_exact_fifth_hundred_after_452_id_baseline():
    baseline = set()
    for rel in DOC["baseline_mapping_paths"]:
        prior = json.loads((ROOT / rel).read_text())
        baseline.update(
            item["source_rule_id"]
            for item in prior.get("mappings", [])
            if item.get("source_rule_id")
        )
    assert len(baseline) == 452

    expected = [
        row["projection_rule_id"]
        for row in _canonical_rows()
        if row["projection_rule_id"] not in baseline
    ][:100]

    assert len(RECORDS) == 100
    assert [item["source_rule_id"] for item in RECORDS] == expected
    assert RECORDS[0]["source_rule_id"] == "CA05-446"
    assert RECORDS[-1]["source_rule_id"] == "CA06-546"
    assert "CA05-469" not in expected
    assert len(baseline | set(expected)) == 552
    assert DOC["scope"]["reasoning_sub_batches"] == [50, 50]


def test_counts_close_exactly():
    counts = DOC["progress_counts"]
    assert counts["first_time_complete_condition_mappings"] == 27
    assert counts["methodology_or_context_only"] == 17
    assert counts["blocked_outcome_mappings"] == 56
    assert counts["new_production_executable_rules"] == 0
    assert counts["unique_structured_rule_records_before"] == 452
    assert counts["unique_structured_rule_records_after"] == 552
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
        "COMPLETE_CONDITION_MAPPING": 27,
        "METHODOLOGY_OR_CONTEXT_ONLY": 17,
        "BLOCKED_OUTCOME_MAPPING": 56,
    }
    assert Counter(item["review_sub_batch"] for item in RECORDS) == {1: 50, 2: 50}


def test_tiantong_six_palace_contexts_do_not_collapse_into_tongliang():
    assert BY_ID["CA05-453"]["source_context"]["paragraph_scope"].startswith("卯酉")
    assert BY_ID["CA05-455"]["source_context"]["paragraph_scope"].startswith("辰戌")
    assert BY_ID["CA05-456"]["source_context"]["paragraph_scope"].startswith("巳亥")
    assert BY_ID["CA05-453"]["condition"] is not None
    assert BY_ID["CA05-456"]["condition"] is None


def test_ca06_501_remains_yinshen_lianzhen_opposite_tanlang_context():
    item = BY_ID["CA06-501"]
    assert item["source_context"]["paragraph_scope"].startswith("寅申")
    atoms = _atoms(item["source_context"]["supported_chart_context_only"])
    assert any(
        atom["atom_type"] == "PALACE_RELATION"
        and atom["args"]["relation"] == "OPPOSITE"
        for atom in atoms
    )
    assert item["condition"] is None


def test_dignity_group_absence_and_temporal_semantics_stay_blocked():
    expected = {
        "CA05-459": "DIGNITY_AND_GROUP",
        "CA05-473": "ABSENCE_AND_GROUP",
        "CA05-496": "TEMPORAL",
        "CA06-536": "DIGNITY",
        "CA06-541": "ABSENCE",
        "CA06-545": "TEMPORAL",
    }
    for rid, blocker in expected.items():
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] == blocker


def test_real_world_choices_are_not_inferred_from_chart():
    for rid in ["CA05-487", "CA05-499", "CA05-500", "CA06-521"]:
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] == "CONTEXT_STATE"


def test_named_and_flanking_structures_are_not_approximated():
    for rid in ["CA05-485", "CA05-486", "CA05-489", "CA05-491", "CA06-540"]:
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] == "COMPOSITE"


def test_explicit_transformation_carriers_are_preserved():
    cases = {
        "CA06-503": ("廉贞", "禄"),
        "CA06-504": ("破军", "禄"),
        "CA06-514": ("廉贞", "禄"),
        "CA06-515": ("天府", "科"),
        "CA06-518": ("廉贞", "忌"),
        "CA06-527": ("贪狼", "忌"),
        "CA06-528": ("廉贞", "忌"),
    }
    for rid, expected in cases.items():
        carriers = {
            (atom["args"]["star"], atom["args"]["mutagen"])
            for atom in _atoms(BY_ID[rid]["condition"])
            if atom["atom_type"] == "TRANSFORMATION_PRESENT"
        }
        assert expected in carriers


def test_methodology_and_examples_do_not_activate_direct_rules():
    for rid in ["CA05-458", "CA05-470", "CA05-474", "CA05-477", "CA06-517", "CA06-529", "CA06-535", "CA06-546"]:
        assert BY_ID[rid]["review_disposition"] == "METHODOLOGY_OR_CONTEXT_ONLY"
        assert BY_ID[rid]["condition"] is None


def test_preg_inheritance_is_explicit():
    expected = {
        "CA05-448": ["CA05-447"],
        "CA05-454": ["CA05-453"],
        "CA05-476": ["CA05-475"],
        "CA05-490": ["CA05-489"],
        "CA05-496": ["CA05-495"],
        "CA06-505": ["CA06-504"],
        "CA06-525": ["CA06-524"],
        "CA06-529": ["CA06-528"],
        "CA06-545": ["CA06-544"],
    }
    for rid, inherited in expected.items():
        assert BY_ID[rid]["source_context"]["inherited_source_rule_ids"] == inherited


def test_source_spans_cover_printed_pages_143_to_146():
    assert [x["printed_page"] for x in DOC["source_spans"]] == [143, 144, 145, 146]
    assert all(x["visual_reviewed"] for x in DOC["source_spans"])
    assert all(len(x["extracted_text_not_silently_corrected"]) > 500 for x in DOC["source_spans"])


def test_review_remains_nonproduction():
    g = DOC["guardrails"]
    assert g["source_rows_modified"] is False
    assert g["product_runtime_modified"] is False
    assert g["production_registry_modified"] is False
    assert g["new_atoms_or_semantic_defaults"] is False
    assert g["outcome_probability_or_empirical_validity_claimed"] is False
