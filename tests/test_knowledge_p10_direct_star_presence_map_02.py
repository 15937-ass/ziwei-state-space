import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "knowledge/palaces/P10_property/wp07a/PROPERTY_DIRECT_STAR_PRESENCE_MAP_02_v0.1.json"
ONTOLOGY = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
CSV_FILES = [
    ROOT / "validation/wp05/TP01_property_projection_review_001_100.csv",
    ROOT / "validation/wp05/TP02_property_projection_review_101_200.csv",
    ROOT / "validation/wp05/TP03_property_projection_review_201_300.csv",
    ROOT / "validation/wp05/TP04_property_projection_review_301_358.csv",
]
READ_FILES = [
    ROOT / "knowledge/wp05/property/PROPERTY_TP02_SOURCE_READJUDICATION_100_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP03_SOURCE_READJUDICATION_100_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP04_SOURCE_READJUDICATION_58_v0.1.json",
]
TIME_FILES = [
    ROOT / "knowledge/wp05/property/PROPERTY_TP02_SOURCE_TIME_SCOPE_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP03_SOURCE_TIME_SCOPE_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP04_SOURCE_TIME_SCOPE_v0.1.json",
]
EXPECTED = {
    "TP02-134": ("武曲", "武曲守田宅", "service_institution", "financial_institution_service_scene", "SCENE_TRANSLATION", "田宅宫printed_p160"),
    "TP02-139": ("天同", "天同守田宅宫", "property_acquisition", "self_made_property_acquisition_is_supported", "FUNCTIONAL_PROJECTION", "田宅宫printed_p160"),
    "TP03-207": ("天府", "天府守田宅一般情况", "service_institution", "work_or_service_institution_tends_to_be_stable", "FUNCTIONAL_PROJECTION", "田宅宫printed_p162"),
    "TP03-214": ("天府", "天府守田宅一般情况", "fengshui_sensitivity", "fengshui_sensitivity_is_relatively_low", "FUNCTIONAL_PROJECTION", "田宅宫printed_p162"),
    "TP04-319": ("天梁", "天梁守田宅一般情况", "fengshui_sensitivity", "fengshui_sensitivity_is_relatively_low", "FUNCTIONAL_PROJECTION", "田宅宫printed_p164"),
    "TP04-339": ("七杀", "七杀守田宅一般情况", "fengshui_sensitivity", "fengshui_sensitivity_is_relatively_low", "FUNCTIONAL_PROJECTION", "田宅宫printed_p165"),
}
EXCEPTIONS = {
    "TP03-204": ("天府关陀夹同时火铃夹", "pressure_can_force_property_movement_or_sale", "FUNCTIONAL_PROJECTION", "田宅宫printed_p162"),
    "TP03-209": ("天府见煞忌刑耗同会", "service_institution_personnel_dispute_pressure_strengthens", "FUNCTIONAL_PROJECTION", "田宅宫printed_p162"),
    "TP03-215": ("天府与天姚阴煞同度", "fengshui_sensitivity_strengthens", "STRUCTURAL_CONSTRAINT", "田宅宫printed_p162"),
    "TP04-320": ("天梁与阴煞同度又见火铃", "fengshui_sensitivity_strengthens", "STRUCTURAL_CONSTRAINT", "田宅宫printed_p164"),
    "TP04-340": ("廉贞七杀或武曲七杀", "fengshui_attention_is_more_relevant_in_lian_qisha_or_wu_qisha_variants", "STRUCTURAL_CONSTRAINT", "田宅宫printed_p165"),
}
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
    wanted = set(EXPECTED) | set(EXCEPTIONS)
    for path in CSV_FILES:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                rid = row["projection_rule_id"]
                if rid in wanted:
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
        palaces[branch] = {
            "name": name, "stem": "甲", "branch": branch, "is_body_palace": False,
            "major_stars": stars, "minor_stars": [], "adjective_stars": [],
        }
    return {
        "schema_version": "0.2",
        "engine": {"name": "knowledge-p10-star-presence-remainder-test", "version": "1", "adapter_version": "0.2"},
        "input": {},
        "natal": {"palaces": palaces},
    }


def test_six_direct_rows_match_canonical_source_and_sidecars():
    doc, source, review, scope = load(MAP), csv_rows(), records(READ_FILES), records(TIME_FILES)
    mapped = {item["source_rule_id"]: item for item in doc["mappings"]}
    assert set(mapped) == set(EXPECTED) and len(mapped) == 6
    assert doc["validation"]["nominated_rows"] == doc["validation"]["mapped_rows"] == 6
    assert doc["validation"]["blocked_nominated_rows"] == 0
    for rid, (star, condition, domain, target, mode, location) in EXPECTED.items():
        item, row, audited, time = mapped[rid], source[rid], review[rid], scope[rid]
        prov, projection = item["source_provenance"], item["expected_projection"]
        assert row["source_id"] == prov["source_id"] == "SRC-ZZ-003"
        assert row["source_location"] == prov["source_location"] == location
        assert row["condition"] == audited["canonical_condition"] == item["source_condition_text"] == condition
        assert (row["projection_domain"], row["projection_target"], row["projection_mode"]) == (domain, target, mode)
        assert (projection["projection_domain"], projection["projection_target"], projection["projection_mode"]) == (domain, target, mode)
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


def test_base_rules_keep_contextual_and_compound_exceptions_separate():
    doc, source = load(MAP), csv_rows()
    exceptions = {item["source_rule_id"]: item for item in doc["separate_exceptions"]}
    assert set(exceptions) == set(EXCEPTIONS)
    mapped_ids = {item["source_rule_id"] for item in doc["mappings"]}
    assert not (mapped_ids & set(EXCEPTIONS))
    for rid, (condition, target, mode, location) in EXCEPTIONS.items():
        item, row = exceptions[rid], source[rid]
        assert item["source_condition_text"] == row["condition"] == condition
        assert item["source_location"] == row["source_location"] == location
        assert item["projection_target"] == row["projection_target"] == target
        assert item["projection_mode"] == row["projection_mode"] == mode
        assert row["case_support_only"] == "false"
        assert item["reason_code"] in {"CONTEXTUAL_EXCEPTION_NOT_COLLAPSED", "COMPOUND_EXCEPTION_NOT_COLLAPSED"}


def test_tiantong_direct_rule_has_no_opposite_palace_dependency():
    source = csv_rows()
    row = source["TP02-139"]
    assert row["condition"] == "天同守田宅宫"
    assert row["projection_target"] == "self_made_property_acquisition_is_supported"


def test_no_new_semantics_or_production_entry():
    doc = load(MAP)
    assert all(item["executable_registry_entry"] is False for item in doc["mappings"])
    for key in (
        "production_registry_modified", "product_runtime_modified", "canonical_source_rows_modified",
        "shared_semantics_modified", "new_atom_created", "new_probability_created",
        "new_numeric_weight_created", "new_threshold_created",
    ):
        assert doc["validation"][key] is False
