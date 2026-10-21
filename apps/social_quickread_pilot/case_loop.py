"""De-identified case journal and tiny evaluation loop for Social QuickRead.

This module is intentionally sidecar-only.  It may collect PI-approved public
renders and pan-owner feedback, but it must never promote feedback into
Knowledge canonical truth or mutate Product inference semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from statistics import mean
from typing import Any, Iterable, Mapping


class FeedbackLabel(str, Enum):
    HIT = "HIT"
    PARTIAL = "PARTIAL"
    CONTRADICT = "CONTRADICT"
    NEW_FACT = "NEW_FACT"
    STYLE_ONLY = "STYLE_ONLY"
    UNCLEAR = "UNCLEAR"


@dataclass(frozen=True)
class FeedbackRecord:
    """Reality feedback for one de-identified pilot case."""

    text: str
    label: FeedbackLabel
    target_claim_ids: tuple[str, ...] = ()
    source: str = "PAN_OWNER_FEEDBACK"

    def validate(self) -> None:
        if not self.text.strip():
            raise ValueError("FeedbackRecord.text is required")
        if not self.source.strip():
            raise ValueError("FeedbackRecord.source is required")
        if len(set(self.target_claim_ids)) != len(self.target_claim_ids):
            raise ValueError("FeedbackRecord.target_claim_ids must be unique")


@dataclass(frozen=True)
class PIReview:
    """PI quality review.  Scores are deliberately tiny and interpretable."""

    factual_score: int
    style_score: int
    redundancy_count: int = 0
    hallucination_count: int = 0
    useful_followup: bool = False
    preferred_example: bool = False
    note: str = ""

    def validate(self) -> None:
        if not 1 <= self.factual_score <= 5:
            raise ValueError("PIReview.factual_score must be between 1 and 5")
        if not 1 <= self.style_score <= 5:
            raise ValueError("PIReview.style_score must be between 1 and 5")
        if self.redundancy_count < 0:
            raise ValueError("PIReview.redundancy_count cannot be negative")
        if self.hallucination_count < 0:
            raise ValueError("PIReview.hallucination_count cannot be negative")
        if self.preferred_example and self.hallucination_count:
            raise ValueError("preferred examples cannot contain hallucinations")


@dataclass(frozen=True)
class CaseRecord:
    """A minimal, de-identified Social QuickRead case.

    Deliberately omitted:
    - social account / username
    - post URL
    - raw chart image
    - exact birth timestamp
    - private-message content unrelated to evaluation
    """

    case_id: str
    subject_key: str
    scope: str
    question_summary: str
    public_text: str
    used_claim_ids: tuple[str, ...]
    origin_counts: tuple[tuple[str, int], ...] = ()
    coverage_gaps: tuple[str, ...] = ()
    temporal_features: Mapping[str, Any] | None = None
    feedback: tuple[FeedbackRecord, ...] = ()
    pi_review: PIReview | None = None
    source_platform: str = "xiaohongshu"
    privacy_level: str = "DEIDENTIFIED"

    def validate(self) -> None:
        if not self.case_id.strip():
            raise ValueError("CaseRecord.case_id is required")
        if not self.subject_key.strip():
            raise ValueError("CaseRecord.subject_key is required")
        if not self.scope.strip():
            raise ValueError("CaseRecord.scope is required")
        if not self.question_summary.strip():
            raise ValueError("CaseRecord.question_summary is required")
        if not self.public_text.strip():
            raise ValueError("CaseRecord.public_text is required")
        if self.temporal_features is not None:
            mode = str(self.temporal_features.get("mode", ""))
            if mode and mode != "social_quickread_temporal_4h_v0.1":
                raise ValueError("CaseRecord.temporal_features has unsupported mode")
        if self.privacy_level != "DEIDENTIFIED":
            raise ValueError("CaseRecord must stay DEIDENTIFIED")
        if len(set(self.used_claim_ids)) != len(self.used_claim_ids):
            raise ValueError("CaseRecord.used_claim_ids must be unique")
        if len({name for name, _ in self.origin_counts}) != len(self.origin_counts):
            raise ValueError("CaseRecord.origin_counts keys must be unique")
        if any(count < 0 for _, count in self.origin_counts):
            raise ValueError("CaseRecord.origin_counts cannot be negative")
        for item in self.feedback:
            item.validate()
        if self.pi_review is not None:
            self.pi_review.validate()

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        row = asdict(self)
        row["origin_counts"] = dict(self.origin_counts)
        row["feedback"] = [
            {
                **asdict(item),
                "label": item.label.value,
            }
            for item in self.feedback
        ]
        return row


@dataclass(frozen=True)
class PreferredExample:
    """Style-only few-shot example promoted by the PI."""

    example_id: str
    source_case_id: str
    scope: str
    prompt_pattern: str
    preferred_response: str
    style_only: bool = True

    def validate(self) -> None:
        if not self.example_id.strip():
            raise ValueError("PreferredExample.example_id is required")
        if not self.source_case_id.strip():
            raise ValueError("PreferredExample.source_case_id is required")
        if not self.scope.strip():
            raise ValueError("PreferredExample.scope is required")
        if not self.prompt_pattern.strip():
            raise ValueError("PreferredExample.prompt_pattern is required")
        if not self.preferred_response.strip():
            raise ValueError("PreferredExample.preferred_response is required")
        if self.style_only is not True:
            raise ValueError("PreferredExample must stay style_only")


def build_case_record(
    *,
    bundle: Mapping[str, Any],
    case_id: str,
    subject_key: str,
    scope: str,
    question_summary: str,
    feedback: Iterable[FeedbackRecord] = (),
    pi_review: PIReview | None = None,
    temporal_features: Mapping[str, Any] | None = None,
) -> CaseRecord:
    """Build a case from one finalized dual-output bundle.

    A blocked public render is not training/eval material and is rejected.
    """

    public = bundle.get("public", {})
    if public.get("ready") is not True or not str(public.get("text", "")).strip():
        raise ValueError("case capture requires a public-ready render")

    pi = bundle.get("pi", {})
    sentences = tuple(pi.get("sentences", ()))
    used_claim_ids = tuple(
        dict.fromkeys(
            claim_id
            for sentence in sentences
            for claim_id in sentence.get("claim_ids", ())
        )
    )

    summary = pi.get("summary", {})
    origin_counts = tuple(
        sorted(
            (str(name), int(count))
            for name, count in dict(summary.get("origin_counts", {})).items()
        )
    )
    coverage_gaps = tuple(
        str(item.get("topic") or item.get("request") or item.get("reason") or "").strip()
        for item in pi.get("coverage_gaps", ())
        if str(item.get("topic") or item.get("request") or item.get("reason") or "").strip()
    )

    record = CaseRecord(
        case_id=case_id,
        subject_key=subject_key,
        scope=scope,
        question_summary=question_summary,
        public_text=str(public["text"]).strip(),
        used_claim_ids=used_claim_ids,
        origin_counts=origin_counts,
        coverage_gaps=coverage_gaps,
        temporal_features=temporal_features,
        feedback=tuple(feedback),
        pi_review=pi_review,
    )
    record.validate()
    return record


def promote_preferred_example(
    case: CaseRecord,
    *,
    example_id: str,
    prompt_pattern: str,
) -> PreferredExample:
    """Promote only PI-approved, clean cases into the style few-shot bank."""

    case.validate()
    review = case.pi_review
    if review is None or not review.preferred_example:
        raise ValueError("case is not PI-approved as a preferred example")
    if review.factual_score < 4 or review.style_score < 4:
        raise ValueError("preferred example requires factual/style score >= 4")
    if review.hallucination_count:
        raise ValueError("preferred example cannot contain hallucinations")

    example = PreferredExample(
        example_id=example_id,
        source_case_id=case.case_id,
        scope=case.scope,
        prompt_pattern=prompt_pattern,
        preferred_response=case.public_text,
    )
    example.validate()
    return example


def summarize_cases(cases: Iterable[CaseRecord]) -> dict[str, Any]:
    """Return a tiny, dependency-free evaluation summary."""

    rows = tuple(cases)
    for row in rows:
        row.validate()

    scope_counts: dict[str, int] = {}
    feedback_counts: dict[str, int] = {}
    origin_counts: dict[str, int] = {}
    factual_scores: list[int] = []
    style_scores: list[int] = []
    preferred_examples = 0
    coverage_gap_cases = 0
    contradiction_cases = 0

    for row in rows:
        scope_counts[row.scope] = scope_counts.get(row.scope, 0) + 1
        if row.coverage_gaps:
            coverage_gap_cases += 1
        for name, count in row.origin_counts:
            origin_counts[name] = origin_counts.get(name, 0) + count
        for item in row.feedback:
            key = item.label.value
            feedback_counts[key] = feedback_counts.get(key, 0) + 1
        if any(item.label == FeedbackLabel.CONTRADICT for item in row.feedback):
            contradiction_cases += 1
        if row.pi_review is not None:
            factual_scores.append(row.pi_review.factual_score)
            style_scores.append(row.pi_review.style_score)
            if row.pi_review.preferred_example:
                preferred_examples += 1

    return {
        "total_cases": len(rows),
        "scope_counts": dict(sorted(scope_counts.items())),
        "feedback_counts": dict(sorted(feedback_counts.items())),
        "origin_counts": dict(sorted(origin_counts.items())),
        "coverage_gap_cases": coverage_gap_cases,
        "contradiction_cases": contradiction_cases,
        "preferred_example_cases": preferred_examples,
        "mean_factual_score": (
            round(mean(factual_scores), 3) if factual_scores else None
        ),
        "mean_style_score": (
            round(mean(style_scores), 3) if style_scores else None
        ),
    }
