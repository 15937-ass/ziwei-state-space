import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "knowledge/wp07a/CAREER_DIRECT_TRANSFORM_MAP_CA04_CA09_v0.1.json"
ONTOLOGY_PATH = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
CSV_PATHS = tuple(ROOT / f"validation/wp05/CA{i:02d}_career_projection_review_{start}_{end}.csv" for i, start, end in [
    (4, "301", "400"), (5, "401", "500"), (6, "501", "600"),
    (7, "601", "700"), (8, "701", "800"), (9, "801", "888"),
])
CANONICAL_PALACES = [
    ("P01", "命宫"), ("P02", "兄弟宫"), ("P03", "夫妻宫"),
    ("P04", "子女宫"), ("P05", "财帛宫"), ("P06", "疾厄宫"),
    ("P07", "迁移宫"), ("P08", "交友宫"), ("P09", "事业宫"),
    ("P10", "田宅宫"), ("P11", "福德宫"), ("P12", "父母宫"),
]
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")
EXPECTED = {
    "CA04-327": {"star": "太阳", "mutagen": "忌"},
    "CA05-403": {"star": "天同", "mutagen": "忌"},
    "CA05-469": {"star": "廉贞", "mutagen": "忌"},
    "CA07-671": {"star": "巨门", "mutagen": "禄"},
    "CA07-672": {"star": "巨门", "mutagen": "权"},
    "CA07-673": {"star": "巨门", "mutagen": "忌"},
    "CA08-765": {"star": "天梁", "mutagen": "权"},
    "CA08-766": {"star": "天梁", "mutagen": "科"},
}
READINESS = {
    "CA05-403": "BLOCKED_TIMING_TRIGGER_REQUIRES_TEMPORAL_SPEC",
    "CA08-766": "BLOCKED_PATH_DEPENDENT_TARGET",
}
EXCLUSIONS = {
    "CA04-329": "MULTI_MUTAGEN_DISJUNCTION_OUT_OF_SCOPE",
    "CA04-332": "BRIGHTNESS_AND_NEGATIVE_STAR_CONDITIONS",
    "CA04-368": "PREVIOUS_RULE_CONTEXT_REQUIRED",
    "CA06-558": "BRIGHTNESS_FACT_NOT_EMITTED",
    "CA07-624": "COMPOUND_TRANSFORMATION_SEMANTICS_UNRESOLVED",
    "CA09-853": "PATH_DEPENDENT_TARGET",
}

def _mapping():
    return json.loads(MAPPING_PATH.read_text(encoding="utf-8"))


def _source_rows():
    result = {}
    for path in CSV_PATHS:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            result.update({row["projection_rule_id"]: row for row in csv.DictReader(handle)})
    return result


def _snapshot(star_name, mutagen):
    palaces = {}
    p09_index = next(i for i, (pid, _) in enumerate(CANONICAL_PALACES) if pid == "P09")
    offset = (BRANCHES.index("申") - p09_index) % len(BRANCHES)
    for i, (_, palace_name) in enumerate(CANONICAL_PALACES):
        branch = BRANCHES[(i + offset) % len(BRANCHES)]
        stars = []
        if palace_name == "事业宫":
            stars = [{"name": star_name, "brightness": None, "mutagen": mutagen, "type": None, "scope": None}]
        palaces[branch] = {
            "name": palace_name, "stem": "甲", "branch": branch, "is_body_palace": False,
            "major_stars": stars, "minor_stars": [], "adjective_stars": [],
        }
    return {"schema_version": "0.2", "engine": {"name": "knowledge-atomization-test", "version": "1", "adapter_version": "0.2"}, "input": {}, "natal": {"palaces": palaces}}


def test_nominated_rows_preserve_canonical_source_and_projection():
    doc = _mapping()
    source = _source_rows()
    mapped = {item["source_rule_id"]: item for item in doc["mappings"]}
    assert set(mapped) == set(EXPECTED)
    assert doc["validation"]["nominated_rows"] == 8
    assert doc["validation"]["mapped_rows"] == 8
    for rule_id, expected in EXPECTED.items():
        row, item = source[rule_id], mapped[rule_id]
        prov = item["source_provenance"]
        assert row["source_id"] == prov["source_id"] == "SRC-ZZ-003"
        assert row["source_location"] == prov["source_location"]
        assert row["review_status"] == prov["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert row["source_span_verified"].lower() == "true" and prov["source_span_verified"] is True
        assert row["time_layer"] == prov["time_layer"] == "NATAL"
        assert row["case_support_only"].lower() == "false" and prov["case_support_only"] is False
        assert row["history_feedback"] == prov["history_feedback"]
        assert row["condition"] == item["source_condition_text"]
        assert item["expected_projection"] == {
            "projection_domain": row["projection_domain"],
            "projection_target": row["projection_target"],
            "projection_mode": row["projection_mode"],
        }
        assert item["mapping_status"] == "MAPPED_EXISTING_ATOM"
        assert item["executable_registry_entry"] is False
        atoms = item["condition"]["all_of"]
        assert len(atoms) == 1
        assert atoms[0]["atom_type"] == "TRANSFORMATION_PRESENT"
        assert atoms[0]["args"] == {"palace": "P09", "star": expected["star"], "mutagen": expected["mutagen"]}
        assert item["condition_atom_types"] == ["TRANSFORMATION_PRESENT"]
        assert all(a["atom_type"] in ALLOWED_ATOM_TYPES for a in atoms)


def test_all_mapped_conditions_match_existing_runtime_facts():
    doc = _mapping()
    ontology = load_palace_ontology(ONTOLOGY_PATH)
    mapped = {item["source_rule_id"]: item for item in doc["mappings"]}
    for rule_id, expected in EXPECTED.items():
        item = mapped[rule_id]
        facts = resolve_palace_structure(_snapshot(expected["star"], expected["mutagen"]), ontology).runtime_facts()
        compiled = compile_condition_spec(item["condition"])
        assert compiled.matches(facts), rule_id
        atom = item["condition"]["all_of"][0]
        assert fact_from_atom(atom["atom_type"], **atom["args"]) in facts


def test_timing_path_gates_and_exclusions_are_preserved():
    doc = _mapping()
    mapped = {item["source_rule_id"]: item for item in doc["mappings"]}
    for rule_id, status in READINESS.items():
        assert mapped[rule_id]["execution_readiness"] == status
    assert mapped["CA05-403"]["expected_projection"]["projection_mode"] == "TIMING_TRIGGER"
    assert mapped["CA08-766"]["source_provenance"]["history_feedback"] == "PATH_DEPENDENT_GATE"
    assert all(item["executable_registry_entry"] is False for item in mapped.values())
    exclusions = {item["source_rule_id"]: item for item in doc["exclusions"]}
    for rule_id, reason in EXCLUSIONS.items():
        assert exclusions[rule_id]["reason_code"] == reason
    assert doc["validation"]["source_rows_modified"] is False
    assert doc["validation"]["executable_rule_created"] is False
    assert doc["validation"]["product_runtime_modified"] is False
    assert doc["validation"]["production_registry_modified"] is False