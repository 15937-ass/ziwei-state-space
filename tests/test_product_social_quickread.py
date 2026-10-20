import pytest

from src.product.social_quickread import (
    AssertionMode,
    EvidenceNamespace,
    QuickReadClaim,
    QuickReadConversationContext,
    QuickReadDomain,
    QuickReadEvidenceRef,
    QuickReadPackage,
    QuickReadRenderAudit,
    QuickReadScope,
    QuickReadSentenceAudit,
    QuickReadScopePreset,
    QuickReadTopic,
    build_followup_payload,
    build_pilot_package,
    evidence_rule_ids,
    lint_rendered_text,
    resolve_followup_scope,
    resolve_pilot_scope,
)


def _ref(
    namespace=EvidenceNamespace.CANONICAL,
    *,
    school="ZHONGZHOU",
    rid="ZZ-R1",
):
    return QuickReadEvidenceRef(
        namespace=namespace,
        rule_id=rid,
        source_id="ZHONGZHOU_PRIMARY",
        source_location="p.1",
        review_status="REVIEWED",
        school=school,
    )


def _claim(
    claim_id,
    topic,
    proposition,
    *,
    namespace=EvidenceNamespace.CANONICAL,
    target_period="",
    domains=(),
    semantic_group=None,
    mode=AssertionMode.DIRECT_TENDENCY,
):
    return QuickReadClaim(
        claim_id=claim_id,
        topic=topic,
        proposition=proposition,
        assertion_mode=mode,
        evidence_refs=(_ref(namespace, rid=f"ZZ-{claim_id}"),),
        target_period=target_period,
        domains=domains,
        semantic_group=semantic_group or claim_id,
    )


def test_claim_without_evidence_fails_closed():
    claim = QuickReadClaim(
        claim_id="c1",
        topic=QuickReadTopic.PERSONALITY,
        proposition="做事果决，有自己的主见",
        semantic_group="agency",
        assertion_mode=AssertionMode.DIRECT_TENDENCY,
        evidence_refs=(),
    )
    with pytest.raises(ValueError, match="at least one evidence"):
        claim.validate()


def test_non_zhongzhou_evidence_is_rejected():
    claim = QuickReadClaim(
        claim_id="c1",
        topic=QuickReadTopic.PERSONALITY,
        proposition="做事果决",
        semantic_group="agency",
        assertion_mode=AssertionMode.DIRECT_TENDENCY,
        evidence_refs=(_ref(school="QINTIAN"),),
    )
    with pytest.raises(ValueError, match="ZHONGZHOU"):
        claim.validate()


def test_current_relationship_requires_temporal_and_non_direct_mode():
    no_temporal = QuickReadClaim(
        claim_id="c1",
        topic=QuickReadTopic.CURRENT_RELATIONSHIP,
        proposition="这几年感情容易被带起来",
        semantic_group="relationship_activation",
        assertion_mode=AssertionMode.TENDENCY,
        evidence_refs=(_ref(),),
        target_period="2025-2026",
    )
    with pytest.raises(ValueError, match="TEMPORAL"):
        no_temporal.validate()

    too_direct = QuickReadClaim(
        claim_id="c2",
        topic=QuickReadTopic.CURRENT_RELATIONSHIP,
        proposition="现在已经在谈恋爱",
        semantic_group="relationship_status",
        assertion_mode=AssertionMode.DIRECT_TENDENCY,
        evidence_refs=(_ref(EvidenceNamespace.TEMPORAL, rid="ZZ-T1"),),
        target_period="2026",
    )
    with pytest.raises(ValueError, match="direct fact"):
        too_direct.validate()


def test_specific_year_requires_temporal_evidence_and_period():
    claim = _claim(
        "y1",
        QuickReadTopic.SPECIFIC_YEAR,
        "这一年做事阻力偏大",
        namespace=EvidenceNamespace.TEMPORAL,
        target_period="2024",
    )
    claim.validate()


def test_relationship_scope_selects_only_relationship_claims_including_year_tags():
    claims = (
        _claim("p1", QuickReadTopic.PERSONALITY, "主体性强"),
        _claim(
            "r1",
            QuickReadTopic.PARTNER_PREFERENCE,
            "喜欢果决利落的类型",
        ),
        _claim(
            "y1",
            QuickReadTopic.SPECIFIC_YEAR,
            "2025年感情互动明显",
            namespace=EvidenceNamespace.TEMPORAL,
            target_period="2025",
            domains=(QuickReadDomain.RELATIONSHIP,),
            mode=AssertionMode.TENDENCY,
        ),
        _claim(
            "y2",
            QuickReadTopic.SPECIFIC_YEAR,
            "2025年学习工作有变动",
            namespace=EvidenceNamespace.TEMPORAL,
            target_period="2025",
            domains=(QuickReadDomain.STUDY_WORK,),
        ),
    )
    package = QuickReadPackage(
        claims=claims,
        knowledge_version="kb-test",
        scope=QuickReadScope(preset=QuickReadScopePreset.RELATIONSHIP),
    )
    assert [item.claim_id for item in package.selected_claims()] == ["r1", "y1"]
    payload = package.verbalizer_payload()
    assert payload["scope"]["preset"] == "relationship"
    assert {item["claim_id"] for item in payload["claims"]} == {"r1", "y1"}


def test_custom_scope_can_limit_to_one_topic_and_period():
    claims = (
        _claim(
            "y24",
            QuickReadTopic.SPECIFIC_YEAR,
            "2024年感情压力偏大",
            namespace=EvidenceNamespace.TEMPORAL,
            target_period="2024",
            domains=(QuickReadDomain.RELATIONSHIP,),
            mode=AssertionMode.TENDENCY,
        ),
        _claim(
            "y25",
            QuickReadTopic.SPECIFIC_YEAR,
            "2025年感情更活跃",
            namespace=EvidenceNamespace.TEMPORAL,
            target_period="2025",
            domains=(QuickReadDomain.RELATIONSHIP,),
            mode=AssertionMode.TENDENCY,
        ),
    )
    scope = QuickReadScope(
        preset=QuickReadScopePreset.CUSTOM,
        include_domains=(QuickReadDomain.RELATIONSHIP,),
        include_topics=(QuickReadTopic.SPECIFIC_YEAR,),
        period_labels=("2025",),
    )
    package = QuickReadPackage(claims=claims, knowledge_version="kb-test", scope=scope)
    assert [item.claim_id for item in package.selected_claims()] == ["y25"]


def test_verbalizer_payload_hides_source_and_raw_evidence():
    claim = _claim("c1", QuickReadTopic.PERSONALITY, "整体务实，有行动力")
    package = QuickReadPackage(claims=(claim,), knowledge_version="kb-test")
    payload = package.verbalizer_payload()
    serialized = repr(payload)
    assert "ZHONGZHOU_PRIMARY" not in serialized
    assert "p.1" not in serialized
    assert "ZZ-c1" not in serialized
    assert payload["claims"][0]["proposition"] == "整体务实，有行动力"
    assert payload["style_contract"]["do_not_add_claims"] is True


def test_conversation_context_keeps_all_claims_and_evidence_for_followup():
    claims = (
        _claim("p1", QuickReadTopic.PERSONALITY, "主体性强"),
        _claim("r1", QuickReadTopic.PARTNER_PREFERENCE, "喜欢果决的类型"),
    )
    context = QuickReadConversationContext(
        subject_key="subject-001",
        knowledge_version="kb-test",
        all_claims=claims,
        active_scope=QuickReadScope(preset=QuickReadScopePreset.RELATIONSHIP),
        rendered_text="整体看感情里比较看重对方做事是否果决。",
        chart_context={"birth_input_ref": "birth-001", "ming_palace": "X"},
        natal_profile_ref="natal-001",
        temporal_profile_refs=("temporal-2026",),
    )
    payload = context.continuation_payload()
    assert len(payload["claims"]) == 2
    assert payload["chart_context"]["birth_input_ref"] == "birth-001"
    assert payload["claims"][0]["evidence_refs"][0]["rule_id"] == "ZZ-p1"
    selected = {
        item["claim_id"]
        for item in payload["claims"]
        if item["selected_in_last_render"]
    }
    assert selected == {"r1"}
    assert payload["continuation_policy"]["new_claim_requires_runtime_evidence"] is True


def test_same_session_can_switch_from_relationship_to_personality_scope():
    claims = (
        _claim("p1", QuickReadTopic.PERSONALITY, "主体性强"),
        _claim("r1", QuickReadTopic.PARTNER_PREFERENCE, "喜欢果决的类型"),
    )
    context = QuickReadConversationContext(
        subject_key="subject-001",
        knowledge_version="kb-test",
        all_claims=claims,
        active_scope=QuickReadScope(preset=QuickReadScopePreset.RELATIONSHIP),
        rendered_text="感情简批",
    )
    package = context.package_for_scope(
        QuickReadScope(preset=QuickReadScopePreset.PERSONALITY)
    )
    assert [item.claim_id for item in package.selected_claims()] == ["p1"]


def test_rule_ids_remain_available_for_audit():
    claims = (
        QuickReadClaim(
            claim_id="c1",
            topic=QuickReadTopic.PERSONALITY,
            proposition="果决",
            semantic_group="agency",
            assertion_mode=AssertionMode.DIRECT_TENDENCY,
            evidence_refs=(_ref(rid="ZZ-R2"), _ref(rid="ZZ-R1")),
        ),
    )
    assert evidence_rule_ids(claims) == ("ZZ-R1", "ZZ-R2")


def test_style_linter_flags_report_like_output_and_overhedging():
    text = "# 性格\n- 根据紫微斗数，命主可能应该感觉可能大概率我会猜可能有主见。"
    warnings = lint_rendered_text(text)
    assert "MARKDOWN_HEADING_FORBIDDEN" in warnings
    assert "LIST_FORMAT_FORBIDDEN" in warnings
    assert "FORBIDDEN_TOKEN:根据紫微斗数" in warnings
    assert "FORBIDDEN_TOKEN:命主" in warnings
    assert "OVER_HEDGED" in warnings


def test_pilot_scope_resolver_understands_common_chinese_requests():
    assert resolve_pilot_scope("只看感情，150字").preset is QuickReadScopePreset.RELATIONSHIP
    assert resolve_pilot_scope("事业简批").preset is QuickReadScopePreset.STUDY_WORK
    assert resolve_pilot_scope("看一下父母关系").preset is QuickReadScopePreset.FAMILY
    assert resolve_pilot_scope("随便简批一下").preset is QuickReadScopePreset.FULL


def test_build_pilot_package_filters_claims_for_manual_chatgpt_trial():
    claims = (
        _claim("p1", QuickReadTopic.PERSONALITY, "主体性强"),
        _claim("r1", QuickReadTopic.PARTNER_PREFERENCE, "喜欢果决的类型"),
        _claim("w1", QuickReadTopic.STUDY_WORK, "工作更喜欢有自主空间"),
    )
    package = build_pilot_package(
        claims=claims,
        knowledge_version="kb-test",
        request_text="只要感情简批",
        target_chars_min=100,
        target_chars_max=180,
    )
    assert package.scope.preset is QuickReadScopePreset.RELATIONSHIP
    assert [item.claim_id for item in package.selected_claims()] == ["r1"]
    assert package.target_chars_min == 100
    assert package.target_chars_max == 180


def test_package_rejects_duplicate_semantic_groups_before_verbalizer():
    claims = (
        _claim(
            "p1",
            QuickReadTopic.PERSONALITY,
            "内心很有主见",
            semantic_group="agency_control",
        ),
        _claim(
            "p2",
            QuickReadTopic.PERSONALITY,
            "更在意自己能不能做主",
            semantic_group="agency_control",
        ),
    )
    package = QuickReadPackage(claims=claims, knowledge_version="kb-test")
    with pytest.raises(ValueError, match="redundant semantic claims"):
        package.validate()


def test_same_semantic_group_can_appear_in_different_years():
    claims = (
        _claim(
            "y24",
            QuickReadTopic.SPECIFIC_YEAR,
            "2024年感情摩擦偏多",
            namespace=EvidenceNamespace.TEMPORAL,
            target_period="2024",
            domains=(QuickReadDomain.RELATIONSHIP,),
            semantic_group="relationship_friction",
            mode=AssertionMode.TENDENCY,
        ),
        _claim(
            "y25",
            QuickReadTopic.SPECIFIC_YEAR,
            "2025年感情摩擦偏多",
            namespace=EvidenceNamespace.TEMPORAL,
            target_period="2025",
            domains=(QuickReadDomain.RELATIONSHIP,),
            semantic_group="relationship_friction",
            mode=AssertionMode.TENDENCY,
        ),
    )
    QuickReadPackage(claims=claims, knowledge_version="kb-test").validate()


def test_render_audit_blocks_rephrasing_same_point_twice():
    claims = (
        _claim(
            "p1",
            QuickReadTopic.PERSONALITY,
            "主体性强",
            semantic_group="agency_control",
        ),
        _claim(
            "w1",
            QuickReadTopic.STUDY_WORK,
            "工作里重视自主空间",
            semantic_group="work_autonomy",
        ),
    )
    package = QuickReadPackage(claims=claims, knowledge_version="kb-test")
    audit = QuickReadRenderAudit(
        package=package,
        sentences=(
            QuickReadSentenceAudit("整体看人很有主见。", ("p1",)),
            QuickReadSentenceAudit("不太喜欢别人替自己做决定。", ("p1",)),
        ),
    )
    with pytest.raises(ValueError, match="repeats semantic group"):
        audit.validate()


def test_render_audit_blocks_sentence_without_claim():
    package = QuickReadPackage(
        claims=(
            _claim(
                "p1",
                QuickReadTopic.PERSONALITY,
                "主体性强",
                semantic_group="agency_control",
            ),
        ),
        knowledge_version="kb-test",
    )
    audit = QuickReadRenderAudit(
        package=package,
        sentences=(QuickReadSentenceAudit("外表看着很靠谱。", ()),),
    )
    with pytest.raises(ValueError, match="at least one claim"):
        audit.validate()


def test_followup_without_new_domain_keeps_current_scope():
    current = QuickReadScope(preset=QuickReadScopePreset.RELATIONSHIP)
    scope = resolve_followup_scope("为什么这么说？", current_scope=current)
    assert scope.preset is QuickReadScopePreset.RELATIONSHIP
    assert scope.max_claims == 8


def test_followup_can_switch_domain_without_restarting_subject():
    claims = (
        _claim("r1", QuickReadTopic.PARTNER_PREFERENCE, "喜欢果决的类型"),
        _claim("w1", QuickReadTopic.STUDY_WORK, "适合变化快的工作"),
    )
    context = QuickReadConversationContext(
        subject_key="subject-001",
        knowledge_version="kb-test",
        all_claims=claims,
        active_scope=QuickReadScope(preset=QuickReadScopePreset.RELATIONSHIP),
        rendered_text="感情里双方都比较有主见。",
    )
    payload = build_followup_payload(
        context=context,
        question="那事业呢？",
    )
    assert payload["mode"] == "social_quickread_followup_v0.1"
    assert payload["scope"]["preset"] == "study_work"
    assert [item["claim_id"] for item in payload["claims"]] == ["w1"]
    assert payload["previous_rendered_text"] == "感情里双方都比较有主见。"
    assert payload["style_contract"]["no_overall_recap"] is True


def test_followup_rejects_empty_question():
    context = QuickReadConversationContext(
        subject_key="subject-001",
        knowledge_version="kb-test",
        all_claims=(
            _claim("p1", QuickReadTopic.PERSONALITY, "主体性强"),
        ),
        active_scope=QuickReadScope(preset=QuickReadScopePreset.PERSONALITY),
        rendered_text="整体看人很有主见。",
    )
    with pytest.raises(ValueError, match="follow-up question"):
        build_followup_payload(context=context, question="   ")
