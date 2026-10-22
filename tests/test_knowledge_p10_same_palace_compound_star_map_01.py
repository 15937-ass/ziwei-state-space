import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "knowledge/palaces/P10_property/wp07a/PROPERTY_SAME_PALACE_COMPOUND_STAR_MAP_01_v0.1.json"
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
    "TP01-071": ("天机巨门组合", "property_dispute", "property_dispute_tendency_strengthens", "FUNCTIONAL_PROJECTION", "田宅宫printed_p157"),
    "TP01-072": ("天机巨门组合", "property_acquisition", "property_acquisition_is_more_difficult", "FUNCTIONAL_PROJECTION", "田宅宫printed_p157"),
    "TP01-097": ("太阳天梁组合", "residence_environment", "public_or_communal_housing_scene", "SCENE_TRANSLATION", "田宅宫printed_p158"),
    "TP02-121": ("武曲贪狼同度成火贪铃贪", "property_scale", "ancestral_or_parental_property_can_increase_suddenly", "FUNCTIONAL_PROJECTION", "田宅宫printed_p159"),
    "TP02-126": ("武曲天府", "property", "property_structure_is_generally_supported_and_prefers_tianfu_with_lu", "STRUCTURAL_CONSTRAINT", "田宅宫printed_p159"),
    "TP02-160": ("天同天梁组合", "property_acquisition", "property_trading_or_high_mobility_property_scene", "SCENE_TRANSLATION", "田宅宫printed_p160"),
    "TP02-186": ("廉贞七杀", "property_acquisition", "ancestral_property_is_absent_or_thin_but_self_acquisition_is_possible", "FUNCTIONAL_PROJECTION", "田宅宫printed_p161"),
    "TP03-226": ("太阴天同组合", "residence_environment", "garden_vegetation_or_natural_amenity_property_scene", "SCENE_TRANSLATION", "田宅宫printed_p162"),
    "TP03-227": ("太阴天机组合", "relocation", "residence_or_property_movement_tendency_strengthens", "FUNCTIONAL_PROJECTION", "田宅宫printed_p162"),
    "TP04-306": ("天梁天机组合", "relocation", "frequent_residence_or_work_environment_change_is_structural", "FUNCTIONAL_PROJECTION", "田宅宫printed_p164"),
    "TP04-310": ("天梁天机组合", "household_change", "old_property_renovation_scene", "SCENE_TRANSLATION", "田宅宫printed_p164"),
    "TP04-311": ("天梁天同组合", "household_change", "furniture_or_household_asset_replacement_scene", "SCENE_TRANSLATION", "田宅宫printed_p164"),
    "TP04-340": ("廉贞七杀或武曲七杀", "fengshui_sensitivity", "fengshui_attention_is_more_relevant_in_lian_qisha_or_wu_qisha_variants", "STRUCTURAL_CONSTRAINT", "田宅宫printed_p165"),
}
PALACES = [
    ("P01", "命宫"), ("P02", "兄弟宫"), ("P03", "夫妻宫"), ("P04", "子女宫"),
    ("P05", "财帛宫"), ("P06", "疾厄宫"), ("P07", "迁移宫"), ("P08", "交友宫"),
    ("P09", "事业宫"), ("P10", "田宅宫"), ("P11", "福德宫"), ("P12", "父母宫"),
]
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_rows():
    out = {}
    wanted = set(EXPECTED)
    for path in CSV_FILES:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if row["projection_rule_id"] in wanted:
                    out[row["projection_rule_id"]] = row
    return out


def sidecar_records(paths):
    out = {}
    for path in paths:
        for row in load(path).get("records", []):
            out[row["projection_rule_id"]] = row
    return out


def snapshot(stars_by_palace):
    palaces = {}
    for i, (palace_id, name) in enumerate(PALACES):
        branch = BRANCHES[i]
        stars = [
            {"name": star, "brightness": None, "mutagen": None, "type": None, "scope": None}
            for star in stars_by_palace.get(palace_id, [])
        ]
        palaces[branch] = {
            "name": name, "stem": "甲", "branch": branch, "is_body_palace": False,
            "major_stars": stars, "minor_stars": [], "adjective_stars": [],
        }
    return {
        "schema_version": "0.2",
        "engine": {"name": "knowledge-p10-same-palace-compound-map-test", "version": "1", "adapter_version": "0.2"},
        "input": {},
        "natal": {"palaces": palaces},
    }


def test_thirteen_rows_match_canonical_source_and_sidecars():
    doc = load(MAP)
    source, review, scope = source_rows(), sidecar_records(READ_FILES), sidecar_records(TIME_FILES)
    mapped = {item["source_rule_id"]: item for item in doc["mappings"]}
    assert set(mapped) == set(EXPECTED) and len(mapped) == 13
    assert doc["scope"]["nominated_source_rule_ids"] == list(EXPECTED)
    assert doc["validation"]["nominated_rows"] == doc["validation"]["mapped_rows"] == 13
    assert doc["validation"]["blocked_nominated_rows"] == 0

    for rid, (condition, domain, target, mode, location) in EXPECTED.items():
        item, row, audited, time = mapped[rid], source[rid], review[rid], scope[rid]
        prov, projection = item["source_provenance"], item["expected_projection"]
        assert row["source_id"] == prov["source_id"] == "SRC-ZZ-003"
        assert row["source_location"] == prov["source_location"] == location
        assert row["condition"] == audited["canonical_condition"] == item["source_condition_text"] == condition
        assert (row["projection_domain"], row["projection_target"], row["projection_mode"]) == (domain, target, mode)
        assert (projection["projection_domain"], projection["projection_target"], projection["projection_mode"]) == (domain, target, mode)
        assert row["time_layer"] == prov["time_layer"] == time["legacy_primary_time_layer"] == "NATAL"
        assert time["source_time_layers"] == ["NATAL"]
        assert time["scope_status"] == item["source_time_scope"]["scope_status"] == "SOURCE_SCOPE_MATCHES_PRIMARY_LAYER"
        assert not time.get("unmapped_source_time_labels", [])
        assert row["case_support_only"] == "false" and audited["case_support_only"] is False
        assert row["review_status"] == prov["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert row["source_span_verified"] == "true" and prov["source_span_verified"] is True
        assert item["condition_atom_types"] == ["PALACE_HAS_STAR"]
        assert item["executable_registry_entry"] is False
        atoms = list(item["condition"].get("all_of", []))
        for branch in item["condition"].get("alternatives", []):
            atoms.extend(branch)
        assert atoms and all(atom["atom_type"] == "PALACE_HAS_STAR" for atom in atoms)
        assert all(atom["atom_type"] in ALLOWED_ATOM_TYPES for atom in atoms)
        assert all(atom["args"]["palace"] == "P10" for atom in atoms)


def test_resolver_emits_all_same_palace_patterns_and_compiled_conditions_match():
    doc, ontology = load(MAP), load_palace_ontology(ONTOLOGY)
    for item in doc["mappings"]:
        condition = compile_condition_spec(item["condition"])
        assert len(item["expected_runtime_fact_patterns"]) in (1, 2)
        for pattern in item["expected_runtime_fact_patterns"]:
            stars = {}
            for atom in pattern:
                assert atom["atom_type"] == "PALACE_HAS_STAR"
                stars.setdefault(atom["args"]["palace"], []).append(atom["args"]["star"])
            assert set(stars) == {"P10"}
            facts = resolve_palace_structure(snapshot(stars), ontology).runtime_facts()
            for atom in pattern:
                assert fact_from_atom(atom["atom_type"], **atom["args"]) in facts
            assert condition.matches(facts), item["source_rule_id"]


def test_same_palace_binding_is_not_weakened_to_stars_anywhere():
    doc, ontology = load(MAP), load_palace_ontology(ONTOLOGY)
    item = next(x for x in doc["mappings"] if x["source_rule_id"] == "TP01-071")
    condition = compile_condition_spec(item["condition"])
    other_palace_facts = resolve_palace_structure(
        snapshot({"P04": ["天机", "巨门"]}), ontology
    ).runtime_facts()
    assert not condition.matches(other_palace_facts)


def test_fire_tan_and_bell_tan_are_distinct_explicit_alternatives():
    doc = load(MAP)
    item = next(x for x in doc["mappings"] if x["source_rule_id"] == "TP02-121")
    condition = compile_condition_spec(item["condition"])
    assert len(item["condition"]["alternatives"]) == 2
    assert [branch[0]["args"]["star"] for branch in item["condition"]["alternatives"]] == ["火星", "铃星"]
    assert condition.matches(resolve_palace_structure(snapshot({"P10": ["武曲", "贪狼", "火星"]}), load_palace_ontology(ONTOLOGY)).runtime_facts())
    assert condition.matches(resolve_palace_structure(snapshot({"P10": ["武曲", "贪狼", "铃星"]}), load_palace_ontology(ONTOLOGY)).runtime_facts())
    assert not condition.matches(resolve_palace_structure(snapshot({"P10": ["武曲", "贪狼"]}), load_palace_ontology(ONTOLOGY)).runtime_facts())


def test_lian_qisha_and_wu_qisha_are_distinct_explicit_alternatives():
    doc = load(MAP)
    item = next(x for x in doc["mappings"] if x["source_rule_id"] == "TP04-340")
    condition = compile_condition_spec(item["condition"])
    assert len(item["condition"]["alternatives"]) == 2
    assert item["condition"]["all_of"][0]["args"]["star"] == "七杀"
    assert [branch[0]["args"]["star"] for branch in item["condition"]["alternatives"]] == ["廉贞", "武曲"]
    ontology = load_palace_ontology(ONTOLOGY)
    assert condition.matches(resolve_palace_structure(snapshot({"P10": ["廉贞", "七杀"]}), ontology).runtime_facts())
    assert condition.matches(resolve_palace_structure(snapshot({"P10": ["武曲", "七杀"]}), ontology).runtime_facts())
    assert not condition.matches(resolve_palace_structure(snapshot({"P10": ["七杀"]}), ontology).runtime_facts())


def test_tianfu_treasury_state_remains_an_explicit_unresolved_dependency():
    doc = load(MAP)
    item = next(x for x in doc["mappings"] if x["source_rule_id"] == "TP02-126")
    state = item["source_context"]["unresolved_state_dependency"]
    assert item["mapping_status"] == "MAPPED_GEOMETRY_WITH_EXPLICIT_UNRESOLVED_STATE_DEPENDENCY"
    assert state["state_representable_by_current_approved_atoms"] is False
    assert state["do_not_infer_from_missing_TRANSFORMATION_PRESENT"] is True
    assert all(atom["atom_type"] == "PALACE_HAS_STAR" for atom in item["condition"]["all_of"])


def test_no_new_semantics_or_production_entry():
    doc = load(MAP)
    assert all(item["executable_registry_entry"] is False for item in doc["mappings"])
    for key in (
        "production_registry_modified", "product_runtime_modified", "canonical_source_rows_modified",
        "shared_semantics_modified", "new_atom_created", "new_probability_created",
        "new_numeric_weight_created", "new_threshold_created", "new_time_primitive_created",
    ):
        assert doc["validation"][key] is False
    mapped_ids = {item["source_rule_id"] for item in doc["mappings"]}
    assert not mapped_ids.intersection(item["source_rule_id"] for item in doc["explicit_non_scope"])
