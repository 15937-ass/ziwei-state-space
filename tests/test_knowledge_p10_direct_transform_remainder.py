import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "knowledge/palaces/P10_property/wp07a/PROPERTY_DIRECT_TRANSFORM_REMAINDER_MAP_v0.1.json"
ONTOLOGY = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
CSV_PATHS = {
    "TP01": ROOT / "validation/wp05/TP01_property_projection_review_001_100.csv",
    "TP02": ROOT / "validation/wp05/TP02_property_projection_review_101_200.csv",
    "TP03": ROOT / "validation/wp05/TP03_property_projection_review_201_300.csv",
}
READJUDICATION_PATHS = {
    "TP01": ROOT / "knowledge/wp05/property/PROPERTY_TP01_SOURCE_READJUDICATION_100_v0.1.json",
    "TP02": ROOT / "knowledge/wp05/property/PROPERTY_TP02_SOURCE_READJUDICATION_100_v0.1.json",
    "TP03": ROOT / "knowledge/wp05/property/PROPERTY_TP03_SOURCE_READJUDICATION_100_v0.1.json",
}
TIME_SCOPE_PATHS = {
    "TP01": ROOT / "knowledge/wp05/property/PROPERTY_TP01_SOURCE_TIME_SCOPE_v0.1.json",
    "TP02": ROOT / "knowledge/wp05/property/PROPERTY_TP02_SOURCE_TIME_SCOPE_v0.1.json",
    "TP03": ROOT / "knowledge/wp05/property/PROPERTY_TP03_SOURCE_TIME_SCOPE_v0.1.json",
}

CANONICAL_PALACES = [
    ("P01", "命宫"), ("P02", "兄弟宫"), ("P03", "夫妻宫"), ("P04", "子女宫"),
    ("P05", "财帛宫"), ("P06", "疾厄宫"), ("P07", "迁移宫"), ("P08", "交友宫"),
    ("P09", "事业宫"), ("P10", "田宅宫"), ("P11", "福德宫"), ("P12", "父母宫"),
]
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")
EXPECTED = {
    "TP01-095": {
        "star": "太阳", "mutagen": "忌", "projection_domain": "methodology",
        "projection_target": "taiyang_huaji_here_targets_ancestral_or_career_foundation_not_directly_father_harm",
        "projection_mode": "STRUCTURAL_CONSTRAINT", "source_location": "田宅宫printed_p158",
        "source_condition": "太阳化忌在田宅宫", "prefix": "TP01",
    },
    "TP02-148": {
        "star": "天同", "mutagen": "禄", "projection_domain": "property_scale",
        "projection_target": "property_holdings_can_become_abundant_in_mid_or_later_life_and_higher_status_areas",
        "projection_mode": "FUNCTIONAL_PROJECTION", "source_location": "田宅宫printed_p160",
        "source_condition": "天同化禄", "prefix": "TP02",
    },
    "TP03-270": {
        "star": "巨门", "mutagen": "忌", "projection_domain": "household",
        "projection_target": "home_unrest_or_separation_from_household_strengthens",
        "projection_mode": "FUNCTIONAL_PROJECTION", "source_location": "田宅宫printed_p163",
        "source_condition": "巨门化忌于田宅", "prefix": "TP03",
    },
}

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def source_rows():
    out = {}
    for prefix, path in CSV_PATHS.items():
        with path.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                if row["projection_rule_id"] in EXPECTED or row["projection_rule_id"] in {
                    "TP01-096", "TP02-149", "TP03-271", "TP03-272", "TP03-273"
                }:
                    out[row["projection_rule_id"]] = row
    return out

def source_records(paths, key):
    out = {}
    for prefix, path in paths.items():
        doc = load_json(path)
        records = doc.get("records", [])
        if key == "projection_rule_id":
            for row in records:
                out[row[key]] = row
        else:
            raise AssertionError(f"unsupported key: {key}")
    return out

def snapshot(star_name, mutagen):
    palaces = {}
    for idx, (_, name) in enumerate(CANONICAL_PALACES):
        branch = BRANCHES[idx]
        stars = []
        if name == "田宅宫":
            stars = [{"name": star_name, "brightness": None, "mutagen": mutagen, "type": None, "scope": None}]
        palaces[branch] = {
            "name": name, "stem": "甲", "branch": branch, "is_body_palace": False,
            "major_stars": stars, "minor_stars": [], "adjective_stars": [],
        }
    return {
        "schema_version": "0.2",
        "engine": {"name": "knowledge-p10-direct-transform-test", "version": "1", "adapter_version": "0.2"},
        "input": {}, "natal": {"palaces": palaces},
    }

def test_exact_three_rows_match_canonical_source_and_projection():
    doc = load_json(MAPPING)
    src = source_rows()
    readjudication = source_records(READJUDICATION_PATHS, "projection_rule_id")
    scope = source_records(TIME_SCOPE_PATHS, "projection_rule_id")
    mapped = {x["source_rule_id"]: x for x in doc["mappings"]}
    assert set(mapped) == set(EXPECTED)
    assert doc["validation"]["nominated_rows"] == 3
    assert doc["validation"]["mapped_rows"] == 3
    assert doc["validation"]["blocked_nominated_rows"] == 0
    for rule_id, expected in EXPECTED.items():
        item = mapped[rule_id]
        row = src[rule_id]
        adjudicated = readjudication[rule_id]
        time = scope[rule_id]
        provenance = item["source_provenance"]
        projection = item["expected_projection"]
        assert row["source_id"] == provenance["source_id"] == "SRC-ZZ-003"
        assert row["source_location"] == provenance["source_location"] == expected["source_location"]
        assert row["condition"] == expected["source_condition"] == item["source_condition_text"]
        assert adjudicated["canonical_condition"] == expected["source_condition"]
        assert adjudicated["projection_domain"] == projection["projection_domain"] == expected["projection_domain"]
        assert adjudicated["projection_target"] == projection["projection_target"] == expected["projection_target"]
        assert adjudicated["projection_mode"] == projection["projection_mode"] == expected["projection_mode"]
        assert adjudicated["time_layer"] == provenance["time_layer"] == "NATAL"
        assert adjudicated["case_support_only"] is False
        assert row["case_support_only"] == "false"
        assert row["review_status"] == provenance["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert row["source_span_verified"] == "true" and provenance["source_span_verified"] is True
        assert time["legacy_primary_time_layer"] == "NATAL"
        assert time["source_time_layers"] == ["NATAL"]
        assert item["mapping_status"] == "MAPPED_EXISTING_ATOM"
        assert item["executable_registry_entry"] is False
        assert item["condition"]["all_of"] == [item["expected_runtime_fact"]]
        assert item["condition_atom_types"] == ["TRANSFORMATION_PRESENT"]

def test_runtime_fact_shape_is_emitted_by_current_natal_resolver():
    doc = load_json(MAPPING)
    ontology = load_palace_ontology(ONTOLOGY)
    for item in doc["mappings"]:
        atom = item["condition"]["all_of"][0]
        assert atom["atom_type"] == "TRANSFORMATION_PRESENT"
        assert atom["atom_type"] in ALLOWED_ATOM_TYPES
        args = atom["args"]
        assert args["palace"] == "P10"
        facts = resolve_palace_structure(snapshot(args["star"], args["mutagen"]), ontology).runtime_facts()
        assert fact_from_atom(atom["atom_type"], **args) in facts

def test_compound_exceptions_and_case_only_events_remain_separate():
    doc = load_json(MAPPING)
    src = source_rows()
    exclusions = {x["source_rule_id"]: x for x in doc["exclusions"]}
    required = {"TP01-096", "TP02-149", "TP03-271", "TP03-272", "TP03-273"}
    assert required.issubset(exclusions)
    for rule_id in required:
        row = src[rule_id]
        exclusion = exclusions[rule_id]
        assert exclusion["source_condition_text"] == row["condition"]
        assert exclusion["source_location"] == row["source_location"]
        assert exclusion["case_support_only"] == (row["case_support_only"] == "true")
    assert exclusions["TP02-149"]["reason_code"] == "COMPOUND_MALEFIC_EXCEPTION"
    assert exclusions["TP03-271"]["reason_code"] == "CASE_SUPPORT_ONLY_EVENT_CANDIDATE"
    assert exclusions["TP03-272"]["reason_code"] == "CASE_SUPPORT_ONLY_EVENT_CANDIDATE"
    assert all(exclusions[x]["case_support_only"] is True for x in ("TP03-271", "TP03-272", "TP03-273"))

def test_literal_life_stage_is_preserved_without_numericization():
    doc = load_json(MAPPING)
    scope = source_records(TIME_SCOPE_PATHS, "projection_rule_id")
    item = next(x for x in doc["mappings"] if x["source_rule_id"] == "TP02-148")
    assert "中晚年以后置产业甚丰" in scope["TP02-148"]["literal_life_stage_labels"]
    assert item["source_time_scope"]["literal_life_stage_labels"] == ["中晚年以后置产业甚丰"]
    assert "mid_or_later_life" in item["expected_projection"]["projection_target"]
    assert doc["validation"]["new_threshold_created"] is False

def test_no_new_semantics_or_production_entry():
    doc = load_json(MAPPING)
    assert all(x["condition_atom_types"] == ["TRANSFORMATION_PRESENT"] for x in doc["mappings"])
    assert all(x["executable_registry_entry"] is False for x in doc["mappings"])
    assert doc["validation"]["production_registry_modified"] is False
    assert doc["validation"]["product_runtime_modified"] is False
    assert doc["validation"]["canonical_source_rows_modified"] is False
    assert doc["validation"]["shared_semantics_modified"] is False
    assert doc["validation"]["new_atom_created"] is False
    assert doc["validation"]["new_probability_created"] is False
    assert doc["validation"]["new_numeric_weight_created"] is False
    assert doc["validation"]["new_threshold_created"] is False
