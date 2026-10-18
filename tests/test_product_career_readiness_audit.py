from pathlib import Path

from src.product.career_readiness_audit import (
    SCHEMA_DRIFT_TIME_CONDITION_SWAP,
    audit_career_projection_batches,
)

ROOT = Path(__file__).resolve().parents[1]
BATCHES = tuple(
    ROOT / f"validation/wp05/CA{i:02d}_career_projection_review_{(i-1)*100+1:03d}_{i*100:03d}.csv"
    for i in range(1, 9)
)
SCHEMA_REPAIR_MARKER = ROOT / "validation/wp05/CAREER_CA04_CA08_SCHEMA_REPAIR.md"


def test_current_career_corpus_is_source_verified_but_preclosure():
    summary = audit_career_projection_batches(BATCHES, closure_complete=False)
    assert summary.batch_count == 8
    assert summary.total_rows == 800
    assert summary.source_verified_rows == 800
    assert summary.case_support_only_rows == 14
    assert summary.history_feedback_rows == 28
    assert not summary.ready_for_executable_normalization
    assert "CAREER_CORPUS_CLOSURE_PENDING" in summary.blockers


def test_career_schema_audit_matches_canonical_migration_state():
    summary = audit_career_projection_batches(BATCHES, closure_complete=False)
    clean = summary.batches[:3]
    tail = summary.batches[3:]
    assert all(item.schema_drift_rows == 0 for item in clean)

    if SCHEMA_REPAIR_MARKER.exists():
        # The Knowledge lane has landed the source-preserving schema repair.
        assert summary.schema_drift_rows == 0
        assert all(item.schema_drift_rows == 0 for item in tail)
        assert all(item.schema_drift_type is None for item in summary.batches)
        assert summary.blockers == ("CAREER_CORPUS_CLOSURE_PENDING",)
    else:
        # Before the canonical migration, keep the original blocker visible.
        assert summary.schema_drift_rows == 500
        assert SCHEMA_DRIFT_TIME_CONDITION_SWAP in summary.blockers
        assert all(item.schema_drift_rows == 100 for item in tail)
        assert all(
            item.schema_drift_type == SCHEMA_DRIFT_TIME_CONDITION_SWAP
            for item in tail
        )


def test_closure_flag_cannot_override_unrepaired_schema_drift():
    summary = audit_career_projection_batches(BATCHES, closure_complete=True)
    if SCHEMA_REPAIR_MARKER.exists():
        assert summary.schema_drift_rows == 0
        assert summary.ready_for_executable_normalization
        assert summary.blockers == ()
    else:
        assert not summary.ready_for_executable_normalization
        assert summary.blockers == (SCHEMA_DRIFT_TIME_CONDITION_SWAP,)


def test_canonical_ca01_to_ca09_corpus_is_schema_clean_and_ready_for_normalization_review():
    full_corpus = BATCHES + (
        ROOT / "validation/wp05/CA09_career_projection_review_801_888.csv",
    )
    summary = audit_career_projection_batches(full_corpus, closure_complete=True)

    assert summary.batch_count == 9
    assert summary.total_rows == 888
    assert summary.source_verified_rows == 888
    assert summary.case_support_only_rows == 19
    assert summary.history_feedback_rows == 37
    assert summary.schema_drift_rows == 0
    assert summary.ready_for_executable_normalization
    assert summary.blockers == ()
