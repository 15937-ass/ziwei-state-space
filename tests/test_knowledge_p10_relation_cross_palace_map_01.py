import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "knowledge/palaces/P10_property/wp07a/PROPERTY_RELATION_CROSS_PALACE_MAP_01_v0.1.json"
ONTOLOGY = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
CSV_FILES = [
    ROOT / "validation/wp05/TP01_property_projection_review_001_100.csv",
    ROOT / "validation/wp05/TP02_property_projection_review_101_200.csv",
]
READ_FILES = [
    ROOT / "knowledge/wp05/property/PROPERTY_TP01_SOURCE_READJUDICATION_100_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP02_SOURCE_READJUDICATION_100_v0.1.json",
]
TIME_FILES = [
    ROOT / "knowledge/wp05/property/PROPERTY_TP01_SOURCE_TIME_SCOPE_v0.1.json",
    ROOT / "knowledge/wp05/property/PROPERTY_TP02_SOURCE_TIME_SCOPE_v0.1.json",
]
EXPECTED = {
    "TP01-027": ("紫微七杀同度或对拱", "methodology", "tianfu_condition_is_required_to_refine_property_outcome", "CROSS_PALACE_CONSTRAINT", "田宅宫printed_p156"),
    "TP02-129": ("武曲七杀与天府对拱", "methodology", "tianfu_resource_condition_is_required_to_refine_wuqu_qisha_property_outcome", "CROSS_PALACE_CONSTRAINT", "田宅宫printed_p159"),
    "TP02-163": ("天同与天梁对拱相对同度比较", "property_acquisition", "opposition_variant_is_relatively_smoother_for_property_acquisition", "STRUCTURAL_CONSTRAINT", "田宅宫printed_p160"),
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
    wanted = set(EXPECTED)
    for path in CSV_FILES:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if row["projection_rule_id"] in wanted:
                    out[row["projection_rule_id"]] = row
    return out


def records(paths):
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
        "engine": {"name": "knowledge-p10-relation-cross-palace-test", "version": "1", "adapter_version": "0.2"},
        "input": {},
        "natal": {"palaces": palaces},
    }


def facts_for(stars_by_palace, ontology):
    return resolve_palace_structure(snapshot(stars_by_palace), ontology).runtime_facts()


def test_three_rows_match_latest_canonical_source_and_sidecars():
    doc = load(MAP)
    source, review, scope = csv_rows(), records(READ_FILES), records(TIME_FILES)
    mapped = {item["source_rule_id"]: item for item in doc["mappings"]}
    assert set(mapped) == set(EXPECTED) and len(mapped) == 3
    assert doc["validation"]["nominated_rows"] == doc["validation"]["mapped_rows"] == 3
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
        assert not time.get("unmapped_source_time_labels", [])
        assert row["case_support_only"] == "false" and audited["case_support_only"] is False
        assert row["review_status"] == prov["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert row["source_span_verified"] == "true" and prov["source_span_verified"] is True
        assert item["executable_registry_entry"] is False
        atoms = list(item["condition"].get("all_of", []))
        for branch in item["condition"].get("alternatives", []):
            atoms.extend(branch)
        assert all(atom["atom_type"] in ALLOWED_ATOM_TYPES for atom in atoms)
        assert set(item["condition_atom_types"]) == {"PALACE_HAS_STAR", "PALACE_RELATION"}


def test_resolver_facts_match_each_complete_source_supported_geometry():
    doc, ontology = load(MAP), load_palace_ontology(ONTOLOGY)
    mapped = {item["source_rule_id"]: item for item in doc["mappings"]}
    for rid, item in mapped.items():
        condition = compile_condition_spec(item["condition"])
        for pattern in item["expected_runtime_fact_patterns"]:
            stars = {}
            for atom in pattern:
                if atom["atom_type"] == "PALACE_HAS_STAR":
                    stars.setdefault(atom["args"]["palace"], []).append(atom["args"]["star"])
            facts = facts_for(stars, ontology)
            for atom in pattern:
                assert fact_from_atom(atom["atom_type"], **atom["args"]) in facts
            assert condition.matches(facts), rid


def test_tp01_027_preserves_same_palace_or_opposite_palace_branches():
    doc = load(MAP)
    item = next(x for x in doc["mappings"] if x["source_rule_id"] == "TP01-027")
    condition = compile_condition_spec(item["condition"])
    ontology = load_palace_ontology(ONTOLOGY)
    same = facts_for({"P10": ["紫微", "七杀"]}, ontology)
    opposite = facts_for({"P10": ["紫微"], "P04": ["七杀"]}, ontology)
    incomplete = facts_for({"P10": ["紫微"]}, ontology)
    assert condition.matches(same)
    assert condition.matches(opposite)
    assert not condition.matches(incomplete)
    assert len(item["condition"]["alternatives"]) == 2
    assert all("SELF" not in str(atom) for branch in item["condition"]["alternatives"] for atom in branch)


def test_tp02_129_requires_both_wuqu_qisha_and_opposite_tianfu():
    doc = load(MAP)
    item = next(x for x in doc["mappings"] if x["source_rule_id"] == "TP02-129")
    condition = compile_condition_spec(item["condition"])
    ontology = load_palace_ontology(ONTOLOGY)
    complete = facts_for({"P10": ["武曲", "七杀"], "P04": ["天府"]}, ontology)
    no_tianfu = facts_for({"P10": ["武曲", "七杀"]}, ontology)
    no_qisha = facts_for({"P10": ["武曲"], "P04": ["天府"]}, ontology)
    assert condition.matches(complete)
    assert not condition.matches(no_tianfu)
    assert not condition.matches(no_qisha)
    state = item["source_context"]["unresolved_state_dependency"]
    assert state["state_representable_by_current_approved_atoms"] is False
    assert state["do_not_infer_from_missing_TRANSFORMATION_PRESENT"] is True


def test_tp01_027_tianfu_state_is_not_inferred_from_geometry():
    doc = load(MAP)
    item = next(x for x in doc["mappings"] if x["source_rule_id"] == "TP01-027")
    state = item["source_context"]["unresolved_state_dependency"]
    assert state["state_representable_by_current_approved_atoms"] is False
    assert state["do_not_infer_from_missing_TRANSFORMATION_PRESENT"] is True
    assert "府库空露" in state["required_state"]


def test_tp02_163_retains_relative_comparison_without_runtime_comparator():
    doc = load(MAP)
    item = next(x for x in doc["mappings"] if x["source_rule_id"] == "TP02-163")
    comparison = item["source_context"]["comparison_basis"]
    assert item["expected_projection"]["projection_target"] == "opposition_variant_is_relatively_smoother_for_property_acquisition"
    assert "P10 天同 + P10 天梁同宫" == comparison["baseline_variant"]
    assert comparison["runtime_comparator_created"] is False
    assert "较为顺利" in item["source_anchor_phrase"]


def test_no_new_semantics_or_production_entry():
    doc = load(MAP)
    assert all(item["executable_registry_entry"] is False for item in doc["mappings"])
    for key in (
        "production_registry_modified", "product_runtime_modified", "canonical_source_rows_modified",
        "shared_semantics_modified", "new_atom_created", "new_probability_created",
        "new_numeric_weight_created", "new_threshold_created",
    ):
        assert doc["validation"][key] is False
