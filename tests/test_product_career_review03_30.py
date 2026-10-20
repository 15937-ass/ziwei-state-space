"""Product integration tests for the 30 complete mappings from Knowledge Review-03 (#379)."""
import copy
import json
from pathlib import Path

import pytest

from src.product.career_inference_report import build_career_inference_report
from src.product.career_inference_service import run_career_inference
from src.product.career_natal_domain_provider import load_career_source_mappings, load_default_career_natal_provider
from tests.test_product_career_cross_palace import snapshot

ROOT = Path(__file__).resolve().parents[1]
MP = "knowledge/wp07a/CAREER_100_REVIEW_03_v0.1.json"
REGISTRY_PATH = "product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json"
SELECTED = [
    "CA03-241","CA03-249","CA03-250","CA03-253","CA03-266","CA03-272","CA03-284","CA03-291",
    "CA03-292","CA03-293","CA03-294","CA03-295","CA03-296","CA03-297","CA03-299","CA03-300",
    "CA04-306","CA04-307","CA04-308","CA04-310","CA04-315","CA04-318","CA04-319","CA04-322",
    "CA04-329","CA04-330","CA04-334","CA04-336","CA04-338","CA04-341",
]
MAPPING = json.loads((ROOT / MP).read_text())
REGISTRY = json.loads((ROOT / REGISTRY_PATH).read_text())
BY_ID = {m["source_rule_id"]: m for m in MAPPING["mappings"] if m["source_rule_id"] in SELECTED}


def groups(mapping):
    condition = mapping["condition"]
    return condition.get("alternatives") or [condition.get("all_of", [])]


def branch_for(atoms):
    values = [
        atom["args"]["branch"]
        for atom in atoms
        if atom["atom_type"] == "BRANCH_PRESENT" and atom["args"].get("palace") == "P09"
    ]
    assert len(set(values)) <= 1
    return values[0] if values else "子"


def allowed_branches(mapping):
    return {
        atom["args"]["branch"]
        for atoms in groups(mapping)
        for atom in atoms
        if atom["atom_type"] == "BRANCH_PRESENT" and atom["args"].get("palace") == "P09"
    }


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
    return {r.rule_id for r in provider.build_domain_evidence(value, question="Review-03事业规则验收").active_rules}


def test_exact_review03_selection_and_current_total():
    meta = next(m for m in REGISTRY["additional_source_mappings"] if m["path"] == MP)
    assert meta["mapping_status"] == "REVIEW_COMPLETE_NON_PRODUCTION"
    assert meta["source_context_schema"] == "REVIEW_BATCH_PARAGRAPH_SCOPE_V0_1"
    assert meta["selected_rule_ids"] == SELECTED
    assert set(BY_ID) == set(SELECTED)
    assert len(REGISTRY["rules"]) == 134
    assert len(load_career_source_mappings(ROOT, REGISTRY)) == 134


@pytest.mark.parametrize("rule_id", SELECTED)
def test_every_declared_alternative_runs_through_real_api_and_report(rule_id):
    mapping = BY_ID[rule_id]
    for atoms in groups(mapping):
        value = snapshot(branch_for(atoms), placements_for(atoms))
        before = copy.deepcopy(value)
        run = run_career_inference(ROOT, value, target_id="T-DEMO", question="Knowledge Review-03 Product接入")
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
def test_stars_palaces_mutagens_and_branch_gates_fail_closed(rule_id):
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

            other = "P01" if palace != "P01" else "P02"
            misplaced = copy.deepcopy(missing)
            original_mutagen = next((m for s, m in stars.get(palace, []) if s == star), None)
            misplaced.setdefault(other, []).append((star, original_mutagen))
            assert rule_id not in active_ids(snapshot(branch, misplaced))

        if atom["atom_type"] == "TRANSFORMATION_PRESENT" and atom["args"].get("star"):
            palace = atom["args"]["palace"]
            star = atom["args"]["star"]
            allowed_mutagens = {
                other["args"]["mutagen"]
                for alternative in groups(mapping)
                for other in alternative
                if other["atom_type"] == "TRANSFORMATION_PRESENT"
                and other["args"].get("palace") == palace
                and other["args"].get("star") == star
            }
            for replacement in [None, *[m for m in "禄权科忌" if m not in allowed_mutagens]]:
                wrong = copy.deepcopy(stars)
                wrong[palace] = [(s, replacement if s == star else m) for s, m in wrong[palace]]
                assert rule_id not in active_ids(snapshot(branch, wrong))

    allowed = allowed_branches(mapping)
    if allowed:
        wrong_branch = next(b for b in "子丑寅卯辰巳午未申酉戌亥" if b not in allowed)
        assert rule_id not in active_ids(snapshot(wrong_branch, stars))


def test_reviewed_inheritance_and_transformation_boundaries():
    expected = {
        "CA03-250":["CA03-249"],
        "CA03-284":["CA03-283"],
        "CA03-293":["CA03-292"],
        "CA04-308":["CA04-307"],
        "CA04-330":["CA04-329"],
    }
    for rule_id, inherited in expected.items():
        assert BY_ID[rule_id]["source_context"]["inherited_source_rule_ids"] == inherited

    # 太阳巨门的资源分支只允许太阳化禄或化权。
    solar_mutagens = {
        atom["args"]["mutagen"]
        for atoms in groups(BY_ID["CA04-329"])
        for atom in atoms
        if atom["atom_type"] == "TRANSFORMATION_PRESENT" and atom["args"]["star"] == "太阳"
    }
    assert solar_mutagens == {"禄", "权"}

    # 太阴化忌必须仍绑定太阴，不能偷换成太阳化忌。
    transforms = {
        (atom["args"]["star"], atom["args"]["mutagen"])
        for atoms in groups(BY_ID["CA04-315"])
        for atom in atoms
        if atom["atom_type"] == "TRANSFORMATION_PRESENT"
    }
    assert transforms == {("太阴", "忌")}

    # 对宫类星系继续显式保存P09->P03 OPPOSITE关系。
    relation_rules = {
        rid for rid, mapping in BY_ID.items()
        if any(atom["atom_type"] == "PALACE_RELATION" for atoms in groups(mapping) for atom in atoms)
    }
    assert {"CA03-292","CA04-306","CA04-319","CA04-322","CA04-329","CA04-334"} <= relation_rules
    for rid in relation_rules:
        rels = [atom for atoms in groups(BY_ID[rid]) for atom in atoms if atom["atom_type"] == "PALACE_RELATION"]
        assert all(r["args"] == {"source":"P09","target":"P03","relation":"OPPOSITE"} for r in rels)


def test_blocked_and_context_only_review03_rows_do_not_enter_product():
    blocked = {
        "CA03-236","CA03-237","CA03-238","CA03-239","CA03-240","CA03-242","CA03-243",
        "CA03-244","CA03-251","CA03-259","CA03-260","CA03-267","CA03-268",
    }
    assert not blocked & set(REGISTRY["rules"])


@pytest.mark.parametrize("mutation,error", [
    ("source_status", "reviewed non-executable mapping"),
    ("context_flag", "invalid review-batch paragraph context scope"),
    ("context_drift", "drift in source context"),
    ("condition_drift", "condition atoms"),
    ("blocked", "readiness"),
])
def test_review03_handoff_fails_closed(tmp_path, mutation, error):
    registry = copy.deepcopy(REGISTRY)
    for meta in [registry["source_mapping"], *registry["additional_source_mappings"]]:
        p = tmp_path / meta["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes((ROOT / meta["path"]).read_bytes())

    path = tmp_path / MP
    mapping = json.loads(path.read_text())
    source = next(m for m in mapping["mappings"] if m["source_rule_id"] == "CA03-241")
    rule = registry["rules"]["CA03-241"]

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
