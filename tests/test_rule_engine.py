from src.rule_engine import (
    Rule,
    load_rules,
    query_rules,
    semantic_state_changes,
    trace,
    reject_fixed_event_mapping,
)


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


def test_effective_loader_applies_sidecars_and_quarantine(tmp_path):
    canonical = tmp_path / "rules.csv"
    canonical.write_text(
        "rule_id,school,source_work,source_location,subject,context,condition,target_type,"
        "target_literal,target_normalized,operator,state_change,valence,epistemic_type_source,"
        "evidence_text,status\n"
        "R-1,中州派,W,old,天相,general,x,inference_rule,literal,norm,condition,none,"
        "not_applicable,EXPLICIT,e,reviewed\n"
        "R-2,中州派,W,p2,天同,general,y,qi_state,literal2,norm2,enhance,increase,"
        "unfavorable,EXPLICIT,e2,reviewed\n",
        encoding="utf-8",
    )
    review = tmp_path / "review.csv"
    review.write_text(
        "rule_id,source_epistemic,normalization_epistemic,review_status,source_span_verified,"
        "normalization_verified\n"
        "R-1,EXPLICIT,IMPLEMENTATION,MODEL_SELF_REVIEWED,false,false\n"
        "R-2,UNRESOLVED_SOURCE,UNRESOLVED,MODEL_SELF_REVIEWED,false,false\n",
        encoding="utf-8",
    )
    schema = tmp_path / "schema.csv"
    schema.write_text(
        "rule_id,field,old_value,new_value\n"
        "R-1,target_type,inference_rule,structural_relation\n",
        encoding="utf-8",
    )
    provenance = tmp_path / "provenance.csv"
    provenance.write_text(
        "rule_id,field,old_value,new_value\n"
        "R-1,source_location,old,new\n",
        encoding="utf-8",
    )
    quarantine = tmp_path / "quarantine.csv"
    quarantine.write_text(
        "record_id,effective_status\nR-2,QUARANTINED\n",
        encoding="utf-8",
    )

    rules = load_rules(
        canonical,
        quarantine_path=quarantine,
        schema_overrides_path=schema,
        provenance_overrides_path=provenance,
        review_metadata_path=review,
    )
    assert [r.rule_id for r in rules] == ["R-1"]
    assert rules[0].target_type == "structural_relation"
    assert rules[0].source_location == "new"
    assert rules[0].normalization_epistemic == "IMPLEMENTATION"


def test_verified_query_filter():
    verified = sample_rule()
    verified = Rule(**{**verified.__dict__, "source_span_verified": True})
    unverified = sample_rule()
    assert query_rules([verified, unverified], require_source_verified=True) == [verified]
