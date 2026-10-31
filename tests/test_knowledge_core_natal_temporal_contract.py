import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "knowledge/core/temporal/NATAL_STRUCTURE_PRODUCT_CONSUMPTION_AUDIT_v0.1.json"
CORE_STATE = ROOT / "knowledge/states/CORE_STATE.yaml"


def audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_audit_pins_one_accepted_main_snapshot_and_input_provenance():
    d = audit()
    assert d["snapshot"]["main_commit"] == "019331d9524b48d946a19b91605e2dbb3a41d38d"
    assert d["snapshot"]["evidence_item_count"] <= d["snapshot"]["evidence_item_limit"] == 50
    by_id = {item["id"]: item for item in d["provenance"]}
    required = {
        "MODEL-V05",
        "HISTORY-SCHEMA",
        "EVENT-RELATIVE",
        "WP03-SUMMARY",
        "WP07B-HANDOFF-MD",
        "GAP006-V02",
        "GAP007",
        "GAP011",
        "QUICKREAD-CONTRACT",
        "QUICKREAD-READER",
        "DETAILEDREAD-PLANNER",
        "PL3T-COMPILER",
    }
    assert required <= set(by_id)
    assert all(item["git_blob_sha"] for item in by_id.values())


def test_natal_environment_response_manifestation_and_memory_objects_remain_distinct():
    d = audit()
    objects = {item["object"]: item for item in d["object_crosswalk"]}
    assert set(objects) == {"N", "E_decade", "E_year", "tau_t", "M0", "M_t"}
    assert objects["N"]["v05_model_object"] == "E = {e_p}; e_p = E_p(H_p^natal, G_0)"
    assert objects["tau_t"]["relation"] == "COMPATIBLE_RESPONSE_CROSSWALK"
    assert objects["M0"]["relation"] == "NOT_ONE_TO_ONE"
    assert "D_t" in objects["M_t"]["boundary"]
    assert "H_t" in objects["M_t"]["boundary"]


def test_decade_year_composition_is_held_without_global_default():
    d = audit()
    relation = next(row for row in d["temporal_relation_matrix"] if row["relation_id"] == "R03_DECADE_TO_YEAR")
    assert relation["status"] == "UNKNOWN_HOLD_COMPOSITION_UNSPECIFIED"
    assert relation["executable"] is False
    for phrase in ("inheritance", "AND/OR", "additive composition", "precedence"):
        assert phrase in relation["unresolved"]


def test_product_slots_and_temporal_compiler_contract_are_not_reinterpreted_as_source_truth():
    d = audit()
    findings = {row["id"]: row for row in d["findings"]}
    assert findings["F04"]["epistemic_status"] == "PRODUCT_CONTRACT"
    assert findings["F05"]["disposition"] == "PRESERVE_EXACT_LAYER_MATCH"
    assert findings["F08"]["disposition"] == "PRESERVE_COMPILER_GATE"
    assert findings["F09"]["disposition"] == "EXISTING_GAP_NOT_REOPENED"
    assert d["gap_register"][2]["owner"] == "PRODUCT"
    assert d["gap_register"][3]["owner"] == "PRODUCT"


def test_c9_multiyear_and_same_year_path_subtypes_remain_noninterchangeable():
    d = audit()
    multi = next(row for row in d["temporal_relation_matrix"] if row["relation_id"] == "R09_MULTIYEAR_ANNUAL_SEQUENCE")
    same_year = next(row for row in d["temporal_relation_matrix"] if row["relation_id"] == "R10_SAME_YEAR_ANTECEDENT")
    assert multi["status"] == "DESCRIPTIVE_HOLD"
    assert same_year["status"] == "CASE_PARENT_HOLD"
    assert multi["executable"] is False and same_year["executable"] is False
    assert "Approximate 三四年" in multi["unresolved"]
    assert "CASE_SUPPORT_ONLY" in same_year["unresolved"]


def test_source_negation_and_open_world_valence_remain_fail_closed():
    d = audit()
    negation = next(row for row in d["temporal_relation_matrix"] if row["relation_id"] == "R11_SOURCE_NEGATION")
    valence = next(row for row in d["temporal_relation_matrix"] if row["relation_id"] == "R12_GROUP_AND_VALENCE")
    assert negation["status"] == "DESCRIPTIVE_SOURCE_LOCAL_ONLY"
    assert "missing observations" in negation["unresolved"]
    assert valence["status"] == "DESCRIPTIVE_ONLY"
    assert "GOOD_YEAR" in valence["unresolved"]


def test_event_relative_window_is_not_general_history_memory():
    d = audit()
    event = next(row for row in d["temporal_relation_matrix"] if row["relation_id"] == "R08_EVENT_RELATIVE_WINDOW")
    assert event["status"] == "APPROVED_SINGLE_SCOPED_RULE"
    assert "general event timer" in event["unresolved"]
    assert d["authorization"]["history_memory_rows_added"] == 0


def test_accepted_core_c1_artifact_persists_when_core_recovery_pointer_advances():
    # C1 accepted audit remains immutable; CORE_STATE may advance to a new unit.
    import re
    state = CORE_STATE.read_text(encoding="utf-8")
    assert 'continuation_plan: "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md"' in state
    assert "plan_pointer_issue: 901" in state
    assert 'status: "ACTIVE"' in state or 'status: "IDLE"' in state
    completed = re.search(r"^  last_completed_issue: (\d+)$", state, re.M)
    assert completed and int(completed.group(1)) >= 964
    if 'status: "ACTIVE"' in state:
        active = re.search(r"^  active_issue: (\d+)$", state, re.M)
        assert active and int(active.group(1)) >= 964
        assert re.search(r'^  active_branch: "knowledge/core-\d+-[^"]+"$', state, re.M)
    else:
        assert "active_issue: null" in state
