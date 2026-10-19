import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "knowledge/wp07a/CAREER_NATAL_TRANSFORMATION_MAP_CA01_CA03_v0.1.json"
ONTOLOGY_PATH = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
CSV_PATHS = (
    ROOT / "validation/wp05/CA01_career_projection_review_001_100.csv",
    ROOT / "validation/wp05/CA02_career_projection_review_101_200.csv",
    ROOT / "validation/wp05/CA03_career_projection_review_201_300.csv",
)
CANONICAL_PALACES = [
    ("P01", "命宫"), ("P02", "兄弟宫"), ("P03", "夫妻宫"),
    ("P04", "子女宫"), ("P05", "财帛宫"), ("P06", "疾厄宫"),
    ("P07", "迁移宫"), ("P08", "交友宫"), ("P09", "事业宫"),
    ("P10", "田宅宫"), ("P11", "福德宫"), ("P12", "父母宫"),
]
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")

EXPECTED = {
    "CA01-052": {"star": "紫微", "mutagen": "权", "branches": []},
    "CA01-053": {"star": "紫微", "mutagen": "权", "branches": []},
    "CA01-054": {"star": "紫微", "mutagen": "科", "branches": []},
    "CA01-055": {"star": "紫微", "mutagen": "科", "branches": []},
    "CA01-070": {"star": "紫微", "mutagen": "权", "branches": ["子", "午"]},
    "CA01-071": {"star": "紫微", "mutagen": "权", "branches": ["子", "午"]},
    "CA01-078": {"star": "紫微", "mutagen": "科", "branches": ["子", "午"]},
    "CA02-155": {"star": "天机", "mutagen": "禄", "branches": []},
    "CA02-158": {"star": "天机", "mutagen": "权", "branches": []},
    "CA02-160": {"star": "天机", "mutagen": "科", "branches": []},
    "CA02-164": {"star": "天机", "mutagen": "忌", "branches": []},
    "CA02-194": {"star": "天机", "mutagen": "忌", "branches": ["子", "午"]},
    "CA03-252": {"star": "天机", "mutagen": "忌", "branches": ["巳", "亥"]},
    "CA03-254": {"star": "天机", "mutagen": "科", "branches": []},
    "CA03-279": {"star": "太阳", "mutagen": "禄", "branches": []},
    "CA03-283": {"star": "太阳", "mutagen": "科", "branches": []},
    "CA03-285": {"star": "太阳", "mutagen": "忌", "branches": []},
}
PATH_BLOCKED = {"CA02-158", "CA02-164"}
EVENT_BLOCKED = {"CA02-194"}
EXCLUSIONS = {
    "CA04-368": "PREVIOUS_RULE_CONTEXT_REQUIRED",
    "CA05-403": "TIMING_TRIGGER_OUTPUT",
    "CA06-558": "BRIGHTNESS_FACT_NOT_EMITTED",
    "CA07-624": "COMPOUND_TRANSFORMATION_SEMANTICS_UNRESOLVED",
    "CA09-852": "ALREADY_MAPPED_IN_PILOT",
}

def _load_mapping():
    return json.loads(MAPPING_PATH.read_text(encoding="utf-8"))


def _source_rows():
    rows = {}
    for path in CSV_PATHS:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                rows[row["projection_rule_id"]] = row
    return rows


def _patterns(mapping):
    condition = mapping["condition"]
    if "alternatives" in condition:
        return condition["alternatives"]
    return [condition.get("all_of", [])]


def _snapshot_with_p09_transformation(star_name, mutagen, p09_branch):
    palaces = {}
    p09_index = next(i for i, (palace_id, _) in enumerate(CANONICAL_PALACES) if palace_id == "P09")
    offset = (BRANCHES.index(p09_branch) - p09_index) % len(BRANCHES)
    for index, (_, palace_name) in enumerate(CANONICAL_PALACES):
        branch = BRANCHES[(index + offset) % len(BRANCHES)]
        stars = []
        if palace_name == "事业宫":
            stars = [{
                "name": star_name, "brightness": None, "mutagen": mutagen,
                "type": None, "scope": None,
            }]
        palaces[branch] = {
            "name": palace_name, "stem": "甲", "branch": branch,
            "is_body_palace": False, "major_stars": stars,
            "minor_stars": [], "adjective_stars": [],
        }
    return {
        "schema_version": "0.2",
        "engine": {"name": "knowledge-atomization-test", "version": "1", "adapter_version": "0.2"},
        "input": {}, "natal": {"palaces": palaces},
    }


def test_exactly_nominated_rows_match_canonical_provenance_and_projection():
    document = _load_mapping()
    source_rows = _source_rows()
    mappings = {item["source_rule_id"]: item for item in document["mappings"]}

    assert set(mappings) == set(EXPECTED)
    assert set(source_rows).issuperset(EXPECTED)
    assert document["validation"]["nominated_rows"] == 17
    assert document["validation"]["mapped_rows"] == 17
    assert document["validation"]["blocked_nominated_rows"] == 0

    for rule_id, expected in EXPECTED.items():
        row = source_rows[rule_id]
        item = mappings[rule_id]
        provenance = item["source_provenance"]
        projection = item["expected_projection"]

        assert row["source_id"] == provenance["source_id"] == "SRC-ZZ-003"
        assert row["source_location"] == provenance["source_location"]
        assert row["review_status"] == provenance["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert row["source_span_verified"].lower() == "true"
        assert provenance["source_span_verified"] is True
        assert row["time_layer"] == provenance["time_layer"] == "NATAL"
        assert row["case_support_only"].lower() == "false"
        assert provenance["case_support_only"] is False
        assert row.get("history_feedback", "") == provenance["history_feedback"]
        assert row["condition"] == item["source_condition_text"]
        assert projection["projection_domain"] == row["projection_domain"]
        assert projection["projection_target"] == row["projection_target"]
        assert projection["projection_mode"] == row["projection_mode"]
        assert item["mapping_status"] == "MAPPED_EXISTING_ATOM"
        assert item["executable_registry_entry"] is False

        condition_atoms = [atom for pattern in _patterns(item) for atom in pattern]
        transform_atoms = {json.dumps(atom, sort_keys=True, ensure_ascii=False) for atom in condition_atoms if atom["atom_type"] == "TRANSFORMATION_PRESENT"}
        branch_atoms = [atom for atom in condition_atoms if atom["atom_type"] == "BRANCH_PRESENT"]
        assert len(transform_atoms) == 1
        transform = json.loads(next(iter(transform_atoms)))
        assert transform["args"] == {"palace": "P09", "star": expected["star"], "mutagen": expected["mutagen"]}
        assert {atom["args"]["branch"] for atom in branch_atoms} == set(expected["branches"])
        assert all(atom["args"]["palace"] == "P09" for atom in condition_atoms)
        assert {atom["atom_type"] for atom in condition_atoms} == set(item["condition_atom_types"])
        assert all(atom["atom_type"] in ALLOWED_ATOM_TYPES for atom in condition_atoms)


def test_conditions_match_existing_runtime_facts_and_preserve_branch_gates():
    document = _load_mapping()
    ontology = load_palace_ontology(ONTOLOGY_PATH)
    mappings = {item["source_rule_id"]: item for item in document["mappings"]}

    for rule_id, expected in EXPECTED.items():
        item = mappings[rule_id]
        compiled = compile_condition_spec(item["condition"])
        positive_branches = expected["branches"] or ["申"]

        for p09_branch in positive_branches:
            snapshot = _snapshot_with_p09_transformation(expected["star"], expected["mutagen"], p09_branch)
            facts = resolve_palace_structure(snapshot, ontology).runtime_facts()
            assert compiled.matches(facts), rule_id
            matching_patterns = [
                pattern for pattern in _patterns(item)
                if all(fact_from_atom(atom["atom_type"], **atom["args"]) in facts for atom in pattern)
            ]
            assert matching_patterns, rule_id

        if expected["branches"]:
            wrong_branch = next(branch for branch in BRANCHES if branch not in expected["branches"])
            snapshot = _snapshot_with_p09_transformation(expected["star"], expected["mutagen"], wrong_branch)
            facts = resolve_palace_structure(snapshot, ontology).runtime_facts()
            assert not compiled.matches(facts), rule_id


def test_path_and_event_like_outputs_are_not_silently_promoted():
    document = _load_mapping()
    mappings = {item["source_rule_id"]: item for item in document["mappings"]}
    for rule_id in PATH_BLOCKED:
        assert mappings[rule_id]["execution_readiness"] == "BLOCKED_PATH_DEPENDENT_TARGET"
    for rule_id in EVENT_BLOCKED:
        assert mappings[rule_id]["execution_readiness"] == "BLOCKED_EVENT_LIKE_TARGET_REQUIRES_MANIFESTATION_REVIEW"
    assert all(item["executable_registry_entry"] is False for item in mappings.values())

    exclusions = {item["source_rule_id"]: item for item in document["exclusions"]}
    for rule_id, reason in EXCLUSIONS.items():
        assert exclusions[rule_id]["reason_code"] == reason

    assert document["validation"]["source_rows_modified"] is False
    assert document["validation"]["executable_rule_created"] is False
    assert document["validation"]["product_runtime_modified"] is False
    assert document["validation"]["production_registry_modified"] is False
    assert document["validation"]["history_feedback_metadata_preserved"] is True
