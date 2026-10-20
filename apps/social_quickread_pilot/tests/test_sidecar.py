from apps.social_quickread_pilot.provenance import (
    ClaimOrigin,
    ClaimTrace,
    CoverageGap,
    ObservationRecord,
    RenderedSentenceTrace,
    build_dual_output,
)
from apps.social_quickread_pilot.sidecar import PilotRequest, prepare_pilot
from src.product.social_quickread import (
    AssertionMode,
    EvidenceNamespace,
    QuickReadClaim,
    QuickReadEvidenceRef,
    QuickReadTopic,
)


def _claim(claim_id: str, proposition: str, *, temporal: bool = False):
    namespace = EvidenceNamespace.TEMPORAL if temporal else EvidenceNamespace.CANONICAL
    return QuickReadClaim(
        claim_id=claim_id,
        topic=QuickReadTopic.SPECIFIC_YEAR if temporal else QuickReadTopic.PERSONALITY,
        proposition=proposition,
        semantic_group=claim_id,
        assertion_mode=AssertionMode.TENDENCY if temporal else AssertionMode.DIRECT_TENDENCY,
        evidence_refs=(
            QuickReadEvidenceRef(
                namespace=namespace,
                rule_id=f"ZZ-{claim_id}",
                source_id="SRC-ZZ",
                source_location="p.1",
                review_status="REVIEWED",
            ),
        ),
        target_period="2026" if temporal else "",
    )


def test_dual_output_marks_runtime_semantics_and_llm_wording():
    claims = (
        _claim("p1", "做事果断"),
        _claim("y1", "2026年外部机会增加", temporal=True),
    )
    prepared = prepare_pilot(
        PilotRequest(
            subject_key="QR-001",
            request_text="整体简批",
            knowledge_version="kb-test",
            claims=claims,
            target_chars_min=80,
            target_chars_max=220,
        )
    )
    bundle = build_dual_output(
        package=prepared.package,
        sentences=(
            RenderedSentenceTrace("整体看人做事挺果断。", ("p1",)),
            RenderedSentenceTrace("26年外部机会会明显起来。", ("y1",)),
        ),
        claim_traces=(
            ClaimTrace("p1", ClaimOrigin.RUNTIME_CANONICAL),
            ClaimTrace("y1", ClaimOrigin.RUNTIME_TEMPORAL),
        ),
    )
    assert bundle["public"]["ready"] is True
    assert "果断" in bundle["public"]["text"]
    assert bundle["pi"]["summary"]["origin_counts"]["RUNTIME_CANONICAL"] == 1
    assert bundle["pi"]["summary"]["origin_counts"]["RUNTIME_TEMPORAL"] == 1
    assert bundle["pi"]["sentences"][0]["language_origin"] == "LLM_VERBALIZATION"


def test_llm_added_semantics_blocks_public_output_but_remains_visible_to_pi():
    claim = _claim("p1", "做事果断")
    prepared = prepare_pilot(
        PilotRequest(
            subject_key="QR-002",
            request_text="性格简批",
            knowledge_version="kb-test",
            claims=(claim,),
            target_chars_min=80,
            target_chars_max=220,
        )
    )
    bundle = build_dual_output(
        package=prepared.package,
        sentences=(
            RenderedSentenceTrace(
                "整体看人做事果断，而且长得很高。",
                ("p1",),
                llm_added_semantics=("长得很高",),
            ),
        ),
    )
    assert bundle["public"]["ready"] is False
    assert bundle["public"]["text"] == ""
    assert bundle["pi"]["summary"]["unsupported_llm_additions"] == 1
    assert bundle["pi"]["unsupported_llm_additions"][0]["added_semantics"] == ["长得很高"]


def test_source_fallback_gap_and_observation_are_separate():
    claim = _claim("p1", "做事果断")
    prepared = prepare_pilot(
        PilotRequest(
            subject_key="QR-003",
            request_text="整体简批",
            knowledge_version="kb-test",
            claims=(claim,),
            target_chars_min=80,
            target_chars_max=220,
        )
    )
    bundle = build_dual_output(
        package=prepared.package,
        sentences=(RenderedSentenceTrace("整体看人做事挺果断。", ("p1",)),),
        claim_traces=(
            ClaimTrace("p1", ClaimOrigin.SOURCE_BACKED_FALLBACK, note="manual source retrieval"),
        ),
        coverage_gaps=(
            CoverageGap("未来老婆怎么样", "relationship", "runtime coverage insufficient"),
        ),
        observations=(
            ObservationRecord("事业编，专业技术岗"),
        ),
    )
    assert bundle["pi"]["summary"]["origin_counts"]["SOURCE_BACKED_FALLBACK"] == 1
    assert bundle["pi"]["summary"]["coverage_gap_count"] == 1
    assert bundle["pi"]["observations"][0]["role"] == "OBSERVATION_ONLY_NOT_CANONICAL_TRUTH"
