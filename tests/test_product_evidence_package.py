import pytest

from src.product.evidence_package import (
    ConfidenceBand,
    EvidenceItem,
    EvidencePackage,
)


def test_high_confidence_requires_evidence():
    package = EvidencePackage(
        question="事业趋势",
        confidence_band=ConfidenceBand.HIGH_CONFIDENCE,
    )
    with pytest.raises(ValueError):
        package.validate()


def test_package_serializes_confidence_and_evidence():
    item = EvidenceItem(
        rule_id="RULE-001",
        claim="示例结构性结论",
        source_id="SRC-ZZ-TEST",
        source_location="p1",
        epistemic="EXPLICIT",
        review_status="SOURCE_SPAN_VERIFIED",
    )
    package = EvidencePackage(
        question="事业趋势",
        active_rules=[item],
        confidence_band=ConfidenceBand.HIGH_CONFIDENCE,
        engine_version="product-mvp",
        knowledge_version="test",
    )

    payload = package.to_dict()
    assert payload["confidence_band"] == "HIGH_CONFIDENCE"
    assert payload["active_rules"][0]["rule_id"] == "RULE-001"
