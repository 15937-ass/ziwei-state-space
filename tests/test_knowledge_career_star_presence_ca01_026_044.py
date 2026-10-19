import csv
import json

import pytest
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "knowledge/wp07a/CAREER_STAR_PRESENCE_MAP_CA01_026_044_v0.1.json"
ONTOLOGY_PATH = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
CSV_PATH = ROOT / "validation/wp05/CA01_career_projection_review_001_100.csv"
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")
PALACES = [
    ("P01", "命宫"), ("P02", "兄弟宫"), ("P03", "夫妻宫"),
    ("P04", "子女宫"), ("P05", "财帛宫"), ("P06", "疾厄宫"),
    ("P07", "迁移宫"), ("P08", "交友宫"), ("P09", "事业宫"),
    ("P10", "田宅宫"), ("P11", "福德宫"), ("P12", "父母宫"),
]
EXPECTED = {
    "CA01-026": ("career", "niche_or_nonmainstream_industry_suited", "SCENE_TRANSLATION", {"地空", "地劫"}),
    "CA01-027": ("method", "unconventional_operating_method_suited", "FUNCTIONAL_PROJECTION", {"地空", "地劫"}),
    "CA01-031": ("development", "career_development_slow", "FUNCTIONAL_PROJECTION", {"陀罗"}),
    "CA01-032": ("role", "nominal_status_exceeds_real_authority", "FUNCTIONAL_PROJECTION", {"陀罗"}),
    "CA01-033": ("stability", "career_reversals_or_instability", "FUNCTIONAL_PROJECTION", {"陀罗"}),
    "CA01-034": ("career", "engineering_or_technical_scene", "SCENE_TRANSLATION", {"擎羊"}),
    "CA01-042": ("career", "existing_business_or_salaried_role_preferred", "SCENE_TRANSLATION", {"禄存"}),
    "CA01-044": ("decision", "advance_retreat_indecision", "FUNCTIONAL_PROJECTION", {"禄存", "地空", "地劫"}),
}

def _mapping():
    return json.loads(MAPPING_PATH.read_text(encoding="utf-8"))


def _source_rows():
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["projection_rule_id"]: row for row in csv.DictReader(handle)}


def _snapshot(stars_by_palace):
    p09_index = next(i for i, (pid, _) in enumerate(PALACES) if pid == "P09")
    offset = (BRANCHES.index("申") - p09_index) % len(BRANCHES)
    raw_palaces = {}
    for i, (palace_id, palace_name) in enumerate(PALACES):
        branch = BRANCHES[(i + offset) % len(BRANCHES)]
        raw_palaces[branch] = {
            "name": palace_name, "stem": "甲", "branch": branch, "is_body_palace": False,
            "major_stars": [], "minor_stars": [], "adjective_stars": stars_by_palace.get(palace_id, []),
        }
    return {"schema_version": "0.2", "engine": {"name": "star-presence-test", "version": "1", "adapter_version": "0.2"}, "input": {}, "natal": {"palaces": raw_palaces}}


def _matches(rule_id, stars_by_palace):
    item = next(x for x in _mapping()["mappings"] if x["source_rule_id"] == rule_id)
    ontology = load_palace_ontology(ONTOLOGY_PATH)
    facts = resolve_palace_structure(_snapshot(stars_by_palace), ontology).runtime_facts()
    return compile_condition_spec(item["condition"]).matches(facts)


def test_source_provenance_and_projection_are_preserved():
    doc = _mapping()
    source = _source_rows()
    mapped = {item["source_rule_id"]: item for item in doc["mappings"]}
    assert set(mapped) == set(EXPECTED)
    assert doc["validation"]["nominated_rows"] == doc["validation"]["mapped_rows"] == 8
    for rule_id, (domain, target, mode, stars) in EXPECTED.items():
        row, item = source[rule_id], mapped[rule_id]
        prov = item["source_provenance"]
        assert row["source_id"] == prov["source_id"] == "SRC-ZZ-003"
        assert row["source_location"] == prov["source_location"]
        assert row["condition"] == item["source_condition_text"]
        assert row["review_status"] == prov["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert row["source_span_verified"].lower() == "true" and prov["source_span_verified"] is True
        assert row["time_layer"] == prov["time_layer"] == "NATAL"
        assert row["case_support_only"].lower() == "false" and prov["case_support_only"] is False
        assert row["history_feedback"] == prov["history_feedback"]
        assert row["projection_domain"] == domain == item["expected_projection"]["projection_domain"]
        assert row["projection_target"] == target == item["expected_projection"]["projection_target"]
        assert row["projection_mode"] == mode == item["expected_projection"]["projection_mode"]
        assert {a["args"]["star"] for a in item["condition"]["all_of"]} == stars
        assert all(a["args"]["palace"] == "P09" for a in item["condition"]["all_of"])
        assert all(a["atom_type"] == "PALACE_HAS_STAR" and a["atom_type"] in ALLOWED_ATOM_TYPES for a in item["condition"]["all_of"])
        assert item["executable_registry_entry"] is False


def test_two_star_kong_jie_rules_require_both_stars_in_career_palace():
    both = {"P09": [{"name": "地空"}, {"name": "地劫"}]}
    assert _matches("CA01-026", both)
    assert _matches("CA01-027", both)
    assert not _matches("CA01-026", {"P09": [{"name": "地空"}]})
    assert not _matches("CA01-027", {"P09": [{"name": "地劫"}]})
    assert not _matches("CA01-026", {"P09": [{"name": "地空"}], "P08": [{"name": "地劫"}]})


def test_three_tuoluo_targets_share_condition_but_not_projection():
    stars = {"P09": [{"name": "陀罗"}]}
    for rule_id in ("CA01-031", "CA01-032", "CA01-033"):
        assert _matches(rule_id, stars)
    assert not _matches("CA01-031", {})
    doc = {x["source_rule_id"]: x for x in _mapping()["mappings"]}
    assert len({doc[x]["expected_projection"]["projection_target"] for x in ("CA01-031", "CA01-032", "CA01-033")}) == 3


def test_qingyang_and_lucun_single_star_conditions():
    assert _matches("CA01-034", {"P09": [{"name": "擎羊"}]})
    assert not _matches("CA01-034", {})
    assert _matches("CA01-042", {"P09": [{"name": "禄存"}]})
    assert not _matches("CA01-042", {"P08": [{"name": "禄存"}]})


def test_lucun_kongjie_compound_requires_all_three_in_p09():
    all_three = {"P09": [{"name": "禄存"}, {"name": "地空"}, {"name": "地劫"}]}
    assert _matches("CA01-044", all_three)
    assert not _matches("CA01-044", {"P09": [{"name": "禄存"}, {"name": "地空"}]})
    assert not _matches("CA01-044", {"P09": [{"name": "禄存"}], "P08": [{"name": "地空"}, {"name": "地劫"}]})


def test_exclusions_and_non_execution_are_explicit():
    doc = _mapping()
    exclusions = {x["source_rule_id"]: x["reason_code"] for x in doc["exclusions"]}
    assert exclusions["CA01-035"] == "HUO_LING_SHORTHAND_AMBIGUOUS"
    assert exclusions["CA01-043"] == "PREVIOUS_RULE_CONTEXT_REQUIRED"
    assert all(x["execution_readiness"] == "STATIC_STAR_PRESENCE_CANDIDATE_NOT_EXECUTABLE" for x in doc["mappings"])
    assert all(x["executable_registry_entry"] is False for x in doc["mappings"])
    assert doc["validation"]["source_rows_modified"] is False
    assert doc["validation"]["product_runtime_modified"] is False
    assert doc["validation"]["production_registry_modified"] is False
    assert doc["validation"]["new_atom_or_ontology_semantics_created"] is False


@pytest.mark.parametrize("rule_id", sorted(EXPECTED))
def test_every_required_star_must_be_present_in_p09(rule_id):
    required = EXPECTED[rule_id][3]
    assert _matches(rule_id, {"P09": [{"name": s} for s in sorted(required)]})
    for missing in sorted(required):
        remaining = [{"name": s} for s in sorted(required - {missing})]
        assert not _matches(rule_id, {"P09": remaining})
        for palace_id, _ in PALACES:
            if palace_id != "P09":
                assert not _matches(rule_id, {
                    "P09": remaining, palace_id: [{"name": missing}],
                })


def test_mapping_ids_and_context_exclusions_are_exact():
    doc = _mapping()
    ids = [x["source_rule_id"] for x in doc["mappings"]]
    assert len(ids) == len(set(ids)) == 8
    assert set(doc["scope"]["nominated_source_rule_ids"]) == set(ids) == set(EXPECTED)
    assert {x["source_rule_id"] for x in doc["exclusions"]} == {
        "CA01-035", "CA01-043", "CA01-045",
    }
