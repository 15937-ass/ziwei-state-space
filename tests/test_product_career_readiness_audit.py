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


def test_current_career_corpus_is_source_verified_but_preclosure():
    summary = audit_career_projection_batches(BATCHES, closure_complete=False)
    assert summary.batch_count == 8
    assert summary.total_rows == 800
    assert summary.source_verified_rows == 800
    assert summary.case_support_only_rows == 14
    assert summary.history_feedback_rows == 28
    assert not summary.ready_for_executable_normalization
    assert "CAREER_CORPUS_CLOSURE_PENDING" in summary.blockers


def test_ca04_to_ca08_column_order_drift_is_detected_not_repaired():
    summary = audit_career_projection_batches(BATCHES, closure_complete=False)
    assert summary.schema_drift_rows == 500
    assert SCHEMA_DRIFT_TIME_CONDITION_SWAP in summary.blockers

    clean = summary.batches[:3]
    drifted = summary.batches[3:]
    assert all(item.schema_drift_rows == 0 for item in clean)
    assert all(item.schema_drift_rows == 100 for item in drifted)
    assert all(
        item.schema_drift_type == SCHEMA_DRIFT_TIME_CONDITION_SWAP
        for item in drifted
    )


def test_closure_flag_alone_cannot_override_schema_drift():
    summary = audit_career_projection_batches(BATCHES, closure_complete=True)
    assert not summary.ready_for_executable_normalization
    assert summary.blockers == (SCHEMA_DRIFT_TIME_CONDITION_SWAP,)
