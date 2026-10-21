import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "knowledge/palaces/P10_property/wp07a/PROPERTY_DIRECT_STAR_PRESENCE_MAP_01_v0.1.json"
ONTOLOGY = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
CSV_FILES = [
    ROOT / "validation/wp05/TP01_property_projection_review_001_100.csv",
    ROOT / "validation/wp05/TP02_property_projection_review_101_200.csv",
    ROOT / "validation/wp05/TP03_property_projection_review_201_300.csv",
    ROOT / "validation/wp05/TP04_property_projection_review_301_358.csv",
]
READ_FILES = [
    ROOT / "knowledge/wp05/property/PROPERTY_TP01_SOURCE_READJUDICATION_100_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP02_SOURCE_READJUDICATION_100_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP03_SOURCE_READJUDICATION_100_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP04_SOURCE_READJUDICATION_58_v0.1.json",
]
TIME_FILES = [
    ROOT / "knowledge/wp05/property/PROPERTY_TP01_SOURCE_TIME_SCOPE_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP02_SOURCE_TIME_SCOPE_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP03_SOURCE_TIME_SCOPE_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP04_SOURCE_TIME_SCOPE_v0.1.json",
]
EXPECTED = {
    "TP01-055": ("天机", "天机守田宅宫", "property_stability", "property_and_residential_change_are_structural", "FUNCTIONAL_PROJECTION", "田宅宫printed_p157"),
    "TP02-195": ("天府", "天府守田宅宫", "inheritance_existing_property", "ancestral_or_parental_property_or_reputable_service_institution_base_is_supported", "FUNCTIONAL_PROJECTION", "田宅宫printed_p161-162"),
    "TP03-297": ("天相", "天相守田宅", "fengshui_sensitivity", "fengshui_sensitivity_is_relatively_high", "FUNCTIONAL_PROJECTION", "田宅宫printed_p164"),
    "TP04-319": ("天梁", "天梁守田宅一般情况", "fengshui_sensitivity", "fengshui_sensitivity_is_relatively_low", "FUNCTIONAL_PROJECTION", "田宅宫printed_p164"),
    "TP04-358": ("破军", "破军守田宅", "fengshui_sensitivity", "fengshui_sensitivity_is_relatively_low", "FUNCTIONAL_PROJECTION", "田宅宫printed_p165"),
}
EXCLUDED = {"TP01-018", "TP02-139", "TP02-170", "TP03-261", "TP03-275", "TP03-288", "TP04-320", "TP04-321"}
PALACES = [
    ("P01", "命宫"), ("P02", "兄弟宫"), ("P03", "夫妻宫"), ("P04", "子女宫"),
    ("P05", "财帛宫"), ("P06", "疾厄宫"), ("P07", "迁移宫"), ("P08", "交友宫"),
    ("P09", "事业宫"), ("P10", "田宅宫"), ("P11", "福德宫"), ("P12", "父母宫"),
]
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def csv_rows():
    out = {}
    for path in CSV_FILES:
        with path.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                rid = row["projection_rule_id"]
                if rid in EXPECTED or rid in EXCLUDED:
                    out[rid] = row
    return out

def records(paths):
    out = {}
    for path in paths:
        for row in load(path).get("records", []):
            out[row["projection_rule_id"]] = row
    return out

def snapshot(star_name):
    palaces = {}
    for i, (_, name) in enumerate(PALACES):
        branch = BRANCHES[i]
        stars = [{"name": star_name, "brightness": None, "mutagen": None, "type": None, "scope": None}] if name == "田宅宫" else []
        palaces[branch] = {"name": name, "stem": "甲", "branch": branch, "is_body_palace": False,
                           "major_stars": stars, "minor_stars": [], "adjective_stars": []}
    return {"schema_version": "0.2",
            "engine": {"name": "knowledge-p10-star-presence-test", "version": "1", "adapter_version": "0.2"},
            "input": {}, "natal": {"palaces": palaces}}

def test_five_direct_rows_match_canonical_source_and_sidecars():
    doc, source, review, scope = load(MAP), csv_rows(), records(READ_FILES), records(TIME_FILES)
    mapped = {x["source_rule_id"]: x for x in doc["mappings"]}
    assert set(mapped) == set(EXPECTED) and len(mapped) == 5
    assert doc["validation"]["nominated_rows"] == doc["validation"]["mapped_rows"] == 5
    assert doc["validation"]["blocked_nominated_rows"] == 0
    for rid, (star, condition, domain, target, mode, location) in EXPECTED.items():
        item, row, audited, time = mapped[rid], source[rid], review[rid], scope[rid]
        prov, proj = item["source_provenance"], item["expected_projection"]
        assert row["source_id"] == prov["source_id"] == "SRC-ZZ-003"
        assert row["source_location"] == prov["source_location"] == location
        assert row["condition"] == audited["canonical_condition"] == item["source_condition_text"] == condition
        assert (row["projection_domain"], row["projection_target"], row["projection_mode"]) == (domain, target, mode)
        assert (proj["projection_domain"], proj["projection_target"], proj["projection_mode"]) == (domain, target, mode)
        assert row["time_layer"] == prov["time_layer"] == time["legacy_primary_time_layer"] == "NATAL"
        assert time["source_time_layers"] == ["NATAL"]
        assert row["case_support_only"] == "false" and audited["case_support_only"] is False
        assert row["review_status"] == prov["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert row["source_span_verified"] == "true" and prov["source_span_verified"] is True
        atom = item["condition"]["all_of"][0]
        assert atom == item["expected_runtime_fact"]
        assert atom["atom_type"] == "PALACE_HAS_STAR" and atom["atom_type"] in ALLOWED_ATOM_TYPES
        assert atom["args"] == {"palace": "P10", "star": star}
        assert item["condition_atom_types"] == ["PALACE_HAS_STAR"]
        assert item["executable_registry_entry"] is False

def test_current_resolver_emits_exact_palace_bound_star_fact():
    doc, ontology = load(MAP), load_palace_ontology(ONTOLOGY)
    for item in doc["mappings"]:
        atom = item["condition"]["all_of"][0]
        args = atom["args"]
        facts = resolve_palace_structure(snapshot(args["star"]), ontology).runtime_facts()
        assert fact_from_atom("PALACE_HAS_STAR", **args) in facts

def test_contextual_and_compound_rows_remain_excluded():
    doc, source = load(MAP), csv_rows()
    excluded = {x["source_rule_id"]: x for x in doc["exclusions"]}
    assert set(excluded) == EXCLUDED
    for rid in EXCLUDED:
        assert excluded[rid]["source_condition_text"] == source[rid]["condition"]
        assert excluded[rid]["source_location"] == source[rid]["source_location"]
        assert excluded[rid]["case_support_only"] == (source[rid]["case_support_only"] == "true")
    assert excluded["TP01-018"]["reason_code"] == "EXCLUSIVITY_NOT_CAPTURED_BY_PRESENCE_ATOM"
    assert excluded["TP04-320"]["reason_code"] == "COMPOUND_EXCEPTION_NOT_COLLAPSED"
    assert excluded["TP04-321"]["reason_code"] == "EXCLUSIVITY_AND_BRANCH_SCOPE"

def test_no_new_semantics_or_production_entry():
    doc = load(MAP)
    assert all(x["executable_registry_entry"] is False for x in doc["mappings"])
    for key in ("production_registry_modified", "product_runtime_modified", "canonical_source_rows_modified",
                "shared_semantics_modified", "new_atom_created", "new_probability_created",
                "new_numeric_weight_created", "new_threshold_created"):
        assert doc["validation"][key] is False
