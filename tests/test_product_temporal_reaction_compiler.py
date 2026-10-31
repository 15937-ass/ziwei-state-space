import json
from pathlib import Path

import pytest

from src.product.condition_atoms import fact_from_atom
from src.product.natal_prior import NatalStateProfile
from src.product.temporal_asset_adapter import adapt_target_from_full_snapshot
from src.product.temporal_reaction_compiler import (
    compile_temporal_reaction_registry,
    match_temporal_reactions,
)

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.2.json"
REGISTRY = ROOT / "product/PL3T_TEMPORAL_REACTION_FIXTURE_v0.1.json"


def _bundle():
    snapshot = json.loads(ASSET.read_text(encoding="utf-8"))
    return adapt_target_from_full_snapshot(snapshot, target_id="T-DEMO")


def _natal(with_star=True):
    facts = ()
    if with_star:
        facts = (
            fact_from_atom("PALACE_HAS_STAR", palace="P09", star="紫微"),
        )
    return NatalStateProfile(
        schema_version="0.1",
        profile_id="NATAL-REACTION-TEST",
        engine_version="test",
        knowledge_version="KB-TEST",
        canonical_facts=facts,
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )


def _rules():
    doc = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return compile_temporal_reaction_registry(doc)


def test_asset_bundle_exposes_structured_temporal_condition_facts():
    facts = set(_bundle().condition_facts)
    assert fact_from_atom("TIME_LAYER", layer="YEAR") in facts
    assert fact_from_atom("STAR_PRESENT", layer="YEAR", star="天马") in facts
    assert fact_from_atom(
        "TRANSFORMATION_PRESENT", layer="YEAR", mutagen="科"
    ) in facts


def test_explicit_natal_and_temporal_conditions_match_reaction():
    report = match_temporal_reactions(_natal(), _bundle(), _rules())
    assert report.counts() == {"MATCHED": 1}
    reaction = report.matched[0]
    assert reaction.effect == "ACTIVATE"
    assert reaction.magnitude_status == "UNIDENTIFIED"
    assert reaction.matched_natal_facts
    assert reaction.matched_temporal_facts


def test_star_bound_temporal_transformation_requires_explicit_pl1_binding():
    def run(explicit_mutagen):
        snapshot = json.loads(ASSET.read_text(encoding="utf-8"))
        star = snapshot["temporal"][0]["scopes"]["yearly"]["stars"][0][0]
        star["name"] = "武曲"
        if explicit_mutagen:
            star["mutagen"] = "忌"
        bundle = adapt_target_from_full_snapshot(snapshot, target_id="T-DEMO")

        document = json.loads(REGISTRY.read_text(encoding="utf-8"))
        rule = document["rules"][0]
        rule["reaction_id"] = "TR-STAR-MUTAGEN-TEST"
        rule["rule_id"] = "TR-STAR-MUTAGEN-TEST"
        rule["temporal_condition"] = {
            "all_of": [
                {
                    "atom_type": "TIME_LAYER",
                    "args": {"layer": "YEAR"},
                },
                {
                    "atom_type": "TRANSFORMATION_PRESENT",
                    "args": {
                        "layer": "YEAR",
                        "palace_name": "命宫",
                        "star": "武曲",
                        "mutagen": "忌",
                    },
                },
            ]
        }
        rules = compile_temporal_reaction_registry(document)
        return match_temporal_reactions(_natal(), bundle, rules)

    explicit_report = run(explicit_mutagen=True)
    assert len(explicit_report.matched) == 1
    expected_fact = fact_from_atom(
        "TRANSFORMATION_PRESENT",
        layer="YEAR",
        palace_name="命宫",
        star="武曲",
        mutagen="忌",
    )
    assert expected_fact in explicit_report.matched[0].matched_temporal_facts

    unbound_report = run(explicit_mutagen=False)
    assert unbound_report.matched == ()
    assert unbound_report.issues


def test_missing_natal_antecedent_fails_closed():
    report = match_temporal_reactions(_natal(with_star=False), _bundle(), _rules())
    assert not report.matched
    assert report.issues[0].reason == "NATAL_FACT_ANTECEDENT_MISMATCH"


def test_case_support_only_registry_row_is_rejected():
    doc = json.loads(REGISTRY.read_text(encoding="utf-8"))
    doc["rules"][0]["case_support_only"] = True
    with pytest.raises(ValueError, match="CASE_SUPPORT_ONLY"):
        compile_temporal_reaction_registry(doc)


def test_temporal_atoms_must_bind_to_declared_layer():
    doc = json.loads(REGISTRY.read_text(encoding="utf-8"))
    doc["rules"][0]["temporal_condition"]["all_of"][1]["args"]["layer"] = "MONTH"
    with pytest.raises(ValueError, match="every temporal condition atom"):
        compile_temporal_reaction_registry(doc)


def test_production_registry_is_intentionally_empty_until_kb_wp07b():
    path = ROOT / "product/PL3T_TEMPORAL_REACTION_REGISTRY_v0.1.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert compile_temporal_reaction_registry(doc) == ()
    assert doc["status"] == "EMPTY_UNTIL_KB_WP07B_STRUCTURED_NORMALIZATION"
