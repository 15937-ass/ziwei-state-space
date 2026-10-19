import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "knowledge/wp07a/CAREER_CROSS_PALACE_MAP_CA01_066_CA02_188_CA03_255_v0.1.json"
ONTOLOGY_PATH = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
CSV_PATHS = (
    ROOT / "validation/wp05/CA01_career_projection_review_001_100.csv",
    ROOT / "validation/wp05/CA02_career_projection_review_101_200.csv",
    ROOT / "validation/wp05/CA03_career_projection_review_201_300.csv",
)
BRANCHES = list("子丑寅卯辰巳午未申酉戌")
PALACES = [
    ("P01", "命宫"), ("P02", "兄弟宫"), ("P03", "夫妻宫"),
    ("P04", "子女宫"), ("P05", "财帛宫"), ("P06", "疾厄宫"),
    ("P07", "迁移宫"), ("P08", "交友宫"), ("P09", "事业宫"),
    ("P10", "田宅宫"), ("P11", "福德宫"), ("P12", "父母宫"),
]
EXPECTED = {
    "CA01-066": {"projection_target": "partnership_venture_suited", "projection_mode": "CROSS_PALACE_CONSTRAINT"},
    "CA02-188": {"projection_target": "career_speculation_tendency_strengthened_by_wealth_context", "projection_mode": "CROSS_PALACE_CONSTRAINT"},
    "CA03-255": {"projection_target": "mental_burden_and_extra_work_strengthened", "projection_mode": "CROSS_PALACE_CONSTRAINT"},
}

def _mapping():
    return json.loads(MAPPING_PATH.read_text(encoding="utf-8"))


def _source_rows():
    result = {}
    for path in CSV_PATHS:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            result.update({row["projection_rule_id"]: row for row in csv.DictReader(handle)})
    return result


def _snapshot(stars_by_palace, p09_branch="申"):
    p09_index = next(i for i, (pid, _) in enumerate(PALACES) if pid == "P09")
    offset = (BRANCHES.index(p09_branch) - p09_index) % len(BRANCHES)
    raw_palaces = {}
    for i, (palace_id, palace_name) in enumerate(PALACES):
        branch = BRANCHES[(i + offset) % len(BRANCHES)]
        raw_palaces[branch] = {
            "name": palace_name, "stem": "甲", "branch": branch, "is_body_palace": False,
            "major_stars": stars_by_palace.get(palace_id, []),
            "minor_stars": [], "adjective_stars": [],
        }
    return {
        "schema_version": "0.2",
        "engine": {"name": "knowledge-cross-palace-test", "version": "1", "adapter_version": "0.2"},
        "input": {}, "natal": {"palaces": raw_palaces},
    }


def _matches(rule_id, stars_by_palace, p09_branch="申"):
    doc = _mapping()
    item = next(x for x in doc["mappings"] if x["source_rule_id"] == rule_id)
    ontology = load_palace_ontology(ONTOLOGY_PATH)
    facts = resolve_palace_structure(_snapshot(stars_by_palace, p09_branch), ontology).runtime_facts()
    return compile_condition_spec(item["condition"]).matches(facts)


def test_source_provenance_and_projection_are_preserved():
    doc = _mapping()
    source = _source_rows()
    mapped = {item["source_rule_id"]: item for item in doc["mappings"]}
    assert set(mapped) == set(EXPECTED)
    assert doc["validation"]["nominated_rows"] == doc["validation"]["mapped_rows"] == 3
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
        assert item["executable_registry_entry"] is False
        for atom in item["condition"].get("all_of", []):
            assert atom["atom_type"] in ALLOWED_ATOM_TYPES
        for group in item["condition"].get("alternatives", []):
            assert group
            for atom in group:
                assert atom["atom_type"] in ALLOWED_ATOM_TYPES
        assert set(item["condition_atom_types"]).issubset(ALLOWED_ATOM_TYPES)


def test_ca01_066_branch_alternatives_are_complete_and_bound():
    stars = {"P09": [{"name": "紫微"}], "P05": [{"name": "廉贞", "mutagen": "禄"}]}
    assert _matches("CA01-066", stars, "子")
    assert _matches("CA01-066", stars, "午")
    assert not _matches("CA01-066", stars, "申")
    assert not _matches("CA01-066", {"P09": [{"name": "紫微"}, {"name": "廉贞", "mutagen": "禄"}]}, "午")


def test_ca02_188_requires_all_conditions_in_correct_palaces():
    stars = {"P09": [{"name": "天机", "mutagen": "禄"}], "P05": [{"name": "太阴", "mutagen": "忌"}]}
    assert _matches("CA02-188", stars, "午")
    assert not _matches("CA02-188", stars, "未")
    assert not _matches("CA02-188", {"P09": [{"name": "天机", "mutagen": "禄"}, {"name": "太阴", "mutagen": "忌"}]}, "午")
    assert not _matches("CA02-188", {"P09": [{"name": "天机", "mutagen": "禄"}]}, "午")


def test_ca03_255_preserves_life_palace_system_context():
    stars = {"P09": [{"name": "天机", "mutagen": "科"}], "P01": [{"name": "天同"}, {"name": "巨门", "mutagen": "忌"}]}
    assert _matches("CA03-255", stars)
    assert not _matches("CA03-255", {"P09": [{"name": "天机", "mutagen": "科"}], "P01": [{"name": "巨门", "mutagen": "忌"}]})
    assert not _matches("CA03-255", {"P09": [{"name": "天机", "mutagen": "科"}, {"name": "巨门", "mutagen": "忌"}], "P01": [{"name": "天同"}]})


def test_cross_palace_mappings_remain_non_executable():
    doc = _mapping()
    assert all(item["execution_readiness"] == "STATIC_CROSS_PALACE_CANDIDATE_NOT_EXECUTABLE" for item in doc["mappings"])
    assert all(item["executable_registry_entry"] is False for item in doc["mappings"])
    assert doc["validation"]["product_runtime_modified"] is False
    assert doc["validation"]["production_registry_modified"] is False
    assert doc["validation"]["new_atom_or_ontology_semantics_created"] is False
    assert doc["validation"]["numeric_weights_or_probabilities_created"] is False


def test_exclusions_are_explicit_and_semantically_bounded():
    doc = _mapping()
    exclusions = {item["source_rule_id"]: item["reason_code"] for item in doc["exclusions"]}
    assert exclusions["CA01-020"] == "OMITTED_CONTEXT_WOULD_OVERGENERALIZE"
    assert exclusions["CA01-064"] == "AMBIGUOUS_DE_LU"
    assert exclusions["CA01-065"] == "LU_MA_RELATION_UNRESOLVED"
    assert exclusions["CA02-170"] == "PREVIOUS_RULE_CONTEXT_REQUIRED"
