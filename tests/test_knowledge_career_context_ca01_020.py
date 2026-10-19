import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "knowledge/wp07a/CAREER_CONTEXT_MAP_CA01_020_v0.1.json"
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
        return next(row for row in csv.DictReader(handle) if row["projection_rule_id"] == "CA01-020")


def _snapshot(stars_by_palace):
    offset = (BRANCHES.index("申") - 8) % len(BRANCHES)
    raw_palaces = {}
    for i, (palace_id, palace_name) in enumerate(PALACES):
        branch = BRANCHES[(i + offset) % len(BRANCHES)]
        raw_palaces[branch] = {
            "name": palace_name, "stem": "甲", "branch": branch, "is_body_palace": False,
            "major_stars": stars_by_palace.get(palace_id, []),
            "minor_stars": [], "adjective_stars": [],
        }
    return {"schema_version": "0.2", "engine": {"name": "context-test", "version": "1", "adapter_version": "0.2"}, "input": {}, "natal": {"palaces": raw_palaces}}


def _matches(stars_by_palace):
    item = _mapping()["mappings"][0]
    ontology = load_palace_ontology(ONTOLOGY_PATH)
    facts = resolve_palace_structure(_snapshot(stars_by_palace), ontology).runtime_facts()
    return compile_condition_spec(item["condition"]).matches(facts)


def test_source_fields_and_projection_are_preserved():
    doc = _mapping()
    item = doc["mappings"][0]
    row = _source_row()
    prov = item["source_provenance"]
    assert item["source_rule_id"] == row["projection_rule_id"] == "CA01-020"
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
    assert item["source_epistemic"] == "EXPLICIT_ILLUSTRATIVE_EXAMPLE"
    assert item["execution_readiness"] == "BLOCKED_ILLUSTRATIVE_EXAMPLE_SCOPE_AND_CONTEXT_INHERITANCE_UNRESOLVED"
    assert item["executable_registry_entry"] is False


def test_explicit_career_palace_context_is_required():
    stars = {
        "P01": [{"name": "紫微", "mutagen": "权"}, {"name": "天府"}],
        "P05": [{"name": "武曲", "mutagen": "忌"}],
        "P09": [{"name": "廉贞"}, {"name": "天相"}],
    }
    assert _matches(stars)
    assert not _matches({"P01": stars["P01"], "P05": stars["P05"], "P09": [{"name": "廉贞"}]})
    assert not _matches({"P01": stars["P01"], "P05": stars["P05"], "P09": [{"name": "天相"}]})
    assert not _matches({"P01": stars["P01"], "P05": stars["P05"]})


def test_context_uncertainty_and_non_execution_are_explicit():
    doc = _mapping()
    item = doc["mappings"][0]
    context = item["source_context"]
    assert context["context_type"] == "ILLUSTRATIVE_EXAMPLE_IN_EXPLANATORY_TEXT"
    inherited = {entry["condition"]: entry["status"] for entry in context["inherited_context"]}
    assert inherited["命宫[紫微天府]"] == "INHERITANCE_UNRESOLVED"
    assert inherited["财帛宫武曲独坐"] == "INHERITANCE_UNRESOLVED"
    neighbor = context["excluded_neighbor_context"][0]
    assert neighbor["condition"] == "迁移宫坐禄存"
    assert neighbor["status"] == "NOT_IMPORTED"
    assert doc["validation"]["executable_rule_created"] is False
    assert doc["validation"]["product_runtime_modified"] is False
    assert doc["validation"]["production_registry_modified"] is False
    assert all(atom["atom_type"] in ALLOWED_ATOM_TYPES for atom in item["condition"]["all_of"])