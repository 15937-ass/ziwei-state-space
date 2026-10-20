import pytest

from src.product.social_quickread import (
    AssertionMode,
    EvidenceNamespace,
    QuickReadClaim,
    QuickReadEvidenceRef,
    QuickReadPackage,
    QuickReadTopic,
    evidence_rule_ids,
    lint_rendered_text,
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


def test_claim_without_evidence_fails_closed():
    claim = QuickReadClaim(
        claim_id="c1",
        topic=QuickReadTopic.PERSONALITY,
        proposition="做事果决，有自己的主见",
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
        assertion_mode=AssertionMode.DIRECT_TENDENCY,
        evidence_refs=(_ref(EvidenceNamespace.TEMPORAL, rid="ZZ-T1"),),
        target_period="2026",
    )
    with pytest.raises(ValueError, match="direct fact"):
        too_direct.validate()


def test_specific_year_requires_temporal_evidence_and_period():
    claim = QuickReadClaim(
        claim_id="y1",
        topic=QuickReadTopic.SPECIFIC_YEAR,
        proposition="这一年做事阻力偏大",
        assertion_mode=AssertionMode.DIRECT_TENDENCY,
        evidence_refs=(_ref(EvidenceNamespace.TEMPORAL, rid="ZZ-T2"),),
        target_period="2024",
    )
    claim.validate()


def test_verbalizer_payload_hides_source_and_raw_evidence():
    claim = QuickReadClaim(
        claim_id="c1",
        topic=QuickReadTopic.PERSONALITY,
        proposition="整体务实，有行动力",
        assertion_mode=AssertionMode.DIRECT_TENDENCY,
        evidence_refs=(_ref(),),
    )
    package = QuickReadPackage(claims=(claim,), knowledge_version="kb-test")
    payload = package.verbalizer_payload()
    serialized = repr(payload)
    assert "ZHONGZHOU_PRIMARY" not in serialized
    assert "p.1" not in serialized
    assert "ZZ-R1" not in serialized
    assert payload["claims"][0]["proposition"] == "整体务实，有行动力"
    assert payload["style_contract"]["do_not_add_claims"] is True


def test_rule_ids_remain_available_for_audit():
    claims = (
        QuickReadClaim(
            claim_id="c1",
            topic=QuickReadTopic.PERSONALITY,
            proposition="果决",
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
