import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEX = ROOT / "knowledge/category/CATEGORY_OPEN_LEXICON_v0.1.json"
CAREER = ROOT / "knowledge/wp07c/CAREER_CATEGORY_OPEN_59_v0.1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_exact_18_surfaces_and_59_occurrences():
    lex = load(LEX)
    career = load(CAREER)
    assert len(lex["entries"]) == 18
    assert len({e["surface"] for e in lex["entries"]}) == 18
    assert career["coverage"] == {
        "open_category_occurrences": 59,
        "distinct_source_surfaces": 18,
    }
    assert len(career["records"]) == 59

def test_source_explicit_closed_classes_are_bounded():
    lex = {e["surface"]: e for e in load(LEX)["entries"]}
    assert lex["煞曜"]["members"] == ["擎羊", "陀罗", "火星", "铃星", "地空", "地劫"]
    assert lex["羊陀"]["members"] == ["擎羊", "陀罗"]
    assert lex["吉化"]["members"] == ["化禄", "化权", "化科"]
    assert lex["辅佐诸曜"]["members"] == ["天魁", "天钺", "左辅", "右弼", "文昌", "文曲", "禄存", "天马"]

def test_open_world_categories_remain_open():
    lex = {e["surface"]: e for e in load(LEX)["entries"]}
    for surface in ["吉曜", "凶曜", "桃花", "桃花诸曜"]:
        assert lex[surface]["members"] is None
        assert lex[surface]["membership_status"] == "OPEN_WORLD"
    for surface in ["吉", "凶"]:
        assert lex[surface]["members"] is None
        assert lex[surface]["semantic_kind"] == "OPEN_VALENCE_SHORTHAND"

def test_qualified_auxiliary_does_not_turn_base_eight_into_all_members_trigger():
    lex = {e["surface"]: e for e in load(LEX)["entries"]}
    e = lex["辅佐吉曜"]
    assert e["base_category_ref"] == "CAT_AUXILIARY_EIGHT"
    assert len(e["base_members"]) == 8
    assert e["members"] is None
    assert e["activation_quantifier"] == "UNSPECIFIED"

def test_compounds_preserve_unspecified_source_bundle():
    lex = {e["surface"]: e for e in load(LEX)["entries"]}
    for surface in ["煞忌", "吉化吉曜", "刑耗", "煞刑诸曜", "煞耗", "煞耗诸曜"]:
        assert lex[surface]["semantic_kind"] == "SOURCE_COMPOUND_CATEGORY"
        assert lex[surface]["composition_operator"] == "UNSPECIFIED_SOURCE_BUNDLE"
        assert lex[surface]["members"] is None

def test_occurrence_projection_does_not_unlock_execution():
    data = load(CAREER)
    assert data["summary"]["source_resolution_changes"] == 0
    assert data["summary"]["conditions_compiled"] == 0
    assert data["summary"]["execution_unlocked"] == 0
    for row in data["records"]:
        assert row["relation_binding_unchanged"] is True
        assert row["source_resolution_changed"] is False
        assert row["condition_compiled"] is False
        assert row["execution_unlocked"] is False

def test_no_weights_probabilities_or_product_runtime_change():
    guard = load(LEX)["guardrails"]
    assert guard["product_runtime_modified"] is False
    assert guard["numeric_weights_added"] is False
    assert guard["probabilities_added"] is False
    assert guard["activation_quantifier_inferred"] is False
