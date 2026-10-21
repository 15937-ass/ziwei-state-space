import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "knowledge/palaces/P10_property/wp07a/PROPERTY_DIRECT_TRANSFORM_REMAINDER_MAP_v0.1.json"
ONTOLOGY = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
CSV_FILES = {
    "TP01": ROOT / "validation/wp05/TP01_property_projection_review_001_100.csv",
    "TP02": ROOT / "validation/wp05/TP02_property_projection_review_101_200.csv",
    "TP03": ROOT / "validation/wp05/TP03_property_projection_review_201_300.csv",
}
READ_FILES = {
    "TP01": ROOT / "knowledge/wp05/property/PROPERTY_TP01_SOURCE_READJUDICATION_100_v0.1.json",
    "TP02": ROOT / "knowledge/wp05/property/PROPERTY_TP02_SOURCE_READJUDICATION_100_v0.1.json",
    "TP03": ROOT / "knowledge/wp05/property/PROPERTY_TP03_SOURCE_READJUDICATION_100_v0.1.json",
}
TIME_FILES = {
    "TP01": ROOT / "knowledge/wp05/property/PROPERTY_TP01_SOURCE_TIME_SCOPE_v0.1.json",
    "TP02": ROOT / "knowledge/wp05/property/PROPERTY_TP02_SOURCE_TIME_SCOPE_v0.1.json",
    "TP03": ROOT / "knowledge/wp05/property/PROPERTY_TP03_SOURCE_TIME_SCOPE_v0.1.json",
}
EXPECTED = {
    "TP01-095": ("太阳", "忌", "太阳化忌在田宅宫", "methodology",
                 "taiyang_huaji_here_targets_ancestral_or_career_foundation_not_directly_father_harm",
                 "STRUCTURAL_CONSTRAINT", "田宅宫printed_p158"),
    "TP02-148": ("天同", "禄", "天同化禄", "property_scale",
                 "property_holdings_can_become_abundant_in_mid_or_later_life_and_higher_status_areas",
                 "FUNCTIONAL_PROJECTION", "田宅宫printed_p160"),
    "TP03-270": ("巨门", "忌", "巨门化忌于田宅", "household",
                 "home_unrest_or_separation_from_household_strengthens",
                 "FUNCTIONAL_PROJECTION", "田宅宫printed_p163"),
}
EXCLUDED = {"TP01-096", "TP02-149", "TP03-271", "TP03-272", "TP03-273"}
PALACES = [
    ("P01", "命宫"), ("P02", "兄弟宫"), ("P03", "夫妻宫"), ("P04", "子女宫"),
    ("P05", "财帛宫"), ("P06", "疾厄宫"), ("P07", "迁移宫"), ("P08", "交友宫"),
    ("P09", "事业宫"), ("P10", "田宅宫"), ("P11", "福德宫"), ("P12", "父母宫"),
]
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def collect_records(paths):
    out = {}
    for path in paths.values():
        for row in load(path).get("records", []):
            out[row["projection_rule_id"]] = row
    return out

def collect_source_rows():
    out = {}
    for path in CSV_FILES.values():
        with path.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                rid = row["projection_rule_id"]
                if rid in EXPECTED or rid in EXCLUDED:
                    out[rid] = row
    return out

def snapshot(star_name, mutagen):
    palaces = {}
    for i, (_, name) in enumerate(PALACES):
        branch = BRANCHES[i]
        stars = [{"name": star_name, "brightness": None, "mutagen": mutagen, "type": None, "scope": None}] if name == "田宅宫" else []
        palaces[branch] = {
            "name": name, "stem": "甲", "branch": branch, "is_body_palace": False,
            "major_stars": stars, "minor_stars": [], "adjective_stars": [],
        }
    return {"schema_version": "0.2",
            "engine": {"name": "knowledge-p10-direct-transform-test", "version": "1", "adapter_version": "0.2"},
            "input": {}, "natal": {"palaces": palaces}}

def test_three_direct_rows_match_canonical_source_and_sidecars():
    doc = load(MAP)
    source, readjudication, scopes = collect_source_rows(), collect_records(READ_FILES), collect_records(TIME_FILES)
    mapped = {x["source_rule_id"]: x for x in doc["mappings"]}
    assert set(mapped) == set(EXPECTED) and len(doc["mappings"]) == 3
    assert doc["validation"]["nominated_rows"] == doc["validation"]["mapped_rows"] == 3
    assert doc["validation"]["blocked_nominated_rows"] == 0
    for rid, (star, mutagen, condition, domain, target, mode, location) in EXPECTED.items():
        item, row, review, time = mapped[rid], source[rid], readjudication[rid], scopes[rid]
        proj, prov = item["expected_projection"], item["source_provenance"]
        assert row["source_id"] == prov["source_id"] == "SRC-ZZ-003"
        assert row["source_location"] == prov["source_location"] == location
        assert row["condition"] == review["canonical_condition"] == item["source_condition_text"] == condition
        assert (row["projection_domain"], row["projection_target"], row["projection_mode"]) == (domain, target, mode)
        assert (proj["projection_domain"], proj["projection_target"], proj["projection_mode"]) == (domain, target, mode)
        assert row["time_layer"] == prov["time_layer"] == time["legacy_primary_time_layer"] == "NATAL"
        assert time["source_time_layers"] == ["NATAL"]
        assert row["case_support_only"] == "false" and review["case_support_only"] is False
        assert row["review_status"] == prov["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert row["source_span_verified"] == "true" and prov["source_span_verified"] is True
        atom = item["condition"]["all_of"][0]
        assert atom == item["expected_runtime_fact"]
        assert atom["atom_type"] in ALLOWED_ATOM_TYPES == True
        assert atom["atom_type"] == "TRANSFORMATION_PRESENT"
        assert atom["args"] == {"palace": "P10", "star": star, "mutagen": mutagen}
        assert item["condition_atom_types"] == ["TRANSFORMATION_PRESENT"]
        assert item["mapping_status"] == "MAPPED_EXISTING_ATOM" and item["executable_registry_entry"] is False

def test_existing_natal_resolver_emits_exact_transformation_fact_shape():
    doc, ontology = load(MAP), load_palace_ontology(ONTOLOGY)
    for item in doc["mappings"]:
        atom = item["condition"]["all_of"][0]
        args = atom["args"]
        facts = resolve_palace_structure(snapshot(args["star"], args["mutagen"]), ontology).runtime_facts()
        assert fact_from_atom("TRANSFORMATION_PRESENT", **args) in facts

def test_compound_exceptions_and_case_only_events_stay_separate():
    doc, source = load(MAP), collect_source_rows()
    excluded = {x["source_rule_id"]: x for x in doc["exclusions"]}
    assert set(excluded) == EXCLUDED
    for rid in EXCLUDED:
        item, row = excluded[rid], source[rid]
        assert item["source_condition_text"] == row["condition"]
        assert item["source_location"] == row["source_location"]
        assert item["case_support_only"] == (row["case_support_only"] == "true")
    assert excluded["TP02-149"]["reason_code"] == "COMPOUND_MALEFIC_EXCEPTION"
    assert excluded["TP03-271"]["reason_code"] == excluded["TP03-272"]["reason_code"] == "CASE_SUPPORT_ONLY_EVENT_CANDIDATE"
    assert all(excluded[rid]["case_support_only"] is True for rid in ("TP03-271", "TP03-272", "TP03-273"))

def test_literal_life_stage_is_preserved_without_numeric_threshold():
    doc, scopes = load(MAP), collect_records(TIME_FILES)
    item = next(x for x in doc["mappings"] if x["source_rule_id"] == "TP02-148")
    assert "中晚年以后置产业甚丰" in scopes["TP02-148"]["literal_life_stage_labels"]
    assert item["source_time_scope"]["literal_life_stage_labels"] == ["中晚年以后置产业甚丰"]
    assert doc["validation"]["new_threshold_created"] is False

def test_no_new_semantics_or_production_entry():
    doc = load(MAP)
    assert all(x["executable_registry_entry"] is False for x in doc["mappings"])
    for key in ("production_registry_modified", "product_runtime_modified", "canonical_source_rows_modified",
                "shared_semantics_modified", "new_atom_created", "new_probability_created",
                "new_numeric_weight_created", "new_threshold_created"):
        assert doc["validation"][key] is False
