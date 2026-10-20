"""Product integration tests for the 27 complete Career mappings from Review-05."""
import copy
import json
from pathlib import Path

import pytest

from src.product.career_inference_report import build_career_inference_report
from src.product.career_inference_service import run_career_inference
from src.product.career_natal_domain_provider import load_career_source_mappings, load_default_career_natal_provider
from tests.test_product_career_cross_palace import snapshot

ROOT = Path(__file__).resolve().parents[1]
MP = "knowledge/wp07a/CAREER_100_REVIEW_05_v0.1.json"
REGISTRY_PATH = "product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json"
SELECTED = [
    "CA05-446","CA05-449","CA05-452","CA05-453","CA05-454","CA05-455","CA05-461",
    "CA05-463","CA05-468","CA05-476","CA05-478","CA05-479","CA05-498",
    "CA06-503","CA06-504","CA06-505","CA06-513","CA06-514","CA06-515","CA06-518",
    "CA06-524","CA06-525","CA06-528","CA06-530","CA06-534",
]
MAPPING = json.loads((ROOT / MP).read_text())
REGISTRY = json.loads((ROOT / REGISTRY_PATH).read_text())
BY_ID = {m["source_rule_id"]: m for m in MAPPING["mappings"] if m["source_rule_id"] in SELECTED}


def groups(mapping):
    condition = mapping["condition"]
    return condition.get("alternatives") or [condition.get("all_of", [])]


def branch_for(atoms):
    branches = [
        atom["args"]["branch"]
        for atom in atoms
        if atom["atom_type"] == "BRANCH_PRESENT" and atom["args"].get("palace") == "P09"
    ]
    assert len(set(branches)) <= 1
    return branches[0] if branches else "子"


def placements_for(atoms):
    stars = {}
    for atom in atoms:
        if atom["atom_type"] == "PALACE_HAS_STAR":
            palace, star = atom["args"]["palace"], atom["args"]["star"]
            stars.setdefault(palace, [])
            if not any(name == star for name, _ in stars[palace]):
                stars[palace].append((star, None))
    for atom in atoms:
        if atom["atom_type"] == "TRANSFORMATION_PRESENT" and atom["args"].get("star"):
            palace, star, mutagen = atom["args"]["palace"], atom["args"]["star"], atom["args"]["mutagen"]
            stars.setdefault(palace, [])
            for index, (name, _) in enumerate(stars[palace]):
                if name == star:
                    stars[palace][index] = (star, mutagen)
                    break
            else:
                stars[palace].append((star, mutagen))
    return stars


def active_ids(value):
    provider = load_default_career_natal_provider(ROOT)
    return {r.rule_id for r in provider.build_domain_evidence(value, question="Review-05事业规则验收").active_rules}


def test_review05_owns_selection_not_future_global_total():
    meta = next(m for m in REGISTRY["additional_source_mappings"] if m["path"] == MP)
    assert meta["mapping_status"] == "REVIEW_COMPLETE_NON_PRODUCTION"
    assert meta["source_context_schema"] == "REVIEW_COMPLETE_CONTEXT_V0_1"
    assert meta["selected_rule_ids"] == SELECTED
    assert set(BY_ID) == set(SELECTED)
    assert set(SELECTED) <= set(REGISTRY["rules"])
    assert len(load_career_source_mappings(ROOT, REGISTRY)) == len(REGISTRY["rules"])


@pytest.mark.parametrize("rule_id", SELECTED)
def test_every_declared_alternative_runs_through_real_api_and_report(rule_id):
    mapping = BY_ID[rule_id]
    for atoms in groups(mapping):
        value = snapshot(branch_for(atoms), placements_for(atoms))
        before = copy.deepcopy(value)
        run = run_career_inference(ROOT, value, target_id="T-DEMO", question="Review-05 Product接入")
        report = build_career_inference_report(ROOT, run)
        active = {item["rule_id"]: item for item in report["natal"]["active_rules"]}
        assert rule_id in active
        item = active[rule_id]
        assert item["source_context"] == mapping["source_context"]
        assert item["source_summary"] == mapping["source_span_summary"]
        assert item["condition"] == mapping["source_condition_text"]
        assert item["source"]["source_id"] == mapping["source_provenance"]["source_id"]
        assert item["source"]["source_location"] == mapping["source_provenance"]["source_location"]
        assert item["projection"] == {
            key: mapping["expected_projection"]["projection_" + key]
            for key in ("domain", "target", "mode")
        }
        assert run.status == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
        assert report["real_world_event_prediction_supported"] is False
        assert report["temporal"]["matched_reaction_rule_ids"] == []
        assert value == before


@pytest.mark.parametrize("rule_id", SELECTED)
def test_each_alternative_requires_its_declared_stars_transformations_and_branch(rule_id):
    mapping = BY_ID[rule_id]
    for atoms in groups(mapping):
        branch = branch_for(atoms)
        stars = placements_for(atoms)
        assert rule_id in active_ids(snapshot(branch, stars))

        for atom in atoms:
            if atom["atom_type"] == "PALACE_HAS_STAR":
                palace, star = atom["args"]["palace"], atom["args"]["star"]
                missing = copy.deepcopy(stars)
                missing[palace] = [(s, m) for s, m in missing.get(palace, []) if s != star]
                assert rule_id not in active_ids(snapshot(branch, missing))

                other = "P01" if palace != "P01" else "P02"
                misplaced = copy.deepcopy(missing)
                original_mutagen = next((m for s, m in stars.get(palace, []) if s == star), None)
                misplaced.setdefault(other, []).append((star, original_mutagen))
                assert rule_id not in active_ids(snapshot(branch, misplaced))

            if atom["atom_type"] == "TRANSFORMATION_PRESENT" and atom["args"].get("star"):
                palace, star, required = atom["args"]["palace"], atom["args"]["star"], atom["args"]["mutagen"]
                for replacement in [None, *[m for m in "禄权科忌" if m != required]]:
                    wrong = copy.deepcopy(stars)
                    wrong[palace] = [(s, replacement if s == star else m) for s, m in wrong[palace]]
                    assert rule_id not in active_ids(snapshot(branch, wrong))

        branches = {
            a["args"]["branch"]
            for alternative in groups(mapping)
            for a in alternative
            if a["atom_type"] == "BRANCH_PRESENT" and a["args"].get("palace") == "P09"
        }
        if branches:
            wrong_branch = next(b for b in "子丑寅卯辰巳午未申酉戌亥" if b not in branches)
            assert rule_id not in active_ids(snapshot(wrong_branch, stars))


def test_reviewed_inheritance_relation_and_named_transform_boundaries():
    expected_inheritance = {
        "CA05-454": ["CA05-453"],
        "CA05-476": ["CA05-475"],
        "CA06-505": ["CA06-504"],
        "CA06-525": ["CA06-524"],
    }
    for rule_id, inherited in expected_inheritance.items():
        assert BY_ID[rule_id]["source_context"]["inherited_source_rule_ids"] == inherited

    for rule_id in ["CA05-453", "CA05-454", "CA05-498"]:
        rels = [
            atom for atoms in groups(BY_ID[rule_id]) for atom in atoms
            if atom["atom_type"] == "PALACE_RELATION"
        ]
        assert rels
        assert all(r["args"] == {"source":"P09","target":"P03","relation":"OPPOSITE"} for r in rels)

    expected_transforms = {
        "CA05-476": {("廉贞", "禄")},
        "CA06-503": {("廉贞", "禄")},
        "CA06-504": {("破军", "禄")},
        "CA06-505": {("破军", "禄")},
        "CA06-514": {("廉贞", "禄")},
        "CA06-515": {("天府", "科")},
        "CA06-518": {("廉贞", "忌")},
        "CA06-528": {("廉贞", "忌")},
    }
    for rule_id, expected in expected_transforms.items():
        actual = {
            (atom["args"]["star"], atom["args"]["mutagen"])
            for atoms in groups(BY_ID[rule_id])
            for atom in atoms
            if atom["atom_type"] == "TRANSFORMATION_PRESENT"
        }
        assert actual == expected


def test_case_support_event_candidates_remain_outside_product_registry():
    all_rows = {m["source_rule_id"]: m for m in MAPPING["mappings"]}
    case_only = {"CA05-495", "CA06-527"}
    assert all(all_rows[rid]["source_provenance"]["case_support_only"] is True for rid in case_only)
    assert all(all_rows[rid]["expected_projection"]["projection_mode"] == "EVENT_CANDIDATE" for rid in case_only)
    assert case_only.isdisjoint(REGISTRY["rules"])


def test_nonselected_review05_rows_do_not_enter_product():
    all_review05 = {m["source_rule_id"] for m in MAPPING["mappings"]}
    assert (all_review05 - set(SELECTED)).isdisjoint(REGISTRY["rules"])


@pytest.mark.parametrize("mutation,error", [
    ("source_status", "reviewed non-executable mapping"),
    ("context_flag", "invalid review-complete source context"),
    ("context_drift", "drift in source context"),
    ("condition_drift", "condition atoms"),
    ("blocked", "readiness"),
])
def test_review05_handoff_fails_closed(tmp_path, mutation, error):
    registry = copy.deepcopy(REGISTRY)
    for meta in [registry["source_mapping"], *registry["additional_source_mappings"]]:
        p = tmp_path / meta["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes((ROOT / meta["path"]).read_bytes())

    path = tmp_path / MP
    mapping = json.loads(path.read_text())
    source = next(m for m in mapping["mappings"] if m["source_rule_id"] == "CA05-446")
    rule = registry["rules"]["CA05-446"]

    if mutation == "source_status":
        mapping["status"] = "HUNDRED_RULE_REVIEW_COMPLETE_NOT_PRODUCTION"
    if mutation == "context_flag":
        source["source_context"]["additional_semantics_must_not_be_invented"] = False
    if mutation == "context_drift":
        rule["expected_source_context"]["paragraph_scope"] = "错误段落"
    if mutation == "condition_drift":
        first = rule["condition"].get("alternatives", [rule["condition"].get("all_of", [])])[0]
        first.pop()
    if mutation == "blocked":
        source["execution_readiness"] = "BLOCKED_UNKNOWN"

    path.write_text(json.dumps(mapping, ensure_ascii=False))
    with pytest.raises(ValueError, match=error):
        load_career_source_mappings(tmp_path, registry)
