from pathlib import Path

from src.audit_repository import (
    audit_modifier_catalog,
    audit_rule_catalog,
    composite_condition_score,
    outcome_operator_candidates,
)


def test_illegal_rule_target_type_is_p0():
    rows = [{
        "rule_id": "R-1",
        "target_type": "inference_rule",
        "operator": "condition",
        "source_location": "p1",
    }]
    findings = audit_rule_catalog(Path("x.csv"), rows)
    assert any(f.severity == "P0" and f.field == "target_type" for f in findings)


def test_illegal_modifier_operator_is_p0():
    rows = [{
        "operator_rule_id": "M-1",
        "operator_type": "time_scale_effect",
        "source_location": "p2",
    }]
    findings = audit_modifier_catalog(Path("m.csv"), rows)
    assert any(f.severity == "P0" and f.field == "operator_type" for f in findings)


def test_composite_condition_is_only_a_review_heuristic():
    assert composite_condition_score("A或B/C、D") >= 2
    assert composite_condition_score("单一条件") == 0


def test_outcome_directional_operator_is_layer_review_candidate():
    rows = [{
        "rule_id": "R-2",
        "target_type": "outcome_descriptor",
        "operator": "enhance",
        "source_location": "p3",
    }]
    findings = outcome_operator_candidates(Path("x.csv"), rows)
    assert findings
    assert findings[0].severity == "P1"
