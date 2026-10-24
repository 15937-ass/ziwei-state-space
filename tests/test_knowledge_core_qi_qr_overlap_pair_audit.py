import json
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "core" / "qi-qr-overlap-audit"
CSV_PATH = BASE / "QI_QR_OVERLAP_PAIR_AUDIT_v0.1.csv"
JSON_PATH = BASE / "QI_QR_OVERLAP_PAIR_AUDIT_v0.1.json"
MD_PATH = BASE / "QI_QR_OVERLAP_PAIR_AUDIT_v0.1.md"
EVIDENCE_PATH = ROOT / "validation" / "knowledge" / "core" / "qi-qr-overlap-audit" / "QI_QR_OVERLAP_PAIR_AUDIT_EVIDENCE.md"

EXPECTED = [
    ("QI-01", "QI-14"),
    ("QI-03", "QI-04"),
    ("QI-02", "QI-15"),
    ("QI-08", "QI-06"),
    ("QI-04", "QI-16"),
    ("QI-08", "QI-16"),
    ("QI-17-CAND", "QI-18-CAND"),
    ("QR-01", "QR-04"),
]

def read_csv():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def test_exact_pair_coverage_and_order():
    rows = read_csv()
    pairs = [(r["left_id"], r["right_id"]) for r in rows]
    assert len(rows) == 8
    assert pairs == EXPECTED
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert [(p["left_id"], p["right_id"]) for p in data["pairs"]] == EXPECTED

def test_each_pair_has_evidence_and_counterexample_or_limit():
    for row in read_csv():
        assert row["source_rule_ids"].strip()
        assert row["source_locations"].strip()
        assert row["evidence_summary"].strip()
        assert row["distinction_hypothesis"].strip()
        assert row["counterexample_or_limit"].strip()
        assert row["unresolved_question"].strip()
        assert row["research_disposition"].strip()

def test_all_results_remain_research_only_and_unresolved():
    for row in read_csv():
        assert row["normalization_epistemic"] == "UNRESOLVED"
        assert row["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
        assert row["canonicalization_authorized"].lower() == "false"
        assert row["product_consumption_authorized"].lower() == "false"
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
    assert data["epistemic_policy"]["canonicalization_authorized"] is False
    assert data["epistemic_policy"]["product_consumption_authorized"] is False

def test_candidate_pair_is_not_promoted():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    p = next(p for p in data["pairs"] if p["left_id"] == "QI-17-CAND")
    assert p["left_id"] == "QI-17-CAND"
    assert p["right_id"] == "QI-18-CAND"
    assert p["canonicalization_authorized"] is False
    assert "candidate" in p["research_disposition"].lower()

def test_condition_scope_mismatch_is_preserved():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    p = next(p for p in data["pairs"] if p["pair_id"] == "OVERLAP-05")
    assert "ZZ-PJ-X06" in p["source_rule_ids"]
    assert "或" in p["counterexample_or_limit"] or "条件" in p["counterexample_or_limit"]
    assert "ZZ-PJ-X06" in p["unresolved_question"] or "条件" in p["unresolved_question"]

def test_no_canonicalization_claims_in_report():
    md = MD_PATH.read_text(encoding="utf-8")
    evidence = EVIDENCE_PATH.read_text(encoding="utf-8")
    assert "PROPOSAL_ONLY_NOT_CANONICAL" in md
    assert "PROPOSAL_ONLY_NOT_CANONICAL" in evidence
    assert "不合并、不删除、不改名" in md
    assert "不修改" in evidence
