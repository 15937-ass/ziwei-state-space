"""Lightweight read-only Social QuickRead sidecar.

This package consumes validated QuickReadClaim objects and never mutates
Knowledge/Product canonical assets.
"""

from .provenance import (
    ClaimOrigin,
    ClaimTrace,
    CoverageGap,
    ObservationRecord,
    RenderedSentenceTrace,
    build_dual_output,
)
from .sidecar import PilotRequest, PreparedPilot, prepare_pilot, finalize_pilot

__all__ = [
    "ClaimOrigin",
    "ClaimTrace",
    "CoverageGap",
    "ObservationRecord",
    "RenderedSentenceTrace",
    "build_dual_output",
    "PilotRequest",
    "PreparedPilot",
    "prepare_pilot",
    "finalize_pilot",
]
