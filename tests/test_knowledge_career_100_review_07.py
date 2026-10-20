import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = json.loads((ROOT / "knowledge/wp07a/CAREER_100_REVIEW_07_v0.1.json").read_text())
RECORDS = DOC["mappings"]
BY_ID = {item["source_rule_id"]: item for item in RECORDS}


def test_counts_and_range():
    assert len(RECORDS) == 100
    assert RECORDS[0]["source_rule_id"] == "CA07-647"
    assert RECORDS[-1]["source_rule_id"] == "CA08-749"
    counts = DOC["progress_counts"]
    assert counts["first_time_complete_condition_mappings"] == 24
    assert counts["methodology_or_context_only"] == 11
    assert counts["blocked_outcome_mappings"] == 65
    assert counts["unique_structured_rule_records_before"] == 652
    assert counts["unique_structured_rule_records_after"] == 752


def test_noncomplete_rules_have_null_condition():
    for item in RECORDS:
        if item["review_disposition"] != "COMPLETE_CONDITION_MAPPING":
            assert item["condition"] is None
            assert item["blocker_code"]


def test_key_boundaries():
    assert BY_ID["CA07-674"]["review_disposition"] == "COMPLETE_CONDITION_MAPPING"
    assert BY_ID["CA07-670"]["review_disposition"] == "METHODOLOGY_OR_CONTEXT_ONLY"
    assert BY_ID["CA07-675"]["blocker_code"] == "CONTEXT_STATE"
    assert BY_ID["CA08-710"]["blocker_code"] == "RELATION"
    assert BY_ID["CA08-716"]["blocker_code"] == "RELATION"
    assert BY_ID["CA08-706"]["blocker_code"] == "CONTEXT_STATE"
    assert BY_ID["CA08-746"]["blocker_code"] == "ABSENCE"


def test_source_spans():
    assert [item["printed_page"] for item in DOC["source_spans"]] == [149, 150, 151]
    assert all(item["visual_reviewed"] for item in DOC["source_spans"])
    assert all(len(item["extracted_text_not_silently_corrected"]) > 500 for item in DOC["source_spans"])


def test_guardrails():
    g = DOC["guardrails"]
    assert g["source_rows_modified"] is False
    assert g["product_runtime_modified"] is False
    assert g["production_registry_modified"] is False
    assert g["new_atoms_or_semantic_defaults"] is False
    assert g["outcome_probability_or_empirical_validity_claimed"] is False


def test_complete_mapping_conditions_use_existing_atoms():
    from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec

    def atoms(spec):
        out = list(spec.get("all_of", [])) + list(spec.get("none_of", []))
        for group in spec.get("any_of", []):
            out.extend(group)
        for group in spec.get("alternatives", []):
            out.extend(group)
        return out

    for item in RECORDS:
        if item["review_disposition"] == "COMPLETE_CONDITION_MAPPING":
            aa = atoms(item["condition"])
            assert aa
            assert {atom["atom_type"] for atom in aa} <= ALLOWED_ATOM_TYPES
            compile_condition_spec(item["condition"])


def test_jumen_lu_alternatives_are_not_conjoined():
    for rid in ["CA07-676", "CA07-677"]:
        spec = BY_ID[rid]["condition"]
        assert len(spec["alternatives"]) == 2
        kinds = set()
        for branch in spec["alternatives"]:
            if any(atom["atom_type"] == "TRANSFORMATION_PRESENT" for atom in branch):
                kinds.add("HUALU")
            if any(
                atom["atom_type"] == "PALACE_HAS_STAR"
                and atom["args"].get("star") == "禄存"
                for atom in branch
            ):
                kinds.add("LUCUN")
        assert kinds == {"HUALU", "LUCUN"}


def test_explicit_opposite_transformations_keep_carriers():
    def atoms(spec):
        out = list(spec.get("all_of", []))
        for group in spec.get("alternatives", []):
            out.extend(group)
        return out

    lianzhen = atoms(BY_ID["CA08-742"]["condition"])
    assert any(
        atom["atom_type"] == "TRANSFORMATION_PRESENT"
        and atom["args"] == {"palace": "P03", "star": "廉贞", "mutagen": "忌"}
        for atom in lianzhen
    )
    wuqu = atoms(BY_ID["CA08-744"]["condition"])
    assert any(
        atom["atom_type"] == "TRANSFORMATION_PRESENT"
        and atom["args"] == {"palace": "P03", "star": "武曲", "mutagen": "忌"}
        for atom in wuqu
    )


def test_real_world_role_conditions_stay_external():
    for rid in ["CA07-653", "CA07-655", "CA07-661", "CA07-662", "CA08-706", "CA08-738", "CA08-739"]:
        assert BY_ID[rid]["condition"] is None
        assert BY_ID[rid]["blocker_code"] == "CONTEXT_STATE"
