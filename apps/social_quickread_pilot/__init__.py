"""Lightweight read-only Social QuickRead sidecar.

This package consumes validated QuickReadClaim objects and never mutates
Knowledge/Product canonical assets.
"""

from .case_loop import (
    CaseRecord,
    FeedbackLabel,
    FeedbackRecord,
    PIReview,
    PreferredExample,
    build_case_record,
    promote_preferred_example,
    summarize_cases,
)
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
    "CaseRecord",
    "FeedbackLabel",
    "FeedbackRecord",
    "PIReview",
    "PreferredExample",
    "build_case_record",
    "promote_preferred_example",
    "summarize_cases",
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
