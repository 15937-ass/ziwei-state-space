import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "knowledge/wp07a/CAREER_SPOUSE_KONGJIE_CA01_023_v0.1.json"
ONTOLOGY_PATH = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
CSV_PATH = ROOT / "validation/wp05/CA01_career_projection_review_001_100.csv"
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")
PALACES = [
    ("P01", "命宫"), ("P02", "兄弟宫"), ("P03", "夫妻宫"),
    ("P04", "子女宫"), ("P05", "财帛宫"), ("P06", "疾厄宫"),
    ("P07", "迁移宫"), ("P08", "交友宫"), ("P09", "事业宫"),
    ("P10", "田宅宫"), ("P11", "福德宫"), ("P12", "父母宫"),
]

def _mapping():
    return json.loads(MAPPING_PATH.read_text(encoding="utf-8"))


def _source_row():
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return next(row for row in csv.DictReader(handle) if row["projection_rule_id"] == "CA01-023")


def _snapshot(stars_by_palace, p09_branch):
    p09_index = next(i for i, (pid, _) in enumerate(PALACES) if pid == "P09")
    offset = (BRANCHES.index(p09_branch) - p09_index) % len(BRANCHES)
    raw_palaces = {}
    for i, (palace_id, palace_name) in enumerate(PALACES):
        branch = BRANCHES[(i + offset) % len(BRANCHES)]
        raw_palaces[branch] = {
            "name": palace_name, "stem": "甲", "branch": branch, "is_body_palace": False,
            "major_stars": [], "minor_stars": [],
            "adjective_stars": stars_by_palace.get(palace_id, []),
        }
    return {"schema_version": "0.2", "engine": {"name": "kongjie-test", "version": "1", "adapter_version": "0.2"}, "input": {}, "natal": {"palaces": raw_palaces}}


def _matches(stars_by_palace, p09_branch):
    item = _mapping()["mappings"][0]
    ontology = load_palace_ontology(ONTOLOGY_PATH)
    facts = resolve_palace_structure(_snapshot(stars_by_palace, p09_branch), ontology).runtime_facts()
    return compile_condition_spec(item["condition"]).matches(facts)


def test_source_provenance_and_projection_are_preserved():
    doc = _mapping()
    row = _source_row()
    item = doc["mappings"][0]
    prov = item["source_provenance"]
    assert item["source_rule_id"] == row["projection_rule_id"] == "CA01-023"
    assert row["source_id"] == prov["source_id"] == "SRC-ZZ-003"
    assert row["source_location"] == prov["source_location"]
    assert row["condition"] == item["source_condition_text"]
    assert row["review_status"] == prov["review_status"] == "SOURCE_SPAN_VERIFIED"
    assert row["source_span_verified"].lower() == "true" and prov["source_span_verified"] is True
    assert row["time_layer"] == prov["time_layer"] == "NATAL"
    assert row["case_support_only"].lower() == "false" and prov["case_support_only"] is False
    assert row["history_feedback"] == prov["history_feedback"]
    assert item["expected_projection"] == {
        "projection_domain": row["projection_domain"],
        "projection_target": row["projection_target"],
        "projection_mode": row["projection_mode"],
    }
    assert item["executable_registry_entry"] is False
    assert len(item["condition"]["alternatives"]) == 4
    assert all(atom["atom_type"] in ALLOWED_ATOM_TYPES for atom in item["condition"]["all_of"])
    assert all(atom["atom_type"] in ALLOWED_ATOM_TYPES for branch in item["condition"]["alternatives"] for atom in branch)


def test_both_branch_orientations_and_both_star_allocations_match():
    cases = [
        ("寅", {"P09": [{"name": "地空"}], "P03": [{"name": "地劫"}]}),
        ("寅", {"P09": [{"name": "地劫"}], "P03": [{"name": "地空"}]}),
        ("申", {"P09": [{"name": "地空"}], "P03": [{"name": "地劫"}]}),
        ("申", {"P09": [{"name": "地劫"}], "P03": [{"name": "地空"}]}),
    ]
    for branch, stars in cases:
        assert _matches(stars, branch)


def test_wrong_branches_or_missing_and_misplaced_stars_do_not_match():
    assert not _matches({"P09": [{"name": "地空"}], "P03": [{"name": "地劫"}]}, "卯")
    assert not _matches({"P09": [{"name": "地空"}]}, "寅")
    assert not _matches({"P09": [{"name": "地空"}, {"name": "地劫"}]}, "寅")
    assert not _matches({"P03": [{"name": "地空"}, {"name": "地劫"}]}, "申")


def test_relation_fact_and_non_executable_guard_are_preserved():
    doc = _mapping()
    item = doc["mappings"][0]
    ontology = load_palace_ontology(ONTOLOGY_PATH)
    facts = resolve_palace_structure(_snapshot({"P09": [{"name": "地空"}], "P03": [{"name": "地劫"}]}, "寅"), ontology).runtime_facts()
    assert compile_condition_spec(item["condition"]).matches(facts)
    assert item["condition"]["all_of"][0]["args"] == {"source": "P09", "target": "P03", "relation": "OPPOSITE"}
    assert item["execution_readiness"] == "STATIC_CROSS_PALACE_CANDIDATE_NOT_EXECUTABLE"
    assert item["executable_registry_entry"] is False
    assert doc["validation"]["product_runtime_modified"] is False
    assert doc["validation"]["production_registry_modified"] is False
    assert doc["validation"]["new_atom_or_ontology_semantics_created"] is False

def test_source_branch_gate_and_ocr_uncertainty_are_documented():
    context = _mapping()["mappings"][0]["source_context"]
    assert context["branch_gate_reading"] == "此唯寅申两宫有之"
    assert "OCR 噪声" in context["source_scope_note"]
    assert "寅申" in context["normalized_reading"]
    assert _mapping()["validation"]["branch_gate_preserved"] is True
