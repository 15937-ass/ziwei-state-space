import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "knowledge/wp07a/CAREER_NATAL_ATOMIZATION_MAP_v0.1.json"
ONTOLOGY_PATH = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"

CANONICAL_PALACES = [
    ("P01", "命宫"),
    ("P02", "兄弟宫"),
    ("P03", "夫妻宫"),
    ("P04", "子女宫"),
    ("P05", "财帛宫"),
    ("P06", "疾厄宫"),
    ("P07", "迁移宫"),
    ("P08", "交友宫"),
    ("P09", "事业宫"),
    ("P10", "田宅宫"),
    ("P11", "福德宫"),
    ("P12", "父母宫"),
]
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")

EXPECTED = {
    "CA04-347": {
        "star": "武曲",
        "mutagen": "科",
        "projection_domain": "reputation",
        "projection_target": "career_requires_reputation_building",
        "projection_mode": "FUNCTIONAL_PROJECTION",
        "source_location": "事业宫printed_p140",
    },
    "CA04-349": {
        "star": "武曲",
        "mutagen": "忌",
        "projection_domain": "career",
        "projection_target": "technical_skill_work_scene_preferred",
        "projection_mode": "SCENE_TRANSLATION",
        "source_location": "事业宫printed_p141",
    },
    "CA09-852": {
        "star": "破军",
        "mutagen": "禄",
        "projection_domain": "role",
        "projection_target": "multiple_jobs_side_roles_or_business_lines_are_common",
        "projection_mode": "FUNCTIONAL_PROJECTION",
        "source_location": "事业宫printed_p154",
    },
}


def _load_mapping():
    return json.loads(MAPPING_PATH.read_text(encoding="utf-8"))


def _canonical_source_rows():
    paths = (
        ROOT / "validation/wp05/CA04_career_projection_review_301_400.csv",
        ROOT / "validation/wp05/CA09_career_projection_review_801_888.csv",
    )
    rows = {}
    for path in paths:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if row["projection_rule_id"] in EXPECTED:
                    rows[row["projection_rule_id"]] = row
    return rows


def _snapshot_with_p09_transformation(star_name, mutagen):
    palaces = {}
    for index, (_, palace_name) in enumerate(CANONICAL_PALACES):
        branch = BRANCHES[index]
        stars = []
        if palace_name == "事业宫":
            stars = [
                {
                    "name": star_name,
                    "brightness": None,
                    "mutagen": mutagen,
                    "type": None,
                    "scope": None,
                }
            ]
        palaces[branch] = {
            "name": palace_name,
            "stem": "甲",
            "branch": branch,
            "is_body_palace": False,
            "major_stars": stars,
            "minor_stars": [],
            "adjective_stars": [],
        }
    return {
        "schema_version": "0.2",
        "engine": {
            "name": "knowledge-atomization-test",
            "version": "1",
            "adapter_version": "0.2",
        },
        "input": {},
        "natal": {"palaces": palaces},
    }


def test_exactly_three_nominated_career_rows_are_mapped_without_source_drift():
    document = _load_mapping()
    source_rows = _canonical_source_rows()
    mappings = {item["source_rule_id"]: item for item in document["mappings"]}

    assert set(mappings) == set(EXPECTED)
    assert set(source_rows) == set(EXPECTED)
    assert document["validation"]["nominated_rows"] == 3
    assert document["validation"]["mapped_rows"] == 3
    assert document["validation"]["blocked_nominated_rows"] == 0

    for rule_id, expected in EXPECTED.items():
        row = source_rows[rule_id]
        item = mappings[rule_id]
        provenance = item["source_provenance"]
        projection = item["expected_projection"]

        assert row["source_id"] == provenance["source_id"] == "SRC-ZZ-003"
        assert row["source_location"] == provenance["source_location"] == expected["source_location"]
        assert row["review_status"] == provenance["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert row["source_span_verified"] == "true"
        assert provenance["source_span_verified"] is True
        assert row["time_layer"] == provenance["time_layer"] == "NATAL"
        assert row["case_support_only"] == "false"
        assert provenance["case_support_only"] is False
        assert row["condition"] == item["source_condition_text"]
        assert row["projection_domain"] == projection["projection_domain"] == expected["projection_domain"]
        assert row["projection_target"] == projection["projection_target"] == expected["projection_target"]
        assert row["projection_mode"] == projection["projection_mode"] == expected["projection_mode"]
        assert item["executable_registry_entry"] is False


def test_mapping_conditions_use_only_allowed_atoms_and_match_runtime_fact_shape():
    document = _load_mapping()
    ontology = load_palace_ontology(ONTOLOGY_PATH)

    for item in document["mappings"]:
        atoms = item["condition"]["all_of"]
        assert len(atoms) == 1
        atom = atoms[0]
        assert atom["atom_type"] in ALLOWED_ATOM_TYPES
        assert atom["atom_type"] == "TRANSFORMATION_PRESENT"
        assert atom == item["expected_runtime_fact"]
        assert atom["args"]["palace"] == "P09"

        snapshot = _snapshot_with_p09_transformation(
            atom["args"]["star"], atom["args"]["mutagen"]
        )
        facts = resolve_palace_structure(snapshot, ontology).runtime_facts()
        assert fact_from_atom(atom["atom_type"], **atom["args"]) in facts


def test_required_nearby_exclusions_are_explicit_and_not_promoted():
    document = _load_mapping()
    exclusions = {item["source_rule_id"]: item for item in document["exclusions"]}

    required = {"CA04-345", "CA04-348", "CA09-851", "CA09-863"}
    assert required.issubset(exclusions)
    assert exclusions["CA04-345"]["reason_code"] == "CASE_SUPPORT_ONLY_EVENT_CANDIDATE"
    assert exclusions["CA04-348"]["reason_code"] == "CONTEXT_DEPENDENT_COMMERCE_GATE"
    assert exclusions["CA09-851"]["reason_code"] == "PATH_DEPENDENT_MULTIYEAR_SEQUENCE"
    assert exclusions["CA09-863"]["reason_code"] == "FIRE_BELL_CONDITION_AMBIGUITY"

    assert document["validation"]["source_rows_modified"] is False
    assert document["validation"]["executable_rule_created"] is False
    assert document["validation"]["product_runtime_modified"] is False
    assert document["validation"]["production_registry_modified"] is False
