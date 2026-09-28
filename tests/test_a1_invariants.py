import csv
import json
import re
from pathlib import Path


ROOT = Path(".")


def read_csv(path):
    with (ROOT / path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def canonical_rule_index():
    rows = []
    for path in (
        "knowledge/rules/stars/major_stars_canonical_v0.1.csv",
        "knowledge/rules/systems/sixty_systems_canonical_v0.1.csv",
    ):
        rows.extend(read_csv(path))
    return {row["rule_id"]: row for row in rows}


def test_qi16_is_formal_and_old_merged_persistence_is_gone():
    text = (ROOT / "knowledge/qi_ontology.yaml").read_text(encoding="utf-8")
    assert 'id: QI-16' in text
    assert 'status: "A1_FORMAL_L1"' in text
    assert 'id: QI-17-CAND' in text
    assert 'id: QI-18-CAND' in text
    assert 'name: "持续意志/韧性"' not in text


def test_quarantined_rules_are_not_active_ontology_or_star_core_evidence():
    ontology = (ROOT / "knowledge/qi_ontology.yaml").read_text(encoding="utf-8")
    cores = (ROOT / "knowledge/star_cores.yaml").read_text(encoding="utf-8")
    active_evidence_text = "\n".join(
        re.findall(r"evidence_rules:\s*\[[^\]]*\]", ontology + "\n" + cores)
    )
    for rule_id in ("ZZ-TT-010", "ZZ-SYS-38-032", "ZZ-SYS-38-034"):
        assert rule_id not in active_evidence_text


def test_quarantine_contains_confirmed_source_mismatches():
    rows = read_csv("knowledge/review/quarantine_v0.1.csv")
    by_id = {row["record_id"]: row for row in rows}
    assert by_id["ZZ-TT-010"]["effective_status"] == "QUARANTINED"
    assert by_id["ZZ-SYS-38-032"]["effective_status"] == "QUARANTINED"
    assert by_id["ZZ-SYS-38-032"]["reason_code"] == "SOURCE_MISMATCH_CONFIRMED"
    assert by_id["ZZ-SYS-38-034"]["effective_status"] == "QUARANTINED"
    assert by_id["ZZ-SYS-38-034"]["reason_code"] == "NORMALIZATION_MISMATCH_CONFIRMED"
    assert by_id["ZZ-SYS-50-028"]["effective_status"] == "QUARANTINED"
    assert by_id["ZZ-SYS-50-028"]["reason_code"] == "NORMALIZATION_MISMATCH_CONFIRMED"


def test_all_ontology_evidence_ids_exist_in_canonical():
    ontology = (ROOT / "knowledge/qi_ontology.yaml").read_text(encoding="utf-8")
    ids = set(re.findall(r"\bZZ-[A-Z0-9-]+\b", ontology))
    canonical = canonical_rule_index()
    missing = sorted(ids - set(canonical))
    assert not missing, missing


def test_direct_star_evidence_matches_star_subject():
    text = (ROOT / "knowledge/star_cores.yaml").read_text(encoding="utf-8")
    canonical = canonical_rule_index()
    current_star = None
    for line in text.splitlines():
        name_match = re.match(r'\s+name:\s+"([^"]+)"', line)
        if name_match:
            current_star = name_match.group(1)
        if 'evidence_tier: "DIRECT_STAR"' not in line or current_star is None:
            continue
        ids = re.findall(r"\bZZ-[A-Z0-9-]+\b", line)
        for rule_id in ids:
            assert canonical[rule_id]["subject"] == current_star, (
                current_star,
                rule_id,
                canonical[rule_id]["subject"],
            )


def test_atomicity_logic_covers_all_reviewed_candidates():
    review = read_csv("validation/decontamination/P1_atomicity_source_review_v0.1.csv")
    payload = json.loads(
        (ROOT / "knowledge/logic/p1_atomicity_logic_v0.1.json").read_text(encoding="utf-8")
    )
    assert len(review) == 39
    assert len(payload["records"]) == 39
    ids = {row["record_id"] for row in review}
    logic_ids = {row["rule_id"] for row in payload["records"]}
    assert ids == logic_ids
    assert not any(
        row["execution_mode"] == "EXPLICIT_AST"
        and row["logic"].get("parser_status") == "MANUAL_AST_PENDING"
        for row in payload["records"]
    )


def test_layer_boundary_batch_is_complete_and_not_auto_verified():
    rows = read_csv("validation/decontamination/P1_layer_boundary_batch_audit_v0.2.csv")
    assert len(rows) == 800
    assert all(row["normalization_status"] == "PENDING_SOURCE_SPAN_NORMALIZATION_REVIEW" for row in rows)


def test_observability_language_is_demoted():
    spec = (ROOT / "src/model_spec.py").read_text(encoding="utf-8")
    theory = (ROOT / "theory/state_space_model.md").read_text(encoding="utf-8")
    assert "class ObservationPathSupport" in spec
    assert "STRUCTURALLY_OBSERVABLE" not in spec
    assert "Observation-path support" in theory


def test_lb02_review_and_split_plan_are_consistent():
    reviews = read_csv("validation/decontamination/LB02_source_normalization_review_v0.1.csv")
    plan = read_csv("knowledge/migrations/p1_layer_split_plan_LB02_v0.1.csv")
    assert len(reviews) == 50
    assert sum(row["source_review_result"] == "SOURCE_MISMATCH_CONFIRMED" for row in reviews) == 1
    assert {row["parent_rule_id"] for row in plan} == {
        row["record_id"]
        for row in reviews
        if row["source_review_result"] != "SOURCE_MISMATCH_CONFIRMED"
    }
    assert len({row["parent_rule_id"] for row in plan}) == 49
    assert len(plan) == 76
    assert "ZZ-SYS-38-032" not in {row["parent_rule_id"] for row in plan}


def test_first_two_layer_batches_have_closed_model_review_status():
    rows = read_csv("validation/decontamination/P1_layer_boundary_review_batches_v0.1.csv")
    lb01 = [row for row in rows if row["batch_id"] == "LB-01"]
    lb02 = [row for row in rows if row["batch_id"] == "LB-02"]
    assert len(lb01) == 50
    assert len(lb02) == 50
    assert all(row["status"] == "MODEL_SOURCE_NORMALIZATION_REVIEWED" for row in lb01)
    assert sum(row["status"] == "MODEL_SOURCE_NORMALIZATION_REVIEWED" for row in lb02) == 49
    assert sum(row["status"] == "QUARANTINED_SOURCE_MISMATCH" for row in lb02) == 1


def test_lb03_review_and_split_plan_are_consistent():
    reviews = read_csv("validation/decontamination/LB03_source_normalization_review_v0.1.csv")
    plan = read_csv("knowledge/migrations/p1_layer_split_plan_LB03_v0.1.csv")
    assert len(reviews) == 50
    assert all(row["source_span_verified"] == "true" for row in reviews)
    assert {row["parent_rule_id"] for row in plan} == {row["record_id"] for row in reviews}
    assert len({row["parent_rule_id"] for row in plan}) == 50
    assert len(plan) == 91


def test_first_three_layer_batches_have_closed_model_review_status():
    rows = read_csv("validation/decontamination/P1_layer_boundary_review_batches_v0.1.csv")
    lb01 = [row for row in rows if row["batch_id"] == "LB-01"]
    lb02 = [row for row in rows if row["batch_id"] == "LB-02"]
    lb03 = [row for row in rows if row["batch_id"] == "LB-03"]
    assert all(row["status"] == "MODEL_SOURCE_NORMALIZATION_REVIEWED" for row in lb01)
    assert sum(row["status"] == "MODEL_SOURCE_NORMALIZATION_REVIEWED" for row in lb02) == 49
    assert sum(row["status"] == "QUARANTINED_SOURCE_MISMATCH" for row in lb02) == 1
    assert all(row["status"] == "MODEL_SOURCE_NORMALIZATION_REVIEWED" for row in lb03)


def test_lb04_review_split_and_duplicate_quarantine_are_consistent():
    reviews = read_csv("validation/decontamination/LB04_source_normalization_review_v0.1.csv")
    plan = read_csv("knowledge/migrations/p1_layer_split_plan_LB04_v0.1.csv")
    assert len(reviews) == 50
    duplicates = [row for row in reviews if row["source_review_result"] == "SOURCE_SUPPORTED_DUPLICATE_CONFIRMED"]
    assert [row["record_id"] for row in duplicates] == ["ZZ-SYS-51-045"]
    assert "ZZ-SYS-51-045" not in {row["parent_rule_id"] for row in plan}
    assert len({row["parent_rule_id"] for row in plan}) == 49
    assert len(plan) == 90

    quarantine = {row["record_id"]: row for row in read_csv("knowledge/review/quarantine_v0.1.csv")}
    assert quarantine["ZZ-SYS-51-045"]["reason_code"] == "REDUNDANT_DUPLICATE_CONFIRMED"
    assert quarantine["ZZ-SYS-51-045"]["effective_status"] == "QUARANTINED"


def test_first_four_layer_batches_are_closed_at_model_review_level():
    rows = read_csv("validation/decontamination/P1_layer_boundary_review_batches_v0.1.csv")
    for batch in ("LB-01", "LB-03"):
        selected = [row for row in rows if row["batch_id"] == batch]
        assert len(selected) == 50
        assert all(row["status"] == "MODEL_SOURCE_NORMALIZATION_REVIEWED" for row in selected)

    lb02 = [row for row in rows if row["batch_id"] == "LB-02"]
    lb04 = [row for row in rows if row["batch_id"] == "LB-04"]
    assert sum(row["status"] == "QUARANTINED_SOURCE_MISMATCH" for row in lb02) == 1
    assert sum(row["status"] == "QUARANTINED_REDUNDANT_DUPLICATE" for row in lb04) == 1
    assert sum(row["status"] == "MODEL_SOURCE_NORMALIZATION_REVIEWED" for row in lb04) == 49


def test_lb05_review_and_refit_plan_are_consistent():
    reviews = read_csv("validation/decontamination/LB05_source_normalization_review_v0.1.csv")
    plan = read_csv("knowledge/migrations/p1_layer_split_plan_LB05_v0.1.csv")
    assert len(reviews) == 50
    assert all(row["source_span_verified"] == "true" for row in reviews)
    assert {row["parent_rule_id"] for row in plan} == {row["record_id"] for row in reviews}
    assert len({row["parent_rule_id"] for row in plan}) == 50
    assert len(plan) == 82


def test_lb05_adds_source_reviewed_qi16_contrasts():
    ontology = (ROOT / "knowledge/qi_ontology.yaml").read_text(encoding="utf-8")
    assert "ZZ-SYS-31-014" in ontology
    assert "ZZ-SYS-31-018" in ontology
    assert 'confidence: "high"' in ontology[ontology.index("  - id: QI-16"):ontology.index("relational_network_states:")]


def test_first_five_layer_batches_have_expected_closed_status():
    rows = read_csv("validation/decontamination/P1_layer_boundary_review_batches_v0.1.csv")
    for batch in ("LB-01", "LB-03", "LB-05"):
        selected = [row for row in rows if row["batch_id"] == batch]
        assert len(selected) == 50
        assert all(row["status"] == "MODEL_SOURCE_NORMALIZATION_REVIEWED" for row in selected)

    lb02 = [row for row in rows if row["batch_id"] == "LB-02"]
    lb04 = [row for row in rows if row["batch_id"] == "LB-04"]
    assert sum(row["status"] == "QUARANTINED_SOURCE_MISMATCH" for row in lb02) == 1
    assert sum(row["status"] == "QUARANTINED_REDUNDANT_DUPLICATE" for row in lb04) == 1


def test_lb06_review_split_plan_preserves_pre_a2_reserved_parents():
    reviews = read_csv("validation/decontamination/LB06_source_normalization_review_v0.1.csv")
    plan = read_csv("knowledge/migrations/p1_layer_split_plan_LB06_v0.1.csv")
    assert len(reviews) == 50
    reserved = {"ZZ-SYS-31-033", "ZZ-SYS-38-034", "ZZ-SYS-41-023"}
    assert reserved.isdisjoint({row["parent_rule_id"] for row in plan})
    assert {row["parent_rule_id"] for row in plan} == {
        row["record_id"] for row in reviews
    } - reserved
    assert len({row["parent_rule_id"] for row in plan}) == 47
    assert len(plan) == 86


def test_lb06_queue_is_closed_after_a2_r1():
    rows = read_csv("validation/decontamination/P1_layer_boundary_review_batches_v0.1.csv")
    lb06 = [row for row in rows if row["batch_id"] == "LB-06"]
    assert len(lb06) == 50
    assert sum(row["status"] == "MODEL_SOURCE_NORMALIZATION_REVIEWED" for row in lb06) == 47
    assert sum(row["status"] == "A2_R1_HISTORY_MIGRATED" for row in lb06) == 2
    assert sum(row["status"] == "QUARANTINED_NORMALIZATION_MISMATCH" for row in lb06) == 1
    assert not any(row["status"] == "A2_ARCHITECTURE_HOLD" for row in lb06)


def test_a2_architecture_hold_registry_resolved_by_a2_r1():
    holds = read_csv("validation/decontamination/A2_architecture_hold_v0.1.csv")
    by_id = {row["record_id"]: row for row in holds}
    assert set(by_id) == {"ZZ-SYS-31-033", "ZZ-SYS-38-034", "ZZ-SYS-41-023"}
    assert by_id["ZZ-SYS-31-033"]["execution_status"] == "MIGRATED_A2_R1_ACQUIRED_DISPOSITION"
    assert by_id["ZZ-SYS-41-023"]["execution_status"] == "MIGRATED_A2_R1_ACQUIRED_DISPOSITION"
    assert by_id["ZZ-SYS-38-034"]["execution_status"] == "QUARANTINED_REPLACED_BY_ZZ-SYS-38-021"
    quarantine = {row["record_id"] for row in read_csv("knowledge/review/quarantine_v0.1.csv")}
    assert "ZZ-SYS-38-034" in quarantine


def test_a2_history_transition_sidecar_is_typed_and_source_gated():
    rows = read_csv("knowledge/history/history_transitions_v0.1.csv")
    ids = [row["transition_id"] for row in rows]
    assert len(ids) == len(set(ids))
    assert {"HU-001", "HG-001", "HU-002", "HU-003", "HU-004"} <= set(ids)
    assert {row["memory_kind"] for row in rows} == {"ACQUIRED_DISPOSITION", "PATH_DEPENDENT_GATE"}
    assert all(row["source_epistemic"] == "EXPLICIT" for row in rows)
    assert all(row["persistence_scope"] in {"specific_next_period", "later_periods", "unspecified"} for row in rows)
    source_ids = {row["source_rule_id"] for row in rows}
    assert "ZZ-SYS-38-034" not in source_ids
    assert "ZZ-SYS-38-021" in source_ids

    candidates = read_csv("validation/decontamination/A2_history_marker_candidates_v0.1.csv")
    migrated = {
        row["record_id"]
        for row in candidates
        if row["review_status"].startswith("MIGRATED_A2_R1_")
    }
    assert migrated == source_ids
