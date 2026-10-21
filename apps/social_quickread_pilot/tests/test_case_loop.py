from apps.social_quickread_pilot.case_loop import (
    FeedbackLabel,
    FeedbackRecord,
    PIReview,
    build_case_record,
    promote_preferred_example,
    summarize_cases,
)


def _bundle(*, ready=True):
    return {
        "public": {
            "ready": ready,
            "text": "整体看人做事挺果断，26年外部机会会明显起来。" if ready else "",
        },
        "pi": {
            "summary": {
                "origin_counts": {
                    "SOURCE_BACKED_FALLBACK": 1,
                    "RUNTIME_TEMPORAL": 1,
                }
            },
            "sentences": [
                {"claim_ids": ["p1"]},
                {"claim_ids": ["y1"]},
            ],
            "coverage_gaps": [
                {
                    "request": "未来老婆怎么样",
                    "topic": "relationship",
                    "reason": "runtime coverage insufficient",
                }
            ],
        },
    }


def test_build_case_record_is_deidentified_and_keeps_eval_fields():
    case = build_case_record(
        bundle=_bundle(),
        case_id="XHS-001",
        subject_key="QR-001",
        scope="full",
        question_summary="整体简批",
        feedback=(
            FeedbackRecord(
                "事业方向说得比较准",
                FeedbackLabel.HIT,
                ("p1",),
            ),
        ),
        pi_review=PIReview(
            factual_score=4,
            style_score=5,
            useful_followup=True,
            preferred_example=True,
        ),
    )

    row = case.to_dict()
    assert row["privacy_level"] == "DEIDENTIFIED"
    assert row["used_claim_ids"] == ("p1", "y1")
    assert row["origin_counts"]["SOURCE_BACKED_FALLBACK"] == 1
    assert row["feedback"][0]["label"] == "HIT"
    assert row["coverage_gaps"] == ("relationship",)


def test_blocked_public_render_cannot_enter_case_bank():
    import pytest

    with pytest.raises(ValueError, match="public-ready"):
        build_case_record(
            bundle=_bundle(ready=False),
            case_id="XHS-002",
            subject_key="QR-002",
            scope="relationship",
            question_summary="感情简批",
        )


def test_preferred_examples_need_explicit_pi_approval():
    import pytest

    case = build_case_record(
        bundle=_bundle(),
        case_id="XHS-003",
        subject_key="QR-003",
        scope="relationship",
        question_summary="婚姻怎么样",
        pi_review=PIReview(
            factual_score=5,
            style_score=5,
            preferred_example=False,
        ),
    )
    with pytest.raises(ValueError, match="not PI-approved"):
        promote_preferred_example(
            case,
            example_id="EX-003",
            prompt_pattern="relationship.marriage",
        )


def test_preferred_example_is_style_only():
    case = build_case_record(
        bundle=_bundle(),
        case_id="XHS-004",
        subject_key="QR-004",
        scope="relationship",
        question_summary="未来配偶",
        pi_review=PIReview(
            factual_score=5,
            style_score=5,
            hallucination_count=0,
            preferred_example=True,
        ),
    )

    example = promote_preferred_example(
        case,
        example_id="EX-004",
        prompt_pattern="relationship.partner_profile",
    )
    assert example.style_only is True
    assert example.preferred_response == case.public_text


def test_summary_counts_feedback_gaps_origins_and_scores():
    first = build_case_record(
        bundle=_bundle(),
        case_id="XHS-005",
        subject_key="QR-005",
        scope="relationship",
        question_summary="配偶画像",
        feedback=(
            FeedbackRecord("性格说准了", FeedbackLabel.HIT, ("p1",)),
            FeedbackRecord("实际谈过三段", FeedbackLabel.NEW_FACT),
        ),
        pi_review=PIReview(
            factual_score=5,
            style_score=4,
            preferred_example=True,
        ),
    )
    second = build_case_record(
        bundle=_bundle(),
        case_id="XHS-006",
        subject_key="QR-006",
        scope="career",
        question_summary="适合去哪发展",
        feedback=(
            FeedbackRecord("这一点不符合", FeedbackLabel.CONTRADICT, ("y1",)),
        ),
        pi_review=PIReview(
            factual_score=3,
            style_score=5,
        ),
    )

    summary = summarize_cases((first, second))
    assert summary["total_cases"] == 2
    assert summary["scope_counts"] == {"career": 1, "relationship": 1}
    assert summary["feedback_counts"]["HIT"] == 1
    assert summary["feedback_counts"]["CONTRADICT"] == 1
    assert summary["contradiction_cases"] == 1
    assert summary["coverage_gap_cases"] == 2
    assert summary["preferred_example_cases"] == 1
    assert summary["mean_factual_score"] == 4
    assert summary["mean_style_score"] == 4.5


def test_case_record_can_store_temporal_4h_features():
    temporal = {
        "mode": "social_quickread_temporal_4h_v0.1",
        "schema_version": "0.1",
        "decade_stem": "丁",
        "year_stem": "丙",
        "interactions": [
            {
                "type": "SAME_STAR_CROSS_MUTAGEN",
                "star": "天机",
                "palace": "官禄",
                "layers": ["DECADE", "YEAR"],
                "mutagens": ["科", "权"],
            }
        ],
    }
    case = build_case_record(
        bundle=_bundle(),
        case_id="XHS-007",
        subject_key="QR-007",
        scope="specific_year",
        question_summary="26年怎么样",
        temporal_features=temporal,
    )
    row = case.to_dict()
    assert row["temporal_features"]["decade_stem"] == "丁"
    assert row["temporal_features"]["year_stem"] == "丙"
