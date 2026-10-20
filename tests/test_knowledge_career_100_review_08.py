import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec

ROOT = Path(__file__).resolve().parents[1]
DOC = json.loads((ROOT / "knowledge/wp07a/CAREER_100_REVIEW_08_v0.1.json").read_text())
RECORDS = DOC["mappings"]
BY_ID = {item["source_rule_id"]: item for item in RECORDS}


def _canonical():
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


def _atoms(spec):
    out = list(spec.get("all_of", [])) + list(spec.get("none_of", []))
    for group in spec.get("any_of", []):
        out.extend(group)
    for group in spec.get("alternatives", []):
        out.extend(group)
    return out


def test_exact_next_100_after_752_baseline():
    baseline = set()
    for rel in DOC["baseline_mapping_paths"]:
        prior = json.loads((ROOT / rel).read_text())
        baseline.update(
            item["source_rule_id"]
            for item in prior.get("mappings", [])
            if item.get("source_rule_id")
        )
    assert len(baseline) == 752
    expected = [
        row["projection_rule_id"]
        for row in _canonical()
        if row["projection_rule_id"] not in baseline
    ][:100]
    assert [item["source_rule_id"] for item in RECORDS] == expected
    assert expected[0] == "CA08-750"
    assert expected[-1] == "CA09-851"
    assert {"CA08-765", "CA08-766"}.isdisjoint(expected)
    assert len(baseline | set(expected)) == 852


def test_counts_close():
    counts = DOC["progress_counts"]
    assert counts["first_time_complete_condition_mappings"] == 16
    assert counts["methodology_or_context_only"] == 17
    assert counts["blocked_outcome_mappings"] == 67
    assert counts["unique_structured_rule_records_before"] == 752
    assert counts["unique_structured_rule_records_after"] == 852
    assert 16 + 17 + 67 == 100


def test_embedded_source_rows_match_canonical():
    source = {row["projection_rule_id"]: row for row in _canonical()}
    for item in RECORDS:
        assert item["source_record"] == source[item["source_rule_id"]]
        assert item["source_condition_text"] == item["source_record"]["condition"]


def test_complete_conditions_use_existing_atoms_and_compile():
    for item in RECORDS:
        if item["review_disposition"] == "COMPLETE_CONDITION_MAPPING":
            assert item["condition"] is not None
            atoms = _atoms(item["condition"])
            assert atoms
            assert {atom["atom_type"] for atom in atoms} <= ALLOWED_ATOM_TYPES
            compile_condition_spec(item["condition"])
        else:
            assert item["condition"] is None
            assert item["blocker_code"]


def test_critic_boundaries():
    assert BY_ID["CA08-787"]["condition"] is not None
    atoms = _atoms(BY_ID["CA08-787"]["condition"])
    assert any(
        atom["atom_type"] == "TRANSFORMATION_PRESENT"
        and atom["args"] == {"palace": "P03", "star": "天机", "mutagen": "忌"}
        for atom in atoms
    )
    for rid in ["CA08-757", "CA08-758", "CA08-759", "CA08-789", "CA08-790", "CA08-791"]:
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] == "RELATION"
    assert BY_ID["CA09-814"]["review_disposition"] == "METHODOLOGY_OR_CONTEXT_ONLY"
    assert BY_ID["CA09-851"]["blocker_code"] == "TEMPORAL"


def test_real_world_states_stay_external():
    for rid in ["CA08-750", "CA08-751", "CA08-762", "CA08-763", "CA08-764", "CA08-782", "CA08-794", "CA09-834", "CA09-835", "CA09-841"]:
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] == "CONTEXT_STATE"


def test_source_spans_and_nonproduction():
    assert [item["printed_page"] for item in DOC["source_spans"]] == [151, 152, 153, 154]
    assert all(item["visual_reviewed"] for item in DOC["source_spans"])
    assert all(len(item["extracted_text_not_silently_corrected"]) > 500 for item in DOC["source_spans"])
    assert all(item["executable_registry_entry"] is False for item in RECORDS)
    g = DOC["guardrails"]
    assert g["source_rows_modified"] is False
    assert g["product_runtime_modified"] is False
    assert g["production_registry_modified"] is False
    assert g["new_atoms_or_semantic_defaults"] is False
