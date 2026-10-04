import pytest

from src.product.evidence_package import (
    ConfidenceBand,
    ConflictItem,
    ContrastiveItem,
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


def test_conflicted_requires_explicit_conflict():
    package = EvidencePackage(
        question="财帛结构",
        confidence_band=ConfidenceBand.CONFLICTED,
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
    contrastive = ContrastiveItem(
        rule_id="RULE-002",
        candidate_claim="另一候选",
        missing_all_of=("fact:a",),
    )
    package = EvidencePackage(
        question="事业趋势",
        active_rules=[item],
        contrastive=[contrastive],
        coverage={"EXECUTABLE": 1},
        confidence_band=ConfidenceBand.LOW_CONFIDENCE,
        confidence_rationale="test",
        engine_version="product-mvp",
        knowledge_version="test",
    )

    payload = package.to_dict()
    assert payload["confidence_band"] == "LOW_CONFIDENCE"
    assert payload["active_rules"][0]["rule_id"] == "RULE-001"
    assert payload["contrastive"][0]["rule_id"] == "RULE-002"
