"""Minimal orchestration layer for manual Social QuickRead pilot.

No Knowledge/Product core file is mutated.  The sidecar only consumes validated
QuickReadClaim objects produced upstream, applies the existing QuickRead contract,
and emits a public render plus a PI provenance audit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from src.product.social_quickread import (
    QuickReadClaim,
    QuickReadPackage,
    build_pilot_package,
)

from .provenance import (
    ClaimTrace,
    CoverageGap,
    ObservationRecord,
    RenderedSentenceTrace,
    build_dual_output,
)


@dataclass(frozen=True)
class PilotRequest:
    subject_key: str
    request_text: str
    knowledge_version: str
    claims: tuple[QuickReadClaim, ...]
    target_chars_min: int = 120
    target_chars_max: int = 220

    def validate(self) -> None:
        if not self.subject_key.strip():
            raise ValueError("PilotRequest.subject_key is required")
        if not self.request_text.strip():
            raise ValueError("PilotRequest.request_text is required")
        if not self.knowledge_version.strip():
            raise ValueError("PilotRequest.knowledge_version is required")
        if not self.claims:
            raise ValueError("PilotRequest.claims is required")


@dataclass(frozen=True)
class PreparedPilot:
    subject_key: str
    package: QuickReadPackage
    verbalizer_payload: dict


def prepare_pilot(request: PilotRequest) -> PreparedPilot:
    """Prepare the narrow payload sent to the language model."""

    request.validate()
    package = build_pilot_package(
        claims=request.claims,
        knowledge_version=request.knowledge_version,
        request_text=request.request_text,
        target_chars_min=request.target_chars_min,
        target_chars_max=request.target_chars_max,
    )
    return PreparedPilot(
        subject_key=request.subject_key,
        package=package,
        verbalizer_payload=package.verbalizer_payload(),
    )


def finalize_pilot(
    prepared: PreparedPilot,
    *,
    sentences: Iterable[RenderedSentenceTrace],
    claim_traces: Iterable[ClaimTrace] = (),
    coverage_gaps: Iterable[CoverageGap] = (),
    observations: Iterable[ObservationRecord] = (),
) -> dict:
    """Finalize public + PI outputs after LLM rendering/self-audit."""

    bundle = build_dual_output(
        package=prepared.package,
        sentences=sentences,
        claim_traces=claim_traces,
        coverage_gaps=coverage_gaps,
        observations=observations,
    )
    bundle["subject_key"] = prepared.subject_key
    bundle["mode"] = "social_quickread_sidecar_v0.1"
    return bundle
