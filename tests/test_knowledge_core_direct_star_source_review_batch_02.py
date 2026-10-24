import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "knowledge" / "core" / "direct-star-source-review" / "DIRECT_STAR_SOURCE_REVIEW_BATCH_02_v0.1.csv"
REPORT = ROOT / "knowledge" / "core" / "direct-star-source-review" / "DIRECT_STAR_SOURCE_REVIEW_BATCH_02_v0.1.md"
EVIDENCE = ROOT / "validation" / "knowledge" / "core" / "direct-star-source-review" / "DIRECT_STAR_SOURCE_REVIEW_BATCH_02_EVIDENCE.md"

EXPECTED = {
    "ZZ-TYI-002", "ZZ-TYI-006", "ZZ-TYI-007", "ZZ-TYI-008", "ZZ-TYI-X08",
    "ZZ-TL-002", "ZZ-TL-008", "ZZ-TL-X01", "ZZ-TL-X02",
    "ZZ-JM-002", "ZZ-JM-004", "ZZ-JM-X01",
    "ZZ-TX-001", "ZZ-TX-X02",
    "ZZ-TLIA-002", "ZZ-TLIA-003", "ZZ-TLIA-004", "ZZ-TLIA-006", "ZZ-TLIA-X01", "ZZ-TLIA-X05",
    "ZZ-QS-002", "ZZ-QS-004", "ZZ-QS-006", "ZZ-QS-010", "ZZ-QS-X02",
    "ZZ-PJ-002", "ZZ-PJ-003", "ZZ-PJ-004", "ZZ-PJ-005", "ZZ-PJ-X01", "ZZ-PJ-X02", "ZZ-PJ-X06", "ZZ-PJ-X10",
}

def rows():
    with CSV.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def test_exact_unique_rule_coverage_and_star_counts():
    data = rows()
    ids = [r["rule_id"] for r in data]
    assert len(data) == 33
    assert len(ids) == len(set(ids)) == 33
    assert set(ids) == EXPECTED
    counts = {}
    for r in data:
        counts[r["star"]] = counts.get(r["star"], 0) + 1
    assert counts == {"太阴": 5, "贪狼": 4, "巨门": 3, "天相": 2, "天梁": 6, "七杀": 5, "破军": 8}

def test_provenance_and_literal_span_fields_are_present():
    data = rows()
    for r in data:
        assert r["source_id"] in {"SRC-ZZ-001", "SRC-ZZ-002"}
        assert r["source_pdf_page"].isdigit()
        assert r["source_printed_page"].isdigit()
        assert r["source_span_status"] == "VERIFIED_VISUAL_SCAN"
        assert r["literal_source_span"].strip()
        assert r["current_core_references"].strip()
        assert r["subject_alignment"] == "MATCHED"
        assert r["source_epistemic"] == "EXPLICIT"
        assert r["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL"

def test_normalization_and_canonical_source_flags_are_not_promoted():
    for r in rows():
        assert r["normalization_epistemic_before"] == "UNRESOLVED"
        assert r["normalization_epistemic_after"] == "UNRESOLVED"
        assert r["canonical_source_span_verified_before"].lower() == "false"
        assert r["canonical_source_span_verified_after"].lower() == "false"

def test_role_and_tier_are_separate_axes():
    allowed_roles = {"INTRINSIC", "RELATIONAL", "CONDITIONAL", "UNRESOLVED_OTHER"}
    allowed_tiers = {"DIRECT_STAR", "SAME_STAR_MODIFIER", "SYSTEM_CONTEXT"}
    for r in rows():
        assert r["claim_role"] in allowed_roles
        assert r["current_evidence_tier"] == "DIRECT_STAR"
        assert r["proposed_evidence_tier"] in allowed_tiers
        assert r["core_use_assessment"].strip()
        assert r["condition_scope_assessment"].strip()

def test_repeated_source_claims_are_preserved_not_double_counted():
    by_id = {r["rule_id"]: r for r in rows()}
    assert by_id["ZZ-PJ-002"]["literal_source_span"] == by_id["ZZ-PJ-X01"]["literal_source_span"]
    assert "重叠" in by_id["ZZ-PJ-X01"]["core_use_assessment"] or "同一" in by_id["ZZ-PJ-X01"]["core_use_assessment"]
    assert "无权" in by_id["ZZ-PJ-X06"]["condition_scope_assessment"]
    assert "或" in by_id["ZZ-PJ-X06"]["condition_scope_assessment"]

def test_research_artifacts_remain_proposal_only():
    assert "PROPOSAL_ONLY_NOT_CANONICAL" in REPORT.read_text(encoding="utf-8")
    assert "PROPOSAL_ONLY_NOT_CANONICAL" in EVIDENCE.read_text(encoding="utf-8")
    assert "不修改 canonical" in REPORT.read_text(encoding="utf-8")
    assert "不证明现实预测有效" in REPORT.read_text(encoding="utf-8")
