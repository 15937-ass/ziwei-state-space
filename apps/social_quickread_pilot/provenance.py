"""PI-facing provenance audit for the Social QuickRead sidecar.

The public text may be natural-language LLM verbalization, but every factual
semantic unit must map to validated QuickReadClaim evidence.  This module keeps
"what was inferred" separate from "how the model worded it".
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping

from src.product.social_quickread import (
    QuickReadPackage,
    QuickReadRenderAudit,
    QuickReadSentenceAudit,
)


class ClaimOrigin(str, Enum):
    """Semantic origin of one validated claim."""

    RUNTIME_CANONICAL = "RUNTIME_CANONICAL"
    RUNTIME_TEMPORAL = "RUNTIME_TEMPORAL"
    SOURCE_BACKED_FALLBACK = "SOURCE_BACKED_FALLBACK"


@dataclass(frozen=True)
class ClaimTrace:
    claim_id: str
    origin: ClaimOrigin
    runtime_run_id: str = ""
    note: str = ""

    def validate(self) -> None:
        if not self.claim_id.strip():
            raise ValueError("ClaimTrace.claim_id is required")


@dataclass(frozen=True)
class CoverageGap:
    request: str
    topic: str
    reason: str

    def validate(self) -> None:
        if not self.request.strip():
            raise ValueError("CoverageGap.request is required")
        if not self.topic.strip():
            raise ValueError("CoverageGap.topic is required")
        if not self.reason.strip():
            raise ValueError("CoverageGap.reason is required")


@dataclass(frozen=True)
class ObservationRecord:
    """Reality feedback supplied by the chart owner/user; never canonical truth."""

    text: str
    source: str = "PAN_OWNER_FEEDBACK"

    def validate(self) -> None:
        if not self.text.strip():
            raise ValueError("ObservationRecord.text is required")
        if not self.source.strip():
            raise ValueError("ObservationRecord.source is required")


@dataclass(frozen=True)
class RenderedSentenceTrace:
    """One LLM-rendered sentence plus the semantic claims it verbalizes.

    llm_added_semantics must stay empty for public-ready output.  It records
    factual/interpretive content that the model introduced beyond mapped claims.
    Pure wording changes are *not* listed here.
    """

    text: str
    claim_ids: tuple[str, ...]
    llm_added_semantics: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.text.strip():
            raise ValueError("RenderedSentenceTrace.text is required")
        if not self.claim_ids:
            raise ValueError("RenderedSentenceTrace.claim_ids is required")
        if len(set(self.claim_ids)) != len(self.claim_ids):
            raise ValueError("RenderedSentenceTrace.claim_ids must be unique")


def _default_origin(claim) -> ClaimOrigin:
    namespaces = {ref.namespace.value for ref in claim.evidence_refs}
    if "TEMPORAL" in namespaces:
        return ClaimOrigin.RUNTIME_TEMPORAL
    return ClaimOrigin.RUNTIME_CANONICAL


def build_dual_output(
    *,
    package: QuickReadPackage,
    sentences: Iterable[RenderedSentenceTrace],
    claim_traces: Iterable[ClaimTrace] = (),
    coverage_gaps: Iterable[CoverageGap] = (),
    observations: Iterable[ObservationRecord] = (),
) -> dict[str, Any]:
    """Return public output + PI provenance output.

    Public output is fail-closed: any declared LLM semantic addition blocks the
    public render.  The PI audit remains available so the model-added content can
    be inspected and removed/regenerated.
    """

    package.validate()
    sentence_rows = tuple(sentences)
    if not sentence_rows:
        raise ValueError("at least one rendered sentence is required")
    for item in sentence_rows:
        item.validate()

    trace_rows = tuple(claim_traces)
    for item in trace_rows:
        item.validate()
    trace_by_id = {item.claim_id: item for item in trace_rows}
    if len(trace_by_id) != len(trace_rows):
        raise ValueError("ClaimTrace.claim_id values must be unique")

    selected = {claim.claim_id: claim for claim in package.selected_claims()}
    unknown_trace_ids = sorted(set(trace_by_id) - set(selected))
    if unknown_trace_ids:
        raise ValueError(
            "claim trace references unselected claim(s): " + ", ".join(unknown_trace_ids)
        )

    gap_rows = tuple(coverage_gaps)
    for item in gap_rows:
        item.validate()
    observation_rows = tuple(observations)
    for item in observation_rows:
        item.validate()

    render_audit = QuickReadRenderAudit(
        package=package,
        sentences=tuple(
            QuickReadSentenceAudit(item.text, item.claim_ids)
            for item in sentence_rows
        ),
    )
    # Structural audit remains mandatory even when a semantic addition is found.
    render_audit.validate()

    unsupported = [
        {
            "sentence": item.text,
            "added_semantics": list(item.llm_added_semantics),
        }
        for item in sentence_rows
        if item.llm_added_semantics
    ]

    sentence_audit = []
    used_claim_ids: set[str] = set()
    for item in sentence_rows:
        used_claim_ids.update(item.claim_ids)
        evidence = []
        origins = []
        for claim_id in item.claim_ids:
            claim = selected[claim_id]
            trace = trace_by_id.get(claim_id)
            origin = trace.origin if trace else _default_origin(claim)
            origins.append(origin.value)
            evidence.extend(
                {
                    "namespace": ref.namespace.value,
                    "rule_id": ref.rule_id,
                    "source_id": ref.source_id,
                    "source_location": ref.source_location,
                    "review_status": ref.review_status,
                }
                for ref in claim.evidence_refs
            )
        sentence_audit.append(
            {
                "text": item.text,
                "claim_ids": list(item.claim_ids),
                "semantic_origins": sorted(set(origins)),
                "language_origin": "LLM_VERBALIZATION",
                "llm_added_semantics": list(item.llm_added_semantics),
                "public_eligible": not item.llm_added_semantics,
                "evidence": evidence,
            }
        )

    origins_summary: dict[str, int] = {}
    for claim_id in sorted(used_claim_ids):
        claim = selected[claim_id]
        trace = trace_by_id.get(claim_id)
        origin = trace.origin if trace else _default_origin(claim)
        origins_summary[origin.value] = origins_summary.get(origin.value, 0) + 1

    public_ready = not unsupported
    public_text = render_audit.rendered_text() if public_ready else ""

    return {
        "public": {
            "ready": public_ready,
            "text": public_text,
            "blocked_reason": (
                None
                if public_ready
                else "LLM_ADDED_UNSUPPORTED_SEMANTICS"
            ),
        },
        "pi": {
            "summary": {
                "selected_claims": len(selected),
                "used_claims": len(used_claim_ids),
                "origin_counts": origins_summary,
                "llm_verbalized_sentences": len(sentence_rows),
                "unsupported_llm_additions": len(unsupported),
                "coverage_gap_count": len(gap_rows),
                "observation_count": len(observation_rows),
            },
            "sentences": sentence_audit,
            "unsupported_llm_additions": unsupported,
            "coverage_gaps": [
                {
                    "request": item.request,
                    "topic": item.topic,
                    "reason": item.reason,
                }
                for item in gap_rows
            ],
            "observations": [
                {
                    "text": item.text,
                    "source": item.source,
                    "role": "OBSERVATION_ONLY_NOT_CANONICAL_TRUTH",
                }
                for item in observation_rows
            ],
            "interpretation": {
                "semantic_truth": (
                    "Facts come from mapped validated claims. "
                    "SOURCE_BACKED_FALLBACK is source-traceable but not runtime-executable."
                ),
                "llm_role": (
                    "LLM_VERBALIZATION may change wording only. "
                    "Any new factual/interpretive semantic must be declared and blocks public output."
                ),
            },
        },
    }
