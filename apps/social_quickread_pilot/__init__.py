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
from .temporal_4h import (
    HEAVENLY_STEMS,
    InteractionType,
    Mutagen,
    Temporal4HSnapshot,
    TemporalInputSource,
    TemporalInteraction,
    TemporalLayer,
    TransformationMark,
    TEN_STEM_TRANSFORMATIONS,
    build_temporal_4h_series,
    build_temporal_4h_snapshot,
    detect_interactions,
    normalize_natal_marks,
    quickread_temporal_payload,
    stem_for_gregorian_year,
    transformations_for_stem,
)

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
    "HEAVENLY_STEMS",
    "InteractionType",
    "Mutagen",
    "Temporal4HSnapshot",
    "TemporalInputSource",
    "TemporalInteraction",
    "TemporalLayer",
    "TransformationMark",
    "TEN_STEM_TRANSFORMATIONS",
    "build_temporal_4h_series",
    "build_temporal_4h_snapshot",
    "detect_interactions",
    "normalize_natal_marks",
    "quickread_temporal_payload",
    "stem_for_gregorian_year",
    "transformations_for_stem",
]
