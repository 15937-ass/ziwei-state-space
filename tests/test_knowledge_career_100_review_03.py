import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec

ROOT = Path(__file__).resolve().parents[1]
DOC = json.loads((ROOT / "knowledge/wp07a/CAREER_100_REVIEW_03_v0.1.json").read_text())
RECORDS = DOC["mappings"]


def _atom_types(spec):
    out = []
    for atom in spec.get("all_of", []):
        out.append(atom["atom_type"])
    for group in spec.get("any_of", []):
        out.extend(atom["atom_type"] for atom in group)
    for atom in spec.get("none_of", []):
        out.append(atom["atom_type"])
    for branch in spec.get("alternatives", []):
        out.extend(atom["atom_type"] for atom in branch)
    return out


def test_counts_and_scope():
    counts = DOC["progress_counts"]
    assert len(RECORDS) == 100
    assert RECORDS[0]["source_rule_id"] == "CA03-236"
    assert RECORDS[-1]["source_rule_id"] == "CA04-342"
    assert counts["first_time_complete_condition_mappings"] == 33
    assert counts["methodology_or_context_only"] == 7
    assert counts["blocked_outcome_mappings"] == 60
    assert counts["unique_structured_rule_records_before"] == 252
    assert counts["unique_structured_rule_records_after"] == 352


def test_conditions_are_conservative():
    for item in RECORDS:
        assert item["executable_registry_entry"] is False
        if item["review_disposition"] == "COMPLETE_CONDITION_MAPPING":
            assert item["condition"] is not None
            assert set(_atom_types(item["condition"])) <= ALLOWED_ATOM_TYPES
            compile_condition_spec(item["condition"])
        else:
            assert item["condition"] is None
            assert item["blocker_code"]


def test_guardrails():
    g = DOC["guardrails"]
    assert g["source_rows_modified"] is False
    assert g["product_runtime_modified"] is False
    assert g["production_registry_modified"] is False
    assert g["new_atoms_or_semantic_defaults"] is False
    assert g["null_condition_must_not_be_coerced_to_empty"] is True
    assert g["outcome_probability_or_empirical_validity_claimed"] is False
