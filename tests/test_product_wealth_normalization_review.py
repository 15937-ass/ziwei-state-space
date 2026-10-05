from pathlib import Path

from src.product.wealth_normalization_review import (
    load_normalization_review,
    validate_normalization_review,
)

ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/"product/PL2O_WEALTH_NORMALIZATION_REVIEW_v0.1.csv"

EXPECTED={
    "W01-010","W01-018","W01-019","W01-033","W01-059",
    "W01-064","W01-065","W01-067","W01-071","W01-073",
    "W01-074","W01-076","W01-077","W01-093","W01-099",
}


def test_pl2o_covers_exact_normalization_backlog():
    rows=load_normalization_review(CSV)
    counts=validate_normalization_review(rows,expected_rule_ids=EXPECTED)
    assert counts=={
        "EXECUTABLE_NORMALIZATION_READY":2,
        "OPEN_SET_UNRESOLVED":1,
        "SOURCE_CLARIFIED_RELATION_PENDING":9,
        "SOURCE_CLARIFIED_STRUCTURE_PENDING":1,
        "SOURCE_SPAN_RECHECK":1,
        "SOURCE_SPLIT_REQUIRED":1,
    }


def test_only_067_and_071_are_ready():
    rows=load_normalization_review(CSV)
    ready={r.projection_rule_id for r in rows if r.review_disposition=="EXECUTABLE_NORMALIZATION_READY"}
    assert ready=={"W01-067","W01-071"}


def test_no_human_gate_is_implicitly_approved():
    rows=load_normalization_review(CSV)
    assert all(r.human_gate_required=="NO" for r in rows)


def test_relation_terms_remain_fail_closed():
    rows=load_normalization_review(CSV)
    pending={r.projection_rule_id for r in rows if r.review_disposition=="SOURCE_CLARIFIED_RELATION_PENDING"}
    assert {"W01-010","W01-018","W01-059","W01-064","W01-065","W01-073","W01-074","W01-093","W01-099"}==pending
