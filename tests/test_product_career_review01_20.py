"""Product integration tests for the 20 complete mappings from Knowledge review batch #366."""
import copy
import json
from pathlib import Path

import pytest

from src.product.career_inference_report import build_career_inference_report
from src.product.career_inference_service import run_career_inference
from src.product.career_natal_domain_provider import load_career_source_mappings, load_default_career_natal_provider
from tests.test_product_career_cross_palace import snapshot

ROOT = Path(__file__).resolve().parents[1]
MP = "knowledge/wp07a/CAREER_100_REVIEW_01_v0.1.json"
REGISTRY_PATH = "product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json"
SELECTED = [
    "CA01-067","CA01-068","CA01-072","CA01-076","CA01-077","CA01-084",
    "CA02-102","CA02-103","CA02-104","CA02-105","CA02-109","CA02-110",
    "CA02-111","CA02-112","CA02-114","CA02-119","CA02-120","CA02-122",
    "CA02-124","CA02-128",
]
MAPPING = json.loads((ROOT / MP).read_text())
REGISTRY = json.loads((ROOT / REGISTRY_PATH).read_text())
BY_ID = {m["source_rule_id"]: m for m in MAPPING["mappings"] if m["source_rule_id"] in SELECTED}


def branches(mapping):
    condition = mapping["condition"]
    groups = condition.get("alternatives") or [condition.get("all_of", [])]
    return {
        atom["args"]["branch"]
        for group in groups
        for atom in group
        if atom["atom_type"] == "BRANCH_PRESENT" and atom["args"].get("palace") == "P09"
    }


def groups(mapping):
    condition = mapping["condition"]
    return condition.get("alternatives") or [condition.get("all_of", [])]


def placements_for(atoms):
    stars = {}
    for atom in atoms:
        if atom["atom_type"] == "PALACE_HAS_STAR":
            palace = atom["args"]["palace"]
            star = atom["args"]["star"]
            stars.setdefault(palace, [])
            if not any(s == star for s, _ in stars[palace]):
                stars[palace].append((star, None))
    for atom in atoms:
        if atom["atom_type"] == "TRANSFORMATION_PRESENT" and atom["args"].get("star"):
            palace = atom["args"]["palace"]
            star = atom["args"]["star"]
            mutagen = atom["args"]["mutagen"]
            stars.setdefault(palace, [])
            found = False
            for index, (name, _) in enumerate(stars[palace]):
                if name == star:
                    stars[palace][index] = (name, mutagen)
                    found = True
                    break
            if not found:
                stars[palace].append((star, mutagen))
    return stars


def branch_for(atoms):
    matches = [
        atom["args"]["branch"]
        for atom in atoms
        if atom["atom_type"] == "BRANCH_PRESENT" and atom["args"].get("palace") == "P09"
    ]
    assert len(set(matches)) <= 1
    return matches[0] if matches else "子"


def active_ids(value):
    provider = load_default_career_natal_provider(ROOT)
    return {r.rule_id for r in provider.build_domain_evidence(value, question="20条事业规则验收").active_rules}


def test_exact_batch_selection_and_total_count():
    meta = next(m for m in REGISTRY["additional_source_mappings"] if m["path"] == MP)
    assert meta["mapping_status"] == "HUNDRED_RULE_REVIEW_COMPLETE_NOT_PRODUCTION"
    assert meta["source_context_schema"] == "REVIEW_BATCH_PARAGRAPH_SCOPE_V0_1"
    assert meta["selected_rule_ids"] == SELECTED
    assert set(BY_ID) == set(SELECTED)
    assert len(REGISTRY["rules"]) == 63
    assert len(load_career_source_mappings(ROOT, REGISTRY)) == 63
    assert "CA02-121" not in REGISTRY["rules"]  # adjacent temporal rule stays out


@pytest.mark.parametrize("rule_id", SELECTED)
def test_every_declared_alternative_runs_through_api_and_report(rule_id):
    mapping = BY_ID[rule_id]
    for atoms in groups(mapping):
        value = snapshot(branch_for(atoms), placements_for(atoms))
        before = copy.deepcopy(value)
        run = run_career_inference(ROOT, value, target_id="T-DEMO", question="Knowledge #366 Product接入")
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
def test_required_stars_palaces_mutagens_and_branch_gates_fail_closed(rule_id):
    mapping = BY_ID[rule_id]
    atoms = groups(mapping)[0]
    branch = branch_for(atoms)
    stars = placements_for(atoms)
    assert rule_id in active_ids(snapshot(branch, stars))

    for atom in atoms:
        if atom["atom_type"] == "PALACE_HAS_STAR":
            palace, star = atom["args"]["palace"], atom["args"]["star"]
            missing = copy.deepcopy(stars)
            missing[palace] = [(s, m) for s, m in missing.get(palace, []) if s != star]
            assert rule_id not in active_ids(snapshot(branch, missing))

            wrong_palace = "P01" if palace != "P01" else "P02"
            misplaced = copy.deepcopy(missing)
            original_mutagen = next((m for s, m in stars.get(palace, []) if s == star), None)
            misplaced.setdefault(wrong_palace, []).append((star, original_mutagen))
            assert rule_id not in active_ids(snapshot(branch, misplaced))

        if atom["atom_type"] == "TRANSFORMATION_PRESENT" and atom["args"].get("star"):
            palace = atom["args"]["palace"]
            star = atom["args"]["star"]
            required = atom["args"]["mutagen"]
            for replacement in [None, *[m for m in "禄权科忌" if m != required]]:
                wrong = copy.deepcopy(stars)
                wrong[palace] = [(s, replacement if s == star else m) for s, m in wrong[palace]]
                assert rule_id not in active_ids(snapshot(branch, wrong))

    allowed = branches(mapping)
    if allowed:
        wrong_branch = next(b for b in "子丑寅卯辰巳午未申酉戌亥" if b not in allowed)
        assert rule_id not in active_ids(snapshot(wrong_branch, stars))


def test_inheritance_and_adjacent_temporal_boundaries():
    assert BY_ID["CA01-067"]["source_context"]["inherited_source_rule_ids"] == ["CA01-066"]
    assert BY_ID["CA01-072"]["source_context"]["inherited_source_rule_ids"] == ["CA01-070", "CA01-071"]
    assert BY_ID["CA01-077"]["source_context"]["inherited_source_rule_ids"] == ["CA01-076"]
    assert BY_ID["CA02-105"]["source_context"]["inherited_source_rule_ids"] == ["CA02-104"]
    assert BY_ID["CA02-120"]["source_context"]["inherited_source_rule_ids"] == ["CA02-119"]
    assert "CA02-121" not in REGISTRY["rules"]
    assert BY_ID["CA02-119"]["source_span_summary"].endswith("不并入本条。")
    assert BY_ID["CA02-120"]["source_span_summary"].endswith("不并入本条。")


@pytest.mark.parametrize("mutation,error", [
    ("source_status", "reviewed mapping status"),
    ("context_flag", "invalid review-batch paragraph context scope"),
    ("context_drift", "drift in source context"),
    ("condition_drift", "condition atoms"),
    ("blocked", "readiness"),
])
def test_review_batch_handoff_fails_closed(tmp_path, mutation, error):
    registry = copy.deepcopy(REGISTRY)
    for meta in [registry["source_mapping"], *registry["additional_source_mappings"]]:
        p = tmp_path / meta["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes((ROOT / meta["path"]).read_bytes())

    path = tmp_path / MP
    mapping = json.loads(path.read_text())
    source = next(m for m in mapping["mappings"] if m["source_rule_id"] == "CA01-067")
    rule = registry["rules"]["CA01-067"]

    if mutation == "source_status":
        mapping["status"] = "SOURCE_GROUNDED_MAPPING_COMPLETE_NOT_EXECUTABLE"
    if mutation == "context_flag":
        source["source_context"]["additional_semantics_must_not_be_invented"] = False
    if mutation == "context_drift":
        rule["expected_source_context"]["paragraph_scope"] = "错误段落"
    if mutation == "condition_drift":
        rule["condition"]["alternatives"][0].pop()
    if mutation == "blocked":
        source["execution_readiness"] = "BLOCKED_UNKNOWN"

    path.write_text(json.dumps(mapping, ensure_ascii=False))
    with pytest.raises(ValueError, match=error):
        load_career_source_mappings(tmp_path, registry)
