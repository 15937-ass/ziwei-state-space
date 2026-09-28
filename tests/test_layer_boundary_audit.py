from src.audit_layer_boundary import classify, is_candidate


def row(target, operator="enhance", target_type="outcome_descriptor", evidence=""):
    return {
        "target_type": target_type,
        "operator": operator,
        "target_literal": target,
        "target_normalized": target,
        "evidence_text": evidence,
    }


def test_candidate_definition():
    assert is_candidate(row("发展机会"))
    assert not is_candidate(row("发展机会", operator="project"))
    assert not is_candidate(row("目标导向增强", target_type="qi_state"))


def test_l3_projection_classification():
    got = classify(row("职业发展机会"))
    assert got["audit_class"] == "LIKELY_L3_PROJECTION"
    assert got["proposed_operator"] == "project"


def test_l1_state_classification():
    got = classify(row("目标导向增强"))
    assert got["audit_class"] == "LIKELY_L1_STATE"
    assert got["proposed_target_type"] == "qi_state"


def test_l2_state_classification():
    got = classify(row("支持网络增强"))
    assert got["audit_class"] == "LIKELY_L2_RELATIONAL"
    assert got["proposed_target_type"] == "relational_state"


def test_mixed_state_projection_requires_review():
    got = classify(row("事业发展中目标导向增强"))
    assert got["audit_class"] == "MIXED_STATE_AND_PROJECTION"
    assert got["proposed_target_type"] == "REVIEW_REQUIRED"
