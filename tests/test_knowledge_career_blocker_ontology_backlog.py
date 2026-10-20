import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = json.loads((ROOT / "knowledge/wp07c/CAREER_BLOCKER_ONTOLOGY_BACKLOG_v0.1.json").read_text())
CLOSURE = json.loads((ROOT / "knowledge/wp07a/CAREER_888_CLOSURE_AUDIT_v0.1.json").read_text())


def test_blocker_census_matches_closure():
    records = BACKLOG["blocked_records"]
    assert len(records) == 513
    assert BACKLOG["blocked_rule_count"] == 513
    assert Counter(item["blocker_code"] for item in records) == Counter(CLOSURE["blocker_totals"])


def test_every_blocker_is_traceable():
    ids = [item["source_rule_id"] for item in BACKLOG["blocked_records"]]
    assert len(ids) == len(set(ids))
    assert all(item["source_condition_text"] for item in BACKLOG["blocked_records"])
    assert all(item["review_artifact"] for item in BACKLOG["blocked_records"])


def test_workstream_priorities_and_gates_are_explicit():
    streams = BACKLOG["workstreams"]
    assert [item["priority"] for item in streams] == list(range(1, 9))
    assert streams[0]["workstream_id"] == "WS-GROUP-QUANTIFIER"
    assert streams[0]["affected_blockers"] == 251
    assert streams[1]["workstream_id"] == "WS-SPATIAL-RELATION"
    assert streams[1]["affected_blockers"] == 134
    assert streams[2]["workstream_id"] == "WS-COMPOSITE-PATTERN"
    assert streams[2]["affected_blockers"] == 92
    for item in streams[:7]:
        assert item["semantic_gate_required_for_execution"] is True
        assert item["proposed_human_gate"]
        assert item["gate_question_zh"]


def test_no_semantics_or_product_changes_are_claimed():
    assert BACKLOG["status"] == "PLANNING_COMPLETE_NO_NEW_SEMANTICS"
    invariants = BACKLOG["invariants"]
    assert invariants["no_new_condition_atoms"] is True
    assert invariants["no_new_semantic_defaults"] is True
    assert invariants["no_blocker_auto_unlocked"] is True
    assert invariants["no_product_runtime_change"] is True
    assert invariants["natal_not_rewritten_by_feedback"] is True
    assert invariants["traditional_possibility_not_probability"] is True
    assert invariants["silence_not_negative"] is True


def test_lexical_inventory_is_declared_nonsemantic():
    assert "Literal substring census" in BACKLOG["lexical_inventory_method"]
    group_terms = {
        item["term"]: item["blocked_condition_occurrences"]
        for item in BACKLOG["lexical_inventory"]["group_terms"]
    }
    relation_terms = {
        item["term"]: item["blocked_condition_occurrences"]
        for item in BACKLOG["lexical_inventory"]["relation_terms"]
    }
    assert group_terms["空劫"] == 37
    assert group_terms["吉曜"] == 32
    assert relation_terms["会"] == 83
    assert relation_terms["同会"] == 16


def test_next_work_unit_is_only_recommended_not_opened():
    nxt = BACKLOG["recommended_next_work_unit"]
    assert nxt["workstream_id"] == "WS-GROUP-QUANTIFIER"
    assert nxt["must_not_open_automatically_in_this_work_unit"] is True
