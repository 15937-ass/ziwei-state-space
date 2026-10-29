import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "knowledge/core/activation-semantics/CHONGQI_CHONGHUI_EVIDENCE_MATRIX_v0.1.json"

def load():
    return json.loads(AUDIT.read_text(encoding="utf-8"))

def test_verdict_and_runtime_boundary():
    d = load()
    assert d["verdict"] == "SHARED_DESCRIPTIVE_MINIMUM_ONLY"
    assert d["human_gate_required_now"] is False
    assert d["term_dispositions"]["冲起"]["executable"] is False
    assert d["term_dispositions"]["冲会"]["executable"] is False
    assert d["term_dispositions"]["冲会"]["equivalent_to_chongqi"] is False

def test_evidence_has_source_and_remains_non_executable():
    d = load()
    rows = d["evidence"]
    assert len(rows) >= 8
    assert all(r["source_id"].startswith("SRC-ZZ-") for r in rows)
    assert all(r["source_location"] and r["source_span"] for r in rows)
    assert all(r["executable"] is False for r in rows)

def test_chongqi_minimum_is_not_over_generalized():
    d = load()
    q = [r for r in d["evidence"] if r["term"] == "冲起"]
    assert any(r["id"] == "CQ-001" and r["effect"] == "MUTUAL_STRENGTHENING_AND_CHANGE_PIVOT" for r in q)
    assert any(r["geometry"] == "三方四正" for r in q)
    assert any(r["binding_status"] == "SUBJECT_UNKNOWN" for r in q)
    assert any(r["binding_status"] == "CROSS_STAR_EXPLICIT" for r in q)
    forbidden = set(d["forbidden_inferences"])
    assert "冲起 == strict opposition" in forbidden
    assert "all 冲起 require same star or same transformation" in forbidden

def test_chonghui_is_separate_relation_family():
    d = load()
    h = [r for r in d["evidence"] if r["term"] == "冲会"]
    assert any(r["layer"] == "SOURCE_RELATION_NOT_INTRINSICALLY_TEMPORAL" for r in h)
    assert any(r["geometry"] == "OR(同会,冲会)" for r in h)
    assert "冲起 == 冲会" in d["forbidden_inferences"]

def test_gap_dispositions_stay_fail_closed():
    d = load()
    gaps = {g["gap_id"]: g for g in d["gap_dispositions"]}
    assert gaps["P02-SB06-GAP-G01"]["disposition"] == "DESCRIPTIVE_TERM_CLARIFIED_EXECUTABLE_HOLD"
    assert gaps["WP07B-GAP-003-ACTIVATION-RELATION"]["disposition"] == "SPLIT_TERM_FAMILY_EXECUTABLE_HOLD"
    assert all(g["executable"] is False for g in gaps.values())
