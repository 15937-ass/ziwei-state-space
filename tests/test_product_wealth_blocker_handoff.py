from pathlib import Path

from src.product.wealth_blocker_handoff import load_wealth_blocker_handoff,validate_wealth_blocker_handoff

ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/"product/PL2P_WEALTH_BLOCKER_HANDOFF_v0.1.csv"

KNOWLEDGE={"W01-010","W01-018","W01-019","W01-033","W01-043","W01-059","W01-064","W01-065","W01-073","W01-074","W01-076","W01-077","W01-093","W01-099"}
UPSTREAM={"W01-027","W01-030","W01-034","W01-044","W01-094"}
HUMAN={"W01-016","W01-017","W01-022","W01-023","W01-035","W01-095","W01-096","W01-098"}
TEMPORAL={"W01-011","W01-012","W01-051","W01-052","W01-053","W01-054","W01-055","W01-063","W01-084","W01-085","W01-086","W01-087","W01-088","W01-089"}
EXPECTED=KNOWLEDGE|UPSTREAM|HUMAN|TEMPORAL

def test_pl2p_handoff_exactly_partitions_remaining_41():
    rows=load_wealth_blocker_handoff(CSV)
    counts=validate_wealth_blocker_handoff(rows,expected_pending_rule_ids=EXPECTED)
    assert len(rows)==41
    assert counts=={
        "HUMAN_REVIEW_REQUIRED":8,
        "KNOWLEDGE_REVIEW_HANDOFF":14,
        "PL3_TEMPORAL_HANDOFF":14,
        "UPSTREAM_DEPENDENCY_HOLD":5,
    }

def test_human_review_set_is_exact():
    rows=load_wealth_blocker_handoff(CSV)
    assert {r.projection_rule_id for r in rows if r.handoff_class=="HUMAN_REVIEW_REQUIRED"}==HUMAN

def test_no_unowned_pl2_ready_backlog_remains():
    rows=load_wealth_blocker_handoff(CSV)
    assert all(r.owner!="PRODUCT_PL2_READY" for r in rows)
