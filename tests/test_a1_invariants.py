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


def test_quarantined_rules_are_not_ontology_or_star_core_evidence():
    ontology = (ROOT / "knowledge/qi_ontology.yaml").read_text(encoding="utf-8")
    cores = (ROOT / "knowledge/star_cores.yaml").read_text(encoding="utf-8")
    for rule_id in ("ZZ-TT-010", "ZZ-SYS-38-032"):
        assert rule_id not in ontology
        assert rule_id not in cores


def test_quarantine_contains_confirmed_source_mismatches():
    rows = read_csv("knowledge/review/quarantine_v0.1.csv")
    by_id = {row["record_id"]: row for row in rows}
    assert by_id["ZZ-TT-010"]["effective_status"] == "QUARANTINED"
    assert by_id["ZZ-SYS-38-032"]["effective_status"] == "QUARANTINED"
    assert by_id["ZZ-SYS-38-032"]["reason_code"] == "SOURCE_MISMATCH_CONFIRMED"


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
