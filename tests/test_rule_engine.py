from src.rule_engine import Rule, query_rules, semantic_state_changes, trace, reject_fixed_event_mapping


def sample_rule():
    return Rule(
        rule_id="ZZ-TY-002",
        school="中州派",
        source_work="《中州派紫微斗数深造讲义（上）》",
        source_location="十四正曜·太阳",
        subject="太阳",
        context="general",
        condition="无",
        target_type="qi_state",
        target_literal="发射光和热",
        target_normalized="发射性",
        operator="assert",
        state_change="none",
        valence="context_dependent",
        epistemic_type_source="EXPLICIT",
        evidence_text="太阳最重要的特性是发射光和热。",
        status="draft",
    )


def test_query_and_trace_preserve_provenance():
    r = sample_rule()
    got = query_rules([r], subject="太阳")
    assert got == [r]
    assert trace(r)["source_location"] == "十四正曜·太阳"


def test_semantic_changes_do_not_invent_events():
    r = sample_rule()
    changes = semantic_state_changes([r])
    assert changes[0]["target"] == "发射性"
    assert "发财" not in str(changes)


def test_fixed_event_guardrail():
    try:
        reject_fixed_event_mapping("离婚", [])
    except ValueError:
        pass
    else:
        raise AssertionError("Fixed event mapping without provenance must be rejected.")
