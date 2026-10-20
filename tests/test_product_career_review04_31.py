"""Product integration tests for the 31 complete Career mappings from Review-04."""
import copy
import json
from pathlib import Path

import pytest

from src.product.career_inference_report import build_career_inference_report
from src.product.career_inference_service import run_career_inference
from src.product.career_natal_domain_provider import load_career_source_mappings, load_default_career_natal_provider
from tests.test_product_career_cross_palace import snapshot

ROOT = Path(__file__).resolve().parents[1]
MP = "knowledge/wp07a/CAREER_100_REVIEW_04_v0.1.json"
REGISTRY_PATH = "product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json"
SELECTED = [
    "CA04-351","CA04-352","CA04-361","CA04-364","CA04-369","CA04-370","CA04-371",
    "CA04-380","CA04-381","CA04-387","CA04-389","CA04-395","CA04-396","CA04-398",
    "CA04-399","CA04-400","CA05-401","CA05-406","CA05-407","CA05-408","CA05-421",
    "CA05-425","CA05-426","CA05-427","CA05-428","CA05-430","CA05-431","CA05-432",
    "CA05-434","CA05-440","CA05-444",
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
    return {r.rule_id for r in provider.build_domain_evidence(value, question="Review-04事业规则验收").active_rules}


def test_exact_review04_selection_and_current_total():
    meta = next(m for m in REGISTRY["additional_source_mappings"] if m["path"] == MP)
    assert meta["mapping_status"] == "REVIEW_COMPLETE_NON_PRODUCTION"
    assert meta["source_context_schema"] == "REVIEW_COMPLETE_CONTEXT_V0_1"
    assert meta["selected_rule_ids"] == SELECTED
    assert set(BY_ID) == set(SELECTED)
    assert len(REGISTRY["rules"]) == 165
    assert len(load_career_source_mappings(ROOT, REGISTRY)) == 165


@pytest.mark.parametrize("rule_id", SELECTED)
def test_every_declared_alternative_runs_through_real_api_and_report(rule_id):
    mapping = BY_ID[rule_id]
    for atoms in groups(mapping):
        value = snapshot(branch_for(atoms), placements_for(atoms))
        before = copy.deepcopy(value)
        run = run_career_inference(ROOT, value, target_id="T-DEMO", question="Review-04 Product接入")
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
            palace, star = atom["args"]["palace"], atom["args"]["star"]
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
                # For OR conditions another alternative may legitimately remain true;
                # remove every other unique trigger before asserting fail-closed.
                for alternative in groups(mapping)[1:]:
                    for other in alternative:
                        if other["atom_type"] == "PALACE_HAS_STAR":
                            op, os = other["args"]["palace"], other["args"]["star"]
                            wrong[op] = [(s, mu) for s, mu in wrong.get(op, []) if s != os or s == star]
                if len(groups(mapping)) == 1:
                    assert rule_id not in active_ids(snapshot(branch, wrong))

    allowed = allowed_branches(mapping)
    if allowed:
        wrong_branch = next(b for b in "子丑寅卯辰巳午未申酉戌亥" if b not in allowed)
        assert rule_id not in active_ids(snapshot(wrong_branch, stars))


def test_reviewed_inheritance_and_named_transformation_boundaries():
    assert BY_ID["CA04-396"]["source_context"]["inherited_source_rule_ids"] == ["CA04-395"]
    assert BY_ID["CA04-399"]["source_context"]["inherited_source_rule_ids"] == ["CA04-398"]
    assert BY_ID["CA05-427"]["source_context"]["inherited_source_rule_ids"] == ["CA05-426"]
    assert BY_ID["CA05-431"]["source_context"]["inherited_source_rule_ids"] == ["CA05-430"]

    expected = {
        "CA04-361": {("天府", "科")},
        "CA04-364": {("贪狼", "忌")},
        "CA04-369": {("武曲", "禄"), ("贪狼", "权")},
        "CA04-395": {("破军", "禄")},
        "CA04-396": {("破军", "禄")},
        "CA05-426": {("太阴", "忌")},
        "CA05-427": {("太阴", "忌")},
        "CA05-428": {("天同", "忌")},
        "CA05-440": {("巨门", "禄")},
    }
    for rule_id, pairs in expected.items():
        actual = {
            (atom["args"]["star"], atom["args"]["mutagen"])
            for atoms in groups(BY_ID[rule_id])
            for atom in atoms
            if atom["atom_type"] == "TRANSFORMATION_PRESENT"
        }
        assert actual == pairs


def test_wuqu_general_and_specific_rules_are_layered_not_mutually_exclusive():
    plain = active_ids(snapshot("子", {"P09":[("武曲",None)]}))
    assert {"CA04-336","CA04-338","CA04-341"} <= plain
    assert "CA04-352" not in plain
    assert "CA04-349" not in plain

    ji = active_ids(snapshot("子", {"P09":[("武曲","忌")]}))
    assert {"CA04-336","CA04-338","CA04-341","CA04-349","CA04-352"} <= ji

    tuoluo = active_ids(snapshot("子", {"P09":[("武曲",None),("陀罗",None)]}))
    assert {"CA04-351","CA04-352"} <= tuoluo


def test_nonselected_review04_rows_do_not_enter_product():
    all_review04 = {m["source_rule_id"] for m in MAPPING["mappings"]}
    assert (all_review04 - set(SELECTED)).isdisjoint(REGISTRY["rules"])


@pytest.mark.parametrize("mutation,error", [
    ("source_status", "reviewed non-executable mapping"),
    ("context_flag", "invalid review-complete source context"),
    ("context_drift", "drift in source context"),
    ("condition_drift", "condition atoms"),
    ("blocked", "readiness"),
])
def test_review04_handoff_fails_closed(tmp_path, mutation, error):
    registry = copy.deepcopy(REGISTRY)
    for meta in [registry["source_mapping"], *registry["additional_source_mappings"]]:
        p = tmp_path / meta["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes((ROOT / meta["path"]).read_bytes())

    path = tmp_path / MP
    mapping = json.loads(path.read_text())
    source = next(m for m in mapping["mappings"] if m["source_rule_id"] == "CA04-351")
    rule = registry["rules"]["CA04-351"]

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
