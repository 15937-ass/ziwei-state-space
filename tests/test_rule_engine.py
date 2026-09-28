from src.rule_engine import (
    Rule,
    load_rules,
    apply_layer_split_plan,
    apply_layer_split_plans,
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


def test_layer_split_plan_replaces_parent_with_effective_children(tmp_path):
    parent = sample_rule()
    plan = tmp_path / "split.csv"
    plan.write_text(
        "parent_rule_id,child_rule_id,target_type,target_normalized,operator,state_change,valence,"
        "condition_refinement,source_epistemic,normalization_epistemic,review_status,"
        "source_span_verified,normalization_verified\n"
        "ZZ-TY-002,ZZ-TY-002-A,qi_state,state-a,enhance,increase,context_dependent,"
        "branch-a,EXPLICIT,INFERRED,SOURCE_SPAN_VERIFIED,true,false\n"
        "ZZ-TY-002,ZZ-TY-002-B,outcome_descriptor,out-b,project,none,favorable,"
        "branch-b,EXPLICIT,IMPLEMENTATION,SOURCE_SPAN_VERIFIED,true,false\n",
        encoding="utf-8",
    )

    effective = apply_layer_split_plan([parent], plan)
    assert [r.rule_id for r in effective] == ["ZZ-TY-002-A", "ZZ-TY-002-B"]
    assert all(r.parent_rule_id == "ZZ-TY-002" for r in effective)
    assert effective[1].operator == "project"
    assert "branch:branch-b" in effective[1].condition
    assert trace(effective[0])["parent_rule_id"] == "ZZ-TY-002"


def test_multiple_layer_split_plans_apply_in_order(tmp_path):
    parent_a = sample_rule()
    parent_b = Rule(**{**sample_rule().__dict__, "rule_id": "R-B", "subject": "巨门"})

    plan1 = tmp_path / "split1.csv"
    plan1.write_text(
        "parent_rule_id,child_rule_id,target_type,target_normalized,operator,state_change,valence,"
        "condition_refinement,source_epistemic,normalization_epistemic,review_status,"
        "source_span_verified,normalization_verified\n"
        "ZZ-TY-002,ZZ-TY-002-A,qi_state,state-a,enhance,increase,context_dependent,"
        "branch-a,EXPLICIT,INFERRED,SOURCE_SPAN_VERIFIED,true,false\n",
        encoding="utf-8",
    )
    plan2 = tmp_path / "split2.csv"
    plan2.write_text(
        "parent_rule_id,child_rule_id,target_type,target_normalized,operator,state_change,valence,"
        "condition_refinement,source_epistemic,normalization_epistemic,review_status,"
        "source_span_verified,normalization_verified\n"
        "R-B,R-B-P,outcome_descriptor,out-b,project,none,favorable,"
        "branch-b,EXPLICIT,IMPLEMENTATION,SOURCE_SPAN_VERIFIED,true,false\n",
        encoding="utf-8",
    )

    effective = apply_layer_split_plans([parent_a, parent_b], plan1, plan2)
    assert {r.rule_id for r in effective} == {"ZZ-TY-002-A", "R-B-P"}
    assert {r.parent_rule_id for r in effective} == {"ZZ-TY-002", "R-B"}


def test_architecture_hold_excludes_rule_from_effective_view(tmp_path):
    canonical = tmp_path / "rules.csv"
    canonical.write_text(
        "rule_id,school,source_work,source_location,subject,context,condition,target_type,"
        "target_literal,target_normalized,operator,state_change,valence,epistemic_type_source,"
        "evidence_text,status\n"
        "R-HOLD,中州派,W,p,破军,decade,x,outcome_descriptor,literal,norm,enhance,increase,"
        "unfavorable,EXPLICIT,e,reviewed\n"
        "R-OK,中州派,W,p2,破军,decade,y,qi_state,literal2,norm2,enhance,increase,"
        "context_dependent,EXPLICIT,e2,reviewed\n",
        encoding="utf-8",
    )
    hold = tmp_path / "hold.csv"
    hold.write_text(
        "record_id,status\n"
        "R-HOLD,ARCHITECTURE_HOLD\n",
        encoding="utf-8",
    )
    rules = load_rules(canonical, architecture_hold_path=hold)
    assert [r.rule_id for r in rules] == ["R-OK"]
