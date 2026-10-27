import json
from dataclasses import replace
from pathlib import Path

import pytest

from src.product.quickread_capability import (
    CapabilityManifest,
    CapabilityRecord,
    EvidenceSourceRef,
    QuickReadEvidenceItem,
    QuickReadRequest,
    QuickReadScopeSlot,
    build_quickread_payload,
    validate_model_supplements,
)


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "product"
    / "QUICKREAD_CAPABILITY_SYNTHETIC_FIXTURE_V0_1.json"
)


def _slot(slot_id, domain, layer="NATAL", kind="NATAL_STRUCTURE", namespaces=None):
    if namespaces is None:
        namespaces = ("CANONICAL",) if layer == "NATAL" else ("CANONICAL", "TEMPORAL")
    return QuickReadScopeSlot(
        slot_id=slot_id,
        domain=domain,
        temporal_layer=layer,
        capability_kind=kind,
        required_namespaces=tuple(namespaces),
    )


def _ref(source_id, *, allowed_use="RETRIEVAL_ONLY", namespace="CANONICAL", layer="NATAL",
         location=None, review="HUMAN_VERIFIED"):
    return EvidenceSourceRef(
        source_id=source_id,
        source_location=location or f"synthetic {source_id}",
        review_status=review,
        allowed_use=allowed_use,
        namespace=namespace,
        time_layer=layer,
    )


def _fixture_objects(mode="HYBRID"):
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    slots = (
        _slot("career_natal", "career"),
        _slot("career_year_2027", "career", "YEAR", "TEMPORAL_RESPONSE"),
        _slot("relationship_natal", "relationship"),
    )
    request = QuickReadRequest(
        question="简要看看事业与关系倾向",
        target_id="SYNTHETIC-CHART-001",
        requested_slots=slots,
        mode=mode,
        min_chars=120,
        max_chars=220,
    )
    career_natal_source = _ref(
        "SRC-CAREER-001", location="synthetic source p.1"
    )
    career_year_natal_source = _ref(
        "SRC-CAREER-NATAL-002",
        location="synthetic natal source p.2",
        review="SOURCE_REVIEWED",
    )
    career_year_temporal_source = _ref(
        "SRC-CAREER-YEAR-003",
        namespace="TEMPORAL",
        layer="YEAR",
        location="synthetic year source p.3",
    )
    manifest = CapabilityManifest(
        main_sha=fixture["versions"]["main_sha"],
        knowledge_version=fixture["versions"]["knowledge_version"],
        runtime_version=fixture["versions"]["runtime_version"],
        records=(
            CapabilityRecord(
                slot=slots[0],
                runtime_status="AVAILABLE",
                source_status="AVAILABLE",
                runtime_rule_ids=("RULE-CAREER-NATAL-001",),
                source_refs=(career_natal_source,),
                reason="Synthetic example only.",
            ),
            CapabilityRecord(
                slot=slots[1],
                runtime_status="PARTIAL",
                source_status="PARTIAL",
                runtime_rule_ids=("RULE-CAREER-YEAR-001",),
                source_refs=(career_year_natal_source, career_year_temporal_source),
                reason="Synthetic partial temporal capability.",
            ),
        ),
    )
    items = (
        QuickReadEvidenceItem(
            evidence_id="EV-RUNTIME-001",
            slot_id="career_natal",
            lane="RUNTIME",
            claim="示例：本命事业结构具有某项已计算倾向。",
            rule_id="RULE-CAREER-NATAL-001",
            source_refs=(
                _ref(
                    "SRC-CAREER-001",
                    allowed_use="EXECUTABLE",
                    location="synthetic source p.1",
                ),
            ),
            epistemic_label="CANONICAL_RUNTIME",
        ),
        QuickReadEvidenceItem(
            evidence_id="EV-SOURCE-001",
            slot_id="career_year_2027",
            lane="SOURCE",
            claim="示例：已接受资料中存在与该时间层相关的描述。",
            source_refs=(career_year_natal_source, career_year_temporal_source),
            epistemic_label="SOURCE_GROUNDED",
        ),
        QuickReadEvidenceItem(
            evidence_id="EV-MODEL-001",
            slot_id="relationship_natal",
            lane="MODEL_SUPPLEMENT",
            claim="示例：模型对关系主题提出一项待核实的补充解释。",
            epistemic_label="MODEL_SUPPLEMENT",
            uncertainty="仅为模型补充，未被当前运行时或已接受来源独立证实。",
        ),
    )
    return fixture, request, manifest, items


def test_synthetic_fixture_expected_counts_match_actual_coverage():
    fixture, request, manifest, items = _fixture_objects()
    payload = build_quickread_payload(
        request,
        manifest,
        items,
        chart_context={"normalized_chart": {"synthetic": True}},
    )
    actual = {
        key: payload["coverage"][key]
        for key in fixture["expected_coverage"]
    }
    assert actual == fixture["expected_coverage"]
    assert payload["versions"]["main_sha"] == "SYNTHETIC-MAIN-SHA"


def test_model_supplement_never_increases_runtime_or_source_coverage():
    _, request, manifest, items = _fixture_objects()
    report = build_quickread_payload(
        request, manifest, items, chart_context={"normalized_chart": {"synthetic": True}}
    )["coverage"]
    assert report["runtime_evidenced_slot_count"] == 1
    assert report["source_evidenced_slot_count"] == 1
    assert report["model_supplemented_slot_count"] == 1
    assert report["uncovered_by_runtime_and_source_slot_count"] == 1
    assert report["runtime_evidence_coverage_ratio"] == pytest.approx(1 / 3, abs=0.0001)
    assert report["source_evidence_coverage_ratio"] == pytest.approx(1 / 3, abs=0.0001)


def test_payload_preserves_three_lanes_and_manifest_versions():
    _, request, manifest, items = _fixture_objects()
    payload = build_quickread_payload(
        request, manifest, items, chart_context={"normalized_chart": {"synthetic": True}}
    )
    assert len(payload["evidence"]["runtime"]) == 1
    assert len(payload["evidence"]["source"]) == 1
    assert len(payload["evidence"]["model_supplement"]) == 1
    assert payload["versions"] == {
        "main_sha": manifest.main_sha,
        "knowledge_version": manifest.knowledge_version,
        "runtime_version": manifest.runtime_version,
    }


def test_audit_mode_includes_only_runtime_evidence():
    _, request, manifest, items = _fixture_objects(mode="AUDIT")
    payload = build_quickread_payload(
        request, manifest, items, chart_context={"normalized_chart": {"synthetic": True}}
    )
    assert len(payload["evidence"]["runtime"]) == 1
    assert payload["evidence"]["source"] == []
    assert payload["evidence"]["model_supplement"] == []
    assert payload["chart_context"] == {}
    assert payload["model_supplement_request"]["enabled"] is False
    assert payload["coverage"]["source_evidenced_slot_count"] == 0
    assert payload["coverage"]["model_supplemented_slot_count"] == 0


def test_source_first_mode_includes_source_but_excludes_model_supplement():
    _, request, manifest, items = _fixture_objects(mode="SOURCE_FIRST")
    payload = build_quickread_payload(
        request, manifest, items, chart_context={"normalized_chart": {"synthetic": True}}
    )
    assert len(payload["evidence"]["runtime"]) == 1
    assert len(payload["evidence"]["source"]) == 1
    assert payload["evidence"]["model_supplement"] == []
    assert payload["model_supplement_request"]["enabled"] is False


def test_missing_chart_context_does_not_request_model_supplement():
    _, request, manifest, items = _fixture_objects()
    payload = build_quickread_payload(request, manifest, items)
    assert payload["model_supplement_request"]["enabled"] is False
    assert payload["model_supplement_request"]["slot_ids"] == []
    assert payload["model_supplement_request"]["disabled_reason"] == (
        "NORMALIZED_CHART_CONTEXT_MISSING"
    )


def test_temporal_slot_requires_target_layer_evidence():
    _, request, manifest, items = _fixture_objects()
    year_item = items[1]
    natal_only = replace(
        year_item,
        source_refs=(year_item.source_refs[0],),
    )
    with pytest.raises(ValueError, match="required namespaces"):
        build_quickread_payload(
            request,
            manifest,
            (items[0], natal_only, items[2]),
            chart_context={"normalized_chart": {"synthetic": True}},
        )


def test_source_evidence_is_rejected_when_manifest_marks_it_blocked():
    _, request, manifest, items = _fixture_objects()
    first, second = manifest.records
    blocked_first = replace(
        first,
        source_status="BLOCKED",
        source_refs=(),
    )
    blocked_manifest = replace(manifest, records=(blocked_first, second))
    blocked_source_item = replace(
        items[1],
        slot_id="career_natal",
        source_refs=(
            _ref("SRC-CAREER-001", location="synthetic source p.1"),
        ),
    )
    with pytest.raises(ValueError, match="source evidence supplied while source is unavailable"):
        build_quickread_payload(
            request,
            blocked_manifest,
            (items[0], blocked_source_item, items[2]),
            chart_context={"normalized_chart": {"synthetic": True}},
        )


def test_model_supplement_cannot_invent_rule_or_source_refs():
    with pytest.raises(ValueError, match="may not invent rule_id or source_refs"):
        QuickReadEvidenceItem(
            evidence_id="EV-MODEL-BAD",
            slot_id="career_natal",
            lane="MODEL_SUPPLEMENT",
            claim="unsupported claim",
            rule_id="FAKE-RULE",
            epistemic_label="MODEL_SUPPLEMENT",
            uncertainty="unverified",
        )


def test_case_support_only_requires_case_scope_and_cannot_be_generalized():
    ref = _ref(
        "SRC-CASE-001",
        allowed_use="CASE_SUPPORT_ONLY",
        namespace="CASE",
        location="synthetic case paragraph",
    )
    with pytest.raises(ValueError, match="case-only evidence requires"):
        QuickReadEvidenceItem(
            evidence_id="EV-CASE-BAD",
            slot_id="case_slot",
            lane="SOURCE",
            claim="a case-scoped observation",
            source_refs=(ref,),
            epistemic_label="CASE_SUPPORT_ONLY",
        )
    with pytest.raises(ValueError, match="CASE_SUPPORT_ONLY"):
        QuickReadEvidenceItem(
            evidence_id="EV-CASE-GENERALIZED",
            slot_id="case_slot",
            lane="SOURCE",
            claim="a generalized rule",
            source_refs=(ref,),
            epistemic_label="SOURCE_GROUNDED",
            case_scope="CASE-001",
        )


def test_unreviewed_source_ref_fails_closed():
    with pytest.raises(ValueError, match="not accepted/reviewed"):
        _ref("SRC-DRAFT", review="DRAFT")


def test_duplicate_requested_slots_are_rejected():
    slot = _slot("same", "career")
    with pytest.raises(ValueError, match="duplicate slot IDs"):
        QuickReadRequest(
            question="test",
            target_id="chart",
            requested_slots=(slot, slot),
        )


def test_out_of_scope_evidence_is_rejected():
    _, request, manifest, items = _fixture_objects()
    out_of_scope = QuickReadEvidenceItem(
        evidence_id="EV-OUTSIDE",
        slot_id="not-requested",
        lane="MODEL_SUPPLEMENT",
        claim="supplement",
        epistemic_label="MODEL_SUPPLEMENT",
        uncertainty="unverified",
    )
    with pytest.raises(ValueError, match="outside requested scope"):
        build_quickread_payload(
            request,
            manifest,
            (*items, out_of_scope),
            chart_context={"normalized_chart": {"synthetic": True}},
        )


def test_manifest_scope_mismatch_is_rejected():
    _, request, manifest, items = _fixture_objects()
    wrong_slot = _slot("career_natal", "relationship")
    wrong_record = replace(manifest.records[0], slot=wrong_slot)
    wrong_manifest = replace(manifest, records=(wrong_record, manifest.records[1]))
    with pytest.raises(ValueError, match="scope mismatch"):
        build_quickread_payload(
            request,
            wrong_manifest,
            items,
            chart_context={"normalized_chart": {"synthetic": True}},
        )


def test_model_supplement_validator_accepts_only_requested_model_items():
    _, request, _, items = _fixture_objects()
    validated = validate_model_supplements(request, (items[2],))
    assert validated == (items[2],)
    with pytest.raises(ValueError, match="accepts MODEL_SUPPLEMENT"):
        validate_model_supplements(request, (items[0],))


def test_payload_is_deterministic_for_same_inputs():
    _, request, manifest, items = _fixture_objects()
    context = {"normalized_chart": {"z": 1, "a": 2}}
    first = build_quickread_payload(request, manifest, items, chart_context=context)
    second = build_quickread_payload(request, manifest, items, chart_context=context)
    assert json.dumps(first, ensure_ascii=False, sort_keys=True) == json.dumps(
        second, ensure_ascii=False, sort_keys=True
    )


def test_duplicate_evidence_ids_are_rejected():
    _, request, manifest, items = _fixture_objects()
    duplicate = replace(items[1], evidence_id=items[0].evidence_id)
    with pytest.raises(ValueError, match="duplicate evidence_id"):
        build_quickread_payload(
            request,
            manifest,
            (items[0], duplicate, items[2]),
            chart_context={"normalized_chart": {"synthetic": True}},
        )
