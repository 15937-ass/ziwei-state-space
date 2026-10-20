"""Second hundred-rule review: source fidelity and conservative condition compilation."""

import copy
import csv
import json
from collections import Counter
from pathlib import Path

import pytest

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "knowledge/wp07a/CAREER_100_REVIEW_02_v0.1.json"
DOC = json.loads(PATH.read_text())
RECORDS = {mapping["source_rule_id"]: mapping for mapping in DOC["mappings"]}
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
PALACES = ["命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫", "迁移宫", "交友宫", "事业宫", "田宅宫", "福德宫", "父母宫"]
COMPLETE = {
    "CA02-130", "CA02-131", "CA02-132", "CA02-137", "CA02-138",
    "CA02-142", "CA02-143", "CA02-144", "CA02-146", "CA02-151",
    "CA02-153", "CA02-159", "CA02-161", "CA02-162", "CA02-163",
    "CA02-165", "CA02-172", "CA02-173", "CA02-174", "CA02-183",
    "CA02-190", "CA02-191", "CA02-192", "CA02-193", "CA02-195",
    "CA02-196", "CA02-200", "CA03-201", "CA03-202", "CA03-203",
    "CA03-207", "CA03-208", "CA03-209", "CA03-210", "CA03-220",
    "CA03-221", "CA03-222", "CA03-223", "CA03-226", "CA03-227",
    "CA03-232",
}
EXPECTED_BRANCHES = {
    **{rid: "辰戌" for rid in ("CA02-130", "CA02-131", "CA02-132", "CA02-137", "CA02-138")},
    **{rid: "巳亥" for rid in ("CA02-142", "CA02-143", "CA02-144", "CA02-146", "CA02-151")},
    "CA02-183": "子午", "CA02-190": "午", "CA02-191": "午", "CA02-192": "子", "CA02-193": "子", "CA02-195": "子午",
    "CA02-196": "丑未", "CA02-200": "丑未", "CA03-201": "丑未", "CA03-202": "丑未", "CA03-203": "丑未",
    **{rid: "寅申" for rid in ("CA03-207", "CA03-208", "CA03-209", "CA03-210")},
    **{rid: "卯酉" for rid in ("CA03-220", "CA03-221", "CA03-222", "CA03-223", "CA03-226", "CA03-227")},
    "CA03-232": "辰戌",
}


def source_rows():
    result = []
    for path in sorted((ROOT / "validation/wp05").glob("CA*_career_projection_review_*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            result.extend(csv.DictReader(handle))
    return result


def alternatives(condition):
    common = condition.get("all_of", [])
    return [common + branch for branch in condition["alternatives"]] if condition.get("alternatives") else [common]


def snapshot_for(atoms, forced_branch=None):
    branch = forced_branch or next(
        (atom["args"]["branch"] for atom in atoms if atom["atom_type"] == "BRANCH_PRESENT" and atom["args"]["palace"] == "P09"),
        "申",
    )
    stars = {}
    for atom in atoms:
        if atom["atom_type"] in ("PALACE_HAS_STAR", "TRANSFORMATION_PRESENT"):
            args = atom["args"]
            stars.setdefault(args["palace"], {}).setdefault(args["star"], {"name": args["star"]})
            if atom["atom_type"] == "TRANSFORMATION_PRESENT":
                stars[args["palace"]][args["star"]]["mutagen"] = args["mutagen"]
    offset = (BRANCHES.index(branch) - 8) % 12
    return {
        "schema_version": "0.2",
        "engine": {"name": "batch-review-test", "version": "1", "adapter_version": "0.2"},
        "input": {},
        "natal": {
            "palaces": {
                BRANCHES[(index + offset) % 12]: {
                    "name": name,
                    "stem": "甲",
                    "branch": BRANCHES[(index + offset) % 12],
                    "is_body_palace": False,
                    "major_stars": list(stars.get(f"P{index + 1:02}", {}).values()),
                    "minor_stars": [],
                    "adjective_stars": [],
                }
                for index, name in enumerate(PALACES)
            }
        },
    }


def runtime_facts(snapshot):
    ontology = load_palace_ontology(ROOT / "knowledge/wp05/palace_ontology_v0.1.csv")
    return resolve_palace_structure(snapshot, ontology).runtime_facts()


def test_exact_second_hundred_selection_and_pinned_historical_counts():
    before = set()
    for path in DOC["baseline_mapping_paths"]:
        before.update(mapping["source_rule_id"] for mapping in json.loads((ROOT / path).read_text())["mappings"])
    expected = [row["projection_rule_id"] for row in source_rows() if row["projection_rule_id"] not in before][:100]
    assert len(before) == 152
    assert len(RECORDS) == len(DOC["mappings"]) == 100
    assert list(RECORDS) == DOC["scope"]["nominated_source_rule_ids"] == expected
    assert list(RECORDS)[0] == "CA02-130" and list(RECORDS)[-1] == "CA03-235"
    assert not before.intersection(RECORDS)
    assert len(before | set(RECORDS)) == 252
    assert DOC["scope"]["reasoning_sub_batches"] == [50, 50]
    assert Counter(mapping["review_sub_batch"] for mapping in RECORDS.values()) == {1: 50, 2: 50}
    counts = DOC["progress_counts"]
    assert counts["source_rules_rechecked"] == 100
    assert counts["first_time_complete_condition_mappings"] == 41
    assert counts["methodology_or_context_only"] == 1
    assert counts["blocked_outcome_mappings"] == 58
    assert counts["new_production_executable_rules"] == 0
    assert counts["canonical_source_reviewed_before"] == counts["canonical_source_reviewed_after"] == 888
    assert counts["unique_structured_rule_records_before"] == 152
    assert counts["unique_structured_rule_records_after"] == 252


@pytest.mark.parametrize("rule_id", list(RECORDS))
def test_each_review_preserves_exact_canonical_record_and_individual_reason(rule_id):
    source = next(row for row in source_rows() if row["projection_rule_id"] == rule_id)
    mapping = RECORDS[rule_id]
    assert mapping["source_record"] == source
    assert mapping["source_condition_text"] == source["condition"]
    provenance = mapping["source_provenance"]
    for key in ("source_id", "source_location", "review_status", "time_layer", "history_feedback"):
        assert provenance[key] == source[key]
    assert provenance["source_span_verified"] == (source["source_span_verified"] == "true")
    assert provenance["case_support_only"] == (source["case_support_only"] == "true")
    assert mapping["expected_projection"] == {key: source[key] for key in ("projection_domain", "projection_target", "projection_mode")}
    spans = {span["span_id"]: span for span in DOC["source_spans"]}
    assert mapping["source_span_ids"] and set(mapping["source_span_ids"]) <= set(spans)
    assert all(spans[span_id]["visual_reviewed"] and spans[span_id]["extracted_text_not_silently_corrected"] for span_id in mapping["source_span_ids"])
    assert len(mapping["review_reason_zh"]) > 18
    assert mapping["executable_registry_entry"] is False
    if mapping["condition"] is None:
        assert mapping["blocker_code"]
        assert mapping["execution_readiness"].startswith("BLOCKED_")
        assert mapping["source_context"]["context_is_complete_antecedent"] is False
    else:
        assert mapping["review_disposition"] == "COMPLETE_CONDITION_MAPPING"


@pytest.mark.parametrize("rule_id", sorted(COMPLETE))
def test_each_complete_rule_matches_runtime_and_requires_every_fact(rule_id):
    mapping = RECORDS[rule_id]
    compiled = compile_condition_spec(mapping["condition"])
    for atoms in alternatives(mapping["condition"]):
        assert atoms
        assert all(atom["atom_type"] in ALLOWED_ATOM_TYPES for atom in atoms)
        snapshot = snapshot_for(atoms)
        facts = runtime_facts(snapshot)
        assert compiled.matches(facts)
        for atom in atoms:
            assert not compiled.matches(frozenset(facts - {fact_from_atom(atom["atom_type"], **atom["args"])}))
        for palace in snapshot["natal"]["palaces"].values():
            for star in palace["major_stars"]:
                if not star.get("mutagen"):
                    continue
                for wrong in ("禄", "权", "科", "忌"):
                    if wrong == star["mutagen"]:
                        continue
                    changed = copy.deepcopy(snapshot)
                    next(item for item in changed["natal"]["palaces"][palace["branch"]]["major_stars"] if item["name"] == star["name"])["mutagen"] = wrong
                    matches = compiled.matches(runtime_facts(changed))
                    if rule_id == "CA02-174":
                        assert matches == (wrong in {"禄", "权", "忌"})
                    else:
                        assert not matches


@pytest.mark.parametrize("rule_id", sorted(COMPLETE))
def test_branch_scope_is_exact_or_explicitly_general(rule_id):
    compiled = compile_condition_spec(RECORDS[rule_id]["condition"])
    atoms = alternatives(RECORDS[rule_id]["condition"])[0]
    expected = EXPECTED_BRANCHES.get(rule_id, BRANCHES)
    for branch in BRANCHES:
        assert compiled.matches(runtime_facts(snapshot_for(atoms, branch))) == (branch in expected)


def test_cross_palace_and_transformation_alternatives_are_exact():
    for rule_id in ("CA02-183", "CA02-200", "CA03-201", "CA03-202", "CA03-203"):
        for atoms in alternatives(RECORDS[rule_id]["condition"]):
            relation = [atom for atom in atoms if atom["atom_type"] == "PALACE_RELATION"]
            assert relation == [{"atom_type": "PALACE_RELATION", "args": {"source": "P09", "target": "P03", "relation": "OPPOSITE"}}]
    transforms = [
        next(atom for atom in atoms if atom["atom_type"] == "TRANSFORMATION_PRESENT")["args"]["mutagen"]
        for atoms in alternatives(RECORDS["CA02-174"]["condition"])
    ]
    assert transforms == ["禄", "权", "忌"]
    assert RECORDS["CA02-159"]["condition"] == {
        "all_of": [
            {"atom_type": "PALACE_HAS_STAR", "args": {"palace": "P09", "star": "天机"}},
            {"atom_type": "TRANSFORMATION_PRESENT", "args": {"palace": "P09", "star": "天机", "mutagen": "权"}},
            {"atom_type": "PALACE_HAS_STAR", "args": {"palace": "P09", "star": "左辅"}},
            {"atom_type": "PALACE_HAS_STAR", "args": {"palace": "P09", "star": "右弼"}},
        ]
    }


def test_inheritance_does_not_cross_paragraph_or_drop_blockers():
    assert RECORDS["CA02-130"]["condition"] == RECORDS["CA02-131"]["condition"] == RECORDS["CA02-132"]["condition"]
    assert RECORDS["CA02-137"]["condition"] == RECORDS["CA02-138"]["condition"]
    assert RECORDS["CA02-142"]["condition"] == RECORDS["CA02-143"]["condition"] == RECORDS["CA02-146"]["condition"]
    assert RECORDS["CA02-190"]["condition"] == RECORDS["CA02-191"]["condition"]
    assert RECORDS["CA02-192"]["condition"] == RECORDS["CA02-193"]["condition"]
    assert RECORDS["CA02-200"]["condition"] == RECORDS["CA03-201"]["condition"] == RECORDS["CA03-202"]["condition"] == RECORDS["CA03-203"]["condition"]
    assert RECORDS["CA03-207"]["condition"] == RECORDS["CA03-208"]["condition"] == RECORDS["CA03-209"]["condition"]
    assert RECORDS["CA03-222"]["condition"] == RECORDS["CA03-223"]["condition"]
    assert RECORDS["CA02-189"]["review_disposition"] == "METHODOLOGY_OR_CONTEXT_ONLY"
    assert {rule_id for rule_id, mapping in RECORDS.items() if mapping["condition"] is not None} == COMPLETE


def test_groups_relations_actions_and_timing_never_become_empty_match_all_conditions():
    examples = {
        "CA02-133": "GROUP", "CA02-135": "RELATION", "CA02-139": "COMPOSITE", "CA02-149": "COMPOSITE",
        "CA02-166": "GROUP", "CA02-176": "COMPOSITE", "CA02-179": "TEMPORAL", "CA02-185": "COMPOSITE",
        "CA02-198": "GROUP", "CA03-213": "ABSENCE", "CA03-216": "TEMPORAL", "CA03-224": "CONTEXT_STATE",
        "CA03-229": "RELATION", "CA03-235": "GROUP",
    }
    for rule_id, blocker in examples.items():
        mapping = RECORDS[rule_id]
        assert mapping["condition"] is None
        assert mapping["blocker_code"] == blocker
        assert mapping["review_disposition"] == "BLOCKED_OUTCOME_MAPPING"
    assert DOC["status"] == "HUNDRED_RULE_REVIEW_COMPLETE_NOT_PRODUCTION"
    assert DOC["progress_counts"]["new_production_executable_rules"] == 0
    assert DOC["guardrails"]["production_registry_modified"] is False
    assert all(mapping["executable_registry_entry"] is False for mapping in RECORDS.values())
    assert DOC["guardrails"]["null_condition_must_not_be_coerced_to_empty"] is True
    assert DOC["scope"]["pi_report_requires_substantive_content_synopsis"] is True
    assert len(DOC["content_synopsis_zh"]) == 8
